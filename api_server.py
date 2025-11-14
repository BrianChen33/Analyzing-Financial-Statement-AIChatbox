"""
FastAPI backend for financial statement analysis
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
import os
import tempfile
from pathlib import Path
from datetime import datetime

from src.parsers.enhanced_parser import EnhancedDocumentParser
from src.analyzers.financial_analyzer import FinancialAnalyzer
from src.llm.financial_llm import FinancialLLM
from src.utils import (
    PeerBenchmark,
    extract_from_structured_data,
    extract_from_xbrl,
    build_cash_flow_summary,
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
    question: str
    context: dict


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
            
            if parsed_doc['type'] == 'pdf':
                all_text = '\n'.join([page['text'] for page in parsed_doc['content']])
                financial_data = analyzer.extract_financial_data(all_text)
            elif parsed_doc['type'] in ['excel', 'csv']:
                financial_data = extract_from_structured_data(parsed_doc)
            elif parsed_doc['type'] == 'xbrl':
                financial_data = extract_from_xbrl(parsed_doc)
            elif parsed_doc['type'] == 'image' and llm:
                analysis = llm.analyze_document_with_vision(parsed_doc['base64'])
                financial_data = {'llm_extraction': analysis}
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
                'insights': insights
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
            'insights': primary['insights']
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
    
    try:
        answer = llm.answer_question(request.question, request.context)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


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
