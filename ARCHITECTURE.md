# System Architecture

## Overview

The Financial Statement AI Analyzer uses a modern three-tier architecture with a React frontend, FastAPI backend, and AI/ML services.

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 Frontend Layer (Next.js)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Upload  │  │Dashboard │  │   Chat   │  │  Trends  │   │
│  │Component │  │Component │  │Component │  │Component │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
│  Features:                                                   │
│  • Material-UI components                                    │
│  • ECharts visualizations                                    │
│  • Web Speech API (voice)                                    │
│  • Dark mode support                                         │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/REST
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend Layer (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Endpoints                            │  │
│  │  POST /api/analyze    - Upload & analyze files       │  │
│  │  POST /api/chat       - Q&A interface                │  │
│  │  POST /api/export     - Export reports               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Document Parsers                              │  │
│  │  • PDF Parser (PyPDF2)                               │  │
│  │  • Image Parser (Pillow)                             │  │
│  │  • Excel/CSV Parser (Pandas)                         │  │
│  │  • XBRL Parser (XML)                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Financial Analyzer                            │  │
│  │  • Ratio calculations                                 │  │
│  │  • Trend analysis                                     │  │
│  │  • Risk assessment                                    │  │
│  │  • DuPont decomposition                              │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              AI/ML Services Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           OpenAI GPT-4                                │  │
│  │  • Financial insights generation                      │  │
│  │  • Conversational Q&A                                │  │
│  │  • Context-aware responses                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           GPT-4 Vision                                │  │
│  │  • Image analysis                                     │  │
│  │  • Table recognition                                  │  │
│  │  • OCR capabilities                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Document Analysis Flow

```
User Upload
    │
    ├─→ PDF File
    │       │
    │       ├─→ PyPDF2 Parser
    │       │       │
    │       │       └─→ Text Extraction
    │       │
    │       └─→ Financial Data Extraction
    │
    ├─→ Image File
    │       │
    │       ├─→ Pillow Processing
    │       │       │
    │       │       └─→ Base64 Encoding
    │       │
    │       └─→ GPT-4 Vision Analysis
    │
    ├─→ Excel/CSV File
    │       │
    │       ├─→ Pandas Processing
    │       │       │
    │       │       └─→ DataFrame Creation
    │       │
    │       └─→ Structured Data Extraction
    │
    └─→ XBRL File
            │
            ├─→ XML Parser
            │       │
            │       └─→ Financial Tags Extraction
            │
            └─→ Data Mapping
    │
    ▼
Financial Analyzer
    │
    ├─→ Ratio Calculations
    │   ├─→ Profitability Ratios
    │   ├─→ Liquidity Ratios
    │   ├─→ Leverage Ratios
    │   └─→ Efficiency Ratios
    │
    ├─→ Trend Analysis
    │   ├─→ Multi-period Comparison
    │   ├─→ Growth Rate Calculation
    │   └─→ Pattern Recognition
    │
    └─→ Risk Assessment
        ├─→ Rule-based Detection
        ├─→ Threshold Comparison
        └─→ Severity Classification
    │
    ▼
LLM Enhancement
    │
    ├─→ GPT-4 Insights Generation
    │   ├─→ Financial Health Summary
    │   ├─→ Strengths & Weaknesses
    │   └─→ Recommendations
    │
    └─→ Q&A Preparation
        └─→ Context Preparation
    │
    ▼
Response to Frontend
    │
    ├─→ JSON Response
    │   ├─→ Financial Data
    │   ├─→ Calculated Ratios
    │   ├─→ Risk List
    │   ├─→ AI Insights
    │   └─→ Trends
    │
    └─→ Display in Dashboard
```

### Chat Flow

```
User Question
    │
    └─→ Frontend Chat Component
            │
            └─→ API POST /api/chat
                    │
                    └─→ Backend Chat Handler
                            │
                            ├─→ Extract Context
                            │   ├─→ Financial Data
                            │   ├─→ Ratios
                            │   └─→ Risks
                            │
                            ├─→ Prepare Prompt
                            │   ├─→ System Context
                            │   ├─→ Previous Messages
                            │   └─→ Current Question
                            │
                            └─→ GPT-4 API Call
                                    │
                                    └─→ Generate Answer
                                            │
                                            └─→ Return to Frontend
                                                    │
                                                    └─→ Display Answer
                                                            │
                                                            ├─→ Text Display
                                                            └─→ Optional TTS
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **UI Library**: Material-UI 5
- **Charts**: ECharts for React
- **HTTP Client**: Axios
- **State Management**: React Hooks + SWR
- **Styling**: Emotion (CSS-in-JS)

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Async**: Uvicorn ASGI server
- **Validation**: Pydantic
- **Document Parsing**:
  - PyPDF2 (PDF)
  - Pillow (Images)
  - Pandas + OpenPyXL (Excel/CSV)
  - xml.etree.ElementTree (XBRL)

### AI/ML
- **LLM**: OpenAI GPT-4
- **Vision**: GPT-4 Vision
- **Voice**: Web Speech API (browser-based)

### Infrastructure
- **API**: RESTful HTTP/JSON
- **CORS**: Enabled for localhost development
- **File Upload**: Multipart form data
- **Environment**: Environment variables for config

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Production Setup                          │
└─────────────────────────────────────────────────────────────┘

Frontend (Vercel)                    Backend (Railway/Render)
┌──────────────┐                     ┌──────────────┐
│              │                     │              │
│   Next.js    │────── HTTPS ──────▶│   FastAPI    │
│   Static     │                     │   Server     │
│   Assets     │                     │              │
└──────────────┘                     └───────┬──────┘
                                             │
                                             │ API Calls
                                             │
                                     ┌───────▼──────┐
                                     │              │
                                     │   OpenAI     │
                                     │   API        │
                                     │              │
                                     └──────────────┘
```

## Security Considerations

1. **API Keys**: Stored in environment variables, never in code
2. **CORS**: Configured for specific origins only
3. **File Upload**: Size limits and format validation
4. **Input Sanitization**: All user inputs validated
5. **HTTPS**: Required for production deployment
6. **Rate Limiting**: To be implemented for API endpoints

## Performance Optimization

1. **Frontend**:
   - Code splitting with Next.js
   - Image optimization
   - SWR for caching API responses
   - React.memo for expensive components

2. **Backend**:
   - Async/await for non-blocking I/O
   - Temporary file cleanup
   - Response compression
   - Connection pooling

## Scalability

- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Caching**: Redis for session and response caching (future)
- **Queue**: Celery for async document processing (future)
- **CDN**: Static asset delivery for frontend

## Monitoring

- **Logs**: Structured logging in backend
- **Metrics**: API response times, error rates
- **Health Checks**: `/health` endpoint
- **API Documentation**: Auto-generated with FastAPI
