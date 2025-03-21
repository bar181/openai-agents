"""
Test module for the Multi-Tool Agent functionality.

This module contains tests for the Multi-Tool Agent, which is an advanced agent
that integrates with multiple tool categories to perform complex operations.
"""

from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

def test_multi_tool_agent_json_processing():
    """Test JSON validation and transformation capabilities."""
    response = client.post(
        "/agents/advanced/multi-tool",
        json={"message": "Validate and transform JSON: {'name': 'test', 'value': 123}"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], dict)
    assert "json_validation" in str(data["response"]) or "json_transform" in str(data["response"])

def test_multi_tool_agent_text_analysis():
    """Test sentiment analysis and entity extraction."""
    response = client.post(
        "/agents/advanced/multi-tool",
        json={"message": "Analyze sentiment of 'Great product!' and extract entities"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], dict)
    assert "sentiment" in str(data["response"]) or "entities" in str(data["response"])

def test_multi_tool_agent_data_visualization():
    """Test mock visualization generation."""
    response = client.post(
        "/agents/advanced/multi-tool",
        json={"message": "Create visualization for data: [1, 2, 3, 4, 5]"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], dict)
    assert "visualization" in str(data["response"]) or "chart" in str(data["response"])

def test_multi_tool_agent_multi_step_workflow():
    """Test complex workflow with multiple tool interactions."""
    response = client.post(
        "/agents/advanced/multi-tool",
        json={
            "message": "Fetch data from 'source1', analyze sentiment, store results, and create visualization"
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], dict)
    # Check for evidence of multiple tool usage
    response_str = str(data["response"]).lower()
    assert any(term in response_str for term in ["fetch", "data", "source1"])
    assert any(term in response_str for term in ["sentiment", "analysis", "analyze"])
    assert any(term in response_str for term in ["store", "database", "saved"])
    assert any(term in response_str for term in ["visualization", "chart", "graph"])

def test_multi_tool_agent_with_context():
    """Test context preservation across operations."""
    response = client.post(
        "/agents/advanced/multi-tool",
        json={
            "message": "Use the session_id in context to process data",
            "context": {"session_id": "test123"}
        },
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "context" in data
    assert "session_id" in data["context"]
    assert data["context"]["session_id"] == "test123"
    assert "response" in data
    assert "test123" in str(data["response"])

def test_multi_tool_agent_database_operations():
    """Test database operations with the multi-tool agent."""
    # First store data
    response = client.post(
        "/agents/advanced/multi-tool",
        json={"message": "Store data with key 'test_key' and value 'test_value'"},
        headers=headers
    )
    assert response.status_code == 200
    
    # Then retrieve the data
    response = client.post(
        "/agents/advanced/multi-tool",
        json={"message": "Retrieve data with key 'test_key'"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "test_value" in str(data["response"])

def test_multi_tool_agent_csv_processing():
    """Test CSV processing capabilities."""
    csv_data = "name,age,city\nJohn,30,New York\nJane,25,San Francisco"
    response = client.post(
        "/agents/advanced/multi-tool",
        json={"message": f"Parse this CSV data: {csv_data}"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    response_str = str(data["response"]).lower()
    assert "john" in response_str and "jane" in response_str
    assert "new york" in response_str and "san francisco" in response_str

def test_multi_tool_agent_invalid_api_key():
    """Test the multi-tool agent with an invalid API key."""
    response = client.post(
        "/agents/advanced/multi-tool",
        json={"message": "Echo 'Hello World'"},
        headers={"X-API-KEY": "invalid_key"}
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

def test_multi_tool_agent_missing_message():
    """Test the multi-tool agent with a missing message."""
    response = client.post(
        "/agents/advanced/multi-tool",
        json={},
        headers=headers
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data