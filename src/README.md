# Financial Statement AI Chatbox

当前仓库仅保留运行所需的核心代码（src / frontend / tests 等），旧版文档与示例已清理。本 README 为最新使用说明。

## 功能概览
- **多格式解析**：自动识别 PDF / 图片 / Excel / CSV / XBRL。
- **指标分析**：盈利、流动、杠杆、效率、现金流指标 + DuPont + 多期趋势。
- **风险与同行对标**：内置 General / Technology / Retail / Manufacturing 基准，输出差距及告警。
- **AI 能力（可选）**：若设置 `OPENAI_API_KEY`，可启用 GPT 洞察、Q&A、Vision 图片理解。
- **前端体验**：Next.js + Material UI + ECharts，支持上传、仪表盘、问答、趋势视图及 Markdown/Text 报告导出。

## 快速上手
```bash
git clone <repo>
cd Analyzing-Financial-Statement-AIChatbox-copilot-develop-conversational-ai-agent/Analyzing-Financial-Statement-AIChatbox-copilot-develop-conversational-ai-agent

# Backend
pip install -r requirements.txt
echo OPENAI_API_KEY=sk-xxxx > .env
echo OPENAI_MODEL=gpt-4 >> .env
python api_server.py   # 默认 http://localhost:8000

# Frontend
cd frontend
npm install
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
npm run dev            # 默认 http://localhost:3000
```
打开浏览器上传报表，在上传前选择行业即可查看指标、风险、同行对标及 AI 洞察。未配置 OpenAI 时，仍可使用本地解析与指标功能。

## 常用脚本
- `python api_server.py`：FastAPI 后端
- `streamlit run app.py`：可选的 Streamlit 旧界面
- `npm run dev`：Next.js 前端
- `pytest tests -q`：单元测试

## 目录结构
```
├── api_server.py
├── app.py
├── requirements.txt
├── src/            # 解析、指标、LLM、工具
├── frontend/       # Next.js 应用
└── tests/          # Pytest 覆盖
```

## 环境变量
| 变量 | 说明 | 必需 |
| ---- | ---- | ---- |
| `OPENAI_API_KEY` | OpenAI 密钥，启用 AI 洞察/Q&A/Vision | 否 |
| `OPENAI_MODEL` | GPT 模型名，默认 `gpt-4` | 否 |
| `NEXT_PUBLIC_API_URL` | 前端访问的后端地址 | 是（前端运行时） |

## 提示
- 上传至少两期数据才能查看趋势；若同行对标为空，请确认上传的报表包含收入/利润/资产字段并选择行业。
- 语音输入依赖浏览器 Web Speech API，若网络受限可直接使用文本问答。
- 如需进一步精简或部署说明，可继续告知，我会按需处理。