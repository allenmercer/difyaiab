import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_get_workflows(mocker):
    token = '1234abc'
    payload = {
        "token": token
    }

    # Mock dify backend response get request
    mock_post = mocker.patch('requests.get')

    # Configure the mock to return data
    mock_response = MagicMock()
    mock_response.json.return_value = {"Workflows": "Details"}
    mock_post.return_value = mock_response

    # Test endpoint
    response = client.post("/api/v1/workflows", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"Workflows": "Details"}

def test_get_workflows_no_dify():
    token = '1234abc'
    payload = {
        "token": token
    }

    # Test endpoint
    response = client.post("/api/v1/workflows", json=payload)
    
    assert response.status_code == 500
    assert "Request failed: " in response.text

def test_get_workflow_no_data():
    payload = {}

    # Test endpoint
    response = client.post("/api/v1/workflows", json=payload)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "No data provided"}

def test_get_workflow_no_token():
    token = ''
    payload = {
        "token": token
    }

    # Test endpoint
    response = client.post("/api/v1/workflows", json=payload)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Token is required in the payload"}
