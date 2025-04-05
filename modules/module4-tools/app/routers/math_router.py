from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.tools.math_tools import add, multiply
import anyio
import json

router = APIRouter(tags=["Tools Math"])

class MathRequest(BaseModel):
    a: float = Field(..., description="First number (e.g., 2)")
    b: float = Field(..., description="Second number (e.g., 3)")

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

@router.post(
    "/add",
    summary="Add two numbers",
    description=(
        "Purpose: Returns the sum of two numbers.\n\n"
        "Sample Input: { 'a': 2, 'b': 3 }\n"
        "Sample Output: { 'result': 5 }"
    )
)
async def add_endpoint(request: MathRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(add, a=request.a, b=request.b)
    return {"result": result}

@router.post(
    "/multiply",
    summary="Multiply two numbers",
    description=(
        "Purpose: Returns the product of two numbers.\n\n"
        "Sample Input: { 'a': 4, 'b': 5 }\n"
        "Sample Output: { 'result': 20 }"
    )
)
async def multiply_endpoint(request: MathRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(multiply, a=request.a, b=request.b)
    return {"result": result}
