"""
LLM integration module for conversational AI and financial analysis powered by
Alibaba Cloud's Tongyi Qianwen models.
"""

from __future__ import annotations

import json
import os
from typing import Dict, Any, List, Optional
import textwrap

import requests

from src.utils.data_extraction import FINANCIAL_FIELDS

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass


DEFAULT_TONGYI_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
DEFAULT_TONGYI_MODEL = "qwen-plus"


class TongyiClient:
    """Lightweight client for the Tongyi Qianwen OpenAI-compatible API surface."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 60,
    ) -> None:
        if not api_key:
            raise ValueError(
                "Tongyi API key is missing. Set TONGYI_API_KEY (or DASHSCOPE_API_KEY) in your environment."
            )

        self.api_key = api_key
        self.base_url = (base_url or DEFAULT_TONGYI_BASE_URL).rstrip("/")
        self.model = model or DEFAULT_TONGYI_MODEL
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        )

    def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.4,
        max_tokens: int = 800,
        response_format: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format:
            payload["response_format"] = response_format

        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            timeout=self.timeout,
        )
        if response.status_code >= 400:
            raise RuntimeError(
                f"Tongyi request failed ({response.status_code}): {response.text.strip()}"
            )
        return response.json()


class FinancialLLM:
    """Handles Tongyi interactions for financial statement analysis and Q&A."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("TONGYI_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url or os.getenv("TONGYI_BASE_URL", DEFAULT_TONGYI_BASE_URL)
        self.model = model or os.getenv("TONGYI_MODEL", DEFAULT_TONGYI_MODEL)

        self.client = TongyiClient(
            api_key=self.api_key,
            base_url=self.base_url,
            model=self.model,
        )

        self.conversation_histories: Dict[str, List[Dict[str, str]]] = {}
        self.default_user_id = "default"

    def analyze_document_with_vision(self, image_base64: str, prompt: Optional[str] = None) -> str:
        """Placeholder for future Tongyi vision support."""

        raise NotImplementedError(
            "Vision analysis is not yet supported for the Tongyi integration."
        )

    def generate_financial_insights(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, float],
        risks: List[Dict[str, str]],
    ) -> str:
        """Generate comprehensive insights from financial analysis."""

        prompt = (
            f"As a financial analyst, provide comprehensive insights based on this financial data:\n\n"
            f"Financial Metrics:\n{self._format_dict(financial_data)}\n\n"
            f"Financial Ratios:\n{self._format_dict(ratios)}\n\n"
            f"Identified Risks:\n{self._format_risks(risks)}\n\n"
            "Please provide:\n1. Overall financial health assessment\n2. Key strengths and weaknesses\n"
            "3. Trends and patterns\n4. Recommendations for stakeholders\n5. Areas requiring attention\n\n"
            "Be specific, actionable, and professional."
        )

        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": prompt},
        ]

        return self._complete(messages, temperature=0.35, max_tokens=900)

    def answer_question(
        self,
        question: str,
        context: Dict[str, Any],
        user_id: Optional[str] = None,
    ) -> str:
        """Answer user questions about the financial statement."""

        context_str = (
            f"Financial Data Available:\n{self._format_dict(context.get('financial_data', {}))}\n\n"
            f"Financial Ratios:\n{self._format_dict(context.get('ratios', {}))}\n\n"
            f"Risks:\n{self._format_risks(context.get('risks', []))}\n\n"
            f"Trends:\n{self._format_dict(context.get('trends', {}))}\n"
        )

        active_user_id = user_id or self.default_user_id
        messages = [
            {
                "role": "system",
                "content": self._build_system_prompt(
                    "Always leverage the supplied financial context and keep your answer concise."
                ),
            },
            {
                "role": "user",
                "content": f"Financial context for this user:\n{context_str}\nAcknowledge the context before answering follow-up questions.",
            },
        ]
        messages.extend(self._get_history(active_user_id))
        messages.append({"role": "user", "content": question})

        answer = self._complete(messages, temperature=0.3, max_tokens=650)
        self._update_history(active_user_id, "user", question)
        self._update_history(active_user_id, "assistant", answer)
        return answer

    def generate_summary(self, document_text: str) -> str:
        """Generate a concise summary of the financial statement."""

        prompt = (
            "Summarize the following financial statement, highlighting:\n"
            "1. Key financial figures\n2. Most important insights\n3. Notable changes or trends\n\n"
            f"Document:\n{document_text[:3000]}\n\nProvide a concise, structured summary."
        )

        messages = [
            {
                "role": "system",
                "content": self._build_system_prompt(
                    "Summaries should highlight performance, risk, and forward-looking signals in English."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        return self._complete(messages, temperature=0.4, max_tokens=520)

    def extract_structured_data(
        self,
        document_text: str,
        *,
        period_hint: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Ask Tongyi to convert raw financial text into structured metrics."""

        if not document_text.strip():
            return {}

        schema_example = json.dumps(
            {
                "metadata": {
                    "entity": "ACME Corp",
                    "period_label": "FY2023",
                    "fiscal_year": "2023",
                    "currency": "USD",
                },
                "metrics": {
                    "revenue": 1250000000.0,
                    "sales": 1250000000.0,
                    "gross_profit": 520000000.0,
                    "operating_income": 210000000.0,
                    "net_income": 155000000.0,
                    "total_assets": 1800000000.0,
                    "current_assets": 620000000.0,
                    "total_liabilities": 950000000.0,
                    "current_liabilities": 420000000.0,
                    "equity": 850000000.0,
                    "cash": 120000000.0,
                    "operating_cash_flow": 240000000.0,
                    "investing_cash_flow": -80000000.0,
                    "financing_cash_flow": -60000000.0,
                    "free_cash_flow": 160000000.0,
                    "total_debt": 400000000.0,
                    "interest_expense": 12000000.0,
                },
                "notes": [
                    "Gross margin improved to 41% year over year.",
                    "Net debt declined by 5% due to debt repayment.",
                ],
            },
            indent=2,
        )

        schema_partial_example = json.dumps(
            {
                "metadata": {
                    "entity": "Beta Manufacturing",
                    "period_label": "Q2 2023",
                    "fiscal_year": "2023",
                    "currency": "USD",
                },
                "metrics": {
                    "revenue": 42000000.0,
                    "net_income": 3200000.0,
                    "total_assets": None,
                    "equity": None,
                    "operating_cash_flow": 5800000.0,
                    "investing_cash_flow": -1200000.0,
                    "free_cash_flow": 4600000.0,
                },
                "notes": [
                    "Management guidance points to stable demand for the remainder of FY2023."
                ],
            },
            indent=2,
        )

        excerpt = document_text[:6000]
        system_prompt = textwrap.dedent(
            f"""
            You are a forensic accountant extracting structured metrics from corporate filings. Always respond with
            JSON that matches this schema (omit fields by setting them to null, never invent new keys):
            {schema_example}

            Partial responses are allowed when a figure is missing. Example:
            {schema_partial_example}

            Rules:
            1. Return numbers as floats in USD with no units or thousands separators.
            2. If a value is unknown, set it to null instead of guessing.
            3. Use the notes array for any qualitative insights (max 3 short strings).
            4. Keep output strictly in JSON—no commentary before or after the object.
            """
        ).strip()

        user_prompt = textwrap.dedent(
            f"""
            Document excerpt:
            {excerpt}

            Period hint: {period_hint or 'unknown'}
            Extract the metrics above and output JSON that follows the schema exactly.
            """
        ).strip()

        raw = self._complete(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=900,
            response_format={"type": "json_object"},
        )
        payload = self._safe_json_loads(raw)
        return self._normalize_structured_payload(payload)

    def reset_conversation(self, user_id: Optional[str] = None) -> None:
        """Clear conversation history for a user or entirely."""

        if user_id:
            self.conversation_histories.pop(user_id, None)
        else:
            self.conversation_histories.clear()

    def _format_dict(self, data: Dict) -> str:
        """Format dictionary for display."""
        if not data:
            return "  - None"
        return "\n".join([f"  - {k}: {v}" for k, v in data.items()])

    def _format_risks(self, risks: List[Dict[str, str]]) -> str:
        """Format risks list for display."""
        if not risks:
            return "  - No significant risks identified"
        return "\n".join([f"  - [{r.get('severity','N/A')}] {r.get('type','')}: {r.get('description','')}" for r in risks])

    def _build_system_prompt(self, extra: Optional[str] = None) -> str:
        base = (
            "You are a senior financial analyst who must always respond in English. "
            "Provide structured, factual, and concise answers grounded in corporate financial statements."
        )
        if extra:
            base = f"{base} {extra.strip()}"
        return base

    def _complete(
        self,
        messages: List[Dict[str, Any]],
        temperature: float = 0.4,
        max_tokens: int = 800,
        response_format: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
    ) -> str:
        response = self.client.create_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format,
            model=model,
        )
        try:
            return response["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            raise RuntimeError("Tongyi response did not include completion text.")

    def _get_history(self, user_id: str) -> List[Dict[str, str]]:
        history = self.conversation_histories.get(user_id, [])
        return history[-10:]

    def _update_history(self, user_id: str, role: str, content: str) -> None:
        history = self.conversation_histories.setdefault(user_id, [])
        history.append({"role": role, "content": content})
        if len(history) > 20:
            self.conversation_histories[user_id] = history[-20:]

    def _safe_json_loads(self, payload: str) -> Dict[str, Any]:
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            trimmed = payload.strip()
            start = trimmed.find("{")
            end = trimmed.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(trimmed[start : end + 1])
                except json.JSONDecodeError:
                    return {}
            return {}

    def _normalize_structured_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not payload:
            return {}

        metrics = payload.get("metrics") or {}
        if not metrics:
            metrics = {
                field: payload.get(field)
                for field in FINANCIAL_FIELDS
                if payload.get(field) is not None
            }

        payload["metrics"] = metrics
        payload.setdefault("metadata", {})
        payload.setdefault("notes", [])
        return payload

