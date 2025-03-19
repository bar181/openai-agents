# File: root/modules/module2-story-agent/tests/test_mod2_story.py
# Run in module folder: python -m pytest tests/test_mod2_story.py

from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY  # API_KEY is loaded from .env via config.py

client = TestClient(app)

def test_story_telling_agent():
    """
    Test the Story Telling Agent endpoint.
    This endpoint builds on the deterministic agent from Module 1 to generate a story outline.
    It should return an outline that contains the provided topic, checked in a case-insensitive manner.
    """
    topic = "A brave knight"
    response = client.post(
        "/agents/story/story",
        json={"topic": topic},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "outline" in data, "Response JSON must contain the key 'outline'"
    # Perform a case-insensitive check on the topic in the outline.
    assert topic.lower() in data["outline"].lower(), (
        f"Expected the outline to include '{topic}', got: {data['outline']}"
    )
