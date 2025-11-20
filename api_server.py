"""
FastAPI backend for financial statement analysis
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
import tempfile
from pathlib import Path
from datetime import datetime
import json
import threading
import hashlib
import uuid

from src.parsers.enhanced_parser import EnhancedDocumentParser
from src.analyzers.financial_analyzer import FinancialAnalyzer
from src.llm.financial_llm import FinancialLLM
from src.utils import (
    PeerBenchmark,
    extract_from_structured_data,
    extract_from_xbrl,
    build_cash_flow_summary,
    merge_llm_structured_data,
)

app = FastAPI(title="Financial Statement AI Analyzer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data persistence helpers
DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"
CHAT_HISTORY_FILE = DATA_DIR / "chat_history.json"

DATA_DIR.mkdir(exist_ok=True)

_file_lock = threading.Lock()


def _load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default


def _save_json(path: Path, payload):
    with path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _hash_password(raw: str) -> str:
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def _get_users():
    return _load_json(USERS_FILE, {})


def _get_user_by_id(user_id: str):
    users = _get_users()
    return users.get(user_id)


def _get_user_by_email(email: str):
    email_key = email.strip().lower()
    users = _get_users()
    for record in users.values():
        if record.get('email') == email_key:
            return record
    return None


def _append_chat_history(user_id: str, question: str, answer: str):
    entry = {
        "id": str(uuid.uuid4()),
        "question": question,
        "answer": answer,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    with _file_lock:
        history = _load_json(CHAT_HISTORY_FILE, {})
        user_history = history.get(user_id, [])
        user_history.append(entry)
        history[user_id] = user_history[-200:]
        _save_json(CHAT_HISTORY_FILE, history)
    return entry


# Initialize components
parser = EnhancedDocumentParser()
analyzer = FinancialAnalyzer()
benchmark_engine = PeerBenchmark()

try:
    llm = FinancialLLM()
except Exception as e:
    print(f"Warning: LLM initialization failed: {e}")
    llm = None


class ChatRequest(BaseModel):
    user_id: str
    question: str
    context: dict


class AuthRequest(BaseModel):
    name: Optional[str] = None
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AnalysisResponse(BaseModel):
    financial_data: dict
    ratios: dict
    risks: List[dict]
    insights: Optional[str] = None
    trends: Optional[dict] = None


@app.get("/")
async def root():
    return {"message": "Financial Statement AI Analyzer API", "version": "2.0"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "llm_available": llm is not None
    }


@app.post("/api/auth/register")
async def register_user(request: AuthRequest):
    email = request.email.strip().lower()
    if not email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    with _file_lock:
        users = _load_json(USERS_FILE, {})
        for record in users.values():
            if record.get('email') == email:
                raise HTTPException(status_code=400, detail="User already exists")

        user_id = str(uuid.uuid4())
        user_record = {
            "id": user_id,
            "name": request.name or email.split('@')[0].title(),
            "email": email,
            "password": _hash_password(request.password),
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        users[user_id] = user_record
        _save_json(USERS_FILE, users)

    sanitized = {k: v for k, v in user_record.items() if k != 'password'}
    return {"user": sanitized}


@app.post("/api/auth/login")
async def login_user(request: LoginRequest):
    email = request.email.strip().lower()
    if not email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user_record = _get_user_by_email(email)
    if not user_record:
        raise HTTPException(status_code=404, detail="User not found")

    if user_record.get('password') != _hash_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    sanitized = {k: v for k, v in user_record.items() if k != 'password'}
    return {"user": sanitized}


@app.post("/api/analyze")
async def analyze_files(
    files: List[UploadFile] = File(...),
    industry: Optional[str] = Form(None)
):
    """
    Analyze uploaded financial statement files with optional industry benchmark context.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    results = []
    temp_dir = tempfile.mkdtemp()
    selected_industry = (industry or 'general').strip()
    
    try:
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)
            
            parsed_doc = parser.parse_document(file_path)
            period_label = Path(file.filename).stem
            llm_metadata: Dict[str, Any] = {}
            llm_notes: List[str] = []
            
            if parsed_doc['type'] == 'pdf':
                all_text = '\n'.join([page['text'] for page in parsed_doc['content']])
                financial_data = analyzer.extract_financial_data(all_text)
                if llm and all_text.strip():
                    try:
                        structured = llm.extract_structured_data(all_text, period_hint=period_label)
                        if structured:
                            financial_data, llm_metadata, llm_notes = merge_llm_structured_data(
                                financial_data,
                                structured,
                            )
                    except Exception as exc:
                        print(f"Warning: structured extraction failed for {file.filename}: {exc}")
            elif parsed_doc['type'] in ['excel', 'csv']:
                financial_data = extract_from_structured_data(parsed_doc)
            elif parsed_doc['type'] == 'xbrl':
                financial_data = extract_from_xbrl(parsed_doc)
            elif parsed_doc['type'] == 'image' and llm:
                try:
                    analysis = llm.analyze_document_with_vision(parsed_doc['base64'])
                    financial_data = {'llm_extraction': analysis}
                except NotImplementedError:
                    financial_data = {}
                    print("Vision analysis is not supported in the current LLM provider.")
                except Exception as exc:
                    financial_data = {}
                    print(f"Vision analysis failed for {file.filename}: {exc}")
            else:
                financial_data = {}
            
            ratios = analyzer.calculate_ratios(financial_data)
            risks = analyzer.assess_risks(financial_data, ratios)
            dupont = analyzer.calculate_dupont_analysis(financial_data, ratios)
            cash_flow = build_cash_flow_summary(financial_data)
            benchmark = benchmark_engine.compare(financial_data, ratios, selected_industry)
            
            insights = None
            if llm and financial_data:
                insights = llm.generate_financial_insights(financial_data, ratios, risks)
            
            results.append({
                'filename': file.filename,
                'period': period_label,
                'type': parsed_doc['type'],
                'financial_data': financial_data,
                'ratios': ratios,
                'risks': risks,
                'dupont': dupont,
                'cash_flow': cash_flow,
                'benchmark': benchmark,
                'insights': insights,
                'llm_metadata': llm_metadata,
                'llm_notes': llm_notes,
            })
        
        if len(results) == 1:
            result = results[0]
            result['trends'] = None
            result['historical_data'] = [{
                'period': result['period'],
                **{
                    key: result['financial_data'].get(key)
                    for key in ['revenue', 'sales', 'net_income', 'total_assets']
                    if result['financial_data'].get(key) is not None
                }
            }]
            result['industry'] = (result.get('benchmark') or {}).get('industry', selected_industry.title())
            return result
        
        historical_data = [
            {
                'period': r['period'],
                **{
                    key: r['financial_data'].get(key)
                    for key in ['revenue', 'sales', 'net_income', 'total_assets']
                    if r['financial_data'].get(key) is not None
                }
            }
            for r in results
        ]
        trends = analyzer.identify_trends(historical_data)
        primary = results[-1]
        
        return {
            'files_analyzed': len(results),
            'results': results,
            'financial_data': primary['financial_data'],
            'ratios': primary['ratios'],
            'risks': primary['risks'],
            'dupont': primary.get('dupont', {}),
            'cash_flow': primary.get('cash_flow'),
            'benchmark': primary.get('benchmark'),
            'trends': trends,
            'historical_data': historical_data,
            'industry': (primary.get('benchmark') or {}).get('industry', selected_industry.title()),
            'insights': primary['insights'],
            'llm_metadata': primary.get('llm_metadata', {}),
            'llm_notes': primary.get('llm_notes', []),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Handle chat questions about financial statements
    """
    if not llm:
        raise HTTPException(status_code=503, detail="LLM service not available")
    
    user_record = _get_user_by_id(request.user_id)
    if not user_record:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        answer = llm.answer_question(request.question, request.context, user_id=request.user_id)
        entry = _append_chat_history(request.user_id, request.question, answer)
        return {"answer": answer, "entry": entry}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.get("/api/chat/history/{user_id}")
async def get_chat_history(user_id: str):
    user_record = _get_user_by_id(user_id)
    if not user_record:
        raise HTTPException(status_code=404, detail="User not found")

    history = _load_json(CHAT_HISTORY_FILE, {})
    return {"history": history.get(user_id, [])}


@app.post("/api/export")
async def export_report(data: dict, format: str = "markdown"):
    """
    Export analysis report in specified format
    
    Args:
        data: Analysis data to export
        format: Export format (markdown, text)
    """
    try:
        from src.utils.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        
        if format.lower() == "markdown":
            content = generator.generate_markdown_report(data)
            return {
                "format": "markdown",
                "content": content,
                "filename": f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            }
        elif format.lower() == "text":
            content = generator.generate_text_report(data)
            return {
                "format": "text",
                "content": content,
                "filename": f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}. Supported formats: markdown, text")
    
    except ImportError:
        raise HTTPException(status_code=500, detail="Report generator module not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
