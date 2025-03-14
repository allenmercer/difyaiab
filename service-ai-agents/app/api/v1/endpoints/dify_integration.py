from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.core.config import settings
import requests
import yaml

router = APIRouter()

DIFY_BACKEND = settings.DIFY_BACKEND

def get_auth(email: str, password: str):
    try:
        auth_url = f'{DIFY_BACKEND}/console/api/login'
        auth_headers = {'Content-Type': 'application/json'}
        auth_payload = {"email": email, "password": password, "language": "en-US", "remember_me": True}
        auth_response = requests.post(auth_url, headers=auth_headers, json=auth_payload)
        auth_response.raise_for_status()
        data = auth_response.json()
        token = data['data']['access_token']
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {e}")
    
    return token

"""
This endpoint gets a list of workflows. Currently limited to 30.
The payload needs a auth token from Dify
"""
@router.post('/workflows')
async def get_workflows(data: dict):
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    token = data.get("token")

    if not token:
        raise HTTPException(status_code=400, detail="Token is required in the payload")

    url = f'{DIFY_BACKEND}/console/api/apps?page=1&limit=30&name='
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        dify_import = requests.get(url, headers=headers)
        dify_import.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

    return dify_import.json()


"""
This endpoint submits workflow to Dify.
The. payload needs a email and password for Dify 
to authenticate and the yaml file.
"""

@router.post("/import")
async def file_import(email: str = Form(), password: str = Form(), file: UploadFile = File(...)):    
    contents = await file.read()
    
    # This method needs to get removed once we have Auth working
    token = get_auth(email, password)

    try:
        yaml_data = yaml.safe_load(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading YAML file: {e}")

    try:
        url = f'{DIFY_BACKEND}/console/api/apps/imports'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        payload = {
            "mode": "yaml-content",
            "yaml_content": yaml.dump(yaml_data, default_flow_style=False)
        }
        dify_import = requests.post(url, headers=headers, json=payload)
        dify_import.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

    return dify_import.json()