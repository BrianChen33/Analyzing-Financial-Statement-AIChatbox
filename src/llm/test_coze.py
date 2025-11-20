"""Simple manual smoke test for the Tongyi Qianwen endpoint."""

import os
import requests


BASE_URL = os.getenv("TONGYI_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
API_KEY = os.getenv("TONGYI_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
MODEL = os.getenv("TONGYI_MODEL", "qwen-plus")


def ask(question: str) -> str:
    if not API_KEY:
        raise RuntimeError("Set TONGYI_API_KEY before running this script.")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an English-speaking financial assistant."},
            {"role": "user", "content": question},
        ],
    }
    resp = requests.post(
        f"{BASE_URL.rstrip('/')}/chat/completions",
        json=payload,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    print(ask("Give me a one-sentence overview of your capabilities."))
