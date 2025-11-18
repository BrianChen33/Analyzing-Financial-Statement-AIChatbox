"""
LLM integration module for conversational AI and financial analysis

This module provides a FinancialLLM wrapper that can use either OpenAI
or Coze as a backend. It avoids hard-coded secrets and handles optional
dependencies gracefully.
"""

import os
from typing import Dict, Any, List, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

try:
    from cozepy import (
        COZE_CN_BASE_URL,
        COZE_COM_BASE_URL,
        ChatEventType,
        Coze,
        Message,
        TokenAuth,
    )

    COZE_AVAILABLE = True
except Exception:
    COZE_AVAILABLE = False
    COZE_CN_BASE_URL = None  # type: ignore
    COZE_COM_BASE_URL = None  # type: ignore
    ChatEventType = None  # type: ignore
    Coze = None  # type: ignore
    Message = None  # type: ignore
    TokenAuth = None  # type: ignore

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass


class FinancialLLM:
    """Handles LLM interactions for financial statement analysis and Q&A."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "openai",
        coze_token: Optional[str] = None,
        coze_bot_id: Optional[str] = None,
        coze_base_url: Optional[str] = None,
        coze_default_user_id: str = "111",
    ):
        """Initialize the LLM client.

        Args:
            api_key: OpenAI API key (if not provided, reads from environment).
            provider: Which backend to use ("openai" or "coze").
            coze_token: Coze access token (uses COZE_API_TOKEN env var if not provided).
            coze_bot_id: Coze bot id (uses COZE_BOT_ID env var if not provided).
            coze_base_url: Override Coze API endpoint.
            coze_default_user_id: Default user id when talking to Coze bot.
        """

        self.provider = provider.lower()
        self.conversation_history: List[Dict[str, str]] = []

        if self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ValueError(
                    "OpenAI library not installed. Install with: pip install openai"
                )

            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
                )

            self.client = OpenAI(api_key=self.api_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4")

        elif self.provider == "coze":
            if not COZE_AVAILABLE:
                raise ValueError(
                    "Coze library not installed. Install with: pip install cozepy"
                )

            # Do NOT hard-code secrets here; prefer environment variables.
            self.coze_token = coze_token or os.getenv("COZE_API_TOKEN")
            if not self.coze_token:
                raise ValueError(
                    "Coze access token not found. Set COZE_API_TOKEN environment variable."
                )

            self.coze_bot_id = coze_bot_id or os.getenv("COZE_BOT_ID")
            if not self.coze_bot_id:
                raise ValueError("Coze bot id not configured. Set COZE_BOT_ID.")

            base_from_region = (
                COZE_CN_BASE_URL if os.getenv("COZE_REGION", "cn").lower() == "cn" else COZE_COM_BASE_URL
            )
            self.coze_base_url = coze_base_url or base_from_region
            self.coze_default_user_id = coze_default_user_id or os.getenv(
                "COZE_DEFAULT_USER_ID", "111"
            )

            self.coze_client = Coze(auth=TokenAuth(token=self.coze_token), base_url=self.coze_base_url)

        else:
            raise ValueError("Unsupported provider. Use 'openai' or 'coze'.")

    def analyze_document_with_vision(self, image_base64: str, prompt: str = None) -> str:
        """Analyze financial statement image using GPT-4 Vision.

        Note: Vision analysis is currently supported only when using the OpenAI provider.
        """

        if self.provider != "openai":
            raise ValueError("Vision analysis is only supported with the OpenAI provider.")

        if not prompt:
            prompt = (
                "Analyze this financial statement image and extract:\n"
                "1. Key financial metrics (revenue, net income, assets, liabilities, equity)\n"
                "2. Important line items and their values\n"
                "3. Any notable observations or irregularities\n\n"
                "Provide the information in a structured format."
            )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                            },
                        ],
                    }
                ],
                max_tokens=1500,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error analyzing image: {str(e)}"

    def generate_financial_insights(
        self,
        financial_data: Dict[str, Any],
        ratios: Dict[str, float],
        risks: List[Dict[str, str]],
    ) -> str:
        """Generate comprehensive insights from financial analysis."""

        if self.provider != "openai":
            raise ValueError("Insight generation is only supported with the OpenAI provider.")

        prompt = (
            f"As a financial analyst, provide comprehensive insights based on this financial data:\n\n"
            f"Financial Metrics:\n{self._format_dict(financial_data)}\n\n"
            f"Financial Ratios:\n{self._format_dict(ratios)}\n\n"
            f"Identified Risks:\n{self._format_risks(risks)}\n\n"
            "Please provide:\n1. Overall financial health assessment\n2. Key strengths and weaknesses\n"
            "3. Trends and patterns\n4. Recommendations for stakeholders\n5. Areas requiring attention\n\n"
            "Be specific, actionable, and professional."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst with deep knowledge of financial statements, ratios, and risk assessment."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating insights: {str(e)}"

    def answer_question(self, question: str, context: Dict[str, Any]) -> str:
        """Answer user questions about the financial statement."""

        if self.provider != "openai":
            raise ValueError("Q&A is only supported with the OpenAI provider.")

        context_str = (
            f"Financial Data Available:\n{self._format_dict(context.get('financial_data', {}))}\n\n"
            f"Financial Ratios:\n{self._format_dict(context.get('ratios', {}))}\n\n"
            f"Risks:\n{self._format_risks(context.get('risks', []))}\n\n"
            f"Trends:\n{self._format_dict(context.get('trends', {}))}\n"
        )

        messages = [
            {"role": "system", "content": f"You are a helpful financial analyst assistant. Use this context to answer questions:\n\n{context_str}"}
        ]
        messages.extend(self.conversation_history[-5:])
        messages.append({"role": "user", "content": question})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=600,
            )
            answer = response.choices[0].message.content
            self._update_history("user", question)
            self._update_history("assistant", answer)
            return answer
        except Exception as e:
            return f"Error answering question: {str(e)}"

    def generate_summary(self, document_text: str) -> str:
        """Generate a concise summary of the financial statement."""

        if self.provider != "openai":
            raise ValueError("Summaries are only supported with the OpenAI provider.")

        prompt = (
            "Summarize the following financial statement, highlighting:\n"
            "1. Key financial figures\n2. Most important insights\n3. Notable changes or trends\n\n"
            f"Document:\n{document_text[:3000]}\n\nProvide a concise, structured summary."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert at summarizing financial statements."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=500,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []

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

    def _update_history(self, role: str, content: str) -> None:
        """Maintain a bounded conversation history."""
        self.conversation_history.append({"role": role, "content": content})
        # Keep only the last 20 messages
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

    def coze_stream_chat(self, prompt: str, user_id: Optional[str] = None) -> str:
        """Stream a chat completion from a Coze bot.

        This method aggregates streaming events into a single response string.
        """

        if self.provider != "coze":
            raise ValueError("coze_stream_chat is only available when provider='coze'.")

        active_user_id = user_id or self.coze_default_user_id
        response_chunks: List[str] = []
        token_usage: Optional[int] = None

        for event in self.coze_client.chat.stream(
            bot_id=self.coze_bot_id,
            user_id=active_user_id,
            additional_messages=[Message.build_user_question_text(prompt)],
        ):
            if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                if event.message and event.message.content:
                    response_chunks.append(event.message.content)
            if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                token_usage = getattr(event.chat.usage, "token_count", None)

        aggregated_response = "".join(response_chunks)
        if token_usage is not None:
            aggregated_response += f"\n\n[Coze token usage: {token_usage}]"

        return aggregated_response

