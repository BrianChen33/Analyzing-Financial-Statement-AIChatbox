"""
Example: Basic usage of the Financial Chatbot
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.chatbot import FinancialChatbot


def main():
    """
    Demonstrate basic chatbot functionality
    """
    print("=" * 60)
    print("Financial Statement AI Chatbox - Basic Example")
    print("=" * 60)
    
    # Initialize chatbot
    print("\n1. Initializing chatbot...")
    chatbot = FinancialChatbot()
    
    # Example: Manual financial data entry
    print("\n2. Creating sample financial data...")
    
    from src.analyzers import FinancialAnalyzer
    analyzer = FinancialAnalyzer()
    
    # Sample financial data
    financial_data = {
        'revenue': 5000000,
        'net_income': 500000,
        'total_assets': 10000000,
        'total_liabilities': 6000000,
        'equity': 4000000
    }
    
    print("\nSample Financial Data:")
    for key, value in financial_data.items():
        print(f"  {key.replace('_', ' ').title()}: ${value:,}")
    
    # Calculate ratios
    print("\n3. Calculating financial ratios...")
    ratios = analyzer.calculate_ratios(financial_data)
    
    print("\nCalculated Ratios:")
    for key, value in ratios.items():
        print(f"  {key.replace('_', ' ').title()}: {value:.2f}%")
    
    # Assess risks
    print("\n4. Assessing financial risks...")
    risks = analyzer.assess_risks(financial_data, ratios)
    
    print("\nRisk Assessment:")
    if not risks:
        print("  ✓ No significant risks identified")
    else:
        for risk in risks:
            print(f"  [{risk['severity']}] {risk['type']}")
            print(f"    → {risk['description']}")
    
    # Trend analysis example
    print("\n5. Analyzing trends (with historical data)...")
    
    historical_data = [
        {'revenue': 4000000, 'net_income': 350000},  # Previous year
        {'revenue': 4500000, 'net_income': 425000},  # Middle year
        {'revenue': 5000000, 'net_income': 500000}   # Current year
    ]
    
    trends = analyzer.identify_trends(historical_data)
    
    print("\nTrend Analysis:")
    if 'revenue_trend' in trends and trends['revenue_trend']:
        print(f"  Revenue Trend: {trends['revenue_trend'].title()}")
        print(f"  Revenue Growth Rate: {trends['revenue_growth_rate']:.2f}%")
    if 'profit_trend' in trends and trends['profit_trend']:
        print(f"  Profit Trend: {trends['profit_trend'].title()}")
        print(f"  Profit Growth Rate: {trends['profit_growth_rate']:.2f}%")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)
    
    # Show next steps
    print("\n📚 Next Steps:")
    print("  1. Try the web interface: streamlit run app.py")
    print("  2. Analyze real documents: python src/chatbot.py <file.pdf>")
    print("  3. Check out more examples in the examples/ directory")


if __name__ == '__main__':
    main()
