"""
Report generation module for exporting financial analysis reports
"""

from typing import Dict, Any, Optional
from datetime import datetime
import os


class ReportGenerator:
    """Generate financial analysis reports in various formats"""
    
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    
    def generate_markdown_report(self, analysis_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Generate a Markdown format report
        
        Args:
            analysis_data: Complete analysis results
            filename: Optional filename to save the report
            
        Returns:
            Markdown report content
        """
        financial_data = analysis_data.get('financial_data', {})
        ratios = analysis_data.get('ratios', {})
        risks = analysis_data.get('risks', [])
        trends = analysis_data.get('trends', {})
        insights = analysis_data.get('insights', '')
        benchmark = analysis_data.get('benchmark')
        dupont = analysis_data.get('dupont', {})
        benchmark = analysis_data.get('benchmark')
        
        report = []
        report.append("# Financial Statement Analysis Report\n")
        report.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append("---\n\n")
        
        # Executive Summary
        report.append("## Executive Summary\n\n")
        if insights:
            report.append(f"{insights}\n\n")
        else:
            report.append("This report provides a comprehensive analysis of the financial statement.\n\n")
        
        # Financial Data
        report.append("## Key Financial Metrics\n\n")
        report.append("| Metric | Value |\n")
        report.append("|--------|-------|\n")
        
        metrics = [
            ('Revenue', financial_data.get('revenue')),
            ('Net Income', financial_data.get('net_income')),
            ('Total Assets', financial_data.get('total_assets')),
            ('Total Liabilities', financial_data.get('total_liabilities')),
            ('Equity', financial_data.get('equity')),
            ('Gross Profit', financial_data.get('gross_profit')),
            ('Operating Income', financial_data.get('operating_income')),
        ]
        
        for metric, value in metrics:
            if value is not None:
                if isinstance(value, (int, float)):
                    formatted_value = f"${value:,.2f}" if abs(value) >= 1 else f"${value:.2f}"
                else:
                    formatted_value = str(value)
                report.append(f"| {metric} | {formatted_value} |\n")
        
        report.append("\n")
        
        # Financial Ratios
        report.append("## Financial Ratios\n\n")
        report.append("### Profitability Ratios\n\n")
        report.append("| Ratio | Value |\n")
        report.append("|-------|-------|\n")
        
        profitability_ratios = [
            ('Profit Margin', ratios.get('profit_margin'), '%'),
            ('Gross Margin', ratios.get('gross_margin'), '%'),
            ('Operating Margin', ratios.get('operating_margin'), '%'),
            ('ROA', ratios.get('roa'), '%'),
            ('ROE', ratios.get('roe'), '%'),
        ]
        
        for ratio_name, value, unit in profitability_ratios:
            if value is not None:
                report.append(f"| {ratio_name} | {value:.2f}{unit} |\n")
        
        report.append("\n### Liquidity Ratios\n\n")
        report.append("| Ratio | Value |\n")
        report.append("|-------|-------|\n")
        
        liquidity_ratios = [
            ('Current Ratio', ratios.get('current_ratio'), ''),
            ('Quick Ratio', ratios.get('quick_ratio'), ''),
            ('Cash Ratio', ratios.get('cash_ratio'), ''),
        ]
        
        for ratio_name, value, unit in liquidity_ratios:
            if value is not None:
                report.append(f"| {ratio_name} | {value:.2f}{unit} |\n")
        
        report.append("\n### Leverage Ratios\n\n")
        report.append("| Ratio | Value |\n")
        report.append("|-------|-------|\n")
        
        leverage_ratios = [
            ('Debt-to-Asset Ratio', ratios.get('debt_to_asset_ratio'), '%'),
            ('Debt-to-Equity Ratio', ratios.get('debt_to_equity_ratio'), '%'),
            ('Equity Multiplier', ratios.get('equity_multiplier'), 'x'),
            ('Interest Coverage', ratios.get('interest_coverage'), 'x'),
        ]
        
        for ratio_name, value, unit in leverage_ratios:
            if value is not None:
                report.append(f"| {ratio_name} | {value:.2f}{unit} |\n")
        
        report.append("\n### Efficiency Ratios\n\n")
        report.append("| Ratio | Value |\n")
        report.append("|-------|-------|\n")
        
        efficiency_ratios = [
            ('Asset Turnover', ratios.get('asset_turnover'), 'x'),
            ('Inventory Turnover', ratios.get('inventory_turnover'), 'x'),
        ]
        
        for ratio_name, value, unit in efficiency_ratios:
            if value is not None:
                report.append(f"| {ratio_name} | {value:.2f}{unit} |\n")
        
        # DuPont Analysis
        if dupont and dupont.get('roe') is not None:
            report.append("\n## DuPont Analysis\n\n")
            report.append("ROE decomposition:\n\n")
            report.append(f"- **ROE:** {dupont.get('roe', 0):.2f}%\n")
            report.append(f"- **Profit Margin:** {dupont.get('profit_margin', 0):.2f}%\n")
            report.append(f"- **Asset Turnover:** {dupont.get('asset_turnover', 0):.2f}x\n")
            report.append(f"- **Equity Multiplier:** {dupont.get('equity_multiplier', 0):.2f}x\n\n")
        
        # Trend Analysis
        if trends:
            report.append("## Trend Analysis\n\n")
            if trends.get('revenue_trend'):
                report.append(f"- **Revenue Trend:** {trends['revenue_trend']}\n")
                if trends.get('revenue_growth_rate') is not None:
                    report.append(f"  - Growth Rate: {trends['revenue_growth_rate']:.2f}%\n")
            if trends.get('profit_trend'):
                report.append(f"- **Profit Trend:** {trends['profit_trend']}\n")
                if trends.get('profit_growth_rate') is not None:
                    report.append(f"  - Growth Rate: {trends['profit_growth_rate']:.2f}%\n")
            report.append("\n")
        
        # Risk Assessment
        if risks:
            report.append("## Risk Assessment\n\n")
            for risk in risks:
                severity_emoji = "🔴" if risk.get('severity') == 'High' else "🟡"
                report.append(f"### {severity_emoji} {risk.get('type', 'Unknown Risk')}\n\n")
                report.append(f"**Severity:** {risk.get('severity', 'Unknown')}\n\n")
                report.append(f"**Description:** {risk.get('description', 'No description available')}\n\n")
        
        # Peer Benchmarking
        if benchmark:
            report.append("## Peer Benchmarking\n\n")
            report.append(f"**Industry:** {benchmark.get('industry', 'General')}\n\n")
            if benchmark.get('summary'):
                report.append(f"{benchmark['summary']}\n\n")
            if benchmark.get('metrics'):
                report.append("| Metric | Company | Benchmark | Δ |\n")
                report.append("|--------|---------|-----------|---|\n")
                for metric in benchmark['metrics']:
                    name = metric['metric'].replace('_', ' ').title()
                    report.append(
                        f"| {name} | {metric.get('company', 'N/A')} | "
                        f"{metric.get('benchmark', 'N/A')} | "
                        f"{metric.get('difference', '0')} |\n"
                    )
                report.append("\n")
            if benchmark.get('alerts'):
                report.append("**Alerts:**\n")
                for alert in benchmark['alerts']:
                    report.append(f"- {alert}\n")
                report.append("\n")
        
        # Recommendations
        report.append("## Recommendations\n\n")
        if risks:
            high_risks = [r for r in risks if r.get('severity') == 'High']
            if high_risks:
                report.append("### Immediate Actions Required\n\n")
                for risk in high_risks:
                    report.append(f"- Address {risk.get('type', 'identified risk')}: {risk.get('description', '')}\n")
                report.append("\n")
        
        report.append("---\n")
        report.append("*This report was generated automatically by the Financial Statement AI Analyzer.*\n")
        
        content = ''.join(report)
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return content
    
    def generate_text_report(self, analysis_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Generate a plain text format report
        
        Args:
            analysis_data: Complete analysis results
            filename: Optional filename to save the report
            
        Returns:
            Text report content
        """
        financial_data = analysis_data.get('financial_data', {})
        ratios = analysis_data.get('ratios', {})
        risks = analysis_data.get('risks', [])
        trends = analysis_data.get('trends', {})
        insights = analysis_data.get('insights', '')
        
        report = []
        report.append("=" * 60 + "\n")
        report.append("FINANCIAL STATEMENT ANALYSIS REPORT\n")
        report.append("=" * 60 + "\n")
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append("=" * 60 + "\n\n")
        
        # Executive Summary
        report.append("EXECUTIVE SUMMARY\n")
        report.append("-" * 60 + "\n")
        if insights:
            report.append(f"{insights}\n\n")
        
        # Financial Data
        report.append("KEY FINANCIAL METRICS\n")
        report.append("-" * 60 + "\n")
        for key, value in financial_data.items():
            if value is not None:
                if isinstance(value, (int, float)):
                    formatted_value = f"${value:,.2f}" if abs(value) >= 1 else f"${value:.2f}"
                else:
                    formatted_value = str(value)
                report.append(f"{key.replace('_', ' ').title()}: {formatted_value}\n")
        report.append("\n")
        
        # Financial Ratios
        report.append("FINANCIAL RATIOS\n")
        report.append("-" * 60 + "\n")
        for key, value in ratios.items():
            if value is not None:
                unit = '%' if 'ratio' in key.lower() or 'margin' in key.lower() or key.lower() in ['roa', 'roe'] else ''
                report.append(f"{key.replace('_', ' ').title()}: {value:.2f}{unit}\n")
        report.append("\n")
        
        # Risk Assessment
        if risks:
            report.append("RISK ASSESSMENT\n")
            report.append("-" * 60 + "\n")
            for risk in risks:
                report.append(f"[{risk.get('severity', 'Unknown')}] {risk.get('type', 'Unknown Risk')}\n")
                report.append(f"  {risk.get('description', 'No description')}\n\n")
        
        # Trend Analysis
        if trends:
            report.append("TREND ANALYSIS\n")
            report.append("-" * 60 + "\n")
            if trends.get('revenue_trend'):
                report.append(f"Revenue Trend: {trends['revenue_trend']}\n")
            if trends.get('profit_trend'):
                report.append(f"Profit Trend: {trends['profit_trend']}\n")
            report.append("\n")
        
        # Benchmark
        if benchmark:
            report.append("PEER BENCHMARKING\n")
            report.append("-" * 60 + "\n")
            report.append(f"Industry: {benchmark.get('industry', 'General')}\n")
            if benchmark.get('summary'):
                report.append(f"{benchmark['summary']}\n")
            for metric in benchmark.get('metrics', []):
                name = metric['metric'].replace('_', ' ').title()
                report.append(
                    f"{name}: Company={metric.get('company', 'N/A')} "
                    f"Benchmark={metric.get('benchmark', 'N/A')} "
                    f"Δ={metric.get('difference', 0)}\n"
                )
            for alert in benchmark.get('alerts', []):
                report.append(f"  Alert: {alert}\n")
            report.append("\n")
        
        report.append("=" * 60 + "\n")
        report.append("End of Report\n")
        report.append("=" * 60 + "\n")
        
        content = ''.join(report)
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return content

