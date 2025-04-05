# Phase 3: Enhanced Generic Lifecycle Agent Implementation

Phase 3 introduces a robust, **Enhanced Generic Lifecycle Agent**, implementing a sophisticated agent with structured toolset, dynamic execution capabilities, detailed logging, and production-ready functionality. This agent is now part of the advanced agents module due to its enhanced capabilities.

---

## ✅ Objective

Implement an advanced, highly configurable Generic Lifecycle Agent with extensive tool integration, dynamic conditional logic, comprehensive logging, and structured lifecycle management suitable for diverse business and production scenarios.

---

## ✅ Steps Overview

The enhanced implementation involves:

1. **Setup Generic Lifecycle Agent class**
2. **Introduce Structured Toolset**
3. **Create Advanced Router**
4. **Update FastAPI Router**
5. **Integrate with FastAPI Application (`main.py`)**
6. **Develop Comprehensive Tests**

---

## 📂 Project Structure Updates

```
module3-basic-agents/
├── app/
│   ├── agents/
│   │   ├── basic/
│   │   │   ├── lifecycle_agent.py
│   │   │   └── dynamic_prompt_agent.py
│   │   └── advanced/
│   │       └── generic_lifecycle_agent.py  # Enhanced generic lifecycle agent
│   ├── routers/
│   │   ├── basic_router.py      # Basic agents router
│   │   └── advanced_router.py   # Advanced agents router
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── math_tools.py
│   │   ├── data_tools.py
│   │   ├── string_tools.py
│   │   ├── datetime_tools.py
│   │   └── echo_tools.py
│   └── main.py                  # FastAPI entry point
├── docs/
│   └── phase3.md               # This implementation guide
├── tests/
│   └── test_advanced_agents.py # Advanced agents tests
```

---

## 🛠 Step-by-Step Implementation

### ✅ Step 1: Setup Generic Lifecycle Agent

**File:** `app/agents/advanced/generic_lifecycle_agent.py`

```python
from typing import Any, Optional, Callable
from pydantic import BaseModel, ConfigDict
from agents import Agent, Runner, RunHooks, Tool

class GenericLifecycleHooks(RunHooks):
    def __init__(self, logger: Optional[Callable[[str], None]] = print):
        self.logger = logger

    async def on_agent_start(self, context, agent: Agent):
        self.logger(f"[START] Agent '{agent.name}' started.")

    async def on_agent_end(self, context, agent: Agent, output: Any):
        self.logger(f"[END] Agent '{agent.name}' ended with output: {output}")

    async def on_tool_start(self, context, agent: Agent, tool: Tool):
        self.logger(f"[TOOL START] '{tool.name}' started.")

    async def on_tool_end(self, context, agent: Agent, tool: Tool, result: Any):
        self.logger(f"[TOOL END] '{tool.name}' ended with result: {result}")

class GenericAgentConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    instructions: str
    tools: Optional[list[Tool]] = None
    output_type: Optional[Any] = None

class GenericLifecycleAgent:
    def __init__(self, config: GenericAgentConfig, hooks: Optional[RunHooks] = None):
        self.agent = Agent(
            name=config.name,
            instructions=config.instructions,
            tools=config.tools or [],
            output_type=config.output_type
        )
        self.hooks = hooks or GenericLifecycleHooks()

    async def run(self, input_data: Any):
        return await Runner.run(
            self.agent,
            hooks=self.hooks,
            input=input_data
        )
```

---

### ✅ Step 2: Introduce Structured Toolset

Create reusable tools under the `tools` directory:

- **math_tools.py:** add, multiply
- **data_tools.py:** fetch_mock_data
- **string_tools.py:** to_uppercase
- **datetime_tools.py:** current_time
- **echo_tools.py:** echo

Example (`data_tools.py`):

```python
from agents import function_tool

@function_tool
def fetch_mock_data(source: str) -> dict:
    """Retrieve MOCK data from an INTERNAL simulated database."""
    return {"source": source, "data": "sample data"}
```

---

### ✅ Step 3: Create Advanced Router

**File:** `app/routers/advanced_router.py`

```python
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key

from app.agents.advanced.generic_lifecycle_agent import (
    GenericLifecycleAgent,
    GenericAgentConfig,
)

from app.tools.echo_tools import echo
from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase
from app.tools.datetime_tools import current_time
from app.tools.data_tools import fetch_mock_data

router = APIRouter(tags=["Advanced Agents"])

class GenericExecuteRequest(BaseModel):
    message: str = Field(..., description="Message input for generic lifecycle agent")

class GenericExecuteResponse(BaseModel):
    response: str = Field(..., description="Response from generic lifecycle agent")

# Instantiate the Generic Lifecycle Agent with enhanced toolset
config = GenericAgentConfig(
    name="GenericLifecycleAgent",
    instructions=(
        "You have access to the following INTERNAL tools only:\n"
        "- echo(message: str): echoes a message.\n"
        "- add(a: float, b: float): returns the sum of two numbers.\n"
        "- multiply(a: float, b: float): returns the product of two numbers.\n"
        "- to_uppercase(text: str): converts text to uppercase.\n"
        "- current_time(): returns current UTC time.\n"
        "- fetch_mock_data(source: str): retrieves MOCK data from a simulated internal database.\n\n"
        "When a user requests to fetch or retrieve data from any source, use fetch_mock_data to get the data "
        "and return the data value from the result."
    ),
    tools=[echo, add, multiply, to_uppercase, current_time, fetch_mock_data]
)
generic_agent = GenericLifecycleAgent(config)

@router.post(
    "/generic-lifecycle/execute",
    response_model=GenericExecuteResponse,
    dependencies=[Depends(verify_api_key)]
)
async def execute_generic_agent(request: GenericExecuteRequest):
    result = await generic_agent.run(request.message)
    return GenericExecuteResponse(response=str(result.final_output))
```

---

### ✅ Step 4: Update FastAPI Application (`main.py`)

```python
from fastapi import FastAPI
from app.routers import hello_world, story_router, basic_router, advanced_router

app = FastAPI(title="Module3 - Basic Agents", version="1.0.0")

app.include_router(hello_world.router, prefix="/agent")
app.include_router(story_router.router, prefix="/agents/story")
app.include_router(basic_router.router, prefix="/agents/basic")
app.include_router(advanced_router.router, prefix="/agents/advanced")

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
```

---

### ✅ Step 5: Develop Comprehensive Tests

**File:** `tests/test_advanced_agents.py`

```python
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)
headers = {"X-API-KEY": API_KEY}

def test_generic_lifecycle_agent_echo_tool():
    response = client.post(
        "/agents/advanced/generic-lifecycle/execute",
        json={"message": "Echo 'Hello World'"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Echo: Hello World"

def test_generic_lifecycle_agent_data_fetch_tool():
    response = client.post(
        "/agents/advanced/generic-lifecycle/execute",
        json={"message": "Fetch MOCK data from 'source1'"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "sample data" in data["response"]
```

Run tests:

```bash
python -m pytest tests/test_advanced_agents.py -v
```

---

## 🎯 Summary and Completion Checklist

- [✔] **Generic Lifecycle Agent implemented in advanced module**
- [✔] **Structured, reusable toolset created**
- [✔] **Advanced Router configured with enhanced functionality**
- [✔] **Basic Router simplified to focus on basic agents**
- [✔] **FastAPI application updated with new router structure**
- [✔] **Comprehensive unit and integration tests written and verified**

The generic lifecycle agent, now part of the advanced agents module, provides a robust, scalable foundation with enhanced capabilities for complex tasks. The separation into basic and advanced modules provides a clear organization of agent capabilities based on their complexity and features.

---

**End of Phase 3 Document**
