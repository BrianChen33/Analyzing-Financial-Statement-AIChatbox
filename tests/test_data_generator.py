"""
Generate test data for financial statement analysis
"""

import json
from typing import Dict, Any


def generate_test_financial_data(company_name: str = "Test Company", period: str = "2024") -> Dict[str, Any]:
    """
    Generate realistic test financial data
    
    Args:
        company_name: Name of the company
        period: Period identifier
        
    Returns:
        Dictionary with financial data
    """
    # Base values for a healthy company
    revenue = 10000000
    gross_profit = revenue * 0.4  # 40% gross margin
    operating_income = revenue * 0.15  # 15% operating margin
    net_income = revenue * 0.10  # 10% net margin
    
    total_assets = revenue * 1.5
    current_assets = total_assets * 0.4
    total_liabilities = total_assets * 0.5
    current_liabilities = total_liabilities * 0.4
    equity = total_assets - total_liabilities
    
    cash = current_assets * 0.3
    inventory = current_assets * 0.3
    accounts_receivable = current_assets * 0.4
    
    operating_cash_flow = net_income * 1.2
    investing_cash_flow = -revenue * 0.1
    financing_cash_flow = -revenue * 0.05
    free_cash_flow = operating_cash_flow + investing_cash_flow
    
    total_debt = total_liabilities * 0.6
    interest_expense = total_debt * 0.05
    
    return {
        'company_name': company_name,
        'period': period,
        'revenue': revenue,
        'sales': revenue,
        'gross_profit': gross_profit,
        'operating_income': operating_income,
        'net_income': net_income,
        'total_assets': total_assets,
        'current_assets': current_assets,
        'total_liabilities': total_liabilities,
        'current_liabilities': current_liabilities,
        'equity': equity,
        'cash': cash,
        'cash_equivalents': cash,
        'inventory': inventory,
        'accounts_receivable': accounts_receivable,
        'operating_cash_flow': operating_cash_flow,
        'investing_cash_flow': investing_cash_flow,
        'financing_cash_flow': financing_cash_flow,
        'free_cash_flow': free_cash_flow,
        'total_debt': total_debt,
        'interest_expense': interest_expense
    }


def generate_test_analysis_result(company_name: str = "Test Company", period: str = "2024") -> Dict[str, Any]:
    """
    Generate complete test analysis result
    
    Args:
        company_name: Name of the company
        period: Period identifier
        
    Returns:
        Complete analysis result dictionary
    """
    from src.analyzers.financial_analyzer import FinancialAnalyzer
    
    analyzer = FinancialAnalyzer()
    financial_data = generate_test_financial_data(company_name, period)
    
    ratios = analyzer.calculate_ratios(financial_data)
    risks = analyzer.assess_risks(financial_data, ratios)
    dupont = analyzer.calculate_dupont_analysis(financial_data, ratios)
    
    return {
        'filename': f'{company_name}_{period}.pdf',
        'type': 'pdf',
        'financial_data': financial_data,
        'ratios': ratios,
        'risks': risks,
        'dupont': dupont,
        'insights': f"Based on the financial analysis, {company_name} demonstrates strong financial performance with healthy profitability ratios and manageable leverage. The company shows good liquidity and efficient asset utilization.",
        'trends': None
    }


def generate_multi_period_test_data(company_name: str = "Test Company", periods: int = 3) -> Dict[str, Any]:
    """
    Generate multi-period test data for trend analysis
    
    Args:
        company_name: Name of the company
        periods: Number of periods to generate
        
    Returns:
        Analysis result with trend data
    """
    from src.analyzers.financial_analyzer import FinancialAnalyzer
    
    analyzer = FinancialAnalyzer()
    historical_data = []
    
    base_revenue = 10000000
    growth_rate = 0.15  # 15% annual growth
    
    for i in range(periods):
        period = f"202{4-i}" if periods <= 3 else f"202{4-i}"
        revenue = base_revenue * ((1 + growth_rate) ** (periods - 1 - i))
        
        financial_data = generate_test_financial_data(company_name, period)
        financial_data['revenue'] = revenue
        financial_data['net_income'] = revenue * 0.10
        financial_data['total_assets'] = revenue * 1.5
        
        historical_data.append(financial_data)
    
    # Use latest period for main analysis
    latest_data = historical_data[-1]
    ratios = analyzer.calculate_ratios(latest_data)
    risks = analyzer.assess_risks(latest_data, ratios)
    dupont = analyzer.calculate_dupont_analysis(latest_data, ratios)
    trends = analyzer.identify_trends(historical_data)
    
    return {
        'filename': f'{company_name}_multi_period.pdf',
        'type': 'pdf',
        'financial_data': latest_data,
        'ratios': ratios,
        'risks': risks,
        'dupont': dupont,
        'trends': trends,
        'historical_data': historical_data,
        'insights': f"Multi-period analysis for {company_name} shows consistent growth trends with improving financial metrics over time."
    }


if __name__ == "__main__":
    # Generate and save test data
    test_data_1 = generate_test_analysis_result("TechCorp Inc", "2024")
    test_data_2 = generate_test_analysis_result("Manufacturing Co", "2024")
    test_data_3 = generate_multi_period_test_data("Growth Industries", 3)
    
    # Save to JSON files
    with open('tests/test_data_1.json', 'w') as f:
        json.dump(test_data_1, f, indent=2, default=str)
    
    with open('tests/test_data_2.json', 'w') as f:
        json.dump(test_data_2, f, indent=2, default=str)
    
    with open('tests/test_data_3.json', 'w') as f:
        json.dump(test_data_3, f, indent=2, default=str)
    
    print("Test data generated successfully!")
    print(f"- test_data_1.json: Single period analysis for TechCorp Inc")
    print(f"- test_data_2.json: Single period analysis for Manufacturing Co")
    print(f"- test_data_3.json: Multi-period analysis for Growth Industries")

