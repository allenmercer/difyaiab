from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.workflow_service import workflow_factory
from app.core.resources import Resource
from ai_ailevate_logging.logger import Logger
import yaml

router = APIRouter()


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


@router.websocket("/chat")
async def chat_with_llm(websocket: WebSocket):
    await websocket.accept()

    logger = Logger("Dify-POC-Agent")
    try:
        while True:
            # Parse the incoming message
            data = await websocket.receive_text()

            logger.debug("Entered socket")

            try:
                if data.strip().lower() == "generate default dsl":
                    default_dsl = Resource.DSL_DEFAULT
                    await websocket.send_text(default_dsl)
                # help classify which type of workflow to use
                else:
                    template_response = await workflow_factory.classify_workflow(data)
                    logger.info("Workflow classified: " + template_response)
                    if "other" in template_response:
                        logger.warning("Workflow is not specified")
                        await websocket.send_text(
                            "Workflow specified is not yet supported :("
                        )
                    else:
                        logger.debug("Building workflow...")

                        # Generate app name and description
                        app_name = await workflow_factory.generate_app_name(data)
                        app_description = (
                            await workflow_factory.generate_app_description(data)
                        )

                        # Create a complex workflow with dynamically determined nodes
                        workflow = await workflow_factory.create_complex_workflow(data)

                        # Build DSL
                        CURRENT_DSL_VERSION = "0.1.5"
                        dsl = {
                            "app": {
                                "name": app_name,
                                "mode": "workflow",
                                "icon": "🤖",
                                "icon_background": "#FFEAD5",
                                "description": app_description,
                            },
                            "version": CURRENT_DSL_VERSION,
                            "kind": "app",
                            "workflow": workflow,
                        }

                        # Convert to YAML and send
                        dsl_yaml = yaml.dump(dsl, sort_keys=False, Dumper=NoAliasDumper)
                        await websocket.send_text(dsl_yaml)

            except Exception as e:
                logger.error(f"Error creating complex workflow: {str(e)}")
                await websocket.send_text(f"Error creating complex workflow: {str(e)}")
    except WebSocketDisconnect:
        logger.info("Disconnected from Chat")
