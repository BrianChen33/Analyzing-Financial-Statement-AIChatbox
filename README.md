# 💰 Financial Statement AI Chatbox

A comprehensive conversational AI agent for analyzing financial statements with advanced features including multi-format support, interactive dashboards, voice capabilities, and peer benchmarking.

## 🌟 Key Features

### Document Processing
- **📤 Multi-Format Support**: PDF, Images (PNG/JPG), Excel, CSV, XBRL
- **🔍 Advanced OCR**: Automatic table recognition and text extraction
- **🖼️ Multimodal Analysis**: GPT-4 Vision for analyzing financial statement images

### Financial Analysis
- **📊 Comprehensive Indicators**: 
  - Profitability: Profit Margin, ROA, ROE, Gross Margin
  - Liquidity: Current Ratio, Quick Ratio, Cash Ratio
  - Leverage: Debt-to-Asset, Debt-to-Equity, Interest Coverage
  - Efficiency: Asset Turnover, Inventory Turnover
  - Cash Flow: Operating Cash Flow, Free Cash Flow
- **📈 DuPont Analysis**: Three-factor ROE decomposition
- **📉 Trend Analysis**: Multi-period comparison and growth analysis
- **⚠️ Risk Detection**: Automated identification of financial anomalies

### User Interfaces
- **🖥️ Next.js Web App**: Modern, responsive UI with Material-UI
- **📱 Mobile-Friendly**: Responsive design for all devices
- **🌓 Dark Mode**: Eye-friendly interface switching
- **💬 Interactive Chat**: AI-powered Q&A about financial statements
- **🎤 Voice Input**: Speech recognition for questions (Web Speech API)
- **🔊 Voice Output**: Text-to-speech for responses

### Advanced Features
- **📊 Visual Dashboard**: Interactive charts with ECharts
- **📈 Trend Visualization**: Line charts, bar charts, radar charts
- **🔄 Session History**: Save and restore analysis sessions
- **📥 Export Reports**: PDF and Markdown report generation
- **🆚 Peer Benchmarking**: Compare with industry standards (coming soon)

## 🏗️ Architecture

### Frontend (Next.js + Material-UI)
- **Technology Stack**: Next.js 14, TypeScript, Material-UI 5
- **Components**: 
  - FileUpload: Multi-format drag-and-drop upload
  - FinancialDashboard: Key metrics and charts
  - ChatInterface: AI-powered Q&A with voice support
  - TrendAnalysis: Multi-period trends and DuPont analysis
- **Features**: Dark mode, responsive design, session management

### Backend (FastAPI)
- **API Server**: RESTful API with FastAPI
- **Document Parsing**: Enhanced parser for PDF, Excel, CSV, XBRL
- **Financial Analysis**: Comprehensive ratio calculations and trend analysis
- **LLM Integration**: GPT-4 for insights and conversational AI
- **Data Processing**: Pandas for structured data, PyPDF2 for PDFs

### System Workflow
1. **Document Upload**: User uploads files via web interface
2. **Format Detection**: Backend identifies file type and routes to appropriate parser
3. **Data Extraction**: Extract financial data using appropriate method:
   - PDFs: Text extraction with PyPDF2
   - Images: GPT-4 Vision analysis
   - Excel/CSV: Pandas dataframe processing
   - XBRL: XML parsing with financial tag mapping
4. **Financial Analysis**: Calculate ratios, identify trends, assess risks
5. **AI Enhancement**: GPT-4 generates insights and answers questions
6. **Visualization**: Display results in interactive dashboard with charts
7. **Export**: Generate PDF/Markdown reports (coming soon)

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (for LLM features)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- OpenAI API key (for LLM features)

### Backend Setup

1. **Clone and Install Python Dependencies**

```bash
git clone https://github.com/BrianChen33/Analyzing-Financial-Statement-AIChatbox.git
cd Analyzing-Financial-Statement-AIChatbox
pip install -r requirements.txt
```

2. **Configure Environment**

Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

3. **Start FastAPI Backend**

```bash
python api_server.py
# API runs on http://localhost:8000
```

### Frontend Setup

1. **Install Node Dependencies**

```bash
cd frontend
npm install
```

2. **Configure Frontend**

Create `.env.local`:
```bash
API_URL=http://localhost:8000
```

3. **Start Next.js Development Server**

```bash
npm run dev
# Frontend runs on http://localhost:3000
```

### Alternative: Streamlit Interface (Legacy)

```bash
streamlit run app.py
# Opens on http://localhost:8501
```

## 💻 Usage

### Web Interface

1. **Upload Document**: Use the sidebar to upload a financial statement (PDF or image)
2. **Analyze**: Click "Analyze Document" to process the file
3. **Review Summary**: View extracted metrics, ratios, and risks in the Summary tab
4. **Ask Questions**: Use the Q&A Chat tab to ask questions about the document
5. **View Details**: Check the Details tab for comprehensive analysis

### Command Line

```bash
# Analyze a financial statement
python src/chatbot.py uploads/statement.pdf

# The system will:
# 1. Parse the document
# 2. Extract financial data
# 3. Calculate ratios
# 4. Assess risks
# 5. Generate AI insights
# 6. Enter interactive Q&A mode
```

### Example Questions

Once a document is analyzed, you can ask questions like:
- "What is the company's profitability?"
- "Are there any major financial risks?"
- "How has revenue changed over time?"
- "What is the debt-to-asset ratio?"
- "Explain the profit margin"

## 📁 Project Structure

```
Analyzing-Financial-Statement-AIChatbox/
├── src/
│   ├── __init__.py
│   ├── chatbot.py              # Main chatbot orchestrator
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── document_parser.py  # PDF and image parsing
│   ├── analyzers/
│   │   ├── __init__.py
│   │   └── financial_analyzer.py  # Financial calculations
│   └── llm/
│       ├── __init__.py
│       └── financial_llm.py    # LLM integration
├── tests/                       # Unit tests
├── uploads/                     # Uploaded documents (gitignored)
├── app.py                       # Streamlit web interface
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | `gpt-4` |
| `UPLOAD_FOLDER` | Directory for uploads | `uploads` |
| `MAX_FILE_SIZE` | Max upload size in bytes | `10485760` (10MB) |

## 📊 Supported Financial Metrics

The system can extract and calculate:

### Balance Sheet Items
- Total Assets
- Total Liabilities
- Equity

### Income Statement Items
- Revenue/Sales
- Net Income
- Operating Income

### Financial Ratios
- **Profitability**: Profit Margin, ROA, ROE
- **Leverage**: Debt-to-Asset Ratio
- **Efficiency**: Asset Turnover

### Risk Indicators
- Profitability Risk
- Leverage Risk
- Loss Risk
- Asset Efficiency Risk

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 🛠️ Development

### Adding New Features

1. **New Financial Indicators**: Add to `src/analyzers/financial_analyzer.py`
2. **New Document Types**: Extend `src/parsers/document_parser.py`
3. **Custom Analysis**: Modify `src/llm/financial_llm.py`

### Code Structure

- **Parsers**: Handle document ingestion and text extraction
- **Analyzers**: Perform financial calculations and pattern recognition
- **LLM**: Integrate with AI models for insights and Q&A
- **Chatbot**: Orchestrate the entire workflow

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT-4 and Vision API
- Streamlit for the web framework
- The financial analysis community for domain knowledge

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This system is for educational and analytical purposes. Always verify financial analysis with professional accountants and financial advisors.