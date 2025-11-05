"""
Financial analyzer module for calculating key financial indicators,
identifying trends, and assessing risks
"""

from typing import Dict, Any, List


class FinancialAnalyzer:
    """
    Analyzes financial statements and calculates key financial indicators
    """
    
    def __init__(self):
        self.indicators = []
    
    def extract_financial_data(self, text_data: str) -> Dict[str, Any]:
        """
        Extract financial data from text content
        
        Args:
            text_data: Text content from financial statement
            
        Returns:
            Dictionary with extracted financial data
        """
        # This is a simplified extraction - in production, would use more sophisticated NLP
        financial_data = {
            'revenue': None,
            'net_income': None,
            'total_assets': None,
            'total_liabilities': None,
            'equity': None,
            'cash_flow': None
        }
        
        # Look for common financial statement keywords
        lines = text_data.lower().split('\n')
        for line in lines:
            if 'revenue' in line or 'sales' in line:
                # Extract numeric values (simplified)
                numbers = self._extract_numbers(line)
                if numbers and not financial_data['revenue']:
                    financial_data['revenue'] = numbers[0]
            
            if 'net income' in line:
                numbers = self._extract_numbers(line)
                if numbers and not financial_data['net_income']:
                    financial_data['net_income'] = numbers[0]
            
            if 'total assets' in line:
                numbers = self._extract_numbers(line)
                if numbers and not financial_data['total_assets']:
                    financial_data['total_assets'] = numbers[0]
            
            if 'total liabilities' in line:
                numbers = self._extract_numbers(line)
                if numbers and not financial_data['total_liabilities']:
                    financial_data['total_liabilities'] = numbers[0]
        
        return financial_data
    
    def calculate_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate key financial ratios
        
        Args:
            financial_data: Dictionary with financial metrics
            
        Returns:
            Dictionary with calculated ratios
        """
        ratios = {}
        
        # Profitability Ratios
        if financial_data.get('revenue') and financial_data.get('net_income'):
            if financial_data['revenue'] > 0:
                ratios['profit_margin'] = (financial_data['net_income'] / financial_data['revenue']) * 100
        
        # Leverage Ratios
        if financial_data.get('total_assets') and financial_data.get('total_liabilities'):
            if financial_data['total_assets'] > 0:
                ratios['debt_to_asset_ratio'] = (financial_data['total_liabilities'] / financial_data['total_assets']) * 100
        
        # Return on Assets (ROA)
        if financial_data.get('net_income') and financial_data.get('total_assets'):
            if financial_data['total_assets'] > 0:
                ratios['roa'] = (financial_data['net_income'] / financial_data['total_assets']) * 100
        
        # Return on Equity (ROE)
        if financial_data.get('net_income') and financial_data.get('equity'):
            if financial_data['equity'] and financial_data['equity'] > 0:
                ratios['roe'] = (financial_data['net_income'] / financial_data['equity']) * 100
        
        return ratios
    
    def identify_trends(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify trends from historical financial data
        
        Args:
            historical_data: List of financial data dictionaries from multiple periods
            
        Returns:
            Dictionary with trend analysis
        """
        trends = {
            'revenue_trend': None,
            'profit_trend': None,
            'growth_rate': None
        }
        
        if len(historical_data) < 2:
            trends['message'] = "Insufficient data for trend analysis. Need at least 2 periods."
            return trends
        
        # Calculate revenue trend
        revenues = [d.get('revenue', 0) for d in historical_data if d.get('revenue')]
        if len(revenues) >= 2:
            growth = ((revenues[-1] - revenues[0]) / revenues[0]) * 100 if revenues[0] > 0 else 0
            trends['revenue_trend'] = 'increasing' if growth > 0 else 'decreasing'
            trends['revenue_growth_rate'] = round(growth, 2)
        
        # Calculate profit trend
        profits = [d.get('net_income', 0) for d in historical_data if d.get('net_income')]
        if len(profits) >= 2:
            growth = ((profits[-1] - profits[0]) / profits[0]) * 100 if profits[0] > 0 else 0
            trends['profit_trend'] = 'increasing' if growth > 0 else 'decreasing'
            trends['profit_growth_rate'] = round(growth, 2)
        
        return trends
    
    def assess_risks(self, financial_data: Dict[str, Any], ratios: Dict[str, float]) -> List[Dict[str, str]]:
        """
        Assess financial risks based on ratios and data
        
        Args:
            financial_data: Financial metrics
            ratios: Calculated financial ratios
            
        Returns:
            List of identified risks with severity levels
        """
        risks = []
        
        # Check profitability risk
        if ratios.get('profit_margin', 0) < 5:
            risks.append({
                'type': 'Profitability Risk',
                'severity': 'High',
                'description': 'Profit margin is below 5%, indicating low profitability'
            })
        
        # Check leverage risk
        if ratios.get('debt_to_asset_ratio', 0) > 60:
            risks.append({
                'type': 'Leverage Risk',
                'severity': 'Medium',
                'description': 'Debt-to-asset ratio exceeds 60%, indicating high leverage'
            })
        
        # Check negative income
        if financial_data.get('net_income', 0) < 0:
            risks.append({
                'type': 'Loss Risk',
                'severity': 'High',
                'description': 'Company is reporting net losses'
            })
        
        # Check ROA
        if ratios.get('roa', 0) < 2:
            risks.append({
                'type': 'Asset Efficiency Risk',
                'severity': 'Medium',
                'description': 'Return on assets is below 2%, indicating poor asset utilization'
            })
        
        return risks
    
    def _extract_numbers(self, text: str) -> List[float]:
        """Extract numeric values from text"""
        import re
        # Find numbers with optional commas and decimals
        numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', text)
        return [float(n.replace(',', '')) for n in numbers]
