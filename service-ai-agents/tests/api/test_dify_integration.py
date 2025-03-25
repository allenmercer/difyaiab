import yaml
import pytest
import requests
from fastapi import HTTPException, FastAPI
from fastapi.testclient import TestClient
from app.api.v1.endpoints.dify_integration import router, get_auth

app = FastAPI()
app.include_router(router)
client = TestClient(app)

class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.RequestException("Error occurred")

    def json(self):
        return self._json

# Tests for get_auth function
def test_get_auth_success(monkeypatch):
    def fake_post(url, headers, json):
        return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
    monkeypatch.setattr(requests, "post", fake_post)
    
    token = get_auth("test@example.com", "password")
    assert token == "fake_token"

def test_get_auth_failure(monkeypatch):
    def fake_post(url, headers, json):
        return FakeResponse({}, status_code=400)
    monkeypatch.setattr(requests, "post", fake_post)
    
    with pytest.raises(HTTPException) as excinfo:
        get_auth("test@example.com", "wrong_password")
    assert "Authentication failed" in str(excinfo.value.detail)

# Tests for the /workflows endpoint
def test_get_workflows_success(monkeypatch):
    def fake_post(url, headers, json):
        return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
    monkeypatch.setattr(requests, "post", fake_post)
    
    def fake_get(url, headers):
        return FakeResponse({"data": [{"name": "Workflow1"}, {"name": "Workflow2"}]}, status_code=200)
    monkeypatch.setattr(requests, "get", fake_get)

    payload = {"email": "test@example.com", "password": "password"}
    response = client.post("/workflows", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "workflows" in data
    assert data["workflows"] == ["Workflow1", "Workflow2"]

def test_get_workflows_no_payload():
    response = client.post("/workflows", json={})
    assert response.status_code == 400
    assert "No data provided" in response.json()["detail"]

def test_get_workflows_missing_email():
    payload = {"password": "password"}
    response = client.post("/workflows", json=payload)
    assert response.status_code == 400
    assert "Email is required" in response.json()["detail"]

def test_get_workflows_missing_password():
    payload = {"email": "test@example.com"}
    response = client.post("/workflows", json=payload)
    assert response.status_code == 400
    assert "Password is required" in response.json()["detail"]

def test_get_workflows_requests_failure(monkeypatch):
    def fake_post(url, headers, json):
        return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
    monkeypatch.setattr(requests, "post", fake_post)
    
    def fake_get(url, headers):
        fake = FakeResponse({}, status_code=500)
        fake.raise_for_status()
        return fake
    monkeypatch.setattr(requests, "get", fake_get)
    
    payload = {"email": "test@example.com", "password": "password"}
    response = client.post("/workflows", json=payload)
    assert response.status_code == 500
    assert "Request failed" in response.json()["detail"]

# Tests for the /import endpoint
def test_file_import_success(monkeypatch):
    def fake_post(url, headers, json=None):
        if "login" in url:
            return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
        else:
            return FakeResponse({"result": "success"}, status_code=200)
    monkeypatch.setattr(requests, "post", fake_post)
    
    valid_yaml = {"key": "value"}
    yaml_bytes = yaml.dump(valid_yaml).encode('utf-8')
    
    response = client.post(
        "/import",
        data={"email": "test@example.com", "password": "password"},
        files={"file": ("test.yaml", yaml_bytes, "application/x-yaml")}
    )
    assert response.status_code == 200
    assert response.json()["result"] == "success"

def test_file_import_invalid_yaml(monkeypatch):
    def fake_post(url, headers, json=None):
        return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
    monkeypatch.setattr(requests, "post", fake_post)
    
    invalid_yaml = ":\n not valid yaml"
    response = client.post(
        "/import",
        data={"email": "test@example.com", "password": "password"},
        files={"file": ("test.yaml", invalid_yaml.encode('utf-8'), "application/x-yaml")}
    )
    assert response.status_code == 500
    assert "Error reading YAML file" in response.json()["detail"]

def test_file_import_requests_failure(monkeypatch):
    def fake_post(url, headers, json=None):
        if "login" in url:
            return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
        elif "imports" in url:
            fake = FakeResponse({}, status_code=500)
            fake.raise_for_status()
            return fake
    monkeypatch.setattr(requests, "post", fake_post)
    
    valid_yaml = {"key": "value"}
    yaml_bytes = yaml.dump(valid_yaml).encode("utf-8")
    
    response = client.post(
        "/import",
        data={"email": "test@example.com", "password": "password"},
        files={"file": ("test.yaml", yaml_bytes, "application/x-yaml")}
    )
    assert response.status_code == 500
    assert "Request failed" in response.json()["detail"]

# Tests for the /import_from_chat endpoint
def test_import_from_chat_success(monkeypatch):
    def fake_post(url, headers, json=None):
        if "login" in url:
            return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
        else:
            return FakeResponse({"result": "success"}, status_code=200)
    monkeypatch.setattr(requests, "post", fake_post)
    
    valid_yaml_str = yaml.dump({"key": "value"})
    payload = {"email": "test@example.com", "password": "password", "file": valid_yaml_str}
    response = client.post("/import_from_chat", json=payload)
    assert response.status_code == 200
    assert response.json()["result"] == "success"

def test_import_from_chat_no_payload():
    response = client.post("/import_from_chat", json={})
    assert response.status_code == 400
    assert "No data provided" in response.json()["detail"]

def test_import_from_chat_missing_email():
    payload = {"password": "password", "file": "dummy"}
    response = client.post("/import_from_chat", json=payload)
    assert response.status_code == 400
    assert "Email is required" in response.json()["detail"]

def test_import_from_chat_missing_password():
    payload = {"email": "test@example.com", "file": "dummy"}
    response = client.post("/import_from_chat", json=payload)
    assert response.status_code == 400
    assert "Password is required" in response.json()["detail"]

def test_import_from_chat_missing_file():
    payload = {"email": "test@example.com", "password": "password"}
    response = client.post("/import_from_chat", json=payload)
    assert response.status_code == 400
    assert "File is required" in response.json()["detail"]

def test_import_from_chat_invalid_yaml(monkeypatch):
    def fake_post(url, headers, json=None):
        if "login" in url:
            return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
        else:
            return FakeResponse({"result": "success"}, status_code=200)
    monkeypatch.setattr(requests, "post", fake_post)
    
    invalid_yaml = ":\n not valid yaml"
    payload = {"email": "test@example.com", "password": "password", "file": invalid_yaml}
    response = client.post("/import_from_chat", json=payload)
    assert response.status_code == 500
    assert "Error reading YAML file" in response.json()["detail"]

def test_import_from_chat_requests_failure(monkeypatch):
    def fake_post(url, headers, json=None):
        if "login" in url:
            return FakeResponse({"data": {"access_token": "fake_token"}}, status_code=200)
        elif "imports" in url:
            fake = FakeResponse({}, status_code=500)
            fake.raise_for_status()
            return fake
    monkeypatch.setattr(requests, "post", fake_post)
    
    valid_yaml_str = yaml.dump({"key": "value"})
    payload = {"email": "test@example.com", "password": "password", "file": valid_yaml_str}
    response = client.post("/import_from_chat", json=payload)
    assert response.status_code == 500
    assert "Request failed" in response.json()["detail"]