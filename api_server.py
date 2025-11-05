"""
FastAPI backend for financial statement analysis
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
import os
import tempfile
from pathlib import Path

from src.parsers.enhanced_parser import EnhancedDocumentParser
from src.analyzers.financial_analyzer import FinancialAnalyzer
from src.llm.financial_llm import FinancialLLM

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
async def analyze_files(files: List[UploadFile] = File(...)):
    """
    Analyze uploaded financial statement files
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    results = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        for file in files:
            # Save uploaded file temporarily
            file_path = os.path.join(temp_dir, file.filename)
            
            with open(file_path, 'wb') as f:
                content = await file.read()
                f.write(content)
            
            # Parse the document
            parsed_doc = parser.parse_document(file_path)
            
            # Extract financial data
            if parsed_doc['type'] == 'pdf':
                all_text = '\n'.join([page['text'] for page in parsed_doc['content']])
                financial_data = analyzer.extract_financial_data(all_text)
            elif parsed_doc['type'] in ['excel', 'csv']:
                # Extract from structured data
                financial_data = extract_from_structured_data(parsed_doc)
            elif parsed_doc['type'] == 'xbrl':
                financial_data = extract_from_xbrl(parsed_doc)
            elif parsed_doc['type'] == 'image' and llm:
                # Use vision model
                analysis = llm.analyze_document_with_vision(parsed_doc['base64'])
                financial_data = {'llm_extraction': analysis}
            else:
                financial_data = {}
            
            # Calculate ratios
            ratios = analyzer.calculate_ratios(financial_data)
            
            # Assess risks
            risks = analyzer.assess_risks(financial_data, ratios)
            
            # Generate insights
            insights = None
            if llm and financial_data:
                insights = llm.generate_financial_insights(financial_data, ratios, risks)
            
            results.append({
                'filename': file.filename,
                'type': parsed_doc['type'],
                'financial_data': financial_data,
                'ratios': ratios,
                'risks': risks,
                'insights': insights
            })
        
        # If multiple files, combine results
        if len(results) == 1:
            return results[0]
        else:
            # For multiple files, aggregate results
            return {
                'files_analyzed': len(results),
                'results': results,
                'financial_data': results[0]['financial_data'],  # Use first file's data
                'ratios': results[0]['ratios'],
                'risks': results[0]['risks'],
                'insights': results[0]['insights']
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Cleanup temporary files
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
async def export_report(data: dict, format: str = "pdf"):
    """
    Export analysis report in specified format
    """
    # This would generate PDF/Markdown reports
    raise HTTPException(status_code=501, detail="Export feature coming soon")


def extract_from_structured_data(parsed_doc: dict) -> dict:
    """Extract financial data from Excel/CSV"""
    financial_data = {
        'revenue': None,
        'net_income': None,
        'total_assets': None,
        'total_liabilities': None,
        'equity': None
    }
    
    try:
        if parsed_doc['type'] == 'excel':
            # Look through all sheets for financial data
            for sheet_name, sheet_data in parsed_doc['content'].items():
                data = sheet_data['data']
                # Look for financial statement patterns
                for row in data:
                    for key, value in row.items():
                        key_lower = str(key).lower()
                        if 'revenue' in key_lower or 'sales' in key_lower:
                            try:
                                financial_data['revenue'] = float(value)
                            except (ValueError, TypeError):
                                pass
                        elif 'net income' in key_lower or 'profit' in key_lower:
                            try:
                                financial_data['net_income'] = float(value)
                            except (ValueError, TypeError):
                                pass
        
        elif parsed_doc['type'] == 'csv':
            data = parsed_doc['data']
            for row in data:
                for key, value in row.items():
                    key_lower = str(key).lower()
                    if 'revenue' in key_lower:
                        try:
                            financial_data['revenue'] = float(value)
                        except (ValueError, TypeError):
                            pass
    except Exception as e:
        print(f"Error extracting structured data: {e}")
    
    return financial_data


def extract_from_xbrl(parsed_doc: dict) -> dict:
    """Extract financial data from XBRL"""
    financial_data = {
        'revenue': None,
        'net_income': None,
        'total_assets': None,
        'total_liabilities': None,
        'equity': None
    }
    
    if 'data' in parsed_doc:
        xbrl_data = parsed_doc['data']
        # Map XBRL tags to our fields
        tag_mappings = {
            'revenue': ['Revenue', 'Revenues', 'SalesRevenue'],
            'net_income': ['NetIncome', 'NetIncomeLoss', 'ProfitLoss'],
            'total_assets': ['Assets', 'AssetsCurrent', 'AssetsTotal'],
            'total_liabilities': ['Liabilities', 'LiabilitiesTotal'],
            'equity': ['Equity', 'StockholdersEquity', 'ShareholdersEquity']
        }
        
        for field, tags in tag_mappings.items():
            for tag in tags:
                if tag in xbrl_data:
                    try:
                        financial_data[field] = float(xbrl_data[tag].replace(',', ''))
                        break
                    except (ValueError, AttributeError):
                        pass
    
    return financial_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
