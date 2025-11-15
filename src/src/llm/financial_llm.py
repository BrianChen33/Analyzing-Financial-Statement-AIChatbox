"""
LLM integration module for conversational AI and financial analysis
"""

import os
from typing import Dict, Any, List, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class FinancialLLM:
    """
    Handles LLM interactions for financial statement analysis and Q&A
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM client
        
        Args:
            api_key: OpenAI API key (if not provided, reads from environment)
        """
        if not OPENAI_AVAILABLE:
            raise ValueError("OpenAI library not installed. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.conversation_history = []
    
    def analyze_document_with_vision(self, image_base64: str, prompt: str = None) -> str:
        """
        Analyze financial statement image using GPT-4 Vision
        
        Args:
            image_base64: Base64 encoded image
            prompt: Custom prompt for analysis
            
        Returns:
            Analysis result from the model
        """
        if not prompt:
            prompt = """Analyze this financial statement image and extract:
            1. Key financial metrics (revenue, net income, assets, liabilities, equity)
            2. Important line items and their values
            3. Any notable observations or irregularities
            
            Provide the information in a structured format."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def generate_financial_insights(self, 
                                   financial_data: Dict[str, Any],
                                   ratios: Dict[str, float],
                                   risks: List[Dict[str, str]]) -> str:
        """
        Generate comprehensive insights from financial analysis
        
        Args:
            financial_data: Extracted financial metrics
            ratios: Calculated financial ratios
            risks: Identified risks
            
        Returns:
            AI-generated insights and recommendations
        """
        prompt = f"""As a financial analyst, provide comprehensive insights based on this financial data:

Financial Metrics:
{self._format_dict(financial_data)}

Financial Ratios:
{self._format_dict(ratios)}

Identified Risks:
{self._format_risks(risks)}

Please provide:
1. Overall financial health assessment
2. Key strengths and weaknesses
3. Trends and patterns
4. Recommendations for stakeholders
5. Areas requiring attention

Be specific, actionable, and professional."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst with deep knowledge of financial statements, ratios, and risk assessment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        """
        Answer user questions about the financial statement
        
        Args:
            question: User's question
            context: Financial data and analysis context
            
        Returns:
            Answer to the question
        """
        # Build context for the conversation
        context_str = f"""Financial Data Available:
{self._format_dict(context.get('financial_data', {}))}

Financial Ratios:
{self._format_dict(context.get('ratios', {}))}

Risks:
{self._format_risks(context.get('risks', []))}

Trends:
{self._format_dict(context.get('trends', {}))}
"""
        
        # Add to conversation history
        messages = [
            {"role": "system", "content": f"You are a helpful financial analyst assistant. Use this context to answer questions:\n\n{context_str}"}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[-5:])  # Keep last 5 exchanges
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            
            return answer
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def generate_summary(self, document_text: str) -> str:
        """
        Generate a concise summary of the financial statement
        
        Args:
            document_text: Full text of the financial document
            
        Returns:
            Summary of key points
        """
        prompt = f"""Summarize the following financial statement, highlighting:
1. Key financial figures
2. Most important insights
3. Notable changes or trends

Document:
{document_text[:3000]}  # Limit to avoid token limits

Provide a concise, structured summary."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert at summarizing financial statements."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def _format_dict(self, data: Dict) -> str:
        """Format dictionary for display"""
        return '\n'.join([f"  - {k}: {v}" for k, v in data.items()])
    
    def _format_risks(self, risks: List[Dict[str, str]]) -> str:
        """Format risks list for display"""
        if not risks:
            return "  - No significant risks identified"
        return '\n'.join([f"  - [{r['severity']}] {r['type']}: {r['description']}" for r in risks])
