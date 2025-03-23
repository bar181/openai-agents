Here's a detailed, clear, and comprehensive `phase1.md` that aligns with the overall structure of the **Module 5 – Orchestration** implementation. It includes clear instructions, pseudocode, helpful code snippets, and SDK references, structured for easy developer implementation:

Save this document as:

```
modules/module5-orchestration/docs/phase1.md
```

---

# Module 5 – Phase 1: Environment & Setup

Welcome to **Phase 1** of Module 5, focused on setting up the environment, folder structure, and basic placeholders for orchestration features (guardrails, handoffs, tracing, and advanced routing). This module is a continuation of Module 4, and existing files must remain unmodified.

---

## Objectives

By the end of this phase, you should have:

1. Verified that all Module 4 files and tests pass.
2. Created the new orchestration folder structure.
3. Set up basic placeholders for orchestration agents, routers, and tests.
4. Defined environment variables and configuration settings.
5. Ensured basic logging and configuration checks.

---

## Step-by-Step Implementation

### Step 1: Verify Existing Module 4

Before proceeding, ensure Module 4 is fully functional:

- Run all tests:
  ```bash
  pytest tests/
  ```
- Confirm all endpoints from Module 4 return successful responses.
- Do not modify any existing files during Module 5 implementation.

---

### Step 2: Create the Project Structure

In your existing `module5-orchestration` directory, add the following structure clearly separated from Module 4:

```plaintext
module5-orchestration/
├── app/
│   ├── agents/
│   │   └── orchestration/
│   │       ├── __init__.py
│   │       ├── input_guardrails.py      # Placeholder
│   │       ├── output_guardrails.py     # Placeholder
│   │       ├── handoff_agent.py         # Placeholder
│   │       └── trace_processor.py       # Placeholder
│   ├── routers/
│   │   └── orchestration_router.py      # Placeholder
│   └── config.py                        # Add orchestration configs here
├── tests/
│   └── test_orchestration.py            # Placeholder tests
└── docs/
    ├── phase1.md                        # This file
    ├── implementation_plan.md
    └── implementation_process.md
```

**Implementation Notes:**
- Create `__init__.py` files to enable Python package structure.
- Placeholder files can initially be empty or contain minimal structure.

---

### Step 3: Define Environment Variables

Add orchestration-specific environment variables to `.env`:

```env
# Orchestration-specific keys
TRACE_LOG_LEVEL=INFO
ORCHESTRATION_MODE=DEVELOPMENT
```

Update `app/config.py` to load these new variables clearly:

**`app/config.py`** snippet:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Existing keys from Module 4
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REQUESTRY_API_KEY = os.getenv("REQUESTRY_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# New orchestration-specific configs
TRACE_LOG_LEVEL = os.getenv("TRACE_LOG_LEVEL", "INFO")
ORCHESTRATION_MODE = os.getenv("ORCHESTRATION_MODE", "DEVELOPMENT")
```

---

### Step 4: Basic Placeholder Setup

Create basic placeholders for orchestration-related files:

#### Example: `input_guardrails.py` (empty placeholder)

```python
# app/agents/orchestration/input_guardrails.py

from agents import input_guardrail

@input_guardrail
def check_input_relevance(ctx, agent, input_data):
    # Placeholder function
    pass
```

#### Example: `output_guardrails.py` (empty placeholder)

```python
# app/agents/orchestration/output_guardrails.py

from agents import output_guardrail

@output_guardrail
def check_output_safety(ctx, agent, agent_output):
    # Placeholder function
    pass
```

#### Example: `handoff_agent.py` (empty placeholder)

```python
# app/agents/orchestration/handoff_agent.py

from agents import Agent, handoff

# Placeholder agent
class HandoffAgent(Agent):
    pass
```

#### Example: `trace_processor.py` (empty placeholder)

```python
# app/agents/orchestration/trace_processor.py

from agents.tracing import TraceProcessor

class CustomTraceProcessor(TraceProcessor):
    pass
```

#### Example: `orchestration_router.py` (basic router setup)

```python
# app/routers/orchestration_router.py

from fastapi import APIRouter

router = APIRouter()

@router.post("/input-guardrails")
async def input_guardrails_endpoint():
    return {"status": "input guardrails placeholder"}

@router.post("/output-guardrails")
async def output_guardrails_endpoint():
    return {"status": "output guardrails placeholder"}

@router.post("/handoffs")
async def handoffs_endpoint():
    return {"status": "handoffs placeholder"}

@router.get("/trace-status")
async def trace_status_endpoint():
    return {"status": "trace placeholder"}
```

---

### Step 5: Create Placeholder Tests

In `tests/test_orchestration.py`, include initial placeholder tests to validate basic setup:

```python
# tests/test_orchestration.py

import pytest

@pytest.mark.asyncio
async def test_input_guardrails_placeholder():
    assert True

@pytest.mark.asyncio
async def test_output_guardrails_placeholder():
    assert True

@pytest.mark.asyncio
async def test_handoff_placeholder():
    assert True

def test_trace_processor_placeholder():
    assert True
```

Run these tests to confirm they pass:

```bash
pytest tests/test_orchestration.py
```

---

### Step 6: Verify Basic Logging & Configuration

Optionally, create a simple logging verification test to ensure your orchestration-specific configs are loaded correctly:

```python
# tests/test_orchestration.py

import logging
from app import config

def test_logging_and_config():
    logging.basicConfig(level=config.TRACE_LOG_LEVEL)
    logger = logging.getLogger("test_logger")
    logger.info(f"Orchestration mode: {config.ORCHESTRATION_MODE}")
    assert config.ORCHESTRATION_MODE == "DEVELOPMENT"
```

---

### Step 7: Finalize Documentation & Updates

Complete this phase by updating:

- `docs/implementation_process.md`:
  ```markdown
  ## Phase 1 Updates
  - Created orchestration folder structure and placeholder files.
  - Initialized orchestration-specific environment variables.
  - Verified placeholder tests are running successfully.
  - Basic logging and config check completed.
  ```

Commit all changes clearly:

```bash
git add .
git commit -m "Module 5 – Phase 1: Initial setup, placeholders, and basic tests"
```

---

## SDK Files for Future Reference (to be utilized in subsequent phases)

These files will be referenced extensively in future phases with a summary of these files included code snippets in the root folder: /common/OpenAIOrchestration.md file

- [`guardrail.py`](https://github.com/openai/openai-agents-python/blob/main/src/agents/guardrail.py)  
- [`handoffs.py`](https://github.com/openai/openai-agents-python/blob/main/src/agents/handoffs.py)  
- [`handoff_filters.py`](https://github.com/openai/openai-agents-python/blob/main/src/agents/extensions/handoff_filters.py)  
- [`tracing`](https://github.com/openai/openai-agents-python/tree/main/src/agents/tracing)

*Note:* Full implementations from these SDK files will be detailed in phases 2 through 5.

---

## Completion & Next Steps

Phase 1 is complete when:

- All placeholder files and directories are created.
- Environment variables are defined.
- Basic placeholder tests pass successfully.
- Documentation is fully updated.

Proceed next to **Phase 2**, where you'll implement detailed Input and Output Guardrails.

---

**Congratulations on completing Phase 1 of Module 5!**