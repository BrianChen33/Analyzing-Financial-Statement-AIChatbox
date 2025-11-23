echo TONGYI_MODEL=qwen-plus >> .env
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
# Financial Statement AI Chatbox

Modern FastAPI + Next.js workspace for multimodal financial-statement analysis, now powered end-to-end by Alibaba Cloud's Tongyi Qianwen LLM.
This is a project by Group 17.
Group member:
CHEN Fengyuan 23096069D
FU Shenghong 22108687D
JIANG Zeyou 23098309D

## Feature Highlights
- **Multi-format parsing** – ingest PDF, image, Excel, CSV, and XBRL statements with automatic normalization.
- **Insightful analytics** – profitability/liquidity/leverage/efficiency ratios, DuPont drill-down, cash-flow rollups, and historical trend detection.
- **Risk + peer benchmarking** – compare against General/Technology/Retail/Manufacturing yardsticks and surface alert narratives.
- **Tongyi-native AI** – structured extraction, dashboard insights, and conversational Q&A via the DashScope OpenAI-compatible endpoint (Singapore region by default).
- **Responsive front end** – Material UI dashboard with authentication, upload workflow, KPI cards, and persistent Q&A archives.

## Quick Start
```bash
git clone <repo>
cd Analyzing-Financial-Statement-AIChatbox

# Backend
python -m venv .venv
.venv\Scripts\activate  # or source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt

# Configure Tongyi Qianwen
echo TONGYI_API_KEY=your_tongyi_api_key >> .env
echo TONGYI_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1 >> .env
echo TONGYI_MODEL=qwen-plus >> .env


python api_server.py  # runs on http://localhost:8000

# Frontend
cd frontend
npm install
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
npm run dev  # runs on http://localhost:3000
```
Upload one or more statements, pick the closest industry, and the dashboard will populate metrics, risks, peer comparisons, and AI-driven commentary entirely in English.

## Authentication & Chat History
1. Register or sign in from the front-end auth panel (emails are stored in `data/users.json`, which is git-ignored).
2. Every chat exchange is appended to `data/chat_history.json` and rendered in the Conversation Archive sidebar.
3. Remove those JSON files to reset credentials or chat history.

## Common Scripts
- `python api_server.py` – FastAPI backend
- `streamlit run app.py` – optional Streamlit UI
- `npm run dev` – Next.js frontend
- `pytest tests -q` – backend unit tests

## Project Layout
```
├── api_server.py
├── app.py
├── requirements.txt
├── src/            # parsers, analytics, Tongyi client, utilities
├── frontend/       # Next.js dashboard
└── tests/          # pytest coverage
```

## Environment Variables
| Variable | Description | Required |
| --- | --- | --- |
| `TONGYI_API_KEY` | DashScope/Tongyi API key (never check real keys into git) | Yes |
| `TONGYI_BASE_URL` | Base URL for the compatible-mode endpoint (defaults to `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`) | No |
| `TONGYI_MODEL` | Tongyi chat model name (defaults to `qwen-plus`) | No |
| `NEXT_PUBLIC_API_URL` | Front-end URL for the FastAPI backend | Yes (frontend) |

## Tips
- Upload at least two periods to unlock the revenue/profit trend charts.
- If benchmarking returns empty results, confirm that the uploaded statement contains revenue/profit/asset fields and that the industry selector is set.
- Voice input relies on the browser Web Speech API; fall back to text chat when network restrictions apply.
- Theme tweaks live in `frontend/src/pages/_app.tsx` if you want to match corporate branding.
- For demostration, you can use this into `.env`:
- TONGYI_API_KEY=sk-5cf4c238d79e4fb1bcc7e8e5d307c0b3
- TONGYI_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
- TONGYI_MODEL=qwen-plus