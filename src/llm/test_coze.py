# 保存为 test_coze.py 后运行：python test_coze.py
import os
from cozepy import (
    Coze,
    TokenAuth,
    COZE_CN_BASE_URL,
    COZE_COM_BASE_URL,
    ChatEventType,
    Message,
)

token = os.getenv("COZE_API_TOKEN")
bot_id = os.getenv("COZE_BOT_ID")
if not token or not bot_id:
    raise RuntimeError("请先设置 COZE_API_TOKEN 和 COZE_BOT_ID 环境变量")

region = os.getenv("COZE_REGION", "cn").lower()
base_url = COZE_CN_BASE_URL if region == "cn" else COZE_COM_BASE_URL
user_id = os.getenv("COZE_DEFAULT_USER_ID", "111")

client = Coze(auth=TokenAuth(token=token), base_url=base_url)

def ask(question: str) -> str:
    chunks = []
    token_usage = None
    for event in client.chat.stream(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=[Message.build_user_question_text(question)],
    ):
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            if event.message and event.message.content:
                chunks.append(event.message.content)
        elif event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
            token_usage = getattr(event.chat.usage, "token_count", None)
    result = "".join(chunks)
    if token_usage is not None:
        result += f"\n\n[Coze token usage: {token_usage}]"
    return result

if __name__ == "__main__":
    print(ask("你好，用一句话介绍你自己"))
