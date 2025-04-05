# File: root/modules/module3-basic-agents/app/routers/basic_router.py

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
import json
import asyncio
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

from app.agents.basic.stream_text_agent import StreamTextAgent
from app.agents.basic.stream_items_agent import StreamItemsAgent

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

# Streaming Text Agent Models
class TextStreamRequest(BaseModel):
    prompt: str = Field(..., description="The prompt to generate a streaming text response for")
    instructions: str = Field("You are a helpful assistant.", description="Optional custom instructions for the agent")

# Streaming Items Agent Models
class ItemStreamRequest(BaseModel):
    category: str = Field(..., description="The category of items to generate (e.g., 'jokes', 'facts')")
    count: int = Field(None, description="Optional number of items to generate (if not provided, the agent will decide)")
    instructions: str = Field("Generate items based on the request.", description="Optional custom instructions for the agent")

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

# Streaming Text Endpoint
@router.post(
    "/stream-text",
    dependencies=[Depends(verify_api_key)],
    summary="Stream a text response from the agent",
    description="""
    Stream a text response from the agent.
    
    This endpoint returns a streaming response where each chunk is a piece of the generated text.
    The text is generated in real-time and sent to the client as it becomes available.
    
    Parameters:
    - **prompt**: The user input to generate a response for
    - **instructions**: Optional custom instructions for the agent
    
    Returns:
    - A streaming response with text chunks
    """
)
async def stream_text_endpoint(request: TextStreamRequest):
    """Stream a text response from the agent."""
    agent = StreamTextAgent(
        name="TextStreamer",
        instructions=request.instructions
    )
    
    # Initialize the agent
    await agent.initialize()
    
    async def generate():
        try:
            async for chunk in agent.execute(request.prompt):
                yield chunk
        finally:
            # Ensure the agent is terminated properly
            await agent.terminate()
    
    return StreamingResponse(generate(), media_type="text/plain")

# Streaming Items Endpoint
@router.post(
    "/stream-items",
    dependencies=[Depends(verify_api_key)],
    summary="Stream a sequence of items from the agent",
    description="""
    Stream a sequence of items from the agent.
    
    This endpoint returns a streaming response where each chunk is a JSON object
    representing an event in the generation process (status, count, item, or complete).
    
    Parameters:
    - **category**: The category of items to generate (e.g., "jokes", "facts")
    - **count**: Optional number of items to generate (if not provided, the agent will decide)
    - **instructions**: Optional custom instructions for the agent
    
    Returns:
    - A streaming response with JSON objects representing generation events
    """
)
async def stream_items_endpoint(request: ItemStreamRequest):
    """Stream a sequence of items from the agent."""
    agent = StreamItemsAgent(
        name="ItemStreamer",
        instructions=request.instructions
    )
    
    # Initialize the agent
    await agent.initialize()
    
    async def generate():
        try:
            async for item in agent.execute(request.category, request.count):
                yield json.dumps(item) + "\n"
        finally:
            # Ensure the agent is terminated properly
            await agent.terminate()
    
    return StreamingResponse(generate(), media_type="application/x-ndjson")
