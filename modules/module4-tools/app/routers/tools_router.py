from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.dependencies import verify_api_key

# Import sample tools from the tools package
from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase, concatenate
# (Import additional tools as needed)

router = APIRouter(tags=["Tools"])

# --- Math Tools Endpoints ---
class MathOperationRequest(BaseModel):
    a: float
    b: float

@router.post("/add", summary="Add two numbers", description="Returns the sum of two numbers.")
async def add_numbers(request: MathOperationRequest, api_key: str = Depends(verify_api_key)):
    result = add.function(a=request.a, b=request.b)
    return {"result": result}

@router.post("/multiply", summary="Multiply two numbers", description="Returns the product of two numbers.")
async def multiply_numbers(request: MathOperationRequest, api_key: str = Depends(verify_api_key)):
    result = multiply.function(a=request.a, b=request.b)
    return {"result": result}

# --- String Tools Endpoints ---
class StringOperationRequest(BaseModel):
    text: str

@router.post("/to_uppercase", summary="Convert text to uppercase", description="Returns the input text in uppercase.")
async def uppercase_text(request: StringOperationRequest, api_key: str = Depends(verify_api_key)):
    result = to_uppercase.function(text=request.text)
    return {"result": result}

class ConcatenateRequest(BaseModel):
    text1: str
    text2: str

@router.post("/concatenate", summary="Concatenate two strings", description="Returns the concatenated result of two strings.")
async def concatenate_text(request: ConcatenateRequest, api_key: str = Depends(verify_api_key)):
    result = concatenate.function(text1=request.text1, text2=request.text2)
    return {"result": result}

# --- Multi-Tool Agent Endpoint ---
class MultiToolRequest(BaseModel):
    input_text: str

@router.post(
    "/multi-tool",
    summary="Multi-tool agent",
    description="Executes the multi-tool agent to process the input using multiple tools."
)
async def multi_tool(request: MultiToolRequest, api_key: str = Depends(verify_api_key)):
    # For now, return a placeholder response.
    # Later, this endpoint will call a multi-tool agent that orchestrates several tools.
    return {"final_output": f"Processed input: {request.input_text} with multiple tools."}
