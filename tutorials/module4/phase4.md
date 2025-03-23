```markdown
# Module 4 – Phase 4: Model Recommender

**Objective:**  
Implement a recommender agent that selects an appropriate LLM provider and model based on a simple input structure. The agent should accept a JSON payload (e.g., with "task_type" and "prompt_length") and return a recommended provider and model. Optionally, you may extend the logic to use an LLM for decision-making; for now, a simple lookup is sufficient.

---

## Step 1: Create `recommender_agent.py`

Create the file `app/agents/llm_providers/recommender_agent.py` with the following implementation:

<details>
<summary><strong>Sample Implementation</strong></summary>

```python
# app/agents/llm_providers/recommender_agent.py
from typing import Any, Dict

class RecommenderAgent:
    """
    Recommender Agent

    Purpose:
    - Accepts a task specification and prompt length.
    - Returns a recommended provider and model.
    
    Expected Input:
    {
      "task_type": "reasoning",
      "prompt_length": 200
    }
    
    Expected Output:
    {
      "status": "success",
      "recommended_provider": "openai",
      "model": "gpt-o3-mini"
    }
    """

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        # Extract values with defaults
        task_type = prompt_data.get("task_type", "").lower()
        prompt_length = prompt_data.get("prompt_length", 100)
        
        # Simple decision logic based on task type and prompt length.
        if task_type == "reasoning":
            recommended_provider = "openai"
            model = "gpt-o3-mini"
        elif task_type == "conversation":
            recommended_provider = "openai"
            model = "gpt-4o-mini"
        else:
            # Default recommendation if no clear task type is provided.
            recommended_provider = "openai"
            model = "gpt-o3-mini"
        
        return {
            "status": "success",
            "recommended_provider": recommended_provider,
            "model": model
        }
```
</details>

**Explanation:**  
- The agent extracts the `task_type` and `prompt_length` (with a default of 100 if not provided).
- It then uses simple conditional logic to recommend a provider and model.
- The output is a consistent JSON structure with keys: `status`, `recommended_provider`, and `model`.

---

## Step 2: Create Tests in `test_recommender_agent.py`

Create the file `tests/test_recommender_agent.py` with tests covering different scenarios.

<details>
<summary><strong>Sample Test Code</strong></summary>

```python
# tests/test_recommender_agent.py
import pytest
from app.agents.llm_providers.recommender_agent import RecommenderAgent

@pytest.mark.asyncio
async def test_recommender_reasoning():
    agent = RecommenderAgent()
    input_data = {
        "task_type": "reasoning",
        "prompt_length": 200
    }
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    assert result["recommended_provider"] == "openai"
    assert result["model"] == "gpt-o3-mini"

@pytest.mark.asyncio
async def test_recommender_conversation():
    agent = RecommenderAgent()
    input_data = {
        "task_type": "conversation",
        "prompt_length": 50
    }
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    assert result["recommended_provider"] == "openai"
    assert result["model"] == "gpt-4o-mini"

@pytest.mark.asyncio
async def test_recommender_default():
    agent = RecommenderAgent()
    input_data = {}  # No task_type provided
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    # Default fallback as defined in the agent logic.
    assert result["recommended_provider"] == "openai"
    assert result["model"] == "gpt-o3-mini"
```
</details>

**Explanation:**  
- The tests verify that the recommender returns the expected provider and model for a "reasoning" task, a "conversation" task, and for unspecified input.
- Running these tests with `pytest` should validate that the agent behaves as expected.

---

## Step 3: Add Endpoint in `llm_router.py`

Extend `app/routers/llm_router.py` to include an endpoint for the recommender agent.

<details>
<summary><strong>Sample Endpoint Code</strong></summary>

```python
# app/routers/llm_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.llm_providers.recommender_agent import RecommenderAgent

router = APIRouter()

class RecommenderRequest(BaseModel):
    task_type: str
    prompt_length: int

@router.post("/recommend-model")
async def recommend_model_endpoint(request_data: RecommenderRequest):
    agent = RecommenderAgent()
    result = agent.process_prompt(request_data.dict())
    if result.get("status") != "success":
        raise HTTPException(status_code=400, detail=result.get("message", "Error in recommendation"))
    return result
```
</details>

**Explanation:**  
- A new endpoint `/agents/llm-providers/recommend-model` accepts a JSON payload conforming to `RecommenderRequest`.
- It calls the recommender agent's `process_prompt` method and returns the result.
- Errors are handled with an `HTTPException`.

---

## Step 4: Refactor and Documentation Updates

- **Refactor:**  
  - Review the recommender agent logic and tests.  
  - Ensure the output format is consistent with other agents (e.g., similar structure to the OpenAI and Gemini agents).

- **Documentation:**  
  - Update `docs/guidelines.md` to include the recommender endpoint.
  - Add a note in `docs/implementation_process.md` indicating that Phase 4 is complete.
  - Cross-reference `/common/provider_references.md` if needed to clarify provider options.

---

## Final Checklist for Phase 4

- [ ] **Recommender Agent Implementation:**
  - `recommender_agent.py` correctly processes input and returns recommendations.
- [ ] **Tests:**
  - `tests/test_recommender_agent.py` covers multiple scenarios and passes.
- [ ] **Endpoint:**
  - `/agents/llm-providers/recommend-model` is available and responds as expected.
- [ ] **Refactoring:**
  - Code is consistent with other agent implementations.
- [ ] **Documentation:**
  - Relevant docs and process logs are updated.

---

**Exit Criteria:**  
- The recommender agent consistently returns plausible recommendations.
- The response format is validated by tests.
- Endpoint `/agents/llm-providers/recommend-model` works correctly.

---

**Next Steps:**  
After Phase 4, review and merge changes, then proceed to Phase 5 (Documentation & Final Checks) to finalize the module.
```