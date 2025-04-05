from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List, Any
import json
from app.dependencies import verify_api_key
from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase, concatenate
from app.tools.datetime_tools import current_time, add_days
from app.tools.echo_tools import echo
from app.tools.data_tools import get_item, summarize_list, fetch_mock_data
from app.tools.json_tools import validate_json, transform_json
from app.tools.csv_tools import parse_csv, generate_csv
from app.tools.analysis_tools import (
    analyze_sentiment, extract_entities, extract_keywords,
    calculate_basic_stats, perform_correlation, find_patterns, apply_regex
)
from app.tools.api_tools import make_request, cache_get, cache_set, check_rate_limit
from app.agents.advanced.multi_tool_agent import multi_tool_agent

import anyio

router = APIRouter(tags=["Tools"])

# -----------------------------------------------------------
# Helper: call_tool
# -----------------------------------------------------------
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
        ctx = {}
        args_json = json.dumps(kwargs)
        return await tool.on_invoke_tool(ctx, args_json)
    elif callable(tool):
        return tool(**kwargs)
    else:
        raise ValueError("Tool is not callable")

# -----------------------------------------------------------
# Existing Endpoints (Math, String, Datetime, Echo, Multi-Tool)
# -----------------------------------------------------------
# (Assumes you already have endpoints for /tools/add, /tools/multiply, etc.)

# -----------------------------------------------------------
# Data Tools Endpoints
# -----------------------------------------------------------
class GetItemRequest(BaseModel):
    items: List[str] = Field(..., description="List of items")
    index: int = Field(..., description="Index of desired item")

@router.post("/get_item", summary="Get an item from a list")
async def get_item_endpoint(request: GetItemRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(get_item, items=request.items, index=request.index)
    return {"result": result}

class SummarizeListRequest(BaseModel):
    items: List[float] = Field(..., description="List of numeric values")

@router.post("/summarize_list", summary="Summarize a list of numbers")
async def summarize_list_endpoint(request: SummarizeListRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(summarize_list, items=request.items)
    return {"result": result}

class FetchMockDataRequest(BaseModel):
    source: str = Field(..., description="Data source identifier")

@router.post("/fetch_mock_data", summary="Fetch mock data from a source")
async def fetch_mock_data_endpoint(request: FetchMockDataRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(fetch_mock_data, source=request.source)
    return {"result": result}

# -----------------------------------------------------------
# JSON Tools Endpoints
# -----------------------------------------------------------
class ValidateJsonRequest(BaseModel):
    json_str: str = Field(..., description="JSON string to validate")

@router.post("/validate_json", summary="Validate JSON string")
async def validate_json_endpoint(request: ValidateJsonRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(validate_json, json_str=request.json_str)
    return {"result": result}

class TransformJsonRequest(BaseModel):
    json_str: str = Field(..., description="JSON string to transform")
    transformation: str = Field(..., description="Transformation type (e.g. 'uppercase_keys')")

@router.post("/transform_json", summary="Transform JSON data")
async def transform_json_endpoint(request: TransformJsonRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(transform_json, json_str=request.json_str, transformation=request.transformation)
    return {"result": result}

# -----------------------------------------------------------
# CSV Tools Endpoints
# -----------------------------------------------------------
class ParseCsvRequest(BaseModel):
    csv_str: str = Field(..., description="CSV data as a string")

@router.post("/parse_csv", summary="Parse CSV data")
async def parse_csv_endpoint(request: ParseCsvRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(parse_csv, csv_str=request.csv_str)
    return {"result": result}

class GenerateCsvRequest(BaseModel):
    data: List[dict] = Field(..., description="List of dict rows to convert to CSV")

@router.post("/generate_csv", summary="Generate CSV data")
async def generate_csv_endpoint(request: GenerateCsvRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(generate_csv, data=request.data)
    return {"result": result}

# -----------------------------------------------------------
# Analysis Tools Endpoints
# -----------------------------------------------------------
class TextRequest(BaseModel):
    text: str = Field(..., description="Input text")

@router.post("/analyze_sentiment", summary="Analyze sentiment")
async def analyze_sentiment_endpoint(request: TextRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(analyze_sentiment, text=request.text)
    return {"result": result}

@router.post("/extract_entities", summary="Extract entities")
async def extract_entities_endpoint(request: TextRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(extract_entities, text=request.text)
    return {"result": result}

@router.post("/extract_keywords", summary="Extract keywords")
async def extract_keywords_endpoint(request: TextRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(extract_keywords, text=request.text)
    return {"result": result}

class BasicStatsRequest(BaseModel):
    data: List[float] = Field(..., description="List of numeric values")

@router.post("/calculate_basic_stats", summary="Calculate basic statistics")
async def calculate_basic_stats_endpoint(request: BasicStatsRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(calculate_basic_stats, data=request.data)
    return {"result": result}

class PerformCorrelationRequest(BaseModel):
    x: List[float] = Field(..., description="List of x values")
    y: List[float] = Field(..., description="List of y values")

@router.post("/perform_correlation", summary="Perform correlation")
async def perform_correlation_endpoint(request: PerformCorrelationRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(perform_correlation, x=request.x, y=request.y)
    return {"result": result}

class FindPatternsRequest(BaseModel):
    data: List[int] = Field(..., description="List of integers to check for patterns")

@router.post("/find_patterns", summary="Find patterns in data")
async def find_patterns_endpoint(request: FindPatternsRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(find_patterns, data=request.data)
    return {"result": result}

class ApplyRegexRequest(BaseModel):
    text: str = Field(..., description="Input text")
    pattern: str = Field(..., description="Regex pattern")

@router.post("/apply_regex", summary="Apply regex pattern to text")
async def apply_regex_endpoint(request: ApplyRegexRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(apply_regex, text=request.text, pattern=request.pattern)
    return {"result": result}

# -----------------------------------------------------------
# API Tools Endpoints
# -----------------------------------------------------------
class MakeRequestRequest(BaseModel):
    url: str = Field(..., description="URL to request")
    method: str = Field(..., description="HTTP method (GET, POST, etc.)")

@router.post("/make_request", summary="Make an HTTP request")
async def make_request_endpoint(request: MakeRequestRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(make_request, url=request.url, method=request.method)
    return {"result": result}

class CacheSetRequest(BaseModel):
    key: str
    value: Any
    ttl: int = Field(..., description="Time to live in seconds")

@router.post("/cache_set", summary="Set a value in cache")
async def cache_set_endpoint(request: CacheSetRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(cache_set, key=request.key, value=request.value, ttl=request.ttl)
    return {"result": result}

class CacheGetRequest(BaseModel):
    key: str

@router.post("/cache_get", summary="Get a value from cache")
async def cache_get_endpoint(request: CacheGetRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(cache_get, key=request.key)
    return {"result": result}

class CheckRateLimitRequest(BaseModel):
    key: str
    max_requests: int
    window_seconds: int

@router.post("/check_rate_limit", summary="Check rate limit")
async def check_rate_limit_endpoint(request: CheckRateLimitRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(check_rate_limit, key=request.key, max_requests=request.max_requests, window_seconds=request.window_seconds)
    return {"result": result}
