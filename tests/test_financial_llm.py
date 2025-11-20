import pytest

import src.llm.financial_llm as financial_llm


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    for key in [
        "TONGYI_API_KEY",
        "TONGYI_BASE_URL",
        "TONGYI_MODEL",
        "DASHSCOPE_API_KEY",
    ]:
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def fake_tongyi(monkeypatch):
    state = {
        "response_text": "ok",
        "calls": [],
    }

    class FakeClient:
        def __init__(self, api_key, base_url=None, model=None):
            self.api_key = api_key
            self.base_url = base_url
            self.model = model

        def create_chat_completion(self, **kwargs):
            state["calls"].append(kwargs)
            return {"choices": [{"message": {"content": state["response_text"]}}]}

    monkeypatch.setattr(financial_llm, "TongyiClient", FakeClient)
    return state


def test_generate_financial_insights(monkeypatch, fake_tongyi):
    fake_tongyi["response_text"] = "insights"
    monkeypatch.setenv("TONGYI_API_KEY", "key")
    llm = financial_llm.FinancialLLM()

    result = llm.generate_financial_insights(
        {"revenue": 1_000_000},
        {"profit_margin": 12},
        [{"severity": "High", "type": "Liquidity", "description": "cash"}],
    )

    assert result == "insights"
    assert fake_tongyi["calls"]


def test_answer_question_maintains_history(monkeypatch, fake_tongyi):
    fake_tongyi["response_text"] = "answer"
    monkeypatch.setenv("TONGYI_API_KEY", "key")
    llm = financial_llm.FinancialLLM()

    context = {"financial_data": {"revenue": 10}, "ratios": {}, "risks": [], "trends": {}}
    out = llm.answer_question("Q?", context, user_id="user-1")

    assert out == "answer"
    history = llm._get_history("user-1")
    assert history[-2:] == [
        {"role": "user", "content": "Q?"},
        {"role": "assistant", "content": "answer"},
    ]


def test_generate_summary(monkeypatch, fake_tongyi):
    fake_tongyi["response_text"] = "summary"
    monkeypatch.setenv("TONGYI_API_KEY", "key")
    llm = financial_llm.FinancialLLM()

    assert llm.generate_summary("doc text") == "summary"


def test_extract_structured_data(monkeypatch, fake_tongyi):
    fake_tongyi["response_text"] = '{"revenue": 100, "net_income": 50}'
    monkeypatch.setenv("TONGYI_API_KEY", "key")
    llm = financial_llm.FinancialLLM()

    data = llm.extract_structured_data("Revenue was 100 and profit 50", period_hint="FY23")
    assert data["metrics"]["revenue"] == 100
    assert data["metrics"]["net_income"] == 50
    assert data["metadata"] == {}


def test_analyze_document_with_vision_not_supported(monkeypatch, fake_tongyi):
    monkeypatch.setenv("TONGYI_API_KEY", "key")
    llm = financial_llm.FinancialLLM()

    with pytest.raises(NotImplementedError):
        llm.analyze_document_with_vision("base64")
