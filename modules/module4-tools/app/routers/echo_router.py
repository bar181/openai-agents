from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.tools.echo_tools import echo
import anyio
import json

router = APIRouter(tags=["Tools Echo"])

async def call_tool(tool, **kwargs):
    if hasattr(tool, "function") and callable(tool.function):
        return tool.function(**kwargs)
    elif hasattr(tool, "on_invoke_tool"):
        ctx = {}
        args_json = json.dumps(kwargs)
        return await tool.on_invoke_tool(ctx, args_json)
    elif callable(tool):
        return tool(**kwargs)
    else:
        raise ValueError("Tool is not callable")

class EchoRequest(BaseModel):
    message: str = Field(..., description="Message to echo (e.g., 'Hello World')")

@router.post(
    "/echo",
    summary="Echo a message",
    description=(
        "Purpose: Echoes back the provided message.\n\n"
        "Sample Input: { 'message': 'Hello World' }\n"
        "Sample Output: { 'result': 'Echo: Hello World' }"
    )
)
async def echo_endpoint(request: EchoRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(echo, message=request.message)
    return {"result": result}
