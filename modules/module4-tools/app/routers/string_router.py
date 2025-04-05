from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.tools.string_tools import to_uppercase, concatenate
import anyio
import json

router = APIRouter(tags=["String Tools"])

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

class ToUppercaseRequest(BaseModel):
    text: str = Field(..., description="Text to convert to uppercase (e.g., 'hello')")

@router.post(
    "/to_uppercase",
    summary="Convert text to uppercase",
    description=(
        "Purpose: Converts provided text to uppercase.\n\n"
        "Sample Input: { 'text': 'hello' }\n"
        "Sample Output: { 'result': 'HELLO' }"
    )
)
async def to_uppercase_endpoint(request: ToUppercaseRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(to_uppercase, text=request.text)
    return {"result": result}

class ConcatenateRequest(BaseModel):
    text1: str = Field(..., description="First text (e.g., 'hello')")
    text2: str = Field(..., description="Second text (e.g., 'world')")

@router.post(
    "/concatenate",
    summary="Concatenate two texts",
    description=(
        "Purpose: Concatenates two strings.\n\n"
        "Sample Input: { 'text1': 'hello', 'text2': 'world' }\n"
        "Sample Output: { 'result': 'helloworld' }"
    )
)
async def concatenate_endpoint(request: ConcatenateRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(concatenate, text1=request.text1, text2=request.text2)
    return {"result": result}
