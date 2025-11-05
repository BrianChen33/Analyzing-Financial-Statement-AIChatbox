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

# 💰 财务报表AI聊天框

一个全面的对话式AI代理，用于分析财务报表，具有多格式支持、交互式仪表板、语音功能和同行基准等高级功能。

## 🌟 主要功能

### 文档处理
- **📤 多格式支持**：PDF、图片（PNG/JPG）、Excel、CSV、XBRL
- **🔍 高级OCR**：自动表格识别和文本提取
- **🖼️ 多模态分析**：使用GPT-4 Vision分析财务报表图片

### 财务分析
- **📊 全面指标**：
  - 盈利能力：利润率、资产回报率（ROA）、股本回报率（ROE）、毛利率
  - 流动性：流动比率、速动比率、现金比率
  - 杠杆：资产负债率、权益负债率、利息覆盖率
  - 效率：资产周转率、库存周转率
  - 现金流：经营现金流、自由现金流
- **📈 杜邦分析**：三因素ROE分解
- **📉 趋势分析**：多期比较和增长分析
- **⚠️ 风险检测**：自动识别财务异常

### 用户界面
- **🖥️ Next.js Web应用**：现代化、响应式UI，使用Material-UI
- **📱 移动友好**：适配所有设备的响应式设计
- **🌓 暗黑模式**：护眼界面切换
- **💬 交互式聊天**：AI驱动的财务报表问答
- **🎤 语音输入**：语音识别提问（Web Speech API）
- **🔊 语音输出**：文本转语音回答

### 高级功能
- **📊 可视化仪表板**：使用ECharts的交互式图表
- **📈 趋势可视化**：折线图、柱状图、雷达图
- **🔄 会话历史**：保存和恢复分析会话
- **📥 导出报告**：生成PDF和Markdown报告
- **🆚 同行基准**：与行业标准比较（即将推出）

## 🏗️ 架构

### 前端（Next.js + Material-UI）
- **技术栈**：Next.js 14、TypeScript、Material-UI 5
- **组件**：
  - FileUpload：多格式拖放上传
  - FinancialDashboard：关键指标和图表
  - ChatInterface：支持语音的AI问答
  - TrendAnalysis：多期趋势和杜邦分析
- **功能**：暗黑模式、响应式设计、会话管理

### 后端（FastAPI）
- **API服务器**：使用FastAPI的RESTful API
- **文档解析**：增强的PDF、Excel、CSV、XBRL解析器
- **财务分析**：全面的比率计算和趋势分析
- **LLM集成**：使用GPT-4进行洞察和对话式AI
- **数据处理**：使用Pandas处理结构化数据，使用PyPDF2处理PDF

### 系统工作流
1. **文档上传**：用户通过Web界面上传文件
2. **格式检测**：后端识别文件类型并路由到相应解析器
3. **数据提取**：使用适当方法提取财务数据：
   - PDF：使用PyPDF2提取文本
   - 图片：使用GPT-4 Vision分析
   - Excel/CSV：使用Pandas数据框处理
   - XBRL：使用XML解析和财务标签映射
4. **财务分析**：计算比率、识别趋势、评估风险
5. **AI增强**：GPT-4生成洞察和回答问题
6. **可视化**：在交互式仪表板中显示结果和图表
7. **导出**：生成PDF/Markdown报告（即将推出）

## 📋 先决条件

- Python 3.8或更高版本
- OpenAI API密钥（用于LLM功能）

## 🚀 快速开始

### 先决条件

- Python 3.8或更高版本
- Node.js 18或更高版本
- OpenAI API密钥（用于LLM功能）

### 后端设置

1. **克隆并安装Python依赖项**

```bash
git clone https://github.com/BrianChen33/Analyzing-Financial-Statement-AIChatbox.git
cd Analyzing-Financial-Statement-AIChatbox
pip install -r requirements.txt
```

2. **配置环境**

创建`.env`文件：
```bash
cp .env.example .env
# 编辑.env并添加您的OpenAI API密钥
```

3. **启动FastAPI后端**

```bash
python api_server.py
# API运行在http://localhost:8000
```

### 前端设置

1. **安装Node依赖项**

```bash
cd frontend
npm install
```

2. **配置前端**

创建`.env.local`：
```bash
API_URL=http://localhost:8000
```

3. **启动Next.js开发服务器**

```bash
npm run dev
# 前端运行在http://localhost:3000
```

### 替代方案：Streamlit界面（旧版）

```bash
streamlit run app.py
# 打开http://localhost:8501
```

## 💻 使用方法

### Web界面

1. **上传文档**：使用侧边栏上传财务报表（PDF或图片）
2. **分析**：点击“分析文档”处理文件
3. **查看摘要**：在“摘要”选项卡中查看提取的指标、比率和风险
4. **提问**：使用“问答聊天”选项卡询问有关文档的问题
5. **查看详情**：在“详情”选项卡中查看全面分析

### 命令行

```bash
# 分析财务报表
python src/chatbot.py uploads/statement.pdf

# 系统将：
# 1. 解析文档
# 2. 提取财务数据
# 3. 计算比率
# 4. 评估风险
# 5. 生成AI洞察
# 6. 进入交互式问答模式
```

### 示例问题

文档分析完成后，您可以提问：
- “公司的盈利能力如何？”
- “是否存在重大财务风险？”
- “收入随时间的变化如何？”
- “资产负债率是多少？”
- “解释一下利润率”

## 📁 项目结构

```
Analyzing-Financial-Statement-AIChatbox/
├── src/
│   ├── __init__.py
│   ├── chatbot.py              # 主聊天机器人协调器
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── document_parser.py  # PDF和图片解析
│   ├── analyzers/
│   │   ├── __init__.py
│   │   └── financial_analyzer.py  # 财务计算
│   └── llm/
│       ├── __init__.py
│       └── financial_llm.py    # LLM集成
├── tests/                       # 单元测试
├── uploads/                     # 上传的文档（已git忽略）
├── app.py                       # Streamlit Web界面
├── requirements.txt             # Python依赖项
├── .env.example                 # 环境变量模板
├── .gitignore                   # Git忽略规则
└── README.md                    # 本文件
```

## 🔧 配置

### 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `OPENAI_API_KEY` | 您的OpenAI API密钥 | 必填 |
| `OPENAI_MODEL` | 使用的GPT模型 | `gpt-4` |
| `UPLOAD_FOLDER` | 上传目录 | `uploads` |
| `MAX_FILE_SIZE` | 最大上传大小（字节） | `10485760`（10MB） |

## 📊 支持的财务指标

系统可以提取和计算：

### 资产负债表项目
- 总资产
- 总负债
- 股东权益

### 损益表项目
- 收入/销售额
- 净利润
- 营业收入

### 财务比率
- **盈利能力**：利润率、资产回报率（ROA）、股本回报率（ROE）
- **杠杆**：资产负债率
- **效率**：资产周转率

### 风险指标
- 盈利风险
- 杠杆风险
- 损失风险
- 资产效率风险

## 🧪 测试

运行测试套件：

```bash
pytest tests/
```

## 🛠️ 开发

### 添加新功能

1. **新财务指标**：添加到`src/analyzers/financial_analyzer.py`
2. **新文档类型**：扩展`src/parsers/document_parser.py`
3. **自定义分析**：修改`src/llm/financial_llm.py`

### 代码结构

- **解析器**：处理文档摄取和文本提取
- **分析器**：执行财务计算和模式识别
- **LLM**：与AI模型集成以获取洞察和问答
- **聊天机器人**：协调整个工作流

## 🤝 贡献

欢迎贡献！请随时提交Pull Request。

## 📝 许可证

本项目采用MIT许可证。

## 🙏 鸣谢

- OpenAI提供的GPT-4和Vision API
- Streamlit提供的Web框架
- 财务分析社区提供的领域知识

## 📧 联系方式

如有问题或需要支持，请在GitHub上提交问题。

---

**注意**：本系统仅用于教育和分析目的。始终与专业会计师和财务顾问核实财务分析。