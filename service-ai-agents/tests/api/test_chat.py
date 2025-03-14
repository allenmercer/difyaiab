import pytest
from unittest.mock import patch, AsyncMock
import yaml
from app.api.v1.endpoints.chat import chat_with_llm


@pytest.mark.asyncio
async def test_default_behavior(monkeypatch, fake_chat_websocket):
    """
    Test the standard workflow generation functionality.
    """
    # Setup
    fake_chat_websocket.incoming_texts = [
        "Create a workflow that uses LLM",
        "__close__",
    ]

    # Mock workflow_factory methods
    async def fake_classify_workflow(data):
        return "llm" if "LLM" in data else "other"

    async def fake_create_workflow(data):
        return {"nodes": [], "edges": []}

    async def fake_generate_name(data):
        return "Test App Name"

    async def fake_generate_description(data):
        return "Test app description"

    # Apply mocks
    monkeypatch.setattr(
        "app.api.v1.endpoints.chat.workflow_factory.classify_workflow",
        fake_classify_workflow,
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.chat.workflow_factory.create_complex_workflow",
        fake_create_workflow,
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.chat.workflow_factory.generate_app_name",
        fake_generate_name,
    )
    monkeypatch.setattr(
        "app.api.v1.endpoints.chat.workflow_factory.generate_app_description",
        fake_generate_description,
    )

    # Mock yaml.dump to return predictable output
    def fake_yaml_dump(data, sort_keys=None, Dumper=None):
        return f"YAML: {data['app']['name']}"

    monkeypatch.setattr("app.api.v1.endpoints.chat.yaml.dump", fake_yaml_dump)

    # Execute
    await chat_with_llm(fake_chat_websocket)

    # Verify
    assert fake_chat_websocket.accepted is True
    assert len(fake_chat_websocket.sent_texts) == 1
    assert "YAML: Test App Name" in fake_chat_websocket.sent_texts[0]


@pytest.mark.asyncio
async def test_generate_default_dsl(monkeypatch, fake_chat_websocket):
    """
    Test sending 'generate default dsl' command.
    """
    # Setup
    fake_chat_websocket.incoming_texts = ["generate default dsl", "__close__"]

    # Mock Resource.DSL_DEFAULT
    monkeypatch.setattr(
        "app.api.v1.endpoints.chat.Resource.DSL_DEFAULT", "DEFAULT DSL CONTENT"
    )

    # Execute
    await chat_with_llm(fake_chat_websocket)

    # Verify
    assert fake_chat_websocket.accepted is True
    assert fake_chat_websocket.sent_texts == ["DEFAULT DSL CONTENT"]


@pytest.mark.asyncio
async def test_unsupported_workflow(monkeypatch, fake_chat_websocket):
    """
    Test handling of workflow types classified as 'other'.
    """
    # Setup
    fake_chat_websocket.incoming_texts = [
        "Give me an unsupported workflow",
        "__close__",
    ]

    # Mock workflow_factory.classify_workflow to return "other"
    async def fake_classify_workflow(data):
        return "other workflow type"

    monkeypatch.setattr(
        "app.api.v1.endpoints.chat.workflow_factory.classify_workflow",
        fake_classify_workflow,
    )

    # Execute
    await chat_with_llm(fake_chat_websocket)

    # Verify
    assert fake_chat_websocket.accepted is True
    assert len(fake_chat_websocket.sent_texts) == 1
    assert "not yet supported" in fake_chat_websocket.sent_texts[0]


@pytest.mark.asyncio
async def test_error_handling(monkeypatch, fake_chat_websocket):
    """
    Test error handling in the chat endpoint.
    """
    # Setup
    fake_chat_websocket.incoming_texts = ["Create a workflow", "__close__"]

    # Mock workflow_factory.classify_workflow to raise an exception
    async def fake_classify_workflow(data):
        raise ValueError("Test error")

    monkeypatch.setattr(
        "app.api.v1.endpoints.chat.workflow_factory.classify_workflow",
        fake_classify_workflow,
    )

    # Execute
    await chat_with_llm(fake_chat_websocket)

    # Verify
    assert fake_chat_websocket.accepted is True
    assert len(fake_chat_websocket.sent_texts) == 1
    assert (
        "Error creating complex workflow: Test error"
        in fake_chat_websocket.sent_texts[0]
    )
