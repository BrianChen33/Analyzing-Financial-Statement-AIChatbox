"""
Financial analyzer module for calculating key financial indicators,
identifying trends, and assessing risks
"""

from typing import Dict, Any, List, Optional
import re


class FinancialAnalyzer:
    """
    Analyzes financial statements and calculates key financial indicators
    """
    
    def __init__(self):
        self.indicators = []
    
    def extract_financial_data(self, text_data: str) -> Dict[str, Any]:
        """
        Extract financial data from text content using pattern matching
        
        Args:
            text_data: Text content from financial statement
            
        Returns:
            Dictionary with extracted financial data
        """
        financial_data = {
            'revenue': None,
            'sales': None,
            'gross_profit': None,
            'operating_income': None,
            'net_income': None,
            'total_assets': None,
            'current_assets': None,
            'total_liabilities': None,
            'current_liabilities': None,
            'equity': None,
            'cash': None,
            'cash_equivalents': None,
            'inventory': None,
            'accounts_receivable': None,
            'operating_cash_flow': None,
            'investing_cash_flow': None,
            'financing_cash_flow': None,
            'free_cash_flow': None,
            'total_debt': None,
            'interest_expense': None
        }
        
        # 将文本转换为小写以便匹配，但保留原始格式用于提取数字
        lines = text_data.split('\n')
        text_lower = text_data.lower()
        
        # 定义关键词模式，按优先级排序
        patterns = {
            'revenue': [r'revenue', r'total\s+revenue', r'sales\s+revenue', r'net\s+sales'],
            'sales': [r'net\s+sales', r'total\s+sales', r'sales'],
            'gross_profit': [r'gross\s+profit', r'gross\s+income'],
            'operating_income': [r'operating\s+income', r'operating\s+profit', r'ebit'],
            'net_income': [r'net\s+income', r'net\s+profit', r'profit\s+after\s+tax'],
            'total_assets': [r'total\s+assets', r'assets\s+total'],
            'current_assets': [r'current\s+assets', r'total\s+current\s+assets'],
            'total_liabilities': [r'total\s+liabilities', r'liabilities\s+total'],
            'current_liabilities': [r'current\s+liabilities', r'total\s+current\s+liabilities'],
            'equity': [r'total\s+equity', r'shareholders\s+equity', r'stockholders\s+equity', r'equity'],
            'cash': [r'cash\s+and\s+cash\s+equivalents', r'cash'],
            'inventory': [r'inventory', r'inventories'],
            'accounts_receivable': [r'accounts\s+receivable', r'receivables'],
            'operating_cash_flow': [r'operating\s+activities', r'cash\s+from\s+operations', r'operating\s+cash\s+flow'],
            'investing_cash_flow': [r'investing\s+activities', r'cash\s+from\s+investing'],
            'financing_cash_flow': [r'financing\s+activities', r'cash\s+from\s+financing'],
            'total_debt': [r'total\s+debt', r'long\s+term\s+debt', r'short\s+term\s+debt'],
            'interest_expense': [r'interest\s+expense', r'interest\s+paid']
        }
        
        # 遍历每一行，查找匹配的模式
        for line in lines:
            line_lower = line.lower()
            
            for key, pattern_list in patterns.items():
                if financial_data[key] is not None:
                    continue
                    
                for pattern in pattern_list:
                    if re.search(pattern, line_lower):
                        numbers = self._extract_numbers(line)
                        if numbers:
                            # 对于多期数据，通常最后一个或最大的数字是当前期的
                            # 但更常见的是最后一个数字
                            financial_data[key] = numbers[-1] if len(numbers) > 0 else numbers[0]
                            break
        
        # 如果没有找到revenue但找到了sales，使用sales作为revenue
        if financial_data['revenue'] is None and financial_data['sales'] is not None:
            financial_data['revenue'] = financial_data['sales']
        
        # 计算自由现金流（如果有运营现金流和投资现金流）
        if financial_data['operating_cash_flow'] is not None and financial_data['investing_cash_flow'] is not None:
            financial_data['free_cash_flow'] = financial_data['operating_cash_flow'] + financial_data['investing_cash_flow']
        
        return financial_data
    
    def calculate_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate comprehensive financial ratios
        
        Args:
            financial_data: Dictionary with financial metrics
            
        Returns:
            Dictionary with calculated ratios
        """
        ratios = {}
        revenue = financial_data.get('revenue') or financial_data.get('sales')
        net_income = financial_data.get('net_income')
        total_assets = financial_data.get('total_assets')
        total_liabilities = financial_data.get('total_liabilities')
        equity = financial_data.get('equity')
        current_assets = financial_data.get('current_assets')
        current_liabilities = financial_data.get('current_liabilities')
        cash = financial_data.get('cash') or financial_data.get('cash_equivalents')
        inventory = financial_data.get('inventory')
        accounts_receivable = financial_data.get('accounts_receivable')
        operating_cash_flow = financial_data.get('operating_cash_flow')
        total_debt = financial_data.get('total_debt')
        interest_expense = financial_data.get('interest_expense')
        gross_profit = financial_data.get('gross_profit')
        operating_income = financial_data.get('operating_income')
        
        # ========== 盈利能力比率 (Profitability Ratios) ==========
        
        # 净利润率
        if revenue and net_income and revenue > 0:
            ratios['profit_margin'] = (net_income / revenue) * 100
        
        # 毛利率
        if revenue and gross_profit and revenue > 0:
            ratios['gross_margin'] = (gross_profit / revenue) * 100
        
        # 营业利润率
        if revenue and operating_income and revenue > 0:
            ratios['operating_margin'] = (operating_income / revenue) * 100
        
        # 资产回报率 (ROA)
        if net_income and total_assets and total_assets > 0:
            ratios['roa'] = (net_income / total_assets) * 100
        
        # 股东权益回报率 (ROE)
        if net_income and equity and equity > 0:
            ratios['roe'] = (net_income / equity) * 100
        
        # ========== 流动性比率 (Liquidity Ratios) ==========
        
        # 流动比率
        if current_assets and current_liabilities and current_liabilities > 0:
            ratios['current_ratio'] = current_assets / current_liabilities
        
        # 速动比率（假设没有应收账款数据时，用流动资产减去存货）
        if current_assets and current_liabilities and current_liabilities > 0:
            quick_assets = current_assets
            if inventory:
                quick_assets = current_assets - inventory
            elif accounts_receivable:
                quick_assets = current_assets - accounts_receivable
            ratios['quick_ratio'] = quick_assets / current_liabilities
        
        # 现金比率
        if cash and current_liabilities and current_liabilities > 0:
            ratios['cash_ratio'] = cash / current_liabilities
        
        # ========== 杠杆比率 (Leverage Ratios) ==========
        
        # 资产负债率
        if total_assets and total_liabilities and total_assets > 0:
            ratios['debt_to_asset_ratio'] = (total_liabilities / total_assets) * 100
        
        # 权益乘数
        if total_assets and equity and equity > 0:
            ratios['equity_multiplier'] = total_assets / equity
        
        # 债务权益比
        if total_liabilities and equity and equity > 0:
            ratios['debt_to_equity_ratio'] = (total_liabilities / equity) * 100
        
        # 利息保障倍数
        if operating_income and interest_expense and interest_expense > 0:
            ratios['interest_coverage'] = operating_income / interest_expense
        elif net_income and interest_expense and interest_expense > 0:
            # 如果没有营业利润，用净利润+利息费用估算
            ratios['interest_coverage'] = (net_income + interest_expense) / interest_expense
        
        # ========== 效率比率 (Efficiency Ratios) ==========
        
        # 资产周转率
        if revenue and total_assets and total_assets > 0:
            ratios['asset_turnover'] = revenue / total_assets
        
        # 库存周转率（需要COGS，这里用简化计算）
        if inventory and inventory > 0:
            # 假设COGS约为revenue的60-70%，这里用revenue估算
            if revenue:
                estimated_cogs = revenue * 0.65
                ratios['inventory_turnover'] = estimated_cogs / inventory
        
        # ========== 现金流比率 (Cash Flow Ratios) ==========
        
        # 现金流与收入比
        if operating_cash_flow and revenue and revenue > 0:
            ratios['cash_flow_to_revenue'] = (operating_cash_flow / revenue) * 100
        
        # 自由现金流
        if financial_data.get('free_cash_flow') is not None:
            ratios['free_cash_flow_margin'] = financial_data['free_cash_flow']
        
        return ratios
    
    def identify_trends(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify trends from historical financial data
        
        Args:
            historical_data: List of financial data dictionaries from multiple periods
            
        Returns:
            Dictionary with trend analysis including growth rates and period comparisons
        """
        trends = {
            'revenue_trend': None,
            'profit_trend': None,
            'asset_trend': None,
            'revenue_growth_rate': None,
            'profit_growth_rate': None,
            'asset_growth_rate': None,
            'periods': [],
            'revenue_values': [],
            'net_income_values': [],
            'total_assets_values': []
        }
        
        if len(historical_data) < 2:
            trends['message'] = "Insufficient data for trend analysis. Need at least 2 periods."
            return trends
        
        # 提取各期的关键指标
        periods = []
        revenues = []
        profits = []
        assets = []
        
        for i, period_data in enumerate(historical_data):
            period_label = period_data.get('period', f'Period {i+1}')
            periods.append(period_label)
            
            revenue = period_data.get('revenue') or period_data.get('sales')
            net_income = period_data.get('net_income')
            total_assets = period_data.get('total_assets')
            
            revenues.append(revenue if revenue else 0)
            profits.append(net_income if net_income else 0)
            assets.append(total_assets if total_assets else 0)
        
        trends['periods'] = periods
        trends['revenue_values'] = revenues
        trends['net_income_values'] = profits
        trends['total_assets_values'] = assets
        
        # 计算总收入趋势（从第一期到最后一期）
        if len(revenues) >= 2 and revenues[0] > 0:
            total_growth = ((revenues[-1] - revenues[0]) / revenues[0]) * 100
            trends['revenue_trend'] = 'increasing' if total_growth > 0 else 'decreasing'
            trends['revenue_growth_rate'] = round(total_growth, 2)
            
            # 计算年均增长率（CAGR）
            if len(revenues) > 2:
                years = len(revenues) - 1
                cagr = ((revenues[-1] / revenues[0]) ** (1 / years) - 1) * 100
                trends['revenue_cagr'] = round(cagr, 2)
        
        # 计算利润趋势
        if len(profits) >= 2:
            if profits[0] != 0:
                total_growth = ((profits[-1] - profits[0]) / abs(profits[0])) * 100
                trends['profit_trend'] = 'increasing' if total_growth > 0 else 'decreasing'
                trends['profit_growth_rate'] = round(total_growth, 2)
            else:
                # 如果第一期利润为0或负数，只判断趋势
                trends['profit_trend'] = 'increasing' if profits[-1] > profits[0] else 'decreasing'
                trends['profit_growth_rate'] = None
        
        # 计算资产趋势
        if len(assets) >= 2 and assets[0] > 0:
            total_growth = ((assets[-1] - assets[0]) / assets[0]) * 100
            trends['asset_trend'] = 'increasing' if total_growth > 0 else 'decreasing'
            trends['asset_growth_rate'] = round(total_growth, 2)
        
        # 计算最近一期的同比增长（如果有至少两期数据）
        if len(revenues) >= 2:
            if revenues[-2] > 0:
                yoy_revenue = ((revenues[-1] - revenues[-2]) / revenues[-2]) * 100
                trends['revenue_yoy'] = round(yoy_revenue, 2)
            
            if profits[-2] != 0:
                yoy_profit = ((profits[-1] - profits[-2]) / abs(profits[-2])) * 100
                trends['profit_yoy'] = round(yoy_profit, 2)
        
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
        
        # ========== 盈利能力风险 ==========
        profit_margin = ratios.get('profit_margin', 0)
        if profit_margin < 0:
            risks.append({
                'type': 'Loss Risk',
                'severity': 'High',
                'description': 'Company is reporting net losses, indicating serious financial distress'
            })
        elif profit_margin < 3:
            risks.append({
                'type': 'Profitability Risk',
                'severity': 'High',
                'description': f'Profit margin is very low ({profit_margin:.2f}%), indicating poor profitability'
            })
        elif profit_margin < 5:
            risks.append({
                'type': 'Profitability Risk',
                'severity': 'Medium',
                'description': f'Profit margin is below 5% ({profit_margin:.2f}%), indicating low profitability'
            })
        
        net_income_value = financial_data.get('net_income')
        if net_income_value is not None and net_income_value < 0:
            if not any(r.get('type') == 'Loss Risk' for r in risks):
                risks.append({
                    'type': 'Loss Risk',
                    'severity': 'High',
                    'description': 'Net income is negative, indicating the company is operating at a loss'
                })
        
        roa = ratios.get('roa', 0)
        if roa < 0:
            risks.append({
                'type': 'Asset Efficiency Risk',
                'severity': 'High',
                'description': 'Negative return on assets indicates poor asset utilization'
            })
        elif roa < 2:
            risks.append({
                'type': 'Asset Efficiency Risk',
                'severity': 'Medium',
                'description': f'Return on assets is below 2% ({roa:.2f}%), indicating poor asset utilization'
            })
        
        roe = ratios.get('roe', 0)
        if roe < 0:
            risks.append({
                'type': 'Shareholder Value Risk',
                'severity': 'High',
                'description': 'Negative return on equity indicates destruction of shareholder value'
            })
        elif roe < 5:
            risks.append({
                'type': 'Shareholder Value Risk',
                'severity': 'Medium',
                'description': f'Return on equity is below 5% ({roe:.2f}%), indicating low returns for shareholders'
            })
        
        # ========== 流动性风险 ==========
        current_ratio = ratios.get('current_ratio', 0)
        if current_ratio < 1:
            risks.append({
                'type': 'Liquidity Risk',
                'severity': 'High',
                'description': f'Current ratio is below 1 ({current_ratio:.2f}), indicating potential liquidity problems'
            })
        elif current_ratio < 1.5:
            risks.append({
                'type': 'Liquidity Risk',
                'severity': 'Medium',
                'description': f'Current ratio is below 1.5 ({current_ratio:.2f}), indicating tight liquidity'
            })
        
        quick_ratio = ratios.get('quick_ratio', 0)
        if quick_ratio < 0.5:
            risks.append({
                'type': 'Liquidity Risk',
                'severity': 'High',
                'description': f'Quick ratio is very low ({quick_ratio:.2f}), indicating limited ability to meet short-term obligations'
            })
        elif quick_ratio < 1:
            risks.append({
                'type': 'Liquidity Risk',
                'severity': 'Medium',
                'description': f'Quick ratio is below 1 ({quick_ratio:.2f}), indicating limited liquid assets'
            })
        
        # ========== 杠杆风险 ==========
        debt_to_asset = ratios.get('debt_to_asset_ratio', 0)
        if debt_to_asset > 70:
            risks.append({
                'type': 'Leverage Risk',
                'severity': 'High',
                'description': f'Debt-to-asset ratio exceeds 70% ({debt_to_asset:.2f}%), indicating very high leverage'
            })
        elif debt_to_asset > 60:
            risks.append({
                'type': 'Leverage Risk',
                'severity': 'Medium',
                'description': f'Debt-to-asset ratio exceeds 60% ({debt_to_asset:.2f}%), indicating high leverage'
            })
        
        debt_to_equity = ratios.get('debt_to_equity_ratio', 0)
        if debt_to_equity > 200:
            risks.append({
                'type': 'Leverage Risk',
                'severity': 'High',
                'description': f'Debt-to-equity ratio is very high ({debt_to_equity:.2f}%), indicating excessive leverage'
            })
        elif debt_to_equity > 100:
            risks.append({
                'type': 'Leverage Risk',
                'severity': 'Medium',
                'description': f'Debt-to-equity ratio is high ({debt_to_equity:.2f}%), indicating significant leverage'
            })
        
        interest_coverage = ratios.get('interest_coverage', None)
        if interest_coverage is not None:
            if interest_coverage < 1:
                risks.append({
                    'type': 'Solvency Risk',
                    'severity': 'High',
                    'description': f'Interest coverage ratio is below 1 ({interest_coverage:.2f}), indicating inability to cover interest payments'
                })
            elif interest_coverage < 2:
                risks.append({
                    'type': 'Solvency Risk',
                    'severity': 'Medium',
                    'description': f'Interest coverage ratio is low ({interest_coverage:.2f}), indicating limited ability to service debt'
                })
        
        # ========== 现金流风险 ==========
        operating_cash_flow = financial_data.get('operating_cash_flow')
        if operating_cash_flow is not None and operating_cash_flow < 0:
            risks.append({
                'type': 'Cash Flow Risk',
                'severity': 'High',
                'description': 'Negative operating cash flow indicates the company is not generating cash from operations'
            })
        
        free_cash_flow = financial_data.get('free_cash_flow')
        if free_cash_flow is not None and free_cash_flow < 0:
            risks.append({
                'type': 'Cash Flow Risk',
                'severity': 'Medium',
                'description': 'Negative free cash flow indicates the company may need external financing'
            })
        
        return risks
    
    def calculate_dupont_analysis(self, financial_data: Dict[str, Any], ratios: Dict[str, float]) -> Dict[str, Any]:
        """
        Perform DuPont analysis (three-factor ROE decomposition)
        
        ROE = Profit Margin × Asset Turnover × Equity Multiplier
        
        Args:
            financial_data: Financial metrics
            ratios: Calculated financial ratios
            
        Returns:
            Dictionary with DuPont analysis components
        """
        dupont = {
            'roe': ratios.get('roe'),
            'profit_margin': ratios.get('profit_margin'),
            'asset_turnover': ratios.get('asset_turnover'),
            'equity_multiplier': ratios.get('equity_multiplier'),
            'components': {}
        }
        
        # 计算各组成部分
        if dupont['roe'] is not None:
            if dupont['profit_margin'] and dupont['asset_turnover'] and dupont['equity_multiplier']:
                # 验证：ROE应该等于三个因子的乘积（考虑单位转换）
                calculated_roe = (dupont['profit_margin'] / 100) * dupont['asset_turnover'] * dupont['equity_multiplier'] * 100
                dupont['calculated_roe'] = round(calculated_roe, 2)
                
                # 计算各因子对ROE的贡献
                if calculated_roe != 0:
                    dupont['components'] = {
                        'profit_margin_contribution': round((dupont['profit_margin'] / 100) * dupont['asset_turnover'] * dupont['equity_multiplier'] * 100, 2),
                        'asset_turnover_contribution': round((dupont['profit_margin'] / 100) * dupont['asset_turnover'] * dupont['equity_multiplier'] * 100, 2),
                        'equity_multiplier_contribution': round((dupont['profit_margin'] / 100) * dupont['asset_turnover'] * dupont['equity_multiplier'] * 100, 2)
                    }
        
        return dupont
    
    def _extract_numbers(self, text: str) -> List[float]:
        """Extract numeric values from text"""
        import re
        # Find numbers with optional commas and decimals
        numbers = re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', text)
        return [float(n.replace(',', '')) for n in numbers]
