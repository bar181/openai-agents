```markdown
# Module 4 – Phase 2: OpenAI Multi-Model Agent

**Objective**: Implement the **OpenAI** multi-model agent (`openai_agent.py`) with support for various model names, environment-based API keys, and consistent request/response formats. Create tests for correct functionality and integrate these changes into the FastAPI router.

---

## Overview

In Phase 2, focus is on:

1. **Implementing** the `openai_agent.py` file:
   - Use environment variables for the API key.
   - Accept user prompts, model selection, and optional `max_tokens` or `temperature`.
   - Return standardized JSON output (status, message, model, usage).
2. **Writing** real tests in `test_openai_agent.py`.
3. **Adding** a new endpoint in `llm_router.py` for `/agents/llm-providers/openai`.
4. **Updating** `docs/implementation_process.md` to reflect progress.

**Dependencies**: 
- Phase 1 folder structure must be complete.
- `.env` should have `OPENAI_API_KEY`.
- [Provider references](../../../../common/provider_references.md) and [Guidelines](./guidelines.md) may provide clarity including detailed code snippets and examples.

---

## Step-by-Step Guide

### Step 1: Write Tests First

Create or expand `test_openai_agent.py` with real test cases.  
Include checks for:
- Missing API key scenario.
- Valid model usage (e.g., `"gpt-o3-mini"`, `"gpt-4o"`).
- Basic success path: prompt returns expected response structure.

<details>
<summary><strong>Sample Test Code</strong></summary>

```python
# tests/test_openai_agent.py
import os
import pytest
import openai
from unittest.mock import patch
from app.agents.llm_providers.openai_agent import OpenAIAgent

@pytest.mark.asyncio
async def test_openai_agent_valid_prompt():
    os.environ["OPENAI_API_KEY"] = "test-key"
    
    agent = OpenAIAgent()
    # Mock openai.ChatCompletion.create to return a fake response
    with patch.object(openai.ChatCompletion, "create") as mock_create:
        mock_create.return_value = {
            "choices": [
                {
                    "message": {"content": "Test response from mock model."}
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }
        
        prompt_data = {
            "prompt": "Hello from tests.",
            "model": "gpt-o3-mini",
            "max_tokens": 50,
            "temperature": 0.5
        }
        result = agent.process_prompt(prompt_data)
        assert result["status"] == "success"
        assert "Test response from mock model." in result["message"]
        assert result["model"] == "gpt-o3-mini"
        assert result["usage"]["prompt_tokens"] == 10

@pytest.mark.asyncio
async def test_openai_agent_missing_api_key():
    # Clear environment to simulate no API key
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    agent = OpenAIAgent()
    prompt_data = {"prompt": "No API key here", "model": "gpt-o3-mini"}
    result = agent.process_prompt(prompt_data)
    assert result["status"] == "error"
    assert "missing" in result["message"].lower()
```
</details>

**Explanation**:
- First test: Mocks OpenAI’s `ChatCompletion.create` and checks agent’s response structure.
- Second test: Simulates missing API key, ensuring an error is returned.

**Run**:
```bash
pytest tests/test_openai_agent.py
```
Expect failures initially, since `OpenAIAgent` is not yet implemented.

---

### Step 2: Implement `openai_agent.py`

Create `openai_agent.py` inside `app/agents/llm_providers/`.  
Goal: 
- Load `OPENAI_API_KEY` from environment.
- Provide `process_prompt(...)` method that calls `openai.ChatCompletion.create`.
- Return JSON with keys `status`, `message`, `model`, `usage`.

<details>
<summary><strong>Example Implementation</strong></summary>

```python
# app/agents/llm_providers/openai_agent.py
import os
import openai
from typing import Any, Dict

class OpenAIAgent:
    """
    OpenAIAgent handles calls to the OpenAI ChatCompletion endpoint,
    supports multiple model names, returns usage info, and handles missing keys.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.default_model = "gpt-o3-mini"

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt using OpenAI's ChatCompletion API.

        Args:
            prompt_data: Dictionary with:
                - prompt (str): user text
                - model (str): optional model name
                - max_tokens (int): optional max token count
                - temperature (float): optional temperature

        Returns:
            A dictionary with status, message, model, usage (or error info).
        """
        # Check for API key
        if not self.api_key:
            return {
                "status": "error",
                "message": "OPENAI_API_KEY missing in environment.",
                "model": "unknown"
            }

        openai.api_key = self.api_key

        # Extract prompt parameters
        prompt = prompt_data.get("prompt", "")
        model_name = prompt_data.get("model", self.default_model)
        max_tokens = prompt_data.get("max_tokens", 100)
        temperature = prompt_data.get("temperature", 0.7)

        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )

            # Extract completion text
            completion_text = response["choices"][0]["message"]["content"]

            # Extract usage (prompt_tokens, completion_tokens, total_tokens)
            usage_data = response.get("usage", {})
            usage = {
                "prompt_tokens": usage_data.get("prompt_tokens", 0),
                "completion_tokens": usage_data.get("completion_tokens", 0),
                "total_tokens": usage_data.get("total_tokens", 0)
            }

            return {
                "status": "success",
                "message": completion_text,
                "model": model_name,
                "usage": usage
            }

        except openai.error.OpenAIError as e:
            return {
                "status": "error",
                "message": f"OpenAI API error: {str(e)}",
                "model": model_name
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "model": model_name
            }
```
</details>

**Explanation**:
- **`self.api_key`** loads from environment.
- **`process_prompt`** gathers user input, calls `openai.ChatCompletion.create`.
- Catches `OpenAIError` for API issues and `Exception` for other failures.

Re-run tests:
```bash
pytest tests/test_openai_agent.py
```
They should pass now, if logic matches the test expectations.

---

### Step 3: Add Endpoint in `llm_router.py`

Open `app/routers/llm_router.py` and define a POST handler for `/openai`.

<details>
<summary><strong>Example Router Update</strong></summary>

```python
# app/routers/llm_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.llm_providers.openai_agent import OpenAIAgent

router = APIRouter()

class OpenAIRequest(BaseModel):
    prompt: str
    model: str = "gpt-o3-mini"
    max_tokens: int = 100
    temperature: float = 0.7

@router.post("/openai")
async def openai_endpoint(request_data: OpenAIRequest):
    agent = OpenAIAgent()
    result = agent.process_prompt(request_data.dict())

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result
```
</details>

**Optional**: `OpenAIRequest` uses Pydantic for request validation.  
Use `HTTPException` to indicate errors.  
Once set, client requests to `/agents/llm-providers/openai` with JSON body:
```json
{
  "prompt": "Say hi",
  "model": "gpt-o3-mini",
  "max_tokens": 50,
  "temperature": 0.2
}
```
should yield a structured response.

---

### Step 4: Update `docs/implementation_process.md`

Open `docs/implementation_process.md` and record Phase 2 progress:
```markdown
## Phase 2 Updates
- Created `openai_agent.py` with multi-model support.
- Added tests in `test_openai_agent.py`.
- Implemented `/openai` endpoint in `llm_router.py`.
- Verified tests passing, no major refactor needed at this time.
```

---

## Completion & Next Steps

You have now:
1. Written real tests for the OpenAI agent.
2. Implemented the `openai_agent.py` logic.
3. Created a FastAPI route in `llm_router.py`.

### Next Step: Phase 3

Move on to **Gemini, Requestry, and OpenRouter**. Each will have a similar pattern of:
1. Write or expand tests.
2. Implement `process_prompt`.
3. Add endpoints.
4. Update logs/docs.

**Congratulations** on finishing Phase 2
