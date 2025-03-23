```markdown
# Module 4 – Phase 1: Environment & Setup

Welcome to **Phase 1** of Module 4. This document guides you through creating the environment, setting up the file structure, and drafting basic tests for the new LLM providers.

---

## Overview

**Objective:** Create the foundation for Module 4. This involves:

1. Copying Module 3 files (ensuring continuity).
2. Setting up the folder structure for Module 4.
3. Initializing environment variables for multiple providers.
4. Adding placeholder test files for each planned agent (OpenAI, Gemini, Requestry, OpenRouter, Recommender).
5. Verifying that your logging and config basics work before moving on.

In each step, we will:
- Write a test file (or skeleton).
- Implement minimal code or folder structure to pass the test (if relevant).
- Verify tests run (they might just be placeholders at this stage).
- Update `docs/implementation_process.md`.

---

## Step-by-Step

### Step 1: Create the Project Structure

**Goal:** Arrange directories for `/module4-llm-providers/`.

#### 1A. Directory Layout

We place code inside `app/` and tests in `tests/`:

```
/workspaces/openai-agents/modules/module4-llm-providers/
├── app/
│   ├── agents/
│   │   └── llm_providers/
│   │       ├── __init__.py
│   │       ├── openai_agent.py              # to be implemented Phase 2
│   │       ├── gemini_agent.py              # Phase 3
│   │       ├── requestry_agent.py           # Phase 3
│   │       ├── openrouter_agent.py          # Phase 3
│   │       └── recommender_agent.py         # Phase 4
│   ├── routers/
│   │   └── llm_router.py                    # Main router for LLM providers
│   ├── config.py                            # Optional shared config
│   ├── dependencies.py                      # Reusable dependencies
│   └── main.py                              # FastAPI entry point if needed
├── docs/
│   ├── phase1.md                            # THIS FILE
│   ├── phase2.md                            # (to be created)
│   ├── phase3.md                            # ...
│   ├── phase4.md
│   ├── phase5.md
│   ├── guidelines.md                        # Provided already
│   └── implementation_process.md            # Will track progress
├── tests/
│   ├── test_openai_agent.py
│   ├── test_gemini_agent.py
│   ├── test_requestry_agent.py
│   ├── test_openrouter_agent.py
│   └── test_recommender_agent.py
└── README.md
```

**Implementation Notes:**
- In this phase, `openai_agent.py`, etc. might just be empty files or minimal placeholders.
- `llm_router.py` may also be empty (or an empty FastAPI router).
- Ensure each folder has an `__init__.py` to make it a Python package.

**Update**: Add or edit `docs/implementation_process.md`:
```markdown
## Phase 1 Updates
- Created the `module4-llm-providers` folder structure.
- Added empty agent files in `app/agents/llm_providers`.
- Added placeholders in `tests/`.
```

---

### Step 2: Environment Variables Setup

We expect these variables in `.env`:
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `REQUESTRY_API_KEY`
- `OPENROUTER_API_KEY`

They might look like this:
```
OPENAI_API_KEY=sk-123abc
GEMINI_API_KEY=gemini-xyz123
REQUESTRY_API_KEY=req-111111
OPENROUTER_API_KEY=openr-222222
```

**Implementation Notes:**
- No real code needed yet, but confirm your `.env` file is not committed to version control.
- Optionally, you can create a `config.py` or `dependencies.py` to load and validate these.

**Quick Pseudocode** in `app/config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
REQUESTRY_KEY = os.getenv("REQUESTRY_API_KEY", "")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")

if not OPENAI_KEY:
    # We might warn or handle missing keys
    pass
```

**Update**: `docs/implementation_process.md`:
```markdown
## Phase 1 Updates (continued)
- Created `.env` with API key placeholders.
- Implemented minimal `app/config.py` to load them.
```

---

### Step 3: Draft Tests

We now create basic test files in the `tests/` folder. At this stage, they can be skeletons. Remember [the testing guidelines](../../../../common/Tests.md) for naming and approach.

#### Example: `test_openai_agent.py`
```python
import pytest

@pytest.mark.asyncio
async def test_openai_agent_placeholder():
    # This is just a placeholder test.
    # In Phase 2, we'll implement real tests for openai_agent.py
    assert True
```

Similarly for each other test file:
- `test_gemini_agent.py`
- `test_requestry_agent.py`
- `test_openrouter_agent.py`
- `test_recommender_agent.py`

**Implementation Steps**:
1. Create these test files.
2. Run `pytest` to confirm they pass (they will if they’re just placeholders).

**Update**: `docs/implementation_process.md`:
```markdown
## Phase 1 Updates (continued)
- Added placeholder test files for OpenAI, Gemini, Requestry, OpenRouter, Recommender.
- Confirmed they pass with `pytest` as empty tests.
```

---

### Step 4: Basic Logging & Config Check

If desired, create a quick test in `test_openai_agent.py` to ensure logging is working:

```python
import logging

def test_basic_logging():
    logger = logging.getLogger(__name__)
    logger.info("Logging test: success")
    assert True
```

This is optional, but helps confirm your environment is ready.

---

### Step 5: Refine & Update Documentation

**Goal**: Make sure everything is consistent before finalizing this phase.

1. **Refactor**: If any directory name or agent file is spelled incorrectly, fix it now.
2. **Update**: 
   - `docs/implementation_process.md` with final notes.
   - Any changes in `docs/guidelines.md` if you want to reflect your new placeholders.
3. **Commit** your changes so this phase is complete.

---

## Sample Code Snippets

<details>
<summary><strong>Minimal main.py (Optional)</strong></summary>

```python
# app/main.py
import logging
from fastapi import FastAPI
from .routers.llm_router import router as llm_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(llm_router, prefix="/agents/llm-providers", tags=["LLM Providers"])
```
</details>

<details>
<summary><strong>Empty llm_router.py</strong></summary>

```python
# app/routers/llm_router.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/openai")
async def openai_endpoint():
    return {"status": "placeholder"}

@router.post("/gemini")
async def gemini_endpoint():
    return {"status": "placeholder"}

@router.post("/requestry")
async def requestry_endpoint():
    return {"status": "placeholder"}

@router.post("/openrouter")
async def openrouter_endpoint():
    return {"status": "placeholder"}

@router.post("/recommend-model")
async def recommend_model_endpoint():
    return {"status": "placeholder"}
```
</details>

---

## Completion & Next Steps

**Phase 1** completes when:
- Folder structure is ready.
- `.env` variables are set or placeholders exist.
- Minimal test files are added.
- Logging (optional check) is verified.

Next up: **Phase 2** – Implementing the **OpenAI multi-model agent** (`openai_agent.py`) and writing real tests in `test_openai_agent.py`.

```plaintext
Remember: 
- Update docs/implementation_process.md 
- Then proceed to Phase 2 
```

**Congratulations on completing Phase 1!**
```
