import pytest
from unittest.mock import patch, AsyncMock
from app.services.workflow_service import (
    workflow_factory,
    WorkflowFactory,
    WorkflowBuilder,
    NodeProcessor,
    StartNodeProcessor,
    EndNodeProcessor,
    LLMNodeProcessor,
    HTTPNodeProcessor,
    generate_llm_model,
    generate_llm_prompt,
    generate_http_data,
    generate_http_end,
    NoAliasDumper,
)


@pytest.mark.asyncio
class TestWorkflowFactory:
    @pytest.fixture
    def mock_llm_call(self):
        """
        Patches 'generic_llm_call' with an AsyncMock.
        """
        patcher = patch(
            "app.services.workflow_service.generic_llm_call", new_callable=AsyncMock
        )
        mocked = patcher.start()
        yield mocked
        patcher.stop()

    @pytest.fixture
    def factory(self):
        """Return a fresh WorkflowFactory instance"""
        return WorkflowFactory()

    async def test_classify_workflow(self, factory, mock_llm_call):
        """Test workflow classification"""
        mock_llm_call.return_value = "llm"
        result = await factory.classify_workflow("use AI to answer questions")
        assert result == "llm"
        mock_llm_call.assert_awaited_once()

    async def test_determine_node_sequence_valid(self, factory, mock_llm_call):
        """Test node sequence determination with valid response"""
        mock_llm_call.return_value = "start,llm,http-request,end"
        result = await factory.determine_node_sequence("my workflow request")
        assert result == ["start", "llm", "http-request", "end"]
        mock_llm_call.assert_awaited_once()

    async def test_determine_node_sequence_empty(self, factory, mock_llm_call):
        """Test node sequence determination with empty response"""
        mock_llm_call.return_value = ""
        result = await factory.determine_node_sequence("my workflow request")
        assert result == ["start", "end"]
        mock_llm_call.assert_awaited_once()

    async def test_determine_node_sequence_missing_start(self, factory, mock_llm_call):
        """Test node sequence determination with missing start node"""
        mock_llm_call.return_value = "llm,end"
        result = await factory.determine_node_sequence("my workflow request")
        assert result == ["start", "llm", "end"]
        mock_llm_call.assert_awaited_once()

    async def test_determine_node_sequence_missing_end(self, factory, mock_llm_call):
        """Test node sequence determination with missing end node"""
        mock_llm_call.return_value = "start,llm"
        result = await factory.determine_node_sequence("my workflow request")
        assert result == ["start", "llm", "end"]
        mock_llm_call.assert_awaited_once()

    async def test_generate_app_name(self, factory, mock_llm_call):
        """Test app name generation"""
        mock_llm_call.return_value = " Test App Name "
        result = await factory.generate_app_name("workflow request")
        assert result == "Test App Name"
        mock_llm_call.assert_awaited_once()

    async def test_generate_app_description(self, factory, mock_llm_call):
        """Test app description generation"""
        mock_llm_call.return_value = " This is a test description. "
        result = await factory.generate_app_description("workflow request")
        assert result == "This is a test description."
        mock_llm_call.assert_awaited_once()

    async def test_create_complex_workflow(self, factory, mock_llm_call):
        """Test complex workflow creation"""
        # Mock determine_node_sequence to return a predefined sequence
        with patch.object(
            factory, "determine_node_sequence", new_callable=AsyncMock
        ) as mock_determine:
            mock_determine.return_value = ["start", "llm", "http-request", "end"]
            # Mock builder.build_workflow
            with patch.object(
                factory.builder, "build_workflow", new_callable=AsyncMock
            ) as mock_build:
                mock_build.return_value = {"nodes": [], "edges": [], "viewport": {}}

                result = await factory.create_complex_workflow("my complex workflow")

                # Verify calls
                mock_determine.assert_awaited_once_with("my complex workflow")
                mock_build.assert_awaited_once_with(
                    "my complex workflow", ["start", "llm", "http-request", "end"]
                )
                assert result == {"nodes": [], "edges": [], "viewport": {}}


class TestWorkflowBuilder:
    @pytest.fixture
    def builder(self):
        """Return a fresh WorkflowBuilder instance"""
        return WorkflowBuilder()

    @pytest.fixture
    def mock_processor(self):
        """Create a mock node processor"""
        processor = AsyncMock()
        processor.node_type = "test-node"
        processor.process = AsyncMock(
            return_value={
                "data": {"type": "test-node"},
                "id": "test-id",
                "height": 100,
                "width": 100,
                "position": {"x": 0, "y": 0},
                "positionAbsolute": {"x": 0, "y": 0},
                "selected": False,
                "sourcePosition": "right",
                "targetPosition": "left",
                "type": "custom",
            }
        )
        return processor

    def test_register_processor(self, builder, mock_processor):
        """Test registering a custom node processor"""
        builder.register_processor(mock_processor)
        assert "test-node" in builder.node_processors
        assert builder.node_processors["test-node"] == mock_processor

    def test_generate_node_id(self, builder):
        """Test node ID generation"""
        id1 = builder._generate_node_id(0)
        id2 = builder._generate_node_id(1)

        # IDs should be strings
        assert isinstance(id1, str)
        assert isinstance(id2, str)

        # ID2 should be greater than ID1 by approximately 10000
        diff = int(id2) - int(id1)
        assert 9000 <= diff <= 11000

    def test_calculate_position(self, builder):
        """Test position calculation"""
        pos1 = builder._calculate_position(0, 3)
        pos2 = builder._calculate_position(1, 3)
        pos3 = builder._calculate_position(2, 3)

        assert pos1 == {"x": 80, "y": 282}
        assert pos2 == {"x": 384, "y": 282}
        assert pos3 == {"x": 688, "y": 282}

    async def test_create_edge(self, builder):
        """Test edge creation"""
        edge = await builder.create_edge("src-id", "tgt-id", "src-type", "tgt-type")

        assert edge["source"] == "src-id"
        assert edge["target"] == "tgt-id"
        assert edge["data"]["sourceType"] == "src-type"
        assert edge["data"]["targetType"] == "tgt-type"
        assert edge["id"] == "src-id-source-tgt-id-target"

    async def test_build_workflow_simple(self, builder):
        """Test building a simple workflow"""
        # Mock processor process methods
        with patch.object(
            StartNodeProcessor, "process", new_callable=AsyncMock
        ) as mock_start:
            with patch.object(
                EndNodeProcessor, "process", new_callable=AsyncMock
            ) as mock_end:
                # Set return values
                mock_start.return_value = {
                    "data": {"type": "start"},
                    "id": "start-id",
                    "height": 100,
                    "width": 100,
                    "position": {"x": 0, "y": 0},
                    "positionAbsolute": {"x": 0, "y": 0},
                    "selected": False,
                    "sourcePosition": "right",
                    "targetPosition": "left",
                    "type": "custom",
                }
                mock_end.return_value = {
                    "data": {"type": "end"},
                    "id": "end-id",
                    "height": 100,
                    "width": 100,
                    "position": {"x": 0, "y": 0},
                    "positionAbsolute": {"x": 0, "y": 0},
                    "selected": False,
                    "sourcePosition": "right",
                    "targetPosition": "left",
                    "type": "custom",
                }

                # Override _generate_node_id to return predictable values
                with patch.object(builder, "_generate_node_id") as mock_gen_id:
                    mock_gen_id.side_effect = ["start-id", "end-id"]

                    result = await builder.build_workflow(
                        "test message", ["start", "end"]
                    )

                    # Verify the result structure
                    assert "nodes" in result
                    assert "edges" in result
                    assert "viewport" in result

                    # Should have 2 nodes
                    assert len(result["nodes"]) == 2

                    # Should have 1 edge
                    assert len(result["edges"]) == 1

                    # Verify processor calls
                    mock_start.assert_awaited_once()
                    mock_end.assert_awaited_once()

    async def test_build_workflow_invalid_node(self, builder):
        """Test building a workflow with an invalid node type"""
        with pytest.raises(ValueError) as excinfo:
            await builder.build_workflow(
                "test message", ["start", "invalid-node", "end"]
            )

        assert "No processor registered for node type: invalid-node" in str(
            excinfo.value
        )


@pytest.mark.asyncio
class TestNodeProcessors:
    @pytest.fixture
    def mock_llm_call(self):
        """
        Patches 'generic_llm_call' with an AsyncMock.
        """
        patcher = patch(
            "app.services.workflow_service.generic_llm_call", new_callable=AsyncMock
        )
        mocked = patcher.start()
        yield mocked
        patcher.stop()

    async def test_start_node_processor(self):
        """Test the start node processor"""
        processor = StartNodeProcessor()
        node = await processor.process(
            message="test message", node_id="test-id", position={"x": 100, "y": 100}
        )

        # Verify node structure
        assert node["data"]["type"] == "start"
        assert node["id"] == "test-id"
        assert node["position"] == {"x": 100, "y": 100}

    async def test_end_node_processor_with_http(self, mock_llm_call):
        """Test the end node processor with HTTP previous node"""
        # Mock generate_http_end
        with patch(
            "app.services.workflow_service.generate_http_end", new_callable=AsyncMock
        ) as mock_http_end:
            mock_http_end.return_value = [
                {"variable": "HTTPResult", "value_selector": ["prev-id", "body"]}
            ]

            processor = EndNodeProcessor()
            node = await processor.process(
                message="test message",
                node_id="test-id",
                position={"x": 100, "y": 100},
                previous_node_id="http-prev-id",
            )

            # Verify node structure
            assert node["data"]["type"] == "end"
            assert node["id"] == "test-id"
            assert node["position"] == {"x": 100, "y": 100}
            assert node["data"]["outputs"] == [
                {"variable": "HTTPResult", "value_selector": ["prev-id", "body"]}
            ]

            # Verify generate_http_end was called
            mock_http_end.assert_awaited_once_with("test message", "http-prev-id")

    async def test_end_node_processor_with_llm(self):
        """Test the end node processor with LLM previous node"""
        processor = EndNodeProcessor()
        node = await processor.process(
            message="test message",
            node_id="test-id",
            position={"x": 100, "y": 100},
            previous_node_id="llm-prev-id",
        )

        # Verify node structure
        assert node["data"]["type"] == "end"
        assert node["id"] == "test-id"
        assert node["position"] == {"x": 100, "y": 100}
        assert node["data"]["outputs"] == [
            {"variable": "Result", "value_selector": ["llm-prev-id", "text"]}
        ]

    async def test_llm_node_processor(self, mock_llm_call):
        """Test the LLM node processor"""
        # Mock UUID generation
        with patch("uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = "mocked-uuid"

            # Mock generate_llm_model and generate_llm_prompt
            with patch(
                "app.services.workflow_service.generate_llm_model",
                new_callable=AsyncMock,
            ) as mock_model:
                with patch(
                    "app.services.workflow_service.generate_llm_prompt",
                    new_callable=AsyncMock,
                ) as mock_prompt:
                    mock_model.return_value = {"provider": "test", "name": "test-model"}
                    mock_prompt.return_value = "Test prompt"

                    processor = LLMNodeProcessor()
                    node = await processor.process(
                        message="test message",
                        node_id="test-id",
                        position={"x": 100, "y": 100},
                    )

                    # Verify node structure
                    assert node["data"]["type"] == "llm"
                    assert node["id"] == "test-id"
                    assert node["position"] == {"x": 100, "y": 100}
                    assert node["data"]["model"] == {
                        "provider": "test",
                        "name": "test-model",
                    }
                    assert node["data"]["prompt_template"][0]["text"] == "Test prompt"

                    # Verify method calls
                    mock_model.assert_awaited_once_with("test message")
                    mock_prompt.assert_awaited_once_with("test message")

    async def test_http_node_processor(self, mock_llm_call):
        """Test the HTTP node processor"""
        # Mock generate_http_data
        with patch(
            "app.services.workflow_service.generate_http_data", new_callable=AsyncMock
        ) as mock_http_data:
            mock_http_data.return_value = {
                "desc": "",
                "type": "http-request",
                "url": "https://test.com",
                "method": "get",
            }

            processor = HTTPNodeProcessor()
            node = await processor.process(
                message="test message", node_id="test-id", position={"x": 100, "y": 100}
            )

            # Verify node structure
            assert node["id"] == "test-id"
            assert node["position"] == {"x": 100, "y": 100}
            assert node["data"]["type"] == "http-request"
            assert node["data"]["url"] == "https://test.com"

            # Verify generate_http_data was called
            mock_http_data.assert_awaited_once_with("test message")


class TestHelperFunctions:
    @pytest.fixture
    def mock_llm_call(self):
        """
        Patches 'generic_llm_call' with an AsyncMock.
        """
        patcher = patch(
            "app.services.workflow_service.generic_llm_call", new_callable=AsyncMock
        )
        mocked = patcher.start()
        yield mocked
        patcher.stop()

    async def test_generate_llm_model(self, mock_llm_call):
        """Test llm model generation"""
        mock_llm_call.return_value = '{"provider": "test", "name": "test-model"}'
        result = await generate_llm_model("test message")
        assert result == {"provider": "test", "name": "test-model"}
        mock_llm_call.assert_awaited_once()

    async def test_generate_llm_prompt(self, mock_llm_call):
        """Test llm prompt generation"""
        mock_llm_call.return_value = " Test prompt "
        result = await generate_llm_prompt("test message")
        assert result == "Test prompt"
        mock_llm_call.assert_awaited_once()

    async def test_generate_http_data(self, mock_llm_call):
        """Test http data generation"""
        mock_llm_call.return_value = '{"url": "https://test.com", "method": "get"}'
        result = await generate_http_data("test message")
        assert result == {"url": "https://test.com", "method": "get"}
        mock_llm_call.assert_awaited_once()

    async def test_generate_http_end(self, mock_llm_call):
        """Test http end node generation"""
        mock_llm_call.return_value = (
            '[{"variable": "body", "value_selector": ["node-id", "body"]}]'
        )
        result = await generate_http_end("test message", "prev-node")
        assert result == [{"variable": "body", "value_selector": ["node-id", "body"]}]
        mock_llm_call.assert_awaited_once()

    def test_no_alias_dumper(self):
        """Test NoAliasDumper functionality"""
        dumper = NoAliasDumper(None)
        assert dumper.ignore_aliases(None) is True
