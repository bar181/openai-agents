# Phase 2: Streaming Agents and Tools Integration

## Objective

In Phase 2, we enhance Module 3 by implementing streaming response functionalities and integrating reusable tools. This phase focuses on providing real-time user interactions through streaming text and items and incorporating tools to extend agent capabilities. We will integrate these agents into our FastAPI application, create structured API endpoints, and ensure all functionalities are thoroughly tested and documented.

---

## Steps Overview

### Step 1: Implement Streaming Text Agent

**Description:**  
Develop an agent capable of streaming text responses incrementally to users, enhancing real-time interaction and feedback. This agent will provide a more engaging user experience by displaying responses as they are generated rather than waiting for the complete response.

**Actions:**

- Create a new agent file: `app/agents/basic/stream_text_agent.py`.
- Implement functionality to generate and stream text progressively.
- Manage asynchronous response handling to ensure smooth streaming.

**Implementation Example:**

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

class StreamTextAgent:
    def __init__(self, name="TextStreamer", instructions="You are a helpful assistant."):
        self.agent = Agent(
            name=name,
            instructions=instructions,
        )
    
    async def stream_response(self, user_input):
        """Stream the agent's response to the user input."""
        result = Runner.run_streamed(self.agent, input=user_input)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                yield event.data.delta

# Usage example
async def demo_text_streaming():
    agent = StreamTextAgent()
    async for text_chunk in agent.stream_response("Please tell me 5 jokes."):
        print(text_chunk, end="", flush=True)
```

---

### Step 2: Implement Streaming Items Agent

**Description:**  
Create an agent that streams sequences of structured items (e.g., jokes, facts, or bullet points) in real-time to enhance dynamic content delivery. This agent will be particularly useful for generating lists, step-by-step instructions, or any content that can be naturally broken down into discrete items.

**Actions:**

- Create a new agent file: `app/agents/basic/stream_items_agent.py`.
- Implement item generation logic with real-time streaming.
- Ensure controlled delays or asynchronous handling for proper streaming effects.

**Implementation Example:**

```python
import asyncio
import random
from agents import Agent, ItemHelpers, Runner, function_tool

class StreamItemsAgent:
    def __init__(self, name="ItemStreamer", instructions="Generate items based on the request."):
        # Define tools that the agent can use
        @function_tool
        def how_many_items() -> int:
            """Determine how many items to generate (1-10)"""
            return random.randint(1, 10)
        
        self.agent = Agent(
            name=name,
            instructions=instructions,
            tools=[how_many_items],
        )
    
    async def stream_items(self, category):
        """Stream items based on the requested category."""
        result = Runner.run_streamed(
            self.agent,
            input=f"Generate {category} items.",
        )
        
        async for event in result.stream_events():
            if event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    yield {"type": "tool_call", "message": "Determining number of items..."}
                elif event.item.type == "tool_call_output_item":
                    yield {"type": "tool_output", "count": event.item.output}
                elif event.item.type == "message_output_item":
                    yield {"type": "message", "content": ItemHelpers.text_message_output(event.item)}

# Usage example
async def demo_items_streaming():
    agent = StreamItemsAgent(instructions="First call the `how_many_items` tool, then generate that many items of the requested category.")
    print("=== Run starting ===")
    async for item in agent.stream_items("jokes"):
        if item["type"] == "tool_call":
            print(item["message"])
        elif item["type"] == "tool_output":
            print(f"Will generate {item['count']} items")
        elif item["type"] == "message":
            print(f"Items:\n{item['content']}")
    print("=== Run complete ===")
```

---

### Step 3: Develop and Integrate Agent Tools

**Description:**  
Define reusable tools that basic agents can utilize, such as data-fetching tools, utilities, or calculators, enhancing their functionality and reusability. These tools will allow agents to perform specific tasks or access external information, making them more versatile and powerful.

**Actions:**

- Create a tools definition file: `app/agents/basic/tools.py`.
- Define reusable functions or utilities (e.g., weather fetching, calculations).
- Integrate these tools with existing agents, making them accessible through function tools.

**Implementation Example:**

```python
from agents import function_tool
import random
import datetime

# Tool to get a random number within a range
@function_tool
def get_random_number(min_value: int = 1, max_value: int = 100) -> int:
    """Generate a random number between min_value and max_value (inclusive)."""
    return random.randint(min_value, max_value)

# Tool to get the current date and time
@function_tool
def get_current_datetime() -> str:
    """Get the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Tool to count words in a text
@function_tool
def count_words(text: str) -> int:
    """Count the number of words in the provided text."""
    return len(text.split())

# Tool to generate a list of items
@function_tool
def generate_items(category: str, count: int = 5) -> list:
    """
    Generate a list of placeholder items for the specified category.
    This is a mock implementation that would be replaced with real data in production.
    """
    categories = {
        "fruits": ["apple", "banana", "orange", "grape", "strawberry", "kiwi", "mango", "pineapple", "watermelon", "pear"],
        "colors": ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white", "brown"],
        "countries": ["USA", "Canada", "UK", "France", "Germany", "Japan", "Australia", "Brazil", "India", "China"]
    }
    
    if category in categories:
        items = categories[category]
        return random.sample(items, min(count, len(items)))
    else:
        return [f"{category} item {i+1}" for i in range(count)]
```

---

### Step 4: API Integration and Endpoint Setup

**Description:**  
Expose streaming functionalities and tools via structured FastAPI endpoints, allowing external clients to interact with agents in real-time. The API will be designed with a RESTful approach, clear documentation, and proper request/response models.

**Actions:**

- Update `app/routers/basic_router.py` to include new streaming endpoints:
  - `/stream-text`: Endpoint to stream text responses.
  - `/stream-items`: Endpoint to stream sequential items.
- Clearly define request and response schemas using Pydantic models.
- Provide comprehensive Swagger documentation for seamless developer interaction.

**Implementation Example:**

```python
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json

from app.agents.basic.stream_text_agent import StreamTextAgent
from app.agents.basic.stream_items_agent import StreamItemsAgent
from app.dependencies import verify_api_key

router = APIRouter()

# Request and response models
class TextStreamRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = None

class ItemStreamRequest(BaseModel):
    category: str
    count: Optional[int] = None

# Streaming text endpoint
@router.post("/stream-text", dependencies=[Depends(verify_api_key)])
async def stream_text_endpoint(request: TextStreamRequest):
    """
    Stream a text response from the agent.
    
    This endpoint returns a streaming response where each chunk is a piece of the generated text.
    The text is generated in real-time and sent to the client as it becomes available.
    
    Parameters:
    - **prompt**: The user input to generate a response for
    - **max_tokens**: Optional maximum number of tokens to generate
    
    Returns:
    - A streaming response with text chunks
    """
    agent = StreamTextAgent()
    
    async def generate():
        async for chunk in agent.stream_response(request.prompt):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/plain")

# Streaming items endpoint
@router.post("/stream-items", dependencies=[Depends(verify_api_key)])
async def stream_items_endpoint(request: ItemStreamRequest):
    """
    Stream a sequence of items from the agent.
    
    This endpoint returns a streaming response where each chunk is a JSON object
    representing an event in the generation process (tool call, tool output, or message).
    
    Parameters:
    - **category**: The category of items to generate (e.g., "jokes", "facts")
    - **count**: Optional number of items to generate (if not provided, the agent will decide)
    
    Returns:
    - A streaming response with JSON objects representing generation events
    """
    agent = StreamItemsAgent(
        instructions=f"Generate {request.count if request.count else 'some'} {request.category}."
    )
    
    async def generate():
        async for item in agent.stream_items(request.category):
            yield json.dumps(item) + "\n"
    
    return StreamingResponse(generate(), media_type="application/x-ndjson")
```

**Swagger UI Integration:**

The Swagger UI will provide comprehensive documentation for these endpoints, including:

1. **Detailed Descriptions**: Each endpoint will have a clear description of its purpose and functionality.
2. **Request Schema**: The UI will display the expected request format, including all required and optional fields.
3. **Response Schema**: The UI will document the structure of the streaming response.
4. **Example Values**: Sample requests will be provided to help developers understand how to use the endpoints.
5. **Authentication Requirements**: The UI will indicate that API key authentication is required.
6. **Try It Out Feature**: Developers can test the endpoints directly from the Swagger UI.

Example Swagger documentation for the `/stream-text` endpoint:

```yaml
/agents/basic/stream-text:
  post:
    summary: Stream Text Response
    description: Stream a text response from the agent in real-time.
    tags:
      - Basic Agents
    security:
      - ApiKeyAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/TextStreamRequest'
          example:
            prompt: "Tell me a story about a space adventure."
            max_tokens: 500
    responses:
      200:
        description: Successful Response - Returns a streaming text response
        content:
          text/plain:
            schema:
              type: string
              format: binary
      401:
        description: Unauthorized - Invalid or missing API key
      422:
        description: Validation Error - Invalid request parameters
```

---

### Step 5: Comprehensive Testing and Documentation Update

**Description:**  
Ensure that streaming functionalities and tool integrations operate correctly and update documentation to guide users in leveraging these new features. Thorough testing is essential to verify that the streaming behavior works as expected and that tools are properly integrated.

**Actions:**

- Write and execute tests (`tests/test_stream_text.py`, `tests/test_stream_items.py`) to verify correct streaming behavior.
- Confirm integration and functionality of tools through unit and integration tests.
- Update Swagger UI and documentation to clearly illustrate streaming endpoints and available tools.

**Test Implementation Example:**

```python
import pytest
from fastapi.testclient import TestClient
import json
from app.main import app

client = TestClient(app)

def test_stream_text():
    """Test the text streaming endpoint."""
    response = client.post(
        "/agents/basic/stream-text",
        json={"prompt": "Tell me a short story."},
        headers={"X-API-Key": "test_api_key"}
    )
    assert response.status_code == 200
    
    # Check that we receive a streaming response
    content = response.content.decode("utf-8")
    assert len(content) > 0
    
    # The response should be a coherent text
    assert isinstance(content, str)
    assert len(content.strip()) > 0

def test_stream_items():
    """Test the items streaming endpoint."""
    response = client.post(
        "/agents/basic/stream-items",
        json={"category": "jokes", "count": 3},
        headers={"X-API-Key": "test_api_key"}
    )
    assert response.status_code == 200
    
    # Parse the streaming response as JSON lines
    events = [json.loads(line) for line in response.content.decode("utf-8").strip().split("\n") if line]
    
    # Check that we have events
    assert len(events) > 0
    
    # Verify the structure of events
    tool_calls = [e for e in events if e["type"] == "tool_call"]
    tool_outputs = [e for e in events if e["type"] == "tool_output"]
    messages = [e for e in events if e["type"] == "message"]
    
    # We should have at least one tool call, one tool output, and one message
    assert len(tool_calls) > 0
    assert len(tool_outputs) > 0
    assert len(messages) > 0
    
    # The message should contain jokes
    message_content = messages[0]["content"]
    assert "joke" in message_content.lower() or "jokes" in message_content.lower()

def test_tools_integration():
    """Test that tools are properly integrated with agents."""
    # This test would verify that the tools are correctly used by the agents
    # For example, we could check that the random number generator tool returns values within the expected range
    
    # Mock implementation for demonstration
    from app.agents.basic.tools import get_random_number, count_words, generate_items
    
    # Test random number generator
    num = get_random_number(1, 10)
    assert 1 <= num <= 10
    
    # Test word counter
    count = count_words("This is a test sentence.")
    assert count == 5
    
    # Test item generator
    items = generate_items("fruits", 3)
    assert len(items) == 3
    assert all(isinstance(item, str) for item in items)
```

---

## Expected Outcomes

By implementing these streaming agents and tools, we will achieve:

1. **Enhanced User Experience**: Real-time streaming of responses creates a more engaging and interactive experience.
2. **Increased Flexibility**: The tools integration allows agents to perform a wider range of tasks.
3. **Better Developer Experience**: Clear API documentation and comprehensive testing make it easier for developers to use our agents.
4. **Improved Performance**: Streaming responses can start displaying content to users faster than waiting for complete responses.

The implementation will follow best practices for asynchronous programming in Python, FastAPI integration, and OpenAI API usage. The code will be modular, well-documented, and thoroughly tested to ensure reliability and maintainability.

---

By following these structured steps, Phase 2 will significantly enhance Module 3, providing robust streaming capabilities, reusable agent tools, and a well-integrated API experience.