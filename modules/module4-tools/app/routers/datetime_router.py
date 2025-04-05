from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.tools.datetime_tools import current_time, add_days
import anyio
import json
from datetime import datetime

router = APIRouter(tags=["Tools Datetime"])

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

class CurrentTimeResponse(BaseModel):
    current_time: str = Field(..., description="Current UTC time in ISO 8601 format (e.g., '2023-04-11T12:34:56.789012+00:00')")

@router.get(
    "/current_time",
    summary="Get current UTC time",
    description=(
        "Purpose: Returns current UTC time as an ISO formatted string.\n\n"
        "Sample Output: { 'current_time': '2023-04-11T12:34:56.789012+00:00' }"
    ),
    response_model=CurrentTimeResponse
)
async def current_time_endpoint(api_key: str = Depends(verify_api_key)):
    result = await call_tool(current_time)
    return {"current_time": result}

class AddDaysRequest(BaseModel):
    base_date: str = Field(..., description="Base date in ISO format (e.g., '2023-01-01')")
    days: int = Field(..., description="Number of days to add (e.g., 5)")

@router.post(
    "/add_days",
    summary="Add days to a date",
    description=(
        "Purpose: Adds a specified number of days to the provided base date.\n\n"
        "Sample Input: { 'base_date': '2023-01-01', 'days': 5 }\n"
        "Sample Output: { 'result': '2023-01-06T...' } (ISO formatted date)"
    )
)
async def add_days_endpoint(request: AddDaysRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(add_days, base_date=request.base_date, days=request.days)
    return {"result": result}
