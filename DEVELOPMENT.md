# Development Guide

## Project Structure

```
Analyzing-Financial-Statement-AIChatbox/
├── frontend/                 # Next.js + Material-UI frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Next.js pages
│   │   ├── styles/          # CSS styles
│   │   └── utils/           # Utility functions
│   ├── package.json
│   └── tsconfig.json
├── src/                     # Python backend
│   ├── parsers/             # Document parsers
│   │   ├── document_parser.py        # Original parser
│   │   └── enhanced_parser.py        # Enhanced multi-format parser
│   ├── analyzers/           # Financial analysis
│   ├── llm/                 # LLM integration
│   └── chatbot.py           # Main chatbot orchestrator
├── api_server.py            # FastAPI REST API
├── app.py                   # Streamlit interface (legacy)
├── requirements.txt         # Python dependencies
└── README.md

```

## Backend Development

### Adding New Document Formats

1. Update `EnhancedDocumentParser` in `src/parsers/enhanced_parser.py`
2. Add parser method (e.g., `_parse_new_format`)
3. Update `supported_formats` list
4. Add format to API endpoint handling

Example:
```python
def _parse_new_format(self, file_path: str) -> Dict[str, Any]:
    # Parsing logic here
    return {
        'type': 'new_format',
        'data': extracted_data,
        'file_path': file_path
    }
```

### Adding New Financial Indicators

1. Update `FinancialAnalyzer` in `src/analyzers/financial_analyzer.py`
2. Add calculation method to `calculate_ratios()`
3. Update risk assessment rules if needed

Example:
```python
def calculate_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
    ratios = {}
    # ... existing ratios ...
    
    # New indicator
    if financial_data.get('revenue') and financial_data.get('operating_expenses'):
        ratios['operating_margin'] = (
            (financial_data['revenue'] - financial_data['operating_expenses']) /
            financial_data['revenue']
        ) * 100
    
    return ratios
```

### Adding API Endpoints

1. Add endpoint to `api_server.py`
2. Define request/response models with Pydantic
3. Implement business logic
4. Add error handling

Example:
```python
@app.post("/api/new-endpoint")
async def new_endpoint(request: NewRequest):
    try:
        # Business logic
        result = process_request(request)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Frontend Development

### Adding New Components

1. Create component in `frontend/src/components/`
2. Use TypeScript and Material-UI
3. Import and use in pages

Example:
```typescript
import { Box, Paper, Typography } from '@mui/material'

interface MyComponentProps {
  data: any
}

export default function MyComponent({ data }: MyComponentProps) {
  return (
    <Paper>
      <Typography variant="h6">{data.title}</Typography>
      {/* Component content */}
    </Paper>
  )
}
```

### Adding New Pages

1. Create file in `frontend/src/pages/`
2. Next.js automatically routes based on filename
3. Use existing layout components

### Styling

- Use Material-UI's `sx` prop for inline styling
- Global styles in `frontend/src/styles/globals.css`
- Theme configuration in `frontend/src/pages/_app.tsx`

## Testing

### Backend Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_chatbot.py -v

# Run with coverage
pytest --cov=src tests/
```

### Frontend Tests (Coming Soon)

```bash
cd frontend
npm test
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=10485760
```

### Frontend (.env.local)
```
API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Financial Statement Analyzer
```

## Deployment

### Backend Deployment

1. **Docker** (Recommended):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api_server.py"]
```

2. **Railway/Heroku**:
```
web: python api_server.py
```

### Frontend Deployment

1. **Vercel** (Recommended):
```bash
cd frontend
vercel deploy
```

2. **Docker**:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## Performance Optimization

### Backend
- Use async/await for I/O operations
- Cache LLM responses
- Implement rate limiting
- Use connection pooling for database

### Frontend
- Use React.memo for expensive components
- Implement code splitting
- Optimize images
- Use SWR for data fetching

## Security Best Practices

1. **Never commit .env files**
2. **Validate all user inputs**
3. **Use HTTPS in production**
4. **Implement rate limiting**
5. **Sanitize file uploads**
6. **Use environment variables for secrets**

## Troubleshooting

### Common Issues

**Issue**: "Module not found" errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
cd frontend && npm install
```

**Issue**: CORS errors in frontend
**Solution**: Check API_URL in `.env.local` and CORS settings in `api_server.py`

**Issue**: LLM features not working
**Solution**: Verify OPENAI_API_KEY in `.env`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Material-UI Documentation](https://mui.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
