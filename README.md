# 💰 Financial Statement AI Chatbox

A conversational AI agent for the financial field that supports users to upload financial statements, automatically extract information, calculate key financial indicators, identify trends and risks, and provide interactive Q&A.

## 🌟 Features

- **📤 Document Upload**: Support for PDF and image formats (PNG, JPG, JPEG)
- **🔍 Automatic Extraction**: AI-powered extraction of financial data from statements
- **📊 Financial Indicators**: Calculate key ratios including:
  - Profit Margin
  - Return on Assets (ROA)
  - Return on Equity (ROE)
  - Debt-to-Asset Ratio
- **📈 Trend Analysis**: Identify revenue and profit trends across multiple periods
- **⚠️ Risk Assessment**: Automatic identification of financial risks with severity levels
- **💡 AI Insights**: LLM-powered analysis and recommendations
- **💬 Interactive Q&A**: Conversational interface to ask questions about the financial statement
- **🖼️ Multimodal Support**: Vision AI for analyzing financial statement images

## 🏗️ Architecture

The system uses a multimodal workflow combining:
- **Document Parsing**: Extract text from PDFs or analyze images with Vision AI
- **Financial Analysis**: Calculate ratios and identify patterns
- **LLM Integration**: Generate insights and answer questions using GPT-4
- **Web Interface**: User-friendly Streamlit interface

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (for LLM features)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/BrianChen33/Analyzing-Financial-Statement-AIChatbox.git
cd Analyzing-Financial-Statement-AIChatbox
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
OPENAI_API_KEY=your-api-key-here
```

### 4. Run the Application

#### Option A: Web Interface (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

#### Option B: Command Line Interface

```bash
python src/chatbot.py path/to/financial_statement.pdf
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