import time
import uuid
from typing import Any, Dict, List, Optional, Protocol, TypedDict

from ai_ailevate_logging.logger import Logger
import yaml
from app.core.prompts import StaticPrompts
from app.services.llm_client import generic_llm_call
from app.utils.JsonUtil import JsonUtil
import yaml

logger = Logger("Dify-POC-Agent")


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


class NodeData(TypedDict, total=False):
    """Base node data structure that all nodes will extend"""

    desc: str
    selected: bool
    title: str
    type: str
    variables: list


class NodePosition(TypedDict):
    """Position information for nodes in the graph"""

    x: int
    y: int


class Node(TypedDict):
    """Base node structure"""

    data: Any
    height: int
    id: str
    position: NodePosition
    positionAbsolute: NodePosition
    selected: bool
    sourcePosition: str
    targetPosition: str
    type: str
    width: int


class Edge(TypedDict):
    """Edge between nodes in the workflow graph"""

    data: Dict[str, Any]
    id: str
    source: str
    sourceHandle: str
    target: str
    targetHandle: str
    type: str
    zIndex: int


class WorkflowGraph(TypedDict):
    """Complete workflow graph structure"""

    edges: List[Edge]
    nodes: List[Node]
    viewport: Dict[str, Any]


class Workflow(TypedDict):
    """Complete workflow graph structure"""

    features: Dict[str, Any]
    graph: WorkflowGraph
    environment_variables: List[Any]
    conversation_variables: List[Any]


class NodeProcessor(Protocol):
    """Protocol defining the interface for all node processors"""

    node_type: str

    async def process(
        self,
        message: str,
        node_id: str,
        position: NodePosition,
        previous_node_id: Optional[str] = None,
        previous_node_type: Optional[str] = None,
    ) -> Node:
        """Process a node and generate its data"""
        ...


class StartNodeProcessor:
    """Start node processor"""

    node_type = "start"

    async def process(
        self,
        message: str,
        node_id: str,
        position: NodePosition,
        previous_node_id: Optional[str] = None,
        previous_node_type: Optional[str] = None,
    ) -> Node:
        return {
            "data": {
                "desc": "",
                "selected": False,
                "title": "Start",
                "type": "start",
                "variables": [],
            },
            "height": 54,
            "id": node_id,
            "position": position,
            "positionAbsolute": position,
            "selected": False,
            "sourcePosition": "right",
            "targetPosition": "left",
            "type": "custom",
            "width": 244,
        }


class EndNodeProcessor:
    """End node processor"""

    node_type = "end"

    async def process(
        self,
        message: str,
        node_id: str,
        position: NodePosition,
        previous_node_id: Optional[str] = None,
        previous_node_type: Optional[str] = None,
    ) -> Node:
        outputs = []
        if previous_node_id:
            # Different output handling based on previous node type
            if previous_node_type and "http" in previous_node_type:
                outputs = await generate_http_end(message, previous_node_id)
            else:
                outputs = [
                    {"variable": "Result", "value_selector": [previous_node_id, "text"]}
                ]

        return {
            "data": {
                "desc": "",
                "selected": False,
                "title": "End",
                "type": "end",
                "outputs": outputs,
            },
            "height": 90,
            "id": node_id,
            "position": position,
            "positionAbsolute": position,
            "selected": False,
            "sourcePosition": "right",
            "targetPosition": "left",
            "type": "custom",
            "width": 244,
        }


class LLMNodeProcessor:
    """LLM node processor"""

    node_type = "llm"

    async def process(
        self,
        message: str,
        node_id: str,
        position: NodePosition,
        previous_node_id: Optional[str] = None,
        previous_node_type: Optional[str] = None,
    ) -> Node:
        return {
            "data": {
                "desc": "",
                "type": "llm",
                "title": "LLM",
                "selected": False,
                "model": await generate_llm_model(message),
                "prompt_template": [
                    {
                        "id": str(uuid.uuid4()),
                        "role": "user",
                        "text": await generate_llm_prompt(message),
                        "edition_type": "basic",
                    }
                ],
                "context": {"enabled": False, "variable_selector": []},
                "vision": {"enabled": False},
                "variables": [],
            },
            "height": 98,
            "id": node_id,
            "position": position,
            "positionAbsolute": position,
            "selected": False,
            "sourcePosition": "right",
            "targetPosition": "left",
            "type": "custom",
            "width": 244,
        }


class HTTPNodeProcessor:
    """HTTP request node processor"""

    node_type = "http-request"

    async def process(
        self,
        message: str,
        node_id: str,
        position: NodePosition,
        previous_node_id: Optional[str] = None,
        previous_node_type: Optional[str] = None,
    ) -> Node:
        return {
            "data": await generate_http_data(message),
            "height": 120,
            "id": node_id,
            "position": position,
            "positionAbsolute": position,
            "selected": False,
            "sourcePosition": "right",
            "targetPosition": "left",
            "type": "custom",
            "width": 244,
        }


class WorkflowBuilder:
    """Workflow builder for assembling nodes and edges into a complete workflow"""

    def __init__(self):
        self.node_processors = {}
        self._register_default_processors()

    def _register_default_processors(self):
        """Register default node processors"""
        processors = [
            StartNodeProcessor(),
            EndNodeProcessor(),
            LLMNodeProcessor(),
            HTTPNodeProcessor(),
        ]

        for processor in processors:
            self.register_processor(processor)

    def register_processor(self, processor: NodeProcessor):
        """Register a new node processor"""
        self.node_processors[processor.node_type] = processor

    def _generate_node_id(self, index: int = 0) -> str:
        """Generate a unique node ID with optional time offset"""
        return str(int(time.time() * 1000) + index * 10000)

    def _calculate_position(self, index: int, total_nodes: int) -> NodePosition:
        """Calculate position for a node based on its index in the workflow"""
        # Basic horizontal flow with equal spacing
        base_x = 80
        step_x = 304
        y = 282

        return {"x": base_x + index * step_x, "y": y}

    def _generate_features(self) -> Dict[str, Any]:
        """Generate default features configuration"""
        return {
            "file_upload": {
                "allowed_file_extensions": [
                    ".JPG",
                    ".JPEG",
                    ".PNG",
                    ".GIF",
                    ".WEBP",
                    ".SVG",
                ],
                "allowed_file_types": ["image"],
                "allowed_file_upload_methods": ["local_file", "remote_url"],
                "enabled": False,
                "fileUploadConfig": {
                    "audio_file_size_limit": 50,
                    "batch_count_limit": 5,
                    "file_size_limit": 15,
                    "image_file_size_limit": 10,
                    "video_file_size_limit": 100,
                    "workflow_file_upload_limit": 10,
                },
                "image": {
                    "enabled": False,
                    "number_limits": 3,
                    "transfer_methods": ["local_file", "remote_url"],
                },
                "number_limits": 3,
            },
            "opening_statement": "",
            "retriever_resource": {"enabled": True},
            "sensitive_word_avoidance": {"enabled": False},
            "speech_to_text": {"enabled": False},
            "suggested_questions": [],
            "suggested_questions_after_answer": {"enabled": False},
            "text_to_speech": {"enabled": False, "language": "", "voice": ""},
        }

    async def create_edge(
        self, source_id: str, target_id: str, source_type: str, target_type: str
    ) -> Edge:
        """Create an edge between two nodes"""
        return {
            "data": {
                "isInIteration": False,
                "sourceType": source_type,
                "targetType": target_type,
            },
            "id": f"{source_id}-source-{target_id}-target",
            "source": source_id,
            "sourceHandle": "source",
            "target": target_id,
            "targetHandle": "target",
            "type": "custom",
            "zIndex": 0,
        }

    async def build_workflow(self, message: str, node_types: List[str]) -> Workflow:
        return {
            "features": self._generate_features(),
            "graph": await self.build_graph(message, node_types),
            "environment_variables": [],
            "conversation_variables": [],
        }

    async def build_graph(self, message: str, node_types: List[str]) -> WorkflowGraph:
        """Build a complete workflow with the specified node types"""
        nodes = []
        edges = []

        # Validate that we have processors for all node types
        for node_type in node_types:
            if node_type not in self.node_processors:
                raise ValueError(f"No processor registered for node type: {node_type}")

        # Always have at least start and end nodes
        if "start" not in node_types:
            node_types.insert(0, "start")

        if "end" not in node_types:
            node_types.append("end")

        # Generate node IDs
        node_ids = [self._generate_node_id(i) for i in range(len(node_types))]

        # Create nodes
        for i, node_type in enumerate(node_types):
            position = self._calculate_position(i, len(node_types))
            previous_id = node_ids[i - 1] if i > 0 else None
            previous_node_type = node_types[i - 1] if i > 0 else None

            # Process the node with the appropriate processor
            processor = self.node_processors[node_type]
            node = await processor.process(
                message=message,
                node_id=node_ids[i],
                position=position,
                previous_node_id=previous_id,
                previous_node_type=previous_node_type,
            )

            nodes.append(node)

            # Create edge with previous node (if not the first node)
            if i > 0:
                edge = await self.create_edge(
                    source_id=node_ids[i - 1],
                    target_id=node_ids[i],
                    source_type=node_types[i - 1],
                    target_type=node_type,
                )
                edges.append(edge)

        logger.debug(f"Edges: {edges}")
        logger.debug(f"Nodes: {nodes}")

        return {
            "edges": edges,
            "nodes": nodes,
            "viewport": {"x": -2.96, "y": -4.71, "zoom": 1.01},
        }


class WorkflowFactory:
    """Factory for creating different types of workflows"""

    def __init__(self):
        self.builder = WorkflowBuilder()

    async def classify_workflow(self, message: str) -> str:
        """Classify the type of workflow based on the message"""
        user_prompt = StaticPrompts.WORKFLOW_CLASSIFICATION.format(message)
        system_message = "You are a helpful assistant and a workflow classifier"
        return await generic_llm_call(system_message, user_prompt)

    async def determine_node_sequence(self, message: str) -> List[str]:
        """Determine the optimal sequence of nodes for a workflow"""
        user_prompt = StaticPrompts.WORKFLOW_NODE_SEQUENCE.format(message)
        system_message = "You are a workflow node sequence generator"

        response = await generic_llm_call(system_message, user_prompt)

        # Split by comma and strip whitespace
        node_types = [node_type.strip() for node_type in response.split(",")]

        # Validate basic requirements (start and end nodes)
        if not node_types or len(node_types) < 2:
            # Default to simplest workflow if response is invalid
            return ["start", "end"]

        if node_types[0] != "start":
            node_types.insert(0, "start")

        if node_types[-1] != "end":
            node_types.append("end")

        return node_types

    async def generate_app_name(self, message: str) -> str:
        """Generate app name via LLM"""
        system_prompt = StaticPrompts.GENERATE_APP_NAME_SYSTEM
        user_prompt = StaticPrompts.GENERATE_APP_NAME_USER.format(message)
        result = await generic_llm_call(system_prompt, user_prompt, 0.2)
        return result.strip()

    async def generate_app_description(self, message: str) -> str:
        """Generate app description via LLM"""
        system_prompt = StaticPrompts.GENERATE_APP_DESCRIPTION_SYSTEM
        user_prompt = StaticPrompts.GENERATE_APP_DESCRIPTION_USER.format(message)
        result = await generic_llm_call(system_prompt, user_prompt, 0.2)
        return result.strip()

    async def create_complex_workflow(self, message: str) -> WorkflowGraph:
        """Create a more complex workflow by determining node sequence dynamically"""
        node_sequence = await self.determine_node_sequence(message)
        logger.info(f"Generated the following node sequence  {node_sequence} ")
        return await self.builder.build_workflow(message, node_sequence)


# Initialize the workflow factory
workflow_factory = WorkflowFactory()


async def generate_llm_model(message: str):
    """
    Generate llm model details
    """
    system_prompt = StaticPrompts.GENERATE_LLM_MODEL_SYSTEM

    user_prompt = StaticPrompts.GENERATE_LLM_MODEL_USER.format(message)

    response = await generic_llm_call(system_prompt, user_prompt, 0.2)
    return JsonUtil.convert_to_dict(response)


async def generate_llm_prompt(message: str):
    """
    Generate prompt for llm
    """
    system_prompt = StaticPrompts.GENERATE_LLM_PROMPT_SYSTEM

    user_prompt = StaticPrompts.GENERATE_LLM_PROMPT_USER.format(message)

    result = await generic_llm_call(system_prompt, user_prompt, 0.2)
    return result.strip()


async def generate_http_data(message: str):
    """
    Generate http data
    """
    system_prompt = StaticPrompts.GENERATE_HTTP_BODY_SYSTEM

    user_prompt = StaticPrompts.GENERATE_HTTP_BODY_USER.format(message)

    response = await generic_llm_call(system_prompt, user_prompt, 0.2)

    return JsonUtil.convert_to_dict(response)


async def generate_http_end(message: str, previous_node: str):
    """
    Generate http data
    """
    system_prompt = StaticPrompts.GENERATE_HTTP_END_NODE_SYSTEM

    user_prompt = StaticPrompts.GENERATE_HTTP_END_NODE_USER.format(
        message, previous_node
    )

    response = await generic_llm_call(system_prompt, user_prompt, 0.2)

    return JsonUtil.convert_to_list_of_dicts(response)
