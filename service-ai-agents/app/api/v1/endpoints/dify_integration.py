from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.core.config import settings
from ai_ailevate_logging.logger import Logger
import requests
import yaml

router = APIRouter()

logger = Logger("Dify-POC-Agent")

DIFY_BACKEND = settings.DIFY_BACKEND


def get_auth(email: str, password: str):
    try:
        auth_url = f"{DIFY_BACKEND}/console/api/login"
        auth_headers = {"Content-Type": "application/json"}
        auth_payload = {
            "email": email,
            "password": password,
            "language": "en-US",
            "remember_me": True,
        }
        auth_response = requests.post(auth_url, headers=auth_headers, json=auth_payload)
        auth_response.raise_for_status()
        data = auth_response.json()
        token = data["data"]["access_token"]
    except requests.RequestException as e:
        logger.info(f"Authentication failed: {e}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {e}")

    return token


@router.post(
    "/workflows",
    summary="Get Workflows from Dify",
    description="This endpoint gets a list of workflows. Currently limited to 30",
    response_description="A JSON object containing a list of workflow names",
)
async def get_workflows(data: dict):
    """
    This endpoint gets a list of workflows. Currently limited to 30.
    The payload needs a auth token from Dify
    """
    if not data:
        logger.error("No data provided in payload")
        raise HTTPException(status_code=400, detail="No data provided in payload")

    email = data.get("email")
    password = data.get("password")

    if not email:
        logger.error("Email is required in the payload")
        raise HTTPException(status_code=400, detail="Email is required in the payload")
    if not password:
        logger.error("Password is required in the payload")
        raise HTTPException(
            status_code=400, detail="Password is required in the payload"
        )

    # This method needs to get removed once we have Auth working
    token = get_auth(email, password)

    try:
        url = f"{DIFY_BACKEND}/console/api/apps?page=1&limit=30&name="

        headers = {"Authorization": f"Bearer {token}"}

        dify_import = requests.get(url, headers=headers)
        dify_import.raise_for_status()
    except requests.RequestException as e:
        logger.info("Request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

    # Parse the JSON data and just get names
    data = dify_import.json()
    workflow_names = [item["name"] for item in data["data"]]
    workflow_dict = {"workflows": workflow_names}

    return workflow_dict


@router.post(
    "/import",
    summary="Submit workflow to Dify",
    description="This endpoint submits a workflow to dify. The paylload requires an email and password as well as the DSL file",
    response_description="A JSON object representing the response from Dify",
)
async def file_import(
    email: str = Form(), password: str = Form(), file: UploadFile = File(...)
):
    """
    This endpoint submits workflow to Dify.
    The. payload needs a email and password for Dify
    to authenticate and the yaml file.
    """
    contents = await file.read()

    # This method needs to get removed once we have Auth working
    token = get_auth(email, password)

    try:
        yaml_data = yaml.safe_load(contents)
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading YAML file: {e}")

    try:
        url = f"{DIFY_BACKEND}/console/api/apps/imports"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        payload = {
            "mode": "yaml-content",
            "yaml_content": yaml.dump(yaml_data, default_flow_style=False),
        }

        dify_import = requests.post(url, headers=headers, json=payload)
        dify_import.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

    return dify_import.json()


@router.post(
    "/import_from_chat",
    summary="Submit Workflow from Chat",
    description="This endpoint submits a workflow from the chabot. The payload must include an email and password and YAM file",
    response_description="The JSON response returned by the Dify import endpoint",
)
async def file_import(data: dict):
    """
    This endpoint submits workflow to Dify from the chatbot.
    The. payload needs a email and password for Dify
    to authenticate and the yaml file.
    """
    if not data:
        logger.error(f"Request failed: No data provided")
        raise HTTPException(status_code=400, detail="No data provided")

    email = data.get("email")
    password = data.get("password")
    yaml_file = data.get("file")

    if not email:
        logger.error("Email is required in the payload")
        raise HTTPException(status_code=400, detail="Email is required in the payload")
    if not password:
        logger.error("Password is required in the payload")
        raise HTTPException(
            status_code=400, detail="Password is required in the payload"
        )
    if not yaml_file:
        logger.error("File is required in the payload")
        raise HTTPException(status_code=400, detail="File is required in the payload")

    # This method needs to get removed once we have Auth working
    token = get_auth(email, password)

    try:
        yaml_data = yaml.safe_load(yaml_file)
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading YAML file: {e}")

    try:
        url = f"{DIFY_BACKEND}/console/api/apps/imports"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        payload = {
            "mode": "yaml-content",
            "yaml_content": yaml.dump(yaml_data, default_flow_style=False),
        }

        dify_import = requests.post(url, headers=headers, json=payload)
        dify_import.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

    return dify_import.json()
