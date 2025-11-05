"""
Example: Advanced analysis with custom data
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analyzers import FinancialAnalyzer


def analyze_company(name, data):
    """Analyze a company's financial data"""
    print(f"\n{'=' * 60}")
    print(f"Analyzing: {name}")
    print('=' * 60)
    
    analyzer = FinancialAnalyzer()
    
    # Display financial data
    print("\n💰 Financial Metrics:")
    for key, value in data.items():
        print(f"  {key.replace('_', ' ').title()}: ${value:,}")
    
    # Calculate and display ratios
    ratios = analyzer.calculate_ratios(data)
    print("\n📊 Financial Ratios:")
    for key, value in ratios.items():
        print(f"  {key.replace('_', ' ').title()}: {value:.2f}%")
    
    # Assess risks
    risks = analyzer.assess_risks(data, ratios)
    print("\n⚠️  Risk Assessment:")
    if not risks:
        print("  ✓ No significant risks identified - Strong financial position")
    else:
        for risk in risks:
            severity_emoji = "🔴" if risk['severity'] == 'High' else "🟡"
            print(f"  {severity_emoji} [{risk['severity']}] {risk['type']}")
            print(f"     → {risk['description']}")
    
    return ratios, risks


def compare_companies(companies_data):
    """Compare multiple companies"""
    print("\n" + "=" * 60)
    print("Company Comparison")
    print("=" * 60)
    
    analyzer = FinancialAnalyzer()
    
    comparison = {}
    for name, data in companies_data.items():
        ratios = analyzer.calculate_ratios(data)
        comparison[name] = ratios
    
    # Compare profit margins
    print("\n📈 Profit Margin Comparison:")
    for name, ratios in comparison.items():
        if 'profit_margin' in ratios:
            print(f"  {name}: {ratios['profit_margin']:.2f}%")
    
    # Compare ROA
    print("\n📈 Return on Assets (ROA) Comparison:")
    for name, ratios in comparison.items():
        if 'roa' in ratios:
            print(f"  {name}: {ratios['roa']:.2f}%")
    
    # Identify best performer
    profit_margins = {name: ratios.get('profit_margin', 0) 
                     for name, ratios in comparison.items()}
    if profit_margins:
        best_performer = max(profit_margins, key=profit_margins.get)
        print(f"\n🏆 Best Profit Margin: {best_performer}")


def main():
    """
    Demonstrate advanced financial analysis
    """
    print("=" * 60)
    print("Financial Analysis - Advanced Example")
    print("=" * 60)
    
    # Company A - Healthy company
    company_a = {
        'revenue': 10000000,
        'net_income': 1500000,
        'total_assets': 15000000,
        'total_liabilities': 6000000,
        'equity': 9000000
    }
    
    # Company B - High leverage
    company_b = {
        'revenue': 8000000,
        'net_income': 800000,
        'total_assets': 12000000,
        'total_liabilities': 9000000,
        'equity': 3000000
    }
    
    # Company C - Low profitability
    company_c = {
        'revenue': 12000000,
        'net_income': 300000,
        'total_assets': 20000000,
        'total_liabilities': 10000000,
        'equity': 10000000
    }
    
    # Analyze each company
    analyze_company("Company A (Healthy)", company_a)
    analyze_company("Company B (High Leverage)", company_b)
    analyze_company("Company C (Low Profitability)", company_c)
    
    # Compare companies
    companies = {
        'Company A': company_a,
        'Company B': company_b,
        'Company C': company_c
    }
    
    compare_companies(companies)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
