# Demo and Screenshots

## Command Line Demo

### 1. Basic Analysis

```bash
$ python examples/basic_usage.py

============================================================
Financial Statement AI Chatbox - Basic Example
============================================================

1. Initializing chatbot...

2. Creating sample financial data...

Sample Financial Data:
  Revenue: $5,000,000
  Net Income: $500,000
  Total Assets: $10,000,000
  Total Liabilities: $6,000,000
  Equity: $4,000,000

3. Calculating financial ratios...

Calculated Ratios:
  Profit Margin: 10.00%
  Debt To Asset Ratio: 60.00%
  Roa: 5.00%
  Roe: 12.50%

4. Assessing financial risks...

Risk Assessment:
  ✓ No significant risks identified

5. Analyzing trends (with historical data)...

Trend Analysis:
  Revenue Trend: Increasing
  Revenue Growth Rate: 25.00%
  Profit Trend: Increasing
  Profit Growth Rate: 42.86%
```

### 2. Company Comparison

```bash
$ python examples/advanced_analysis.py

============================================================
Analyzing: Company A (Healthy)
============================================================

💰 Financial Metrics:
  Revenue: $10,000,000
  Net Income: $1,500,000
  Total Assets: $15,000,000
  Total Liabilities: $6,000,000
  Equity: $9,000,000

📊 Financial Ratios:
  Profit Margin: 15.00%
  Debt To Asset Ratio: 40.00%
  Roa: 10.00%
  Roe: 16.67%

⚠️  Risk Assessment:
  ✓ No significant risks identified - Strong financial position

============================================================
Company Comparison
============================================================

🏆 Best Profit Margin: Company A
```

### 3. Interactive Q&A

```bash
$ python src/chatbot.py financial_statement.pdf

📄 Parsing document: financial_statement.pdf
🔍 Extracting financial data...
📊 Calculating financial ratios...
⚠️  Assessing financial risks...
💡 Generating AI insights...

📊 Financial Statement Analysis Summary
==================================================
[Full analysis displayed]

💬 Interactive Q&A Mode (type 'exit' to quit)
--------------------------------------------------

Your question: What is the company's profitability?

🤖 Answer: Based on the analysis, the company has a profit 
margin of 10%, which indicates moderate profitability...

Your question: Are there any major risks?

🤖 Answer: The analysis shows no significant high-severity 
risks. The debt-to-asset ratio is at 60%, which is at the 
upper limit of what's considered healthy...
```

## Web Interface Demo

### Main Features

1. **Upload Interface** (Sidebar)
   - Drag and drop file upload
   - Support for PDF and images
   - One-click analysis button

2. **Summary Tab**
   - Key financial metrics displayed
   - Color-coded risk assessment
   - Download summary button

3. **Q&A Chat Tab**
   - ChatGPT-style interface
   - Context-aware responses
   - Conversation history

4. **Details Tab**
   - Metric cards with values
   - Color-coded risk indicators
   - AI-generated insights

### Sample Interactions

**User Uploads:** `annual_report_2023.pdf`

**System Displays:**
```
✅ Analysis complete!

Key Metrics:
- Revenue: $12,450,000
- Net Income: $1,890,000
- Profit Margin: 15.18%
- ROA: 8.23%

Risks:
✓ No significant risks identified

AI Insights:
The company demonstrates strong financial health with 
excellent profitability metrics. The 15.18% profit margin 
exceeds industry averages...
```

**User Asks:** "How does our debt level compare to assets?"

**System Responds:**
```
Your debt-to-asset ratio is 45%, which means that 45% of 
your assets are financed by debt. This is considered a 
healthy level, as it's well below the 60% threshold that 
typically indicates high leverage...
```

## Test Results

```bash
$ pytest tests/ -v

tests/test_chatbot.py::TestFinancialAnalyzer::test_calculate_ratios_profit_margin PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_calculate_ratios_roa PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_calculate_ratios_debt_to_asset PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_assess_risks_high_leverage PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_assess_risks_low_profitability PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_assess_risks_negative_income PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_identify_trends_increasing_revenue PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_identify_trends_decreasing_profit PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_identify_trends_insufficient_data PASSED
tests/test_chatbot.py::TestFinancialAnalyzer::test_extract_numbers PASSED
tests/test_chatbot.py::TestDocumentParser::test_supported_formats PASSED
tests/test_chatbot.py::TestDocumentParser::test_unsupported_format_raises_error PASSED
tests/test_chatbot.py::TestChatbotIntegration::test_chatbot_initialization PASSED
tests/test_chatbot.py::TestChatbotIntegration::test_chatbot_reset PASSED

============================================ 14 passed in 0.06s =============================================
```

## Performance Metrics

- **PDF Parsing**: < 1 second for typical 10-page document
- **Financial Analysis**: < 100ms for ratio calculations
- **LLM Response**: 2-5 seconds (depends on OpenAI API)
- **Memory Usage**: < 100MB for typical workload

## Browser Compatibility (Web Interface)

- ✅ Chrome/Edge (Chromium) 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (responsive design)

## System Requirements

- Python 3.8+
- 2GB RAM minimum
- Internet connection (for OpenAI API)
- Modern web browser (for Streamlit UI)

## Error Handling Examples

```python
# Invalid file format
>>> chatbot.upload_and_analyze('document.docx')
{'error': 'Unsupported file format: .docx'}

# Missing file
>>> chatbot.upload_and_analyze('nonexistent.pdf')
{'error': 'File not found: nonexistent.pdf'}

# Without API key (LLM features disabled gracefully)
>>> chatbot = FinancialChatbot()
Warning: OpenAI API key not found...
LLM features will be limited without API key.
```

## Real-World Use Cases

1. **Financial Analysts**: Quick preliminary analysis of financial statements
2. **Investors**: Rapid assessment of company financial health
3. **Accountants**: Automated ratio calculation and risk identification
4. **Business Owners**: Understanding their own financial statements
5. **Students**: Learning financial analysis concepts
6. **Auditors**: Initial screening of financial documents

## Next Steps

After viewing this demo, you can:
1. Try the live system: `streamlit run app.py`
2. Run your own analysis: `python src/chatbot.py your_file.pdf`
3. Explore the code: Check out `src/` directory
4. Run tests: `pytest tests/ -v`
5. Customize: Modify analyzers for your specific needs
