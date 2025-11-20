"""
Main chatbot application integrating all components
"""

import os
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from src.parsers import EnhancedDocumentParser
from src.analyzers import FinancialAnalyzer
from src.llm import FinancialLLM
from src.utils import (
    PeerBenchmark,
    extract_from_structured_data,
    extract_from_xbrl,
    build_cash_flow_summary,
    merge_llm_structured_data,
)


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
        self.parser = EnhancedDocumentParser()
        self.analyzer = FinancialAnalyzer()
        self.peer_benchmark = PeerBenchmark()
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
        
        financial_data, all_text = self._extract_data_from_parsed_doc(parsed_doc, file_path)
        
        # Step 3: Calculate financial ratios
        print("📊 Calculating financial ratios...")
        ratios = self.analyzer.calculate_ratios(financial_data)
        
        # Step 4: Assess risks
        print("⚠️  Assessing financial risks...")
        risks = self.analyzer.assess_risks(financial_data, ratios)
        
        # Step 5: Advanced analytics and AI insights
        dupont = self.analyzer.calculate_dupont_analysis(financial_data, ratios)
        benchmark = self.peer_benchmark.compare(financial_data, ratios)
        cash_flow_summary = build_cash_flow_summary(financial_data)
        insights = None
        if self.llm and financial_data:
            print("💡 Generating AI insights...")
            insights = self.llm.generate_financial_insights(financial_data, ratios, risks)
        
        # Store results for Q&A
        self.analysis_results = {
            'document_type': parsed_doc['type'],
            'period': Path(parsed_doc.get('file_path', file_path)).stem,
            'financial_data': financial_data,
            'ratios': ratios,
            'risks': risks,
            'insights': insights,
            'dupont': dupont,
            'benchmark': benchmark,
            'cash_flow': cash_flow_summary,
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
        
        # Benchmark
        if self.analysis_results.get('benchmark'):
            summary += "\n🏁 Peer Benchmarking:\n"
            summary += f"  • Industry: {self.analysis_results['benchmark'].get('industry')}\n"
            summary += f"  • Summary: {self.analysis_results['benchmark'].get('summary', 'N/A')}\n"
        
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
            financial_data, _ = self._extract_data_from_parsed_doc(parsed_doc, file_path)
            if financial_data:
                financial_data['period'] = Path(file_path).stem
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
    
    def _extract_data_from_parsed_doc(
        self,
        parsed_doc: Dict[str, Any],
        file_path: str
    ) -> Tuple[Dict[str, Any], str]:
        """
        Normalize data extraction handling for all supported document types.
        """
        doc_type = parsed_doc.get('type')
        all_text = ""
        financial_data: Dict[str, Any] = {}
        
        if doc_type == 'pdf':
            all_text = '\n'.join([page.get('text', '') for page in parsed_doc.get('content', [])])
            financial_data = self.analyzer.extract_financial_data(all_text)
            if self.llm and all_text.strip():
                try:
                    structured = self.llm.extract_structured_data(
                        all_text,
                        period_hint=Path(file_path).stem,
                    )
                    if structured:
                        financial_data, _, _ = merge_llm_structured_data(financial_data, structured)
                except Exception as exc:
                    print(f"Warning: LLM structured extraction failed: {exc}")
        elif doc_type in {'excel', 'csv'}:
            financial_data = extract_from_structured_data(parsed_doc)
        elif doc_type == 'xbrl':
            financial_data = extract_from_xbrl(parsed_doc)
        elif doc_type == 'image' and self.llm:
            print("🤖 Using AI vision to analyze document...")
            try:
                analysis = self.llm.analyze_document_with_vision(parsed_doc['base64'])
                financial_data = {'llm_extraction': analysis}
                all_text = analysis
            except NotImplementedError:
                financial_data = {}
                all_text = ""
                print("Vision analysis is not supported in the current LLM provider.")
            except Exception as exc:
                financial_data = {}
                print(f"Vision analysis failed: {exc}")
        else:
            financial_data = {}
        
        return financial_data, all_text


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
