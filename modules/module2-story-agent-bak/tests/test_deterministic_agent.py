from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)

def test_deterministic_agent():
    """Tests the deterministic agent with a simple input."""
    response = client.post(
        "/agent/deterministic",
        json={"message": "Write a story about a cat named Whiskers."},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    # Print the first 25 characters of the response
    print("Response (first 25 chars):", data["response"][:25])
    
    # Verify the response contains the expected content
    assert "Whiskers" in data["response"]
    assert "Adventure" in data["response"]
    assert "Once upon a time" in data["response"]

