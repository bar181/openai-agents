# File: root/modules/module3-basic-agents/tests/test_basic_agents.py

from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

def test_initialize_lifecycle_agent():
    response = client.post("/agents/basic/lifecycle/initialize", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Lifecycle agent initialized."

def test_execute_lifecycle_agent():
    input_data = {"input": "Sample input for lifecycle agent"}
    response = client.post("/agents/basic/lifecycle/execute", json=input_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert input_data["input"] in data["result"]

def test_terminate_lifecycle_agent():
    response = client.post("/agents/basic/lifecycle/terminate", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Lifecycle agent terminated."

def test_update_dynamic_system_prompt():
    prompt_update = {"new_prompt": "You are now an advanced assistant."}
    response = client.post("/agents/basic/dynamic-prompt/update", json=prompt_update, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "prompt" in data
    assert data["prompt"] == prompt_update["new_prompt"]

def test_execute_dynamic_prompt_agent():
    input_data = {"input": "Test dynamic prompt agent execution."}
    response = client.post("/agents/basic/dynamic-prompt/execute", json=input_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert input_data["input"] in data["response"]
