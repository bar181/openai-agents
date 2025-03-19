```markdown
# Testing Guidelines for the FastAPI Agent System

This document outlines the testing standards and practices for the monorepo. It covers how to write, organize, and run tests to ensure that each agent and API endpoint works as expected. Following these guidelines helps maintain code quality and reliability throughout the course.

---

## 1. Overview

- **Objective**: Ensure that each module and its components (agents, routers, etc.) perform as intended.
- **Scope**: Unit tests should cover individual agent functionality, API endpoints, configuration loading, and dependency validations.
- **Tools**: Use `pytest` and `pytest-asyncio` for asynchronous tests and FastAPI's `TestClient` for endpoint testing.

---

## 2. Test Structure

- **Directory**: Place test files in a dedicated `tests/` folder within each module.
- **File Naming**: Follow a consistent naming convention, e.g., `test_<component>.py`.
- **Organization**: Group tests by feature or module. For example, tests for the Hello World agent should reside in `tests/test_hello_world.py`.

---

## 3. Sample Test: Hello World Agent

Below is an example test file (`tests/test_hello_world.py`) for the Hello World agent:

```python
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
```

**Explanation:**
- **TestClient**: Utilized to simulate HTTP requests to the FastAPI app.
- **Endpoint Testing**: Verifies that the `/agent/hello` endpoint returns a 200 status code and the response contains the expected content.
- **Configuration Check**: Uses the API key from `app/config.py` to authenticate the request.

---

## 4. Best Practices for Testing

- **Isolate Tests**: Ensure that tests are independent. Avoid shared state between tests.
- **Clear Assertions**: Write precise assertions to verify the expected outcomes.
- **Error Handling**: Test error responses (e.g., incorrect API keys) to confirm that the system handles errors gracefully.
- **Coverage**: Aim for high test coverage, including both successful scenarios and edge cases.
- **Continuous Integration**: Integrate tests into your CI/CD pipeline to run automatically on changes.

---

## 5. Running Tests

- **Command**: Use `pytest` to run all tests.
  ```bash
  python -m pytest
  ```
- **Async Tests**: When testing asynchronous endpoints, leverage `pytest-asyncio` for proper execution.

---

## 6. Documentation and Maintenance

- **Keep Tests Updated**: As you modify the agents and API endpoints, update your tests accordingly.
- **Review Regularly**: Periodically review test cases to ensure they continue to reflect the intended functionality.
- **Documentation**: Maintain this `tests.md` file in the `/common` directory to serve as a reference for developers and learners.

---

By following these guidelines, you'll establish a robust testing framework that contributes to the overall quality and reliability of the FastAPI Agent System.
```