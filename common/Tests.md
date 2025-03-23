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

## 7. Testing LLM Provider Agents

Based on our experience with Module 4, here are additional guidelines for testing LLM provider agents:

### 7.1 Environment Variables and API Keys

- **Mock API Keys**: When testing agents that require API keys, use mock values in tests rather than real credentials.
- **Handle dotenv Loading**: Be aware that `load_dotenv()` might load API keys from `.env` files even when you've deleted them from the environment. Use patching to prevent this:
  ```python
  @pytest.mark.asyncio
  async def test_agent_init_missing_api_key():
      # Remove API key from environment
      if "PROVIDER_API_KEY" in os.environ:
          del os.environ["PROVIDER_API_KEY"]
      
      # Patch load_dotenv to prevent loading from .env file
      with patch("app.agents.provider_agent.load_dotenv", lambda: None):
          with pytest.raises(ValueError, match="PROVIDER_API_KEY is not set"):
              ProviderAgent()
  ```

### 7.2 Mocking External API Calls

- **Mock Response Objects**: Create comprehensive mock objects that mimic the structure of actual API responses.
- **Handle Complex Objects**: When mocking complex objects like OpenAI responses, ensure all required attributes and nested objects are properly mocked:
  ```python
  mock_message = MagicMock()
  mock_message.content = "Test response"
  mock_choice = MagicMock()
  mock_choice.message = mock_message
  mock_completion.choices = [mock_choice]
  ```

### 7.3 Error Handling

- **Test API Errors**: Ensure your agent properly handles API errors from the provider.
- **Test Missing Usage Data**: Some providers might not return usage statistics. Test that your agent handles missing or None values gracefully:
  ```python
  # Handle None usage
  if hasattr(response, 'usage') and response.usage is not None:
      usage = {
          "prompt_tokens": response.usage.prompt_tokens,
          "completion_tokens": response.usage.completion_tokens,
          "total_tokens": response.usage.total_tokens
      }
  else:
      usage = {
          "prompt_tokens": 0,
          "completion_tokens": 0,
          "total_tokens": 0,
          "note": "Token usage information not available"
      }
  ```

### 7.4 Model Validation

- **Test Model Fallbacks**: If your agent validates model names and falls back to defaults for invalid models, test this behavior.
- **Align Implementation with Tests**: Ensure your implementation's model validation behavior matches what the tests expect. Either:
  - Update tests to expect the fallback behavior, or
  - Update the implementation to match the test's expectations

### 7.5 Complex Exception Handling

- **Handle Complex Exceptions**: Some libraries have complex exception classes that require specific initialization. Consider using generic exceptions in tests:
  ```python
  # Instead of:
  mock_client.chat.completions.create.side_effect = openai.APIError("Test error")
  
  # Use:
  mock_client.chat.completions.create.side_effect = Exception("API error: Test error")
  ```

### 7.6 Managing Environment Variables Between Tests

- **Save and Restore Environment Variables**: When tests modify environment variables that other tests depend on, make sure to save and restore them:
  ```python
  # Save the original API key before running any tests
  original_api_key = os.environ.get("OPENAI_API_KEY")

  @pytest.fixture(autouse=True)
  def restore_api_key():
      """Fixture to restore the original API key after each test."""
      # Setup - restore the original API key if it exists
      if original_api_key:
          os.environ["OPENAI_API_KEY"] = original_api_key
      
      # Let the test run
      yield
      
      # Teardown - restore the original API key again
      if original_api_key:
          os.environ["OPENAI_API_KEY"] = original_api_key
      elif "OPENAI_API_KEY" in os.environ:
          del os.environ["OPENAI_API_KEY"]
  ```

- **Use pytest Fixtures**: Leverage pytest fixtures with `autouse=True` to automatically handle environment setup and teardown for each test.

- **Isolate Test Environments**: When possible, use separate test environments for different components to avoid interference.

---

By following these guidelines, you'll establish a robust testing framework that contributes to the overall quality and reliability of the FastAPI Agent System.