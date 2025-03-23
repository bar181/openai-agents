"""
Test module for the streaming items agent functionality.
"""

import pytest
import json
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

def test_stream_items_endpoint():
    """Test the items streaming endpoint."""
    response = client.post(
        "/agents/basic/stream-items",
        json={"category": "jokes"},
        headers=headers
    )
    assert response.status_code == 200
    
    # Parse the streaming response as JSON lines
    events = [json.loads(line) for line in response.content.decode("utf-8").strip().split("\n") if line]
    
    # Check that we have events
    assert len(events) > 0
    
    # Verify the structure of events
    status_events = [e for e in events if e["type"] == "status"]
    count_events = [e for e in events if e["type"] == "count"]
    item_events = [e for e in events if e["type"] == "item"]
    complete_events = [e for e in events if e["type"] == "complete"]
    
    # We should have at least one status event, one count event, one item event, and one complete event
    assert len(status_events) > 0
    assert len(count_events) > 0
    assert len(item_events) > 0
    assert len(complete_events) > 0
    
    # The count event should have a count field
    assert "count" in count_events[0]
    assert isinstance(count_events[0]["count"], int)
    
    # The item events should have index and content fields
    for item in item_events:
        assert "index" in item
        assert "content" in item
        assert isinstance(item["index"], int)
        assert isinstance(item["content"], str)
    
    # The complete event should have a message field
    assert "message" in complete_events[0]
    assert "Generated" in complete_events[0]["message"]

def test_stream_items_with_count():
    """Test the items streaming endpoint with a specified count."""
    count = 3
    response = client.post(
        "/agents/basic/stream-items",
        json={"category": "facts", "count": count},
        headers=headers
    )
    assert response.status_code == 200
    
    # Parse the streaming response as JSON lines
    events = [json.loads(line) for line in response.content.decode("utf-8").strip().split("\n") if line]
    
    # Check that we have events
    assert len(events) > 0
    
    # Verify the count event
    count_events = [e for e in events if e["type"] == "count"]
    assert len(count_events) > 0
    assert count_events[0]["count"] == count
    
    # Verify the number of item events
    item_events = [e for e in events if e["type"] == "item"]
    assert len(item_events) == count

def test_stream_items_with_custom_instructions():
    """Test the items streaming endpoint with custom instructions."""
    response = client.post(
        "/agents/basic/stream-items",
        json={
            "category": "animals",
            "count": 2,
            "instructions": "You are an expert zoologist. Generate interesting facts about animals."
        },
        headers=headers
    )
    assert response.status_code == 200
    
    # Parse the streaming response as JSON lines
    events = [json.loads(line) for line in response.content.decode("utf-8").strip().split("\n") if line]
    
    # Check that we have events
    assert len(events) > 0
    
    # Verify the item events
    item_events = [e for e in events if e["type"] == "item"]
    assert len(item_events) == 2
    
    # The items should be about animals
    for item in item_events:
        assert "content" in item
        assert isinstance(item["content"], str)

def test_stream_items_invalid_api_key():
    """Test the items streaming endpoint with an invalid API key."""
    response = client.post(
        "/agents/basic/stream-items",
        json={"category": "jokes"},
        headers={"X-API-KEY": "invalid_key"}
    )
    assert response.status_code == 401
    
    # Check that we receive an error message
    data = response.json()
    assert "detail" in data
    assert "Unauthorized" in data["detail"]

def test_stream_items_missing_category():
    """Test the items streaming endpoint with a missing category."""
    response = client.post(
        "/agents/basic/stream-items",
        json={},
        headers=headers
    )
    assert response.status_code == 422
    
    # Check that we receive a validation error
    data = response.json()
    assert "detail" in data
    assert len(data["detail"]) > 0
    assert "category" in str(data["detail"])

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])