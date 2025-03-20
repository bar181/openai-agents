<!-- File: root/modules/module3-basic-agents/docs/phase3.md -->

# Phase 3: Enhanced Generic Lifecycle Agent Implementation

Phase 3 introduces a robust, **Enhanced Generic Lifecycle Agent**, extending the previously implemented Generic Lifecycle Agent with a structured toolset, dynamic execution capabilities, detailed logging, and production-ready functionality.

---

## ✅ Objective

Implement an advanced, highly configurable Generic Lifecycle Agent with extensive tool integration, dynamic conditional logic, comprehensive logging, and structured lifecycle management suitable for diverse business and production scenarios.

---

## ✅ Steps Overview

The enhanced implementation involves:

1. **Setup Enhanced Generic Lifecycle Agent class**
2. **Introduce Structured Toolset**
3. **Update FastAPI Router**
4. **Integrate with FastAPI Application (`main.py`)**
5. **Develop Comprehensive Tests**

---

## 📂 Project Structure Updates

```
module3-basic-agents/
├── app/
│   ├── agents/
│   │   └── basic/
│   │       └── enhanced_generic_agent.py  # Enhanced generic lifecycle agent
│   ├── routers/
│   │   └── basic_router.py                # Updated router
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── math_tools.py
│   │   ├── data_tools.py
│   │   ├── string_tools.py
│   │   ├── datetime_tools.py
│   │   └── echo_tools.py
│   └── main.py                            # FastAPI entry point
├── docs/
│   └── phase3.md                          # This implementation guide
├── tests/
│   └── test_enhanced_generic_agent.py     # Enhanced agent tests
```

---

## 🛠 Step-by-Step Implementation

### ✅ Step 1: Setup Enhanced Generic Lifecycle Agent

**File:** `app/agents/basic/enhanced_generic_agent.py`

```python
from typing import Any, Optional, Callable
from pydantic import BaseModel
from agents import Agent, Runner, RunHooks, Tool

class EnhancedLifecycleHooks(RunHooks):
    async def on_agent_start(self, context, agent: Agent):
        print(f"Agent '{agent.name}' started.")

    async def on_agent_end(self, context, agent: Agent, output: Any):
        print(f"Agent '{agent.name}' completed with output: {output}")

    async def on_tool_start(self, context, agent: Agent, tool: Tool):
        print(f"Tool '{tool.name}' started.")

    async def on_tool_end(self, context, agent: Agent, tool: Tool, result: Any):
        print(f"Tool '{tool.name}' finished with result: {result}")

class EnhancedAgentConfig(BaseModel):
    name: str
    instructions: str
    tools: Optional[list[Tool]] = []

class EnhancedGenericAgent:
    def __init__(self, config: EnhancedAgentConfig, hooks: Optional[RunHooks] = None):
        self.agent = Agent(
            name=config.name,
            instructions=config.instructions,
            tools=config.tools
        )
        self.hooks = hooks or EnhancedLifecycleHooks()

    async def execute(self, input_data: Any):
        return await Runner.run(
            agent=self.agent,
            hooks=self.hooks,
            input=input_data
        )
```

---

### ✅ Step 2: Introduce Structured Toolset

Create reusable tools under the new `tools` directory:

- **math_tools.py:** add, multiply, random_number
- **data_tools.py:** fetch_json, save_to_db
- **string_tools.py:** concat_strings, count_words
- **datetime_tools.py:** current_time, days_between
- **echo_tools.py:** echo

Example (`echo_tools.py`):

```python
from agents import function_tool

@function_tool
def echo(message: str) -> str:
    return f"Echo: {message}"
```

---

### ✅ Step 3: Update FastAPI Router

**File:** `app/routers/basic_router.py`

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.dependencies import verify_api_key
from app.agents.basic.enhanced_generic_agent import (
    EnhancedGenericAgent, EnhancedAgentConfig
)
from app.tools.echo_tools import echo

router = APIRouter(tags=["Enhanced Generic Agent"])

class EnhancedAgentRequest(BaseModel):
    message: str

# Initialize the enhanced agent
enhanced_agent_config = EnhancedAgentConfig(
    name="EnhancedAgent",
    instructions="Echo user's message dynamically.",
    tools=[echo]
)

agent = EnhancedGenericAgent(enhanced_agent_config)

@router.post("/enhanced/execute", dependencies=[Depends(verify_api_key)])
async def execute_enhanced_agent(request: EnhancedAgentRequest):
    result = await agent.execute(request.message)
    return {"response": result.final_output}
```

---

### ✅ Step 4: Integrate with FastAPI (`main.py`)

Update main application:

```python
from fastapi import FastAPI
from app.routers import basic_router

app = FastAPI(title="Enhanced Generic Lifecycle Agent", version="1.0.0")

app.include_router(basic_router.router, prefix="/agents/basic")

@app.get("/")
async def root():
    return {"message": "Enhanced Generic Agent System Running"}
```

---

### ✅ Step 5: Develop Comprehensive Tests

**File:** `tests/test_enhanced_generic_agent.py`

```python
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

def test_enhanced_agent_execution():
    response = client.post(
        "/agents/basic/enhanced/execute",
        json={"message": "Testing Enhanced Agent"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Echo: Testing Enhanced Agent"
```

Run tests:

```bash
python -m pytest tests/test_enhanced_generic_agent.py
```

---

## 🎯 Summary and Completion Checklist

- [✔] **Enhanced Generic Lifecycle Agent implemented.**
- [✔] **Structured, reusable toolset created.**
- [✔] **FastAPI Router endpoints configured.**
- [✔] **Integrated endpoints into FastAPI main application.**
- [✔] **Comprehensive unit and integration tests written and verified.**

The enhanced generic lifecycle agent provides a robust, scalable foundation, simplifying future development and integration tasks for diverse business logic and automation scenarios.

---

**End of Phase 3 Document**

