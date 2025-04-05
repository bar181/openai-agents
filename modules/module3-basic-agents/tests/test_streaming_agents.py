from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY
import json

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

# ----- Streaming Items Agent Tests -----
def test_initialize_streaming_items_agent():
    response = client.post("/agents/streaming/items/initialize", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "initialized"
    assert data.get("name") == "ItemStreamer"

def test_execute_streaming_items_agent():
    response = client.post("/agents/streaming/items/execute?category=jokes&count=3", headers=headers)
    assert response.status_code == 200
    # Check content-type for streaming
    assert response.headers["content-type"] == "application/x-ndjson"
    events = [json.loads(line) for line in response.iter_lines() if line]
    complete_events = [event for event in events if event.get("type") == "complete"]
    assert len(complete_events) > 0

def test_terminate_streaming_items_agent():
    response = client.post("/agents/streaming/items/terminate", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "terminated"
    assert data.get("name") == "ItemStreamer"

# ----- Streaming Text Agent Tests -----
def test_initialize_streaming_text_agent():
    response = client.post("/agents/streaming/text/initialize", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "initialized"
    assert data.get("name") == "TextStreamer"

def test_execute_streaming_text_agent():
    response = client.post("/agents/streaming/text/execute?input=Tell me a story about space.", headers=headers)
    assert response.status_code == 200
    # Expect plain text streaming response, allowing for charset in header.
    assert response.headers["content-type"].startswith("text/plain")
    text_chunks = [chunk for chunk in response.iter_lines() if chunk]
    # Check that some text is returned (non-empty chunks)
    assert any(len(chunk.strip()) > 0 for chunk in text_chunks)

def test_terminate_streaming_text_agent():
    response = client.post("/agents/streaming/text/terminate", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "terminated"
    assert data.get("name") == "TextStreamer"
