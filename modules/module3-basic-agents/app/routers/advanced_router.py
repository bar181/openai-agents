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
- **Data Fetch (`fetch_mock_data`)**: Retrieves mock data from simulated internal database.

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