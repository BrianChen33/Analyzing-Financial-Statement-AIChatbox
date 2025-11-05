"""
Unit tests for the Financial Chatbot system
"""

import pytest
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analyzers.financial_analyzer import FinancialAnalyzer


class TestFinancialAnalyzer:
    """Test the financial analyzer module"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = FinancialAnalyzer()
    
    def test_calculate_ratios_profit_margin(self):
        """Test profit margin calculation"""
        financial_data = {
            'revenue': 1000000,
            'net_income': 100000
        }
        
        ratios = self.analyzer.calculate_ratios(financial_data)
        
        assert 'profit_margin' in ratios
        assert ratios['profit_margin'] == 10.0  # 100,000 / 1,000,000 * 100
    
    def test_calculate_ratios_roa(self):
        """Test Return on Assets calculation"""
        financial_data = {
            'net_income': 50000,
            'total_assets': 1000000
        }
        
        ratios = self.analyzer.calculate_ratios(financial_data)
        
        assert 'roa' in ratios
        assert ratios['roa'] == 5.0  # 50,000 / 1,000,000 * 100
    
    def test_calculate_ratios_debt_to_asset(self):
        """Test Debt-to-Asset ratio calculation"""
        financial_data = {
            'total_assets': 1000000,
            'total_liabilities': 600000
        }
        
        ratios = self.analyzer.calculate_ratios(financial_data)
        
        assert 'debt_to_asset_ratio' in ratios
        assert ratios['debt_to_asset_ratio'] == 60.0  # 600,000 / 1,000,000 * 100
    
    def test_assess_risks_high_leverage(self):
        """Test risk assessment for high leverage"""
        financial_data = {'net_income': 100000}
        ratios = {'debt_to_asset_ratio': 70}
        
        risks = self.analyzer.assess_risks(financial_data, ratios)
        
        # Should identify leverage risk
        leverage_risks = [r for r in risks if r['type'] == 'Leverage Risk']
        assert len(leverage_risks) > 0
        assert leverage_risks[0]['severity'] == 'Medium'
    
    def test_assess_risks_low_profitability(self):
        """Test risk assessment for low profitability"""
        financial_data = {'net_income': 100000}
        ratios = {'profit_margin': 3}
        
        risks = self.analyzer.assess_risks(financial_data, ratios)
        
        # Should identify profitability risk
        profit_risks = [r for r in risks if r['type'] == 'Profitability Risk']
        assert len(profit_risks) > 0
        assert profit_risks[0]['severity'] == 'High'
    
    def test_assess_risks_negative_income(self):
        """Test risk assessment for negative income"""
        financial_data = {'net_income': -50000}
        ratios = {}
        
        risks = self.analyzer.assess_risks(financial_data, ratios)
        
        # Should identify loss risk
        loss_risks = [r for r in risks if r['type'] == 'Loss Risk']
        assert len(loss_risks) > 0
        assert loss_risks[0]['severity'] == 'High'
    
    def test_identify_trends_increasing_revenue(self):
        """Test trend identification for increasing revenue"""
        historical_data = [
            {'revenue': 1000000, 'net_income': 50000},
            {'revenue': 1200000, 'net_income': 60000}
        ]
        
        trends = self.analyzer.identify_trends(historical_data)
        
        assert trends['revenue_trend'] == 'increasing'
        assert trends['revenue_growth_rate'] == 20.0  # (1,200,000 - 1,000,000) / 1,000,000 * 100
    
    def test_identify_trends_decreasing_profit(self):
        """Test trend identification for decreasing profit"""
        historical_data = [
            {'revenue': 1000000, 'net_income': 100000},
            {'revenue': 1100000, 'net_income': 80000}
        ]
        
        trends = self.analyzer.identify_trends(historical_data)
        
        assert trends['profit_trend'] == 'decreasing'
        assert trends['profit_growth_rate'] == -20.0  # (80,000 - 100,000) / 100,000 * 100
    
    def test_identify_trends_insufficient_data(self):
        """Test trend identification with insufficient data"""
        historical_data = [
            {'revenue': 1000000, 'net_income': 50000}
        ]
        
        trends = self.analyzer.identify_trends(historical_data)
        
        assert 'message' in trends
        assert 'Insufficient data' in trends['message']
    
    def test_extract_numbers(self):
        """Test number extraction from text"""
        text = "Revenue: 1,234,567.89 and expenses: 987,654.32"
        numbers = self.analyzer._extract_numbers(text)
        
        assert len(numbers) == 2
        assert numbers[0] == 1234567.89
        assert numbers[1] == 987654.32


class TestDocumentParser:
    """Test the document parser module"""
    
    def setup_method(self):
        """Setup test fixtures"""
        from src.parsers.document_parser import DocumentParser
        self.parser = DocumentParser()
    
    def test_supported_formats(self):
        """Test supported file formats"""
        assert '.pdf' in self.parser.supported_formats
        assert '.png' in self.parser.supported_formats
        assert '.jpg' in self.parser.supported_formats
        assert '.jpeg' in self.parser.supported_formats
    
    def test_unsupported_format_raises_error(self):
        """Test that unsupported formats raise an error"""
        with pytest.raises(ValueError, match="Unsupported file format"):
            self.parser.parse_document("test.docx")


class TestChatbotIntegration:
    """Integration tests for the chatbot"""
    
    def test_chatbot_initialization(self):
        """Test chatbot can be initialized"""
        from src.chatbot import FinancialChatbot
        
        # Should not raise any errors even without API key
        chatbot = FinancialChatbot()
        
        assert chatbot.parser is not None
        assert chatbot.analyzer is not None
        assert chatbot.current_document is None
        assert chatbot.analysis_results == {}
    
    def test_chatbot_reset(self):
        """Test chatbot reset functionality"""
        from src.chatbot import FinancialChatbot
        
        chatbot = FinancialChatbot()
        chatbot.analysis_results = {'test': 'data'}
        
        chatbot.reset()
        
        assert chatbot.current_document is None
        assert chatbot.analysis_results == {}


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
