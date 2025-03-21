"""
Test module for the streaming text agent functionality.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

def test_stream_text_endpoint():
    """Test the text streaming endpoint."""
    response = client.post(
        "/agents/basic/stream-text",
        json={"prompt": "Tell me a short story."},
        headers=headers
    )
    assert response.status_code == 200
    
    # Check that we receive a streaming response
    content = response.content.decode("utf-8")
    assert len(content) > 0
    
    # The response should be a coherent text
    assert isinstance(content, str)
    assert len(content.strip()) > 0

def test_stream_text_with_custom_instructions():
    """Test the text streaming endpoint with custom instructions."""
    response = client.post(
        "/agents/basic/stream-text",
        json={
            "prompt": "Tell me a joke.",
            "instructions": "You are a comedian who specializes in short, clean jokes."
        },
        headers=headers
    )
    assert response.status_code == 200
    
    # Check that we receive a streaming response
    content = response.content.decode("utf-8")
    assert len(content) > 0
    
    # The response should contain a joke
    assert isinstance(content, str)
    assert len(content.strip()) > 0

def test_stream_text_invalid_api_key():
    """Test the text streaming endpoint with an invalid API key."""
    response = client.post(
        "/agents/basic/stream-text",
        json={"prompt": "Tell me a short story."},
        headers={"X-API-KEY": "invalid_key"}
    )
    assert response.status_code == 401
    
    # Check that we receive an error message
    data = response.json()
    assert "detail" in data
    assert "Unauthorized" in data["detail"]

def test_stream_text_missing_prompt():
    """Test the text streaming endpoint with a missing prompt."""
    response = client.post(
        "/agents/basic/stream-text",
        json={},
        headers=headers
    )
    assert response.status_code == 422
    
    # Check that we receive a validation error
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0
    assert "prompt" in str(data["detail"])

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])