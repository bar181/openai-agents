from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
import json
import anyio
from app.dependencies import verify_api_key
from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase, concatenate
from app.tools.datetime_tools import current_time, add_days
from app.tools.echo_tools import echo
from app.agents.advanced.multi_tool_agent import multi_tool_agent

router = APIRouter(tags=["Tools"])

async def call_tool(tool, **kwargs):
    """
    Asynchronously call the given tool with provided keyword arguments.
    
    For tools decorated with @function_tool (which have an "on_invoke_tool" attribute),
    serialize the kwargs as JSON and await the async on_invoke_tool function.
    For plain tools with a callable 'function' attribute, call that synchronously.
    Otherwise, if the tool is callable, call it directly.
    """
    if hasattr(tool, "function") and callable(tool.function):
        return tool.function(**kwargs)
    elif hasattr(tool, "on_invoke_tool"):
        ctx = {}  # Empty context for invocation
        args_json = json.dumps(kwargs)
        return await tool.on_invoke_tool(ctx, args_json)
    elif callable(tool):
        return tool(**kwargs)
    else:
        raise ValueError("Tool is not callable")

# --- Math Tools Endpoints ---
class MathRequest(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")

@router.post("/add", summary="Add two numbers", description="Returns the sum of two numbers.")
async def add_endpoint(request: MathRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(add, a=request.a, b=request.b)
    return {"result": result}

@router.post("/multiply", summary="Multiply two numbers", description="Returns the product of two numbers.")
async def multiply_endpoint(request: MathRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(multiply, a=request.a, b=request.b)
    return {"result": result}

# --- String Tools Endpoints ---
class ToUppercaseRequest(BaseModel):
    text: str = Field(..., description="Text to convert to uppercase")

@router.post("/to_uppercase", summary="Convert text to uppercase", description="Converts provided text to uppercase.")
async def to_uppercase_endpoint(request: ToUppercaseRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(to_uppercase, text=request.text)
    return {"result": result}

class ConcatenateRequest(BaseModel):
    text1: str = Field(..., description="First text")
    text2: str = Field(..., description="Second text")

@router.post("/concatenate", summary="Concatenate two texts", description="Concatenates two strings.")
async def concatenate_endpoint(request: ConcatenateRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(concatenate, text1=request.text1, text2=request.text2)
    return {"result": result}

# --- Datetime Tools Endpoints ---
class CurrentTimeResponse(BaseModel):
    current_time: str = Field(..., description="Current UTC time in ISO format")

@router.get("/current_time", summary="Get current UTC time", description="Returns current UTC time as an ISO formatted string.", response_model=CurrentTimeResponse)
async def current_time_endpoint(api_key: str = Depends(verify_api_key)):
    result = await call_tool(current_time)
    return {"current_time": result}

class AddDaysRequest(BaseModel):
    base_date: str = Field(..., description="Base date in ISO format (YYYY-MM-DD or full ISO string)")
    days: int = Field(..., description="Number of days to add")

@router.post("/add_days", summary="Add days to a date", description="Adds a number of days to the provided date.")
async def add_days_endpoint(request: AddDaysRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(add_days, base_date=request.base_date, days=request.days)
    return {"result": result}

# --- Echo Tool Endpoint ---
class EchoRequest(BaseModel):
    message: str = Field(..., description="Message to echo")

@router.post("/echo", summary="Echo a message", description="Echoes back the provided message.")
async def echo_endpoint(request: EchoRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(echo, message=request.message)
    return {"result": result}

# --- Multi-Tool Agent Endpoint ---
class MultiToolRequest(BaseModel):
    input_data: str = Field(..., description="Input string for the multi-tool agent.")

@router.post("/multi-tool", summary="Run multi-tool agent", description="Runs the multi-tool agent with the provided input and aggregates results.")
async def multi_tool_endpoint(request: MultiToolRequest, api_key: str = Depends(verify_api_key)):
    result = multi_tool_agent.run(request.input_data)
    return result
