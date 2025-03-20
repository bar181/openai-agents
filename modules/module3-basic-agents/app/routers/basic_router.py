# File: root/modules/module3-basic-agents/app/routers/basic_router.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key

from app.agents.basic.lifecycle_agent import (
    initialize_agent,
    execute_agent,
    terminate_agent,
)

from app.agents.basic.dynamic_prompt_agent import (
    update_system_prompt,
    execute_dynamic_prompt_agent,
)

from app.agents.basic.generic_lifecycle_agent import (
    GenericLifecycleAgent,
    GenericAgentConfig,
)

# Corrected tool imports
from app.tools.echo_tools import echo
from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase
from app.tools.datetime_tools import current_time
from app.tools.data_tools import fetch_mock_data

router = APIRouter(tags=["Basic Agents"])

# Input and Output models
class ExecuteLifecycleRequest(BaseModel):
    input: str = Field(..., description="Input data for lifecycle agent execution")

class LifecycleResponse(BaseModel):
    result: str = Field(..., description="Result of lifecycle agent execution")

class PromptUpdateRequest(BaseModel):
    new_prompt: str = Field(..., description="The new prompt for the dynamic agent")

class PromptUpdateResponse(BaseModel):
    prompt: str = Field(..., description="Updated prompt for dynamic agent")

class DynamicPromptExecuteRequest(BaseModel):
    input: str = Field(..., description="Input data for dynamic prompt agent")

class DynamicPromptExecuteResponse(BaseModel):
    response: str = Field(..., description="Agent response after executing dynamic prompt")

class GenericExecuteRequest(BaseModel):
    message: str = Field(..., description="Message input for generic lifecycle agent")

class GenericExecuteResponse(BaseModel):
    response: str = Field(..., description="Response from generic lifecycle agent")

# Instantiate the Generic Lifecycle Agent with enhanced toolset
config = GenericAgentConfig(
    name="GenericLifecycleAgent",
    instructions="Utilize provided tools to process user messages intelligently.",
    tools=[echo, add, multiply, to_uppercase, current_time, fetch_mock_data]
)
generic_agent = GenericLifecycleAgent(config)

# Lifecycle Management Endpoints
@router.post("/lifecycle/initialize", dependencies=[Depends(verify_api_key)])
async def lifecycle_initialize():
    message = initialize_agent()
    return {"message": message}

@router.post("/lifecycle/execute",
             response_model=LifecycleResponse,
             dependencies=[Depends(verify_api_key)])
async def lifecycle_execute(request: ExecuteLifecycleRequest):
    result = execute_agent({"input": request.input})
    return LifecycleResponse(result=result)

@router.post("/lifecycle/terminate", dependencies=[Depends(verify_api_key)])
async def lifecycle_terminate():
    message = terminate_agent()
    return {"message": message}

# Dynamic Prompt Endpoints
@router.post("/dynamic-prompt/update",
             response_model=PromptUpdateResponse,
             dependencies=[Depends(verify_api_key)])
async def dynamic_prompt_update(request: PromptUpdateRequest):
    prompt = update_system_prompt(request.new_prompt)
    return PromptUpdateResponse(prompt=prompt)

@router.post("/dynamic-prompt/execute",
             response_model=DynamicPromptExecuteResponse,
             dependencies=[Depends(verify_api_key)])
async def dynamic_prompt_execute(request: DynamicPromptExecuteRequest):
    response = execute_dynamic_prompt_agent({"input": request.input})
    return DynamicPromptExecuteResponse(response=response)

# Enhanced Generic Lifecycle Agent Endpoint
@router.post(
    "/generic-lifecycle/execute",
    response_model=GenericExecuteResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Execute Enhanced Generic Lifecycle Agent",
    description="""
Executes the Enhanced Generic Lifecycle Agent, which intelligently processes user messages
using a comprehensive suite of integrated tools. The agent follows a structured lifecycle:

- **Initialization:** Agent setup with provided configuration and toolset.
- **Execution:** Processes user-provided input messages utilizing available tools.
- **Termination:** Automatically handles resource cleanup after execution.

### Available Tools:

- **Echo (`echo`)**: Echoes back user input for confirmation or debugging.
- **Math Operations (`add`, `multiply`)**: Performs arithmetic operations on provided numbers.
- **String Manipulation (`to_uppercase`)**: Converts input strings to uppercase.
- **Datetime Utilities (`get_current_utc_time`)**: Retrieves current UTC time in ISO format.

### Example Usage:

**Input Prompt:**

```json
{
  "message": "Add 7 and 3, then uppercase 'hello', and provide current UTC time."
}
```

**Possible Output:**

```json
{
  "response": "Result: 10, HELLO, Current UTC Time: 2025-03-19T18:25:43.123456Z"
}
```

The agent intelligently interprets the instructions in the provided message and applies the appropriate tools to generate a structured response.
"""
)
async def execute_generic_agent(request: GenericExecuteRequest):
    result = await generic_agent.run(request.message)
    return GenericExecuteResponse(response=str(result.final_output))
