# tests/test_hello_world.py
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY  # API_KEY is loaded from .env via config.py

client = TestClient(app)

def test_hello_world():
    # Test the hello endpoint with the API key retrieved from the configuration.
    response = client.post(
        "/agent/hello",
        json={"message": "Hi from Bradley"},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Bradley" in data["response"]
    
    