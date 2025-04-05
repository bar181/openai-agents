from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
import json
from typing import Optional
from app.dependencies import verify_api_key
from app.agents.streaming.stream_items_agent import (
    initialize_stream_items_agent,
    execute_stream_items_agent,
    terminate_stream_items_agent,
)
from app.agents.streaming.stream_text_agent import (
    initialize_stream_text_agent,
    execute_stream_text_agent,
    terminate_stream_text_agent,
)

router = APIRouter(tags=["Streaming Agents"])

# ----- Streaming Items Endpoints -----

@router.post(
    "/items/initialize",
    dependencies=[Depends(verify_api_key)],
    summary="Initialize the streaming items agent",
    description="Initialize the streaming items agent and return its status."
)
async def streaming_items_initialize():
    status = await initialize_stream_items_agent()
    return status

@router.post(
    "/items/execute",
    dependencies=[Depends(verify_api_key)],
    summary="Execute the streaming items agent",
    description="Stream items for the specified category and optional count."
)
async def streaming_items_execute(
    category: str = Query(..., description="The category of items to generate."),
    count: Optional[int] = Query(None, description="Optional number of items to generate.")
):
    async def event_generator():
        async for event in execute_stream_items_agent(category, count):
            yield json.dumps(event) + "\n"
    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

@router.post(
    "/items/terminate",
    dependencies=[Depends(verify_api_key)],
    summary="Terminate the streaming items agent",
    description="Terminate the streaming items agent and return its termination status."
)
async def streaming_items_terminate():
    status = await terminate_stream_items_agent()
    return status

# ----- Streaming Text Endpoints -----

@router.post(
    "/text/initialize",
    dependencies=[Depends(verify_api_key)],
    summary="Initialize the streaming text agent",
    description="Initialize the streaming text agent and return its status."
)
async def streaming_text_initialize():
    status = await initialize_stream_text_agent()
    return status

@router.post(
    "/text/execute",
    dependencies=[Depends(verify_api_key)],
    summary="Execute the streaming text agent",
    description="Stream text for the provided input message."
)
async def streaming_text_execute(
    input: str = Query(..., description="User input message to generate a text response for.")
):
    async def event_generator():
        async for text_chunk in execute_stream_text_agent({"input": input}):
            yield text_chunk
    return StreamingResponse(event_generator(), media_type="text/plain")

@router.post(
    "/text/terminate",
    dependencies=[Depends(verify_api_key)],
    summary="Terminate the streaming text agent",
    description="Terminate the streaming text agent and return its termination status."
)
async def streaming_text_terminate():
    status = await terminate_stream_text_agent()
    return status
