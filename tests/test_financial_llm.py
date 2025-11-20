import os
from types import SimpleNamespace

import pytest

import src.llm.financial_llm as financial_llm


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    for key in [
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "COZE_API_TOKEN",
        "COZE_BOT_ID",
        "COZE_REGION",
        "COZE_DEFAULT_USER_ID",
    ]:
        monkeypatch.delenv(key, raising=False)


def make_fake_openai(monkeypatch, response_text="ok", raise_error=False):
    holder = {}

    class FakeCompletions:
        def __init__(self):
            self.last_request = None

        def create(self, model, messages, **kwargs):
            self.last_request = {"model": model, "messages": messages, "kwargs": kwargs}
            if raise_error:
                raise RuntimeError("openai unavailable")
            return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=response_text))])

    class FakeOpenAI:
        def __init__(self, api_key):
            self.api_key = api_key
            self.chat = SimpleNamespace(completions=FakeCompletions())
            holder["instance"] = self

    monkeypatch.setattr(financial_llm, "OPENAI_AVAILABLE", True)
    monkeypatch.setattr(financial_llm, "OpenAI", lambda api_key: FakeOpenAI(api_key))
    return holder


def fake_coze_setup(monkeypatch, reply_text="coze reply", token_usage=5):
    class FakeChatEventType:
        CONVERSATION_MESSAGE_DELTA = "delta"
        CONVERSATION_CHAT_COMPLETED = "completed"

    class FakeMessage:
        @staticmethod
        def build_user_question_text(prompt):
            return {"prompt": prompt}

    class FakeChat:
        def stream(self, bot_id, user_id, additional_messages):
            yield SimpleNamespace(
                event=FakeChatEventType.CONVERSATION_MESSAGE_DELTA,
                message=SimpleNamespace(content=reply_text),
            )
            yield SimpleNamespace(
                event=FakeChatEventType.CONVERSATION_CHAT_COMPLETED,
                chat=SimpleNamespace(usage=SimpleNamespace(token_count=token_usage)),
            )

    class FakeCoze:
        def __init__(self, auth=None, base_url=None):
            self.auth = auth
            self.base_url = base_url
            self.chat = FakeChat()

    monkeypatch.setattr(financial_llm, "COZE_AVAILABLE", True)
    monkeypatch.setattr(financial_llm, "ChatEventType", FakeChatEventType)
    monkeypatch.setattr(financial_llm, "Message", FakeMessage)
    monkeypatch.setattr(financial_llm, "Coze", FakeCoze)
    monkeypatch.setattr(financial_llm, "TokenAuth", lambda token: token)
    monkeypatch.setattr(financial_llm, "COZE_CN_BASE_URL", "https://api.fake.cn")
    monkeypatch.setattr(financial_llm, "COZE_COM_BASE_URL", "https://api.fake.com")


def test_generate_financial_insights_openai(monkeypatch):
    holder = make_fake_openai(monkeypatch, response_text="insights")
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    llm = financial_llm.FinancialLLM(provider="openai", use_coze_fallback=False)

    result = llm.generate_financial_insights({"rev": 1}, {"m": 2}, [{"severity": "high", "type": "liquidity", "description": "low"}])
    assert result == "insights"
    assert holder["instance"].chat.completions.last_request is not None


def test_answer_question_updates_history(monkeypatch):
    make_fake_openai(monkeypatch, response_text="answer")
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    llm = financial_llm.FinancialLLM(provider="openai", use_coze_fallback=False)

    out = llm.answer_question("Q?", {"financial_data": {"a": 1}, "ratios": {}, "risks": [], "trends": {}})
    assert out == "answer"
    assert llm.conversation_history[-2:] == [
        {"role": "user", "content": "Q?"},
        {"role": "assistant", "content": "answer"},
    ]


def test_generate_summary(monkeypatch):
    make_fake_openai(monkeypatch, response_text="summary")
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    llm = financial_llm.FinancialLLM(provider="openai", use_coze_fallback=False)

    assert llm.generate_summary("doc text") == "summary"


def test_analyze_document_with_vision(monkeypatch):
    holder = make_fake_openai(monkeypatch, response_text="vision")
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    llm = financial_llm.FinancialLLM(provider="openai", use_coze_fallback=False)

    result = llm.analyze_document_with_vision("base64image")
    assert result == "vision"
    last = holder["instance"].chat.completions.last_request
    assert last["model"] == "gpt-4-vision-preview"
    assert any(msg.get("content") for msg in last["messages"])


def test_coze_provider_stream(monkeypatch):
    fake_coze_setup(monkeypatch, reply_text="hello", token_usage=3)
    llm = financial_llm.FinancialLLM(provider="coze", coze_token="t", coze_bot_id="b", coze_base_url="http://fake")

    result = llm.coze_stream_chat("hi")
    assert "hello" in result
    assert "[Coze token usage: 3]" in result


def test_openai_fallback_to_coze(monkeypatch):
    fake_coze_setup(monkeypatch, reply_text="fallback reply", token_usage=2)
    make_fake_openai(monkeypatch, raise_error=True)
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    monkeypatch.setenv("COZE_API_TOKEN", "ctoken")
    monkeypatch.setenv("COZE_BOT_ID", "cbot")

    llm = financial_llm.FinancialLLM(provider="openai", use_coze_fallback=True)
    result = llm.generate_summary("doc")
    assert "fallback reply" in result
    assert "OpenAI fallback due to" in result
