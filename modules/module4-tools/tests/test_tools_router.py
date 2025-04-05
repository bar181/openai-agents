import re
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY  # Assumes API_KEY is defined in your config

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}  # Use the valid API key for testing

# Math Tools
def test_add_endpoint():
    response = client.post("/tools/math/add", json={"a": 2, "b": 3}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] == 5

def test_multiply_endpoint():
    response = client.post("/tools/math/multiply", json={"a": 4, "b": 5}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] == 20

# String Tools
def test_to_uppercase_endpoint():
    response = client.post("/tools/string/to_uppercase", json={"text": "hello"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] == "HELLO"

def test_concatenate_endpoint():
    response = client.post("/tools/string/concatenate", json={"text1": "hello", "text2": "world"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] == "helloworld"

# Datetime Tools
def test_current_time_endpoint():
    response = client.get("/tools/datetime/current_time", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "current_time" in data
    # Validate against an ISO 8601 format (rough check)
    iso_regex = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})"
    assert re.match(iso_regex, data["current_time"])

def test_add_days_endpoint():
    response = client.post("/tools/datetime/add_days", json={"base_date": "2023-01-01", "days": 5}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    # Check that the resulting date starts with "2023-01-06"
    assert data["result"].startswith("2023-01-06")

# Echo Tool
def test_echo_endpoint():
    response = client.post("/tools/echo/echo", json={"message": "Hello World"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] == "Echo: Hello World"

# Multi-Tool Agent
def test_multi_tool_endpoint():
    # The multi-tool agent expects input in the format "num1,num2;text;text"
    # Example: "2,3;hello;world"
    response = client.post("/tools/multi-tool/multi-tool", json={"input_data": "2,3;hello;world"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    # Expect the result to include the following keys:
    assert "math_result" in data
    assert "uppercase_result" in data
    assert "echo_result" in data
    # Validate the outputs:
    assert data["math_result"] == 5.0
    assert data["uppercase_result"] == "HELLO"
    assert data["echo_result"] == "Echo: world"
