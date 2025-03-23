# Module 1 - Phase 4: Integration and Testing

In Phase 4, you will integrate your agent and API router into the complete FastAPI application and verify everything functions as expected using structured tests.

---

## Step 1: Integration Verification

Before testing, confirm your integration is properly set up:

### 1.1 Verify `app/main.py`

Ensure your main application file (`app/main.py`) correctly includes the router:

```python
from fastapi import FastAPI
from app.routers import hello_world

app = FastAPI()

app.include_router(hello_world.router, prefix="/agent")

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
```

---

## Step 2: Writing Tests

Create or verify `tests/test_hello_world.py`. Write integration tests using FastAPI’s `TestClient`:

```python
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)

def test_hello_world():
    response = client.post(
        "/agent/hello",
        json={"message": "Hi from Bradley"},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Hello, world!" in data["response"]
```

- **Explanation:**
  - Confirms that the endpoint returns a successful status code.
  - Ensures the agent's response matches expectations.

---

## Step 3: Running Tests

Execute your tests to verify proper setup and functionality:

```bash
python -m pytest tests/
```

You should see output similar to:
```
================== 1 passed in 0.32s ==================
```

- **If tests fail:** Review the error messages, correct any issues, and rerun.

---

## Step 4: Debugging Common Issues

### Common Problems:
- **401 Unauthorized Error:** Ensure your API key (`API_KEY`) is correctly set in `.env` and matches the header sent by tests.
- **500 Internal Server Error:** Check agent logic or endpoint handling for exceptions.

Use print statements or logging within your endpoint and agent logic to assist debugging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

---

## Step 5: Continuous Integration Recommendations

Consider integrating automated testing into your development workflow:
- Use GitHub Actions or similar CI tools to automatically run tests on code changes.
- Regularly update tests to cover new functionality.

---

## Completion of Phase 4

By the end of this phase, you will have:

- Confirmed proper integration of your agent and API.
- Written and executed comprehensive integration tests.
- Set up a basic debugging and continuous integration strategy.

You're now prepared to finalize your work in **Phase 5: Documentation and Final Review**.