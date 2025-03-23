## 1. `docs/guidelines.md`

# Guidelines for Module 454

This document outlines module 4 coding and design standards.

---

## 1. Naming and Project Structure

- Place LLM provider agents under `app/agents/llm_providers/`.
- Create a single FastAPI router in `app/routers/llm_router.py`.
- Each provider agent should implement a consistent interface, such as:
  ```python
  class BaseLLMAgent:
      def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
          raise NotImplementedError("Implement prompt processing.")
  ```
- Example filenames:
  ```
  gemini_agent.py
  requestry_agent.py
  openrouter_agent.py
  openai_agent.py
  recommender_agent.py
  ```

---

## 2. Endpoint Conventions

Use these endpoint patterns in `llm_router.py`:

1. **POST** `/agents/llm-providers/openai`
2. **POST** `/agents/llm-providers/gemini`
3. **POST** `/agents/llm-providers/requestry`
4. **POST** `/agents/llm-providers/openrouter`
5. **POST** `/agents/llm-providers/recommend-model`

Keep request/response schemas consistent:
- Request:
  ```json
  {
    "prompt": "user text",
    "model": "gpt-o3-mini",
    "max_tokens": 100,
    "temperature": 0.7
  }
  ```
- Response:
  ```json
  {
    "status": "success",
    "message": "...",
    "model": "gpt-o3-mini",
    "usage": { "prompt_tokens": 123, "completion_tokens": 222 }
  }
  ```

---

## 3. Testing Conventions

- Each provider has a test file in `tests/`, for example:
  - `test_openai_agent.py`
  - `test_gemini_agent.py`
  - `test_requestry_agent.py`
  - `test_openrouter_agent.py`
  - `test_recommender_agent.py`
- Write tests **before** implementing each provider:
  1. Define expected input/output
  2. Mock external calls if needed
  3. Ensure coverage for missing model or invalid parameters

---

## 4. Logging and Error Handling

- Use Python’s logging module with consistent patterns:
  ```python
  import logging
  logger = logging.getLogger(__name__)
  logger.info("Processing prompt...")
  ```
- For API errors, return JSON with `status=error`:
  ```json
  {
    "status": "error",
    "message": "API key missing",
    "model": "unknown"
  }
  ```
- Catch provider-specific exceptions (e.g., rate limit or invalid model name).

---

## 5. Implementation Flow

1. **Create tests**: For each agent or new feature, add test files.
2. **Implement or refactor**: Code agent logic, environment usage, router endpoints.
3. **Update docs**:
   - `docs/implementation_process.md`: short summary of changes
   - `README.md`: usage example or new details
4. **Repeat**: Move on after passing tests.

---

## 6. Style Checks

- Follow PEP 8 format (e.g. `black` or `flake8`).
- Use type annotations for function signatures.
- Keep docstrings consistent: “Args: … Returns: … Raises: …” format.
- Maintain minimal usage of `the` and `its` in user-facing text.

---

## 7. Future Expansions

- Additional providers can follow this same structure.
- Agents can extend or implement `BaseLLMAgent`.
- Tests can be expanded for concurrency, streaming, or advanced prompts.

