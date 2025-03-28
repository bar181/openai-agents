# File: root/modules/module2-story-agent/tests/test_mod2_story.py
# Run in module folder: python -m pytest tests/test_mod2_story.py


import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY  # API_KEY is loaded from .env via config.py

client = TestClient(app)

# Save the original OpenAI API key before running any tests
original_openai_api_key = os.environ.get("OPENAI_API_KEY")

@pytest.fixture(autouse=True)
def restore_openai_api_key():
    """Fixture to restore the original OpenAI API key after each test."""
    # Setup - restore the original API key if it exists
    if original_openai_api_key:
        os.environ["OPENAI_API_KEY"] = original_openai_api_key
    
    # Let the test run
    yield
    
    # Teardown - restore the original API key again
    if original_openai_api_key:
        os.environ["OPENAI_API_KEY"] = original_openai_api_key
    elif "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

def test_story_telling_agent_baseline():
    """
    Test the baseline story agent endpoint.
    This endpoint builds on the deterministic agent from Module 1 to generate a story outline.
    It should return an outline that contains the provided topic, checked in a case-insensitive manner.
    """
    topic = "A brave knight"
    response = client.post(
        "/agents/story/baseline",
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

def test_story_telling_agent_custom():
    """
    Test the custom story agent endpoint.
    This endpoint uses enhanced narrative logic to generate a creative story outline.
    It should return an outline that contains the provided topic, checked in a case-insensitive manner.
    """
    topic = "A mysterious adventure"
    simple_topic = "mysterious"
    response = client.post(
        "/agents/story/custom",
        json={"topic": topic},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "outline" in data, "Response JSON must contain the key 'outline'"
    # Perform a case-insensitive check on the simple topic in the outline.
    assert simple_topic.lower() in data["outline"].lower(), (
        f"Expected the outline to include '{simple_topic}', got: {data['outline']}"
    )


def test_story_telling_agent_advanced():
    """
    Test the advanced story agent endpoint.
    This endpoint should generate a complete story (full narrative) that includes the provided topic (case-insensitive).
    """
    topic = "A futuristic odyssey"
    simple_topic = "odyssey"
    response = client.post(
        "/agents/story/advanced",
        json={"topic": topic},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "outline" in data, "Response JSON must contain the key 'outline'"
    # Check that the generated story contains the simple topic (case-insensitive).
    assert simple_topic.lower() in data["outline"].lower(), (
        f"Expected the generated story to include '{simple_topic}', got: {data['outline']}"
    )