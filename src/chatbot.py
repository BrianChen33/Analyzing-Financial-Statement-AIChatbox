"""
Main chatbot application integrating all components
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path

from src.parsers import DocumentParser
from src.analyzers import FinancialAnalyzer
from src.llm import FinancialLLM


class FinancialChatbot:
    """
    Main chatbot orchestrating document parsing, analysis, and conversational AI
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the chatbot with all necessary components
        
        Args:
            api_key: OpenAI API key (optional)
        """
        self.parser = DocumentParser()
        self.analyzer = FinancialAnalyzer()
        try:
            self.llm = FinancialLLM(api_key=api_key)
        except ValueError as e:
            print(f"Warning: {e}")
            print("LLM features will be limited without API key.")
            self.llm = None
        
        self.current_document = None
        self.analysis_results = {}
    
    def upload_and_analyze(self, file_path: str) -> Dict[str, Any]:
        """
        Upload and analyze a financial statement
        
        Args:
            file_path: Path to the financial statement file
            
        Returns:
            Comprehensive analysis results
        """
        if not os.path.exists(file_path):
            return {'error': f'File not found: {file_path}'}
        
        print(f"📄 Parsing document: {file_path}")
        
        # Step 1: Parse the document
        try:
            parsed_doc = self.parser.parse_document(file_path)
            self.current_document = parsed_doc
        except Exception as e:
            return {'error': f'Error parsing document: {str(e)}'}
        
        # Step 2: Extract financial data
        print("🔍 Extracting financial data...")
        
        if parsed_doc['type'] == 'pdf':
            # Extract text from all pages
            all_text = '\n'.join([page['text'] for page in parsed_doc['content']])
            financial_data = self.analyzer.extract_financial_data(all_text)
        elif parsed_doc['type'] == 'image' and self.llm:
            # Use vision model to extract data from image
            print("🤖 Using AI vision to analyze document...")
            analysis = self.llm.analyze_document_with_vision(parsed_doc['base64'])
            financial_data = {'llm_extraction': analysis}
            all_text = analysis
        else:
            financial_data = {}
            all_text = ""
        
        # Step 3: Calculate financial ratios
        print("📊 Calculating financial ratios...")
        ratios = self.analyzer.calculate_ratios(financial_data)
        
        # Step 4: Assess risks
        print("⚠️  Assessing financial risks...")
        risks = self.analyzer.assess_risks(financial_data, ratios)
        
        # Step 5: Generate insights using LLM
        insights = None
        if self.llm and financial_data:
            print("💡 Generating AI insights...")
            insights = self.llm.generate_financial_insights(financial_data, ratios, risks)
        
        # Store results for Q&A
        self.analysis_results = {
            'document_type': parsed_doc['type'],
            'financial_data': financial_data,
            'ratios': ratios,
            'risks': risks,
            'insights': insights,
            'raw_text': all_text if parsed_doc['type'] == 'pdf' else None
        }
        
        return self.analysis_results
    
    def ask_question(self, question: str) -> str:
        """
        Answer a question about the analyzed financial statement
        
        Args:
            question: User's question
            
        Returns:
            Answer to the question
        """
        if not self.analysis_results:
            return "Please upload and analyze a financial statement first."
        
        if not self.llm:
            return "LLM features are not available. Please configure OpenAI API key."
        
        return self.llm.answer_question(question, self.analysis_results)
    
    def get_summary(self) -> str:
        """
        Get a summary of the current analysis
        
        Returns:
            Summary of key findings
        """
        if not self.analysis_results:
            return "No document has been analyzed yet."
        
        summary = "📊 Financial Statement Analysis Summary\n"
        summary += "=" * 50 + "\n\n"
        
        # Financial Data
        if self.analysis_results.get('financial_data'):
            summary += "💰 Key Financial Metrics:\n"
            for key, value in self.analysis_results['financial_data'].items():
                if value is not None:
                    summary += f"  • {key.replace('_', ' ').title()}: {value:,.2f}\n" if isinstance(value, (int, float)) else f"  • {key.replace('_', ' ').title()}: {value}\n"
            summary += "\n"
        
        # Ratios
        if self.analysis_results.get('ratios'):
            summary += "📈 Financial Ratios:\n"
            for key, value in self.analysis_results['ratios'].items():
                summary += f"  • {key.replace('_', ' ').title()}: {value:.2f}%\n"
            summary += "\n"
        
        # Risks
        if self.analysis_results.get('risks'):
            summary += "⚠️  Identified Risks:\n"
            if not self.analysis_results['risks']:
                summary += "  • No significant risks identified\n"
            else:
                for risk in self.analysis_results['risks']:
                    summary += f"  • [{risk['severity']}] {risk['type']}: {risk['description']}\n"
            summary += "\n"
        
        # AI Insights
        if self.analysis_results.get('insights'):
            summary += "💡 AI-Generated Insights:\n"
            summary += self.analysis_results['insights'] + "\n"
        
        return summary
    
    def analyze_trends(self, historical_files: list) -> Dict[str, Any]:
        """
        Analyze trends across multiple financial statements
        
        Args:
            historical_files: List of file paths to historical statements
            
        Returns:
            Trend analysis results
        """
        historical_data = []
        
        for file_path in historical_files:
            parsed_doc = self.parser.parse_document(file_path)
            
            if parsed_doc['type'] == 'pdf':
                all_text = '\n'.join([page['text'] for page in parsed_doc['content']])
                financial_data = self.analyzer.extract_financial_data(all_text)
                historical_data.append(financial_data)
        
        trends = self.analyzer.identify_trends(historical_data)
        
        return {
            'periods_analyzed': len(historical_data),
            'trends': trends
        }
    
    def reset(self):
        """Reset the chatbot state"""
        self.current_document = None
        self.analysis_results = {}
        if self.llm:
            self.llm.reset_conversation()


def main():
    """
    Command-line interface for the Financial Chatbot
    """
    import sys
    
    print("🤖 Financial Statement AI Chatbot")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = FinancialChatbot()
    
    if len(sys.argv) < 2:
        print("\nUsage: python chatbot.py <path_to_financial_statement>")
        print("\nExample: python chatbot.py uploads/financial_statement.pdf")
        return
    
    file_path = sys.argv[1]
    
    # Analyze document
    print(f"\n📂 Analyzing: {file_path}\n")
    results = chatbot.upload_and_analyze(file_path)
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return
    
    # Display summary
    print("\n" + chatbot.get_summary())
    
    # Interactive Q&A
    print("\n💬 Interactive Q&A Mode (type 'exit' to quit)")
    print("-" * 50)
    
    while True:
        try:
            question = input("\nYour question: ").strip()
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not question:
                continue
            
            answer = chatbot.ask_question(question)
            print(f"\n🤖 Answer: {answer}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            break


if __name__ == '__main__':
    main()
