"""
Peer benchmarking utilities for comparing company metrics to industry standards.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

DEFAULT_BENCHMARKS: Dict[str, Dict[str, Dict[str, float]]] = {
    'general': {
        'ratios': {
            'profit_margin': 8.0,
            'roa': 5.0,
            'roe': 12.0,
            'current_ratio': 1.5,
            'quick_ratio': 1.0,
            'debt_to_asset_ratio': 55.0,
            'debt_to_equity_ratio': 110.0,
        }
    },
    'technology': {
        'ratios': {
            'profit_margin': 12.0,
            'roa': 8.0,
            'roe': 15.0,
            'current_ratio': 1.8,
            'quick_ratio': 1.4,
            'debt_to_asset_ratio': 45.0,
            'debt_to_equity_ratio': 90.0,
        }
    },
    'retail': {
        'ratios': {
            'profit_margin': 6.0,
            'roa': 4.0,
            'roe': 10.0,
            'current_ratio': 1.3,
            'quick_ratio': 0.8,
            'debt_to_asset_ratio': 65.0,
            'debt_to_equity_ratio': 150.0,
        }
    },
    'manufacturing': {
        'ratios': {
            'profit_margin': 9.0,
            'roa': 6.0,
            'roe': 13.0,
            'current_ratio': 1.6,
            'quick_ratio': 1.1,
            'debt_to_asset_ratio': 60.0,
            'debt_to_equity_ratio': 130.0,
        }
    }
}


class PeerBenchmark:
    """
    Compare company performance metrics with industry benchmarks.
    """
    
    def __init__(self, benchmarks: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None):
        self.benchmarks = benchmarks or DEFAULT_BENCHMARKS
    
    def compare(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, float],
        industry: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Compare provided ratios to industry averages and return structured insights.
        """
        if not ratios:
            return None
        
        normalized_industry = (industry or 'general').strip().lower()
        if normalized_industry not in self.benchmarks:
            normalized_industry = 'general'
        
        benchmark = self.benchmarks[normalized_industry]
        benchmark_ratios = benchmark.get('ratios', {})
        
        comparisons: List[Dict[str, Any]] = []
        alerts: List[str] = []
        
        for metric, benchmark_value in benchmark_ratios.items():
            company_value = ratios.get(metric)
            if company_value is None:
                continue
            
            difference = company_value - benchmark_value
            comparisons.append({
                'metric': metric,
                'company': round(company_value, 2),
                'benchmark': benchmark_value,
                'difference': round(difference, 2)
            })
            
            if metric in {'profit_margin', 'roa', 'roe'}:
                if difference <= -5:
                    alerts.append(f"{metric.replace('_', ' ').title()} is {abs(round(difference, 2))}% below peers.")
            elif metric in {'current_ratio', 'quick_ratio'}:
                if difference <= -0.3:
                    alerts.append(f"{metric.replace('_', ' ').title()} is materially weaker than peers.")
            elif metric in {'debt_to_asset_ratio', 'debt_to_equity_ratio'}:
                if difference >= 10:
                    alerts.append(f"{metric.replace('_', ' ').title()} exceeds peer leverage by {round(difference, 2)}%.")
        
        if not comparisons:
            return None
        
        summary = self._build_summary(comparisons)
        
        return {
            'industry': normalized_industry.title(),
            'metrics': comparisons,
            'alerts': alerts,
            'summary': summary
        }
    
    def _build_summary(self, comparisons: List[Dict[str, Any]]) -> str:
        """
        Build a natural language summary of benchmarking results.
        """
        if not comparisons:
            return ""
        
        better = [c for c in comparisons if c['difference'] > 0]
        weaker = [c for c in comparisons if c['difference'] < 0]
        
        summary_parts: List[str] = []
        if better:
            top_metric = max(better, key=lambda x: x['difference'])
            summary_parts.append(
                f"Outperforms peers on {top_metric['metric'].replace('_', ' ')} by {abs(top_metric['difference']):.2f}."
            )
        if weaker:
            lag_metric = min(weaker, key=lambda x: x['difference'])
            summary_parts.append(
                f"Lags industry on {lag_metric['metric'].replace('_', ' ')} by {abs(lag_metric['difference']):.2f}."
            )
        
        if not summary_parts:
            return "Company performance is broadly in line with peer benchmarks."
        
        return " ".join(summary_parts)

