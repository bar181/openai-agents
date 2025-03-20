from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

def test_generic_lifecycle_agent_echo_tool():
    response = client.post(
        "/agents/advanced/generic-lifecycle/execute",
        json={"message": "Echo 'Hello World'"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Echo: Hello World"

def test_generic_lifecycle_agent_math_add_tool():
    response = client.post(
        "/agents/advanced/generic-lifecycle/execute",
        json={"message": "Add 2 and 3"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "5" in data["response"], f"Expected sum result in response, got {data['response']}"

def test_generic_lifecycle_agent_math_multiply_tool():
    response = client.post(
        "/agents/advanced/generic-lifecycle/execute",
        json={"message": "Multiply 4 by 5"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "20" in data["response"], f"Expected multiplication result in response, got {data['response']}"

def test_generic_lifecycle_agent_datetime_tool():
    response = client.post(
        "/agents/advanced/generic-lifecycle/execute",
        json={"message": "What's the current UTC time?"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "T" in data["response"], "Expected ISO datetime format in response"

def test_generic_lifecycle_agent_string_uppercase_tool():
    response = client.post(
        "/agents/advanced/generic-lifecycle/execute",
        json={"message": "Convert 'hello' to uppercase"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "HELLO" in data["response"], f"Expected uppercase 'HELLO', got {data['response']}"

def test_generic_lifecycle_agent_data_fetch_tool():
    response = client.post(
        "/agents/advanced/generic-lifecycle/execute",
        json={"message": "Fetch MOCK data from 'source1'"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "sample data" in data["response"], f"Expected fetched data in response, got {data['response']}"
