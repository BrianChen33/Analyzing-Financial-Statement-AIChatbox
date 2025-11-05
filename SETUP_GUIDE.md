# Complete Setup Guide

This guide will help you set up the Financial Statement AI Analyzer with the Next.js frontend.

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn
- OpenAI API key

## Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/BrianChen33/Analyzing-Financial-Statement-AIChatbox.git
cd Analyzing-Financial-Statement-AIChatbox
```

### Step 2: Backend Setup

1. **Create Python Virtual Environment (Recommended)**

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

2. **Install Python Dependencies**

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI & Uvicorn (API server)
- OpenAI (LLM integration)
- Pandas & OpenPyXL (Excel/CSV parsing)
- PyPDF2 (PDF parsing)
- Pillow (Image processing)
- And more...

3. **Configure Environment Variables**

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4
```

Get your API key from: https://platform.openai.com/api-keys

4. **Start the Backend Server**

```bash
python api_server.py
```

The API server will start on `http://localhost:8000`

You can verify it's running by visiting:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Step 3: Frontend Setup

1. **Install Node Dependencies**

```bash
cd frontend
npm install
```

This installs:
- Next.js 14
- React 18
- Material-UI 5
- ECharts for React
- TypeScript
- And more...

2. **Configure Frontend Environment**

Create `.env.local` file in the `frontend` directory:
```bash
echo "API_URL=http://localhost:8000" > .env.local
```

3. **Start the Development Server**

```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

### Step 4: Access the Application

Open your browser and navigate to: **http://localhost:3000**

You should see the Financial Statement AI Analyzer interface!

## Usage Guide

### Uploading Files

1. Click the upload area or drag and drop files
2. Supported formats:
   - PDF documents
   - Images (PNG, JPG, JPEG)
   - Excel files (.xlsx, .xls)
   - CSV files
   - XBRL files (.xbrl, .xml)

3. Click "Analyze Files" to process

### Viewing Results

The interface has 4 tabs:

1. **Upload**: File upload interface
2. **Dashboard**: Key metrics, charts, and risk assessment
3. **Q&A**: Interactive chat with AI assistant
4. **Trends**: Multi-period analysis and DuPont decomposition

### Using the Chat Interface

- Type questions about the analyzed financial statement
- Click the microphone icon for voice input (if supported by browser)
- Click the speaker icon to hear responses read aloud

## Production Deployment

### Backend Deployment

#### Option 1: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "api_server.py"]
```

Build and run:
```bash
docker build -t financial-analyzer-api .
docker run -p 8000:8000 --env-file .env financial-analyzer-api
```

#### Option 2: Railway/Render

1. Create `Procfile`:
```
web: python api_server.py
```

2. Deploy via Railway or Render dashboard
3. Add environment variables in the platform's settings

### Frontend Deployment

#### Option 1: Vercel (Recommended)

```bash
cd frontend
npm install -g vercel
vercel deploy
```

Set environment variable in Vercel dashboard:
```
API_URL=https://your-backend-url.com
```

#### Option 2: Netlify

```bash
cd frontend
npm run build
# Upload 'out' directory to Netlify
```

#### Option 3: Docker

Create `Dockerfile` in frontend directory:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Troubleshooting

### Backend Issues

**Problem**: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: 
```bash
pip install -r requirements.txt
```

**Problem**: "OpenAI API key not found"
**Solution**: Check that `.env` file exists and contains valid `OPENAI_API_KEY`

**Problem**: "Port 8000 already in use"
**Solution**: 
```bash
# Find and kill the process using port 8000
# On macOS/Linux:
lsof -ti:8000 | xargs kill -9
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**Problem**: "Module not found" errors
**Solution**: 
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: "Failed to fetch from API"
**Solution**: 
- Ensure backend is running on port 8000
- Check `API_URL` in `.env.local`
- Verify CORS settings in `api_server.py`

**Problem**: Build fails
**Solution**: 
```bash
cd frontend
npm run build
# Check for TypeScript errors
```

### Common Issues

**Problem**: CORS errors in browser console
**Solution**: Make sure backend `api_server.py` has correct CORS origins:
```python
allow_origins=["http://localhost:3000", "http://localhost:3001"]
```

**Problem**: Files upload but analysis fails
**Solution**: Check backend logs for errors. Ensure file format is supported.

## System Requirements

### Minimum Requirements
- 2GB RAM
- 1GB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Recommended Requirements
- 4GB RAM
- 2GB free disk space
- SSD storage
- Stable internet connection (for OpenAI API)

## Alternative: Streamlit Interface

If you prefer the simpler Streamlit interface:

```bash
# In the project root
streamlit run app.py
```

Access at: http://localhost:8501

## Getting Help

- Check `DEVELOPMENT.md` for development guidelines
- Review API documentation at http://localhost:8000/docs
- Open an issue on GitHub if you encounter problems

## Next Steps

After successful setup:
1. Upload a sample financial statement
2. Explore the dashboard and charts
3. Try the AI chat feature
4. Customize the analysis parameters
5. Export reports (coming soon)

Enjoy analyzing financial statements with AI! 🚀
