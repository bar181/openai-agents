"""
Test module for the Generic Lifecycle Agent functionality.

This module contains tests for the Generic Lifecycle Agent, which is an advanced agent
that integrates with various tools to perform different operations.
"""

from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

def test_generic_lifecycle_agent_echo_tool():
    """Test the echo tool integration with the generic lifecycle agent."""
    response = client.post(
        "/agents/advanced/generic-lifecycle",
        json={"message": "Echo 'Hello World'"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Echo: Hello World"

def test_generic_lifecycle_agent_math_add_tool():
    """Test the math addition tool integration with the generic lifecycle agent."""
    response = client.post(
        "/agents/advanced/generic-lifecycle",
        json={"message": "Add 2 and 3"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "5" in data["response"], f"Expected sum result in response, got {data['response']}"

def test_generic_lifecycle_agent_math_multiply_tool():
    """Test the math multiplication tool integration with the generic lifecycle agent."""
    response = client.post(
        "/agents/advanced/generic-lifecycle",
        json={"message": "Multiply 4 by 5"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "20" in data["response"], f"Expected multiplication result in response, got {data['response']}"

def test_generic_lifecycle_agent_datetime_tool():
    """Test the datetime tool integration with the generic lifecycle agent."""
    response = client.post(
        "/agents/advanced/generic-lifecycle",
        json={"message": "What's the current UTC time?"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "T" in data["response"], "Expected ISO datetime format in response"

def test_generic_lifecycle_agent_string_uppercase_tool():
    """Test the string uppercase tool integration with the generic lifecycle agent."""
    response = client.post(
        "/agents/advanced/generic-lifecycle",
        json={"message": "Convert 'hello' to uppercase"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "HELLO" in data["response"], f"Expected uppercase 'HELLO', got {data['response']}"

def test_generic_lifecycle_agent_data_fetch_tool():
    """Test the data fetch tool integration with the generic lifecycle agent."""
    response = client.post(
        "/agents/advanced/generic-lifecycle",
        json={"message": "Fetch MOCK data from 'source1'"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "sample data" in data["response"], f"Expected fetched data in response, got {data['response']}"

def test_generic_lifecycle_agent_invalid_api_key():
    """Test the generic lifecycle agent with an invalid API key."""
    response = client.post(
        "/agents/advanced/generic-lifecycle",
        json={"message": "Echo 'Hello World'"},
        headers={"X-API-KEY": "invalid_key"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_generic_lifecycle_agent_missing_message():
    """Test the generic lifecycle agent with a missing message."""
    response = client.post(
        "/agents/advanced/generic-lifecycle",
        json={},
        headers=headers
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data