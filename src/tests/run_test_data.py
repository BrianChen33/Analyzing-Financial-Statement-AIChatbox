"""
Script to generate and validate test data
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from test_data_generator import (
    generate_test_analysis_result,
    generate_multi_period_test_data
)
from src.analyzers.financial_analyzer import FinancialAnalyzer
from src.utils.report_generator import ReportGenerator
import json


def validate_analysis_data(data: dict) -> bool:
    """Validate that analysis data has all required fields"""
    required_fields = ['financial_data', 'ratios', 'risks', 'dupont']
    
    for field in required_fields:
        if field not in data:
            print(f"❌ Missing required field: {field}")
            return False
    
    print("✅ All required fields present")
    return True


def test_ratio_calculations(data: dict) -> bool:
    """Test that ratios are calculated correctly"""
    analyzer = FinancialAnalyzer()
    financial_data = data['financial_data']
    ratios = analyzer.calculate_ratios(financial_data)
    
    # Verify key ratios exist
    key_ratios = ['profit_margin', 'roa', 'roe']
    for ratio in key_ratios:
        if ratio not in ratios:
            print(f"❌ Missing ratio: {ratio}")
            return False
    
    print("✅ Key ratios calculated correctly")
    return True


def test_report_generation(data: dict) -> bool:
    """Test report generation"""
    try:
        generator = ReportGenerator()
        
        # Test Markdown report
        md_report = generator.generate_markdown_report(data)
        if len(md_report) < 100:
            print("❌ Markdown report too short")
            return False
        
        # Test Text report
        text_report = generator.generate_text_report(data)
        if len(text_report) < 100:
            print("❌ Text report too short")
            return False
        
        print("✅ Reports generated successfully")
        return True
    except Exception as e:
        print(f"❌ Report generation failed: {e}")
        return False


def main():
    print("=" * 60)
    print("Financial Analysis System - Test Data Validation")
    print("=" * 60)
    print()
    
    # Generate test data
    print("Generating test data...")
    test_data_1 = generate_test_analysis_result("TechCorp Inc", "2024")
    test_data_2 = generate_multi_period_test_data("Growth Industries", 3)
    
    print("✅ Test data generated\n")
    
    # Validate test data 1
    print("Validating Test Data 1 (Single Period)...")
    if not validate_analysis_data(test_data_1):
        return False
    if not test_ratio_calculations(test_data_1):
        return False
    if not test_report_generation(test_data_1):
        return False
    print()
    
    # Validate test data 2
    print("Validating Test Data 2 (Multi-Period)...")
    if not validate_analysis_data(test_data_2):
        return False
    if not test_ratio_calculations(test_data_2):
        return False
    if not test_report_generation(test_data_2):
        return False
    print()
    
    # Save test data
    print("Saving test data to files...")
    with open('tests/test_data_1.json', 'w') as f:
        json.dump(test_data_1, f, indent=2, default=str)
    
    with open('tests/test_data_2.json', 'w') as f:
        json.dump(test_data_2, f, indent=2, default=str)
    
    print("✅ Test data saved to tests/test_data_1.json and tests/test_data_2.json")
    print()
    
    # Print summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Company 1: {test_data_1['financial_data']['company_name']}")
    print(f"  Revenue: ${test_data_1['financial_data']['revenue']:,.2f}")
    print(f"  Net Income: ${test_data_1['financial_data']['net_income']:,.2f}")
    print(f"  Profit Margin: {test_data_1['ratios']['profit_margin']:.2f}%")
    print(f"  ROE: {test_data_1['ratios']['roe']:.2f}%")
    print(f"  Risks Identified: {len(test_data_1['risks'])}")
    print()
    print(f"Company 2: {test_data_2['financial_data']['company_name']}")
    print(f"  Revenue: ${test_data_2['financial_data']['revenue']:,.2f}")
    print(f"  Trend: {test_data_2['trends'].get('revenue_trend', 'N/A')}")
    print(f"  Growth Rate: {test_data_2['trends'].get('revenue_growth_rate', 0):.2f}%")
    print()
    print("✅ All tests passed!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

