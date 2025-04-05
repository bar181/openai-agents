from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key

# Import agents
from app.agents.advanced.generic_lifecycle_agent import (
    GenericLifecycleAgent,
    GenericAgentConfig,
)
from app.agents.advanced.multi_tool_agent import (
    MultiToolAgent,
    MultiToolAgentConfig,
)

# Import tools
from app.tools import (
    # Basic tools
    echo, add, multiply, to_uppercase, current_time, fetch_mock_data,
    # Advanced tools
    json_tool, csv_tool, database_tool, text_analysis_tool,
    statistics_tool, pattern_tool, api_tool, cache_tool,
    rate_limiter_tool, visualization_tool
)

router = APIRouter(tags=["Advanced Agents"])

# Generic Lifecycle Agent
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
    "/generic-lifecycle",
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


# Multi-Tool Agent
class MultiToolExecuteRequest(BaseModel):
    message: str = Field(..., description="Message input for multi-tool agent")
    context: Optional[Dict[str, Any]] = Field(None, description="Optional context for the agent")

class MultiToolExecuteResponse(BaseModel):
    response: Dict[str, Any] = Field(..., description="Response from multi-tool agent")
    context: Optional[Dict[str, Any]] = Field(None, description="Context from the agent execution")

# Instantiate the Multi-Tool Agent with all tools
multi_tool_config = MultiToolAgentConfig(
    name="MultiToolAgent",
    instructions=(
        "You are a multi-tool agent with access to various tools for data processing, "
        "analysis, and integration. You can handle complex tasks by breaking them down "
        "into steps and using the appropriate tools for each step.\n\n"
        "When processing user requests, identify the required tools and execute them "
        "in the correct sequence. Maintain context between steps and handle errors gracefully.\n\n"
        "You have access to the following categories of tools:\n\n"
        "1. Data Processing Tools:\n"
        "   - JSON validation and transformation\n"
        "   - CSV parsing and generation\n"
        "   - Database operations (mock)\n\n"
        "2. Analysis Tools:\n"
        "   - Text analysis (sentiment, entities, keywords)\n"
        "   - Statistical calculations\n"
        "   - Pattern matching\n\n"
        "3. Integration Tools:\n"
        "   - API requests\n"
        "   - Caching\n"
        "   - Rate limiting\n\n"
        "4. Visualization Tools:\n"
        "   - Bar charts\n"
        "   - Line charts\n"
        "   - Pie charts\n"
        "   - Scatter plots\n\n"
        "5. Basic Utility Tools:\n"
        "   - Echo\n"
        "   - Math operations\n"
        "   - String manipulation\n"
        "   - Date/time utilities\n"
        "   - Data fetching\n\n"
        "For complex tasks, break them down into steps and use the appropriate tools for each step."
    ),
    tools=[
        # Basic tools
        echo, add, multiply, to_uppercase, current_time, fetch_mock_data,
        # Advanced tools
        json_tool, csv_tool, database_tool, text_analysis_tool,
        statistics_tool, pattern_tool, api_tool, cache_tool,
        rate_limiter_tool, visualization_tool
    ],
    debug_mode=True
)
multi_tool_agent = MultiToolAgent(multi_tool_config)

@router.post(
    "/multi-tool",
    response_model=MultiToolExecuteResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Execute Multi-Tool Agent with Enhanced Capabilities",
    description="""
Executes the Multi-Tool Agent with comprehensive processing capabilities and intelligent tool selection.

The agent follows a sophisticated execution lifecycle:

- **Initialization:**
  - Loads configuration
  - Initializes tool registry
  - Prepares execution context

- **Processing:**
  - Analyzes input for required tools
  - Builds execution plan
  - Manages state transitions

- **Execution:**
  - Performs multi-step operations
  - Handles errors gracefully
  - Maintains execution context

- **Completion:**
  - Aggregates results
  - Cleans up resources
  - Returns formatted response

### Available Tools:

#### Data Processing:
- **JSON Tools:** Validate and transform JSON data
- **CSV Tools:** Parse and manipulate CSV files
- **Database Tools:** Mock database operations

#### Analysis:
- **Text Analysis:** Extract insights from text
- **Statistics:** Perform statistical calculations
- **Pattern Matching:** Identify patterns in data
- **Visualization:** Generate data visualizations (mock)

#### Integration:
- **API Tools:** Handle external API requests
- **Cache Tools:** Optimize performance with caching
- **Rate Limiter:** Control request rates

### Example Usage:

**Input:**
```json
{
    "message": "Analyze sentiment of text 'Great product!', store result in database, then create visualization"
}
```

**Output:**
```json
{
    "response": {
        "sentiment_analysis": {"score": 0.9, "label": "positive"},
        "storage_status": "success",
        "visualization_url": "mock://charts/sentiment/123"
    }
}
```

The agent intelligently coordinates multiple tools to complete complex tasks while maintaining context and handling errors.
"""
)
async def execute_multi_tool_agent(request: MultiToolExecuteRequest):
    result = await multi_tool_agent.run(request.message, request.context)
    
    # Handle error case where final_output is a string instead of a dict
    if isinstance(result["final_output"], str) and result["final_output"].startswith("Error:"):
        error_message = result["final_output"]
        return MultiToolExecuteResponse(
            response={"error": error_message},
            context=result["context"]
        )
    
    return MultiToolExecuteResponse(
        response=result["final_output"],
        context=result["context"]
    )