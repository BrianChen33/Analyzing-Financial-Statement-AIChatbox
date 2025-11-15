"""
Utilities for extracting structured financial data from spreadsheets, CSV, and XBRL.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional
import math
import re

FINANCIAL_FIELDS = [
    'revenue',
    'sales',
    'gross_profit',
    'operating_income',
    'net_income',
    'total_assets',
    'current_assets',
    'total_liabilities',
    'current_liabilities',
    'equity',
    'cash',
    'cash_equivalents',
    'inventory',
    'accounts_receivable',
    'operating_cash_flow',
    'investing_cash_flow',
    'financing_cash_flow',
    'free_cash_flow',
    'total_debt',
    'interest_expense'
]

KEYWORD_MAP = {
    'revenue': ['revenue', 'sales', 'total revenue', 'net sales'],
    'sales': ['sales', 'net sales'],
    'gross_profit': ['gross profit', 'gross income'],
    'operating_income': ['operating income', 'operating profit', 'ebit'],
    'net_income': ['net income', 'net profit', 'profit after tax'],
    'total_assets': ['total assets', 'assets total'],
    'current_assets': ['current assets', 'total current assets'],
    'total_liabilities': ['total liabilities', 'liabilities total'],
    'current_liabilities': ['current liabilities', 'total current liabilities'],
    'equity': ['total equity', 'shareholders equity', 'stockholders equity'],
    'cash': ['cash and cash equivalents', 'cash'],
    'cash_equivalents': ['cash equivalents'],
    'inventory': ['inventory', 'inventories'],
    'accounts_receivable': ['accounts receivable', 'receivables'],
    'operating_cash_flow': ['cash from operations', 'operating cash flow', 'operating activities'],
    'investing_cash_flow': ['investing activities', 'cash from investing'],
    'financing_cash_flow': ['financing activities', 'cash from financing'],
    'total_debt': ['total debt', 'long term debt', 'short term debt'],
    'interest_expense': ['interest expense', 'interest paid'],
    'free_cash_flow': ['free cash flow']
}

ROW_LABEL_KEYS = {'metric', 'item', 'description', 'account', 'name', 'line', 'category'}


def initialize_financial_data() -> Dict[str, Optional[float]]:
    """
    Return a dictionary with all expected financial fields initialized to None.
    """
    return {field: None for field in FINANCIAL_FIELDS}


def extract_from_structured_data(parsed_doc: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """
    Extract financial metrics from structured Excel/CSV documents produced by the enhanced parser.
    """
    financial_data = initialize_financial_data()
    
    if not parsed_doc:
        return financial_data
    
    rows: List[Dict[str, Any]] = []
    
    if parsed_doc.get('type') == 'excel':
        for sheet in (parsed_doc.get('content') or {}).values():
            rows.extend(sheet.get('data', []))
    elif parsed_doc.get('type') == 'csv':
        rows = parsed_doc.get('data', [])
    else:
        return financial_data
    
    for row in rows:
        if not isinstance(row, dict):
            continue
        
        # First pass: look for direct key matches (column headers)
        for key, value in row.items():
            field = _match_keyword(str(key))
            numeric_value = _to_number(value)
            if field and numeric_value is not None and financial_data.get(field) is None:
                financial_data[field] = numeric_value
        
        # Second pass: look for metric labels in row values (e.g., Metric column)
        for key, value in row.items():
            if value is None:
                continue
            if isinstance(value, str) and _match_keyword(value):
                field = _match_keyword(value)
                if field and financial_data.get(field) is None:
                    numeric_candidates = [
                        _to_number(row.get(other_key))
                        for other_key in row.keys()
                        if other_key != key
                    ]
                    numeric_candidates = [v for v in numeric_candidates if v is not None]
                    if numeric_candidates:
                        financial_data[field] = numeric_candidates[0]
        
        # Third pass: look for dedicated metric columns (e.g., Metric/FY2023 structure)
        label_value = None
        for potential_key in ROW_LABEL_KEYS:
            if potential_key in row:
                label_value = row.get(potential_key)
                break
        
        if isinstance(label_value, str):
            field = _match_keyword(label_value)
            if field and financial_data.get(field) is None:
                numeric_candidates = [
                    _to_number(row.get(other_key))
                    for other_key in row.keys()
                    if other_key not in ROW_LABEL_KEYS
                ]
                numeric_candidates = [v for v in numeric_candidates if v is not None]
                if numeric_candidates:
                    financial_data[field] = numeric_candidates[0]
    
    # Derive free cash flow if not provided but operating/investing cash flows exist
    if financial_data['free_cash_flow'] is None:
        op_cf = financial_data.get('operating_cash_flow')
        inv_cf = financial_data.get('investing_cash_flow')
        if op_cf is not None and inv_cf is not None:
            financial_data['free_cash_flow'] = op_cf + inv_cf
    
    return financial_data


def extract_from_xbrl(parsed_doc: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """
    Extract key financial metrics from XBRL/XML documents.
    """
    financial_data = initialize_financial_data()
    xbrl_data = (parsed_doc or {}).get('data') or {}
    
    if not xbrl_data:
        return financial_data
    
    normalized_data = {str(k).lower(): v for k, v in xbrl_data.items()}
    
    for field, tags in KEYWORD_MAP.items():
        for tag in tags:
            for candidate_key, candidate_value in normalized_data.items():
                normalized_tag = tag.replace(' ', '').lower()
                compact_key = candidate_key.replace(' ', '')
                if normalized_tag == compact_key or normalized_tag in compact_key:
                    numeric_value = _to_number(candidate_value)
                    if numeric_value is not None:
                        financial_data[field] = numeric_value
                        break
            if financial_data.get(field) is not None:
                break
    
    if financial_data['free_cash_flow'] is None:
        op_cf = financial_data.get('operating_cash_flow')
        inv_cf = financial_data.get('investing_cash_flow')
        if op_cf is not None and inv_cf is not None:
            financial_data['free_cash_flow'] = op_cf + inv_cf
    
    return financial_data


def build_cash_flow_summary(financial_data: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """
    Return a normalized cash flow summary to drive visualisations.
    """
    return {
        'operating': financial_data.get('operating_cash_flow'),
        'investing': financial_data.get('investing_cash_flow'),
        'financing': financial_data.get('financing_cash_flow'),
        'free_cash_flow': financial_data.get('free_cash_flow')
    }


def _match_keyword(text: str) -> Optional[str]:
    """
    Attempt to map arbitrary text to one of the known financial fields.
    """
    text_lower = text.strip().lower()
    for field, keywords in KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword in text_lower:
                return field
    return None


def _to_number(value: Any) -> Optional[float]:
    """
    Convert a cell value to a float if possible.
    """
    if value is None:
        return None
    
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return float(value)
    
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            return None
        
        # Handle negative numbers in parentheses: (1,000) -> -1000
        negative = False
        if cleaned.startswith('(') and cleaned.endswith(')'):
            negative = True
            cleaned = cleaned[1:-1]
        
        cleaned = cleaned.replace(',', '')
        cleaned = cleaned.replace('$', '')
        cleaned = cleaned.replace('%', '')
        cleaned = cleaned.replace('USD', '')
        cleaned = cleaned.strip()
        
        # Remove any non-numeric characters except minus sign and decimal point
        cleaned = re.sub(r'[^0-9\.\-]', '', cleaned)
        if not cleaned or cleaned == '-':
            return None
        
        try:
            number = float(cleaned)
            return -number if negative else number
        except ValueError:
            return None
    
    return None

