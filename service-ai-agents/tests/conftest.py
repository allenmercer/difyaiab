import os
import pytest
from fastapi import WebSocketDisconnect

# Set required environment variables immediately upon import
os.environ["LLM_API_KEY"] = "dummy_api_key"
os.environ["LLM_URL"] = "https://dummy.endpoint"
os.environ["LLM_MODEL"] = "dummy_model"
os.environ["LLM_API_VERSION"] = "2024-1-1"
os.environ["DIFY_BACKEND"] = "https://dummydify.endpoint"


# Common FakeWebSocket for testing process_message (simpler version)
class FakeWebSocket:
    def __init__(self):
        self.sent_text = ""

    async def send_text(self, text: str):
        self.sent_text += text


@pytest.fixture
def fake_websocket():
    """Fixture returning a simple FakeWebSocket."""
    return FakeWebSocket()


# Common FakeChatWebSocket for testing chat endpoints
class FakeChatWebSocket:
    def __init__(self):
        self.sent_texts = []
        self.incoming_texts = []
        self.accepted = False
        self.query_params = {}
        self._index = 0

    async def accept(self):
        self.accepted = True

    async def receive_text(self):
        if self._index >= len(self.incoming_texts):
            raise WebSocketDisconnect("No more incoming messages.")

        msg = self.incoming_texts[self._index]
        self._index += 1

        if msg == "__close__":
            raise WebSocketDisconnect("Manual close signal.")

        return msg

    async def send_text(self, text: str):
        self.sent_texts.append(text)


@pytest.fixture
def fake_chat_websocket():
    """Fixture returning a FakeChatWebSocket."""
    return FakeChatWebSocket()
