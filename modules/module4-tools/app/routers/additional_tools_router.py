from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List, Any
import json
import anyio
from app.dependencies import verify_api_key
from app.tools.data_tools import get_item, summarize_list, fetch_mock_data
from app.tools.json_tools import validate_json, transform_json
from app.tools.csv_tools import parse_csv, generate_csv
from app.tools.analysis_tools import (
    analyze_sentiment, extract_entities, extract_keywords,
    calculate_basic_stats, perform_correlation, find_patterns, apply_regex
)
from app.tools.api_tools import make_request, cache_get, cache_set, check_rate_limit

router = APIRouter(tags=["Tools Additional"])

# -----------------------------------------------------------
# Helper: call_tool
# -----------------------------------------------------------
async def call_tool(tool, **kwargs):
    """
    Asynchronously call the given tool with provided keyword arguments.
    
    For tools decorated with @function_tool (which have an "on_invoke_tool" attribute),
    serialize the kwargs as JSON and await the async on_invoke_tool function.
    For plain tools with a callable 'function' attribute, call that.
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
# Data Tools Endpoints
# -----------------------------------------------------------
class GetItemRequest(BaseModel):
    items: List[str] = Field(..., description="List of items (e.g., ['a', 'b', 'c'])")
    index: int = Field(..., description="Index of desired item (e.g., 1)")

@router.post(
    "/get_item",
    summary="Get an item from a list",
    description=(
        "Purpose: Retrieve an item from a list at a given index.\n\n"
        "Sample Input: { 'items': ['a', 'b', 'c'], 'index': 1 }\n"
        "Sample Output: { 'result': 'b' }"
    )
)
async def get_item_endpoint(request: GetItemRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(get_item, items=request.items, index=request.index)
    return {"result": result}

class SummarizeListRequest(BaseModel):
    items: List[float] = Field(..., description="List of numbers (e.g., [1, 2, 3, 4, 5])")

@router.post(
    "/summarize_list",
    summary="Summarize a list of numbers",
    description=(
        "Purpose: Compute statistics (count, min, max, average) for a list of numbers.\n\n"
        "Sample Input: { 'items': [1,2,3,4,5] }\n"
        "Sample Output: { 'result': { 'count': 5, 'min': 1, 'max': 5, 'average': 3.0 } }"
    )
)
async def summarize_list_endpoint(request: SummarizeListRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(summarize_list, items=request.items)
    return {"result": result}

class FetchMockDataRequest(BaseModel):
    source: str = Field(..., description="Data source identifier (e.g., 'source1')")

@router.post(
    "/fetch_mock_data",
    summary="Fetch mock data from a source",
    description=(
        "Purpose: Retrieve mock data based on a provided source identifier.\n\n"
        "Sample Input: { 'source': 'source1' }\n"
        "Sample Output: { 'result': 'sample data from source1' }"
    )
)
async def fetch_mock_data_endpoint(request: FetchMockDataRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(fetch_mock_data, source=request.source)
    return {"result": result}

# -----------------------------------------------------------
# JSON Tools Endpoints
# -----------------------------------------------------------
class ValidateJsonRequest(BaseModel):
    json_str: str = Field(..., description="JSON string to validate (e.g., '{\"name\": \"test\"}')")

@router.post(
    "/validate_json",
    summary="Validate JSON string",
    description=(
        "Purpose: Check if a given string is valid JSON.\n\n"
        "Sample Input: { 'json_str': '{\"name\": \"test\", \"value\": 123}' }\n"
        "Sample Output: { 'result': { 'valid': true } }"
    )
)
async def validate_json_endpoint(request: ValidateJsonRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(validate_json, json_str=request.json_str)
    return {"result": result}

class TransformJsonRequest(BaseModel):
    json_str: str = Field(..., description="JSON string to transform")
    transformation: str = Field(..., description="Transformation type (e.g., 'uppercase_keys')")

@router.post(
    "/transform_json",
    summary="Transform JSON data",
    description=(
        "Purpose: Apply a transformation to JSON data (e.g., convert keys to uppercase).\n\n"
        "Sample Input: { 'json_str': '{\"name\": \"test\", \"value\": 123}', 'transformation': 'uppercase_keys' }\n"
        "Sample Output: { 'result': { 'NAME': 'test', 'VALUE': 123 } }"
    )
)
async def transform_json_endpoint(request: TransformJsonRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(transform_json, json_str=request.json_str, transformation=request.transformation)
    return {"result": result}

# -----------------------------------------------------------
# CSV Tools Endpoints
# -----------------------------------------------------------
class ParseCsvRequest(BaseModel):
    csv_str: str = Field(..., description="CSV data as a string (e.g., 'name,age\\nJohn,30')")

@router.post(
    "/parse_csv",
    summary="Parse CSV data",
    description=(
        "Purpose: Convert a CSV-formatted string into a list of dictionaries.\n\n"
        "Sample Input: { 'csv_str': 'name,age\\nJohn,30\\nJane,25' }\n"
        "Sample Output: { 'result': [{ 'name': 'John', 'age': '30' }, { 'name': 'Jane', 'age': '25' }] }"
    )
)
async def parse_csv_endpoint(request: ParseCsvRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(parse_csv, csv_str=request.csv_str)
    return {"result": result}

class GenerateCsvRequest(BaseModel):
    data: List[dict] = Field(..., description="List of dictionaries to convert to CSV.")

@router.post(
    "/generate_csv",
    summary="Generate CSV data",
    description=(
        "Purpose: Convert a list of dictionaries into a CSV-formatted string.\n\n"
        "Sample Input: { 'data': [ { 'name': 'John', 'age': 30 }, { 'name': 'Jane', 'age': 25 } ] }\n"
        "Sample Output: A CSV string with headers and rows."
    )
)
async def generate_csv_endpoint(request: GenerateCsvRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(generate_csv, data=request.data)
    return {"result": result}

# -----------------------------------------------------------
# Analysis Tools Endpoints
# -----------------------------------------------------------
class TextRequest(BaseModel):
    text: str = Field(..., description="Input text for analysis (e.g., 'Great product!')")

@router.post(
    "/analyze_sentiment",
    summary="Analyze sentiment",
    description=(
        "Purpose: Analyze the sentiment of the input text.\n\n"
        "Sample Input: { 'text': 'Great product!' }\n"
        "Sample Output: { 'result': { 'sentiment': 'positive' } }"
    )
)
async def analyze_sentiment_endpoint(request: TextRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(analyze_sentiment, text=request.text)
    return {"result": result}

@router.post(
    "/extract_entities",
    summary="Extract entities",
    description=(
        "Purpose: Extract named entities (e.g., PERSON, ORG, GPE) from text.\n\n"
        "Sample Input: { 'text': 'John Smith works at Microsoft in Seattle.' }\n"
        "Sample Output: { 'result': { 'entities': [ ... ] } }"
    )
)
async def extract_entities_endpoint(request: TextRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(extract_entities, text=request.text)
    return {"result": result}

@router.post(
    "/extract_keywords",
    summary="Extract keywords",
    description=(
        "Purpose: Extract keywords from text.\n\n"
        "Sample Input: { 'text': 'Artificial intelligence is transforming the technology industry.' }\n"
        "Sample Output: { 'result': { 'keywords': [ 'artificial', 'intelligence', 'technology', ... ] } }"
    )
)
async def extract_keywords_endpoint(request: TextRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(extract_keywords, text=request.text)
    return {"result": result}

class BasicStatsRequest(BaseModel):
    data: List[float] = Field(..., description="List of numeric values (e.g., [1,2,3,4,5])")

@router.post(
    "/calculate_basic_stats",
    summary="Calculate basic statistics",
    description=(
        "Purpose: Calculate statistical measures (mean, median, mode, standard deviation) from a list of numbers.\n\n"
        "Sample Input: { 'data': [1,2,3,4,5] }\n"
        "Sample Output: { 'result': { 'mean': 3.0, 'median': 3.0, ... } }"
    )
)
async def calculate_basic_stats_endpoint(request: BasicStatsRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(calculate_basic_stats, data=request.data)
    return {"result": result}

class PerformCorrelationRequest(BaseModel):
    x: List[float] = Field(..., description="List of x values (e.g., [1,2,3,4,5])")
    y: List[float] = Field(..., description="List of y values (e.g., [2,4,6,8,10])")

@router.post(
    "/perform_correlation",
    summary="Perform correlation",
    description=(
        "Purpose: Calculate the correlation coefficient between two lists of numbers.\n\n"
        "Sample Input: { 'x': [1,2,3,4,5], 'y': [2,4,6,8,10] }\n"
        "Sample Output: { 'result': { 'correlation': 1.0 } }"
    )
)
async def perform_correlation_endpoint(request: PerformCorrelationRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(perform_correlation, x=request.x, y=request.y)
    return {"result": result}

class FindPatternsRequest(BaseModel):
    data: List[int] = Field(..., description="List of integers to search for patterns")

@router.post(
    "/find_patterns",
    summary="Find patterns in data",
    description=(
        "Purpose: Identify repeating patterns in a list of integers.\n\n"
        "Sample Input: { 'data': [1,2,3,1,2,3,1,2,3] }\n"
        "Sample Output: { 'result': { 'patterns': [[1,2,3]] } }"
    )
)
async def find_patterns_endpoint(request: FindPatternsRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(find_patterns, data=request.data)
    return {"result": result}

class ApplyRegexRequest(BaseModel):
    text: str = Field(..., description="Input text containing potential matches")
    pattern: str = Field(..., description="Regex pattern to apply (e.g., '\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b')")

@router.post(
    "/apply_regex",
    summary="Apply regex to text",
    description=(
        "Purpose: Extract all matches of a regex pattern from the given text.\n\n"
        "Sample Input: { 'text': 'Contact us at info@example.com', 'pattern': '\\\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Z|a-z]{2,}\\\\b' }\n"
        "Sample Output: { 'result': { 'matches': ['info@example.com'] } }"
    )
)
async def apply_regex_endpoint(request: ApplyRegexRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(apply_regex, text=request.text, pattern=request.pattern)
    return {"result": result}

# -----------------------------------------------------------
# API Tools Endpoints
# -----------------------------------------------------------
class MakeRequestRequest(BaseModel):
    url: str = Field(..., description="URL to request (e.g., 'https://jsonplaceholder.typicode.com/todos/1')")
    method: str = Field(..., description="HTTP method (e.g., 'GET')")

@router.post(
    "/make_request",
    summary="Make an HTTP request",
    description=(
        "Purpose: Perform an HTTP request to the specified URL using the given method.\n\n"
        "Sample Input: { 'url': 'https://jsonplaceholder.typicode.com/todos/1', 'method': 'GET' }\n"
        "Sample Output: A JSON response from the target URL."
    )
)
async def make_request_endpoint(request: MakeRequestRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(make_request, url=request.url, method=request.method)
    return {"result": result}

class CacheSetRequest(BaseModel):
    key: str = Field(..., description="Cache key (e.g., 'test_cache_key')")
    value: Any = Field(..., description="Value to cache (e.g., 'test_cache_value')")
    ttl: int = Field(..., description="Time to live in seconds (e.g., 60)")

@router.post(
    "/cache_set",
    summary="Set a cache value",
    description=(
        "Purpose: Store a value in the cache with a specified TTL.\n\n"
        "Sample Input: { 'key': 'test_cache_key', 'value': 'test_cache_value', 'ttl': 60 }\n"
        "Sample Output: { 'result': { 'success': true } }"
    )
)
async def cache_set_endpoint(request: CacheSetRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(cache_set, key=request.key, value=request.value, ttl=request.ttl)
    return {"result": result}

class CacheGetRequest(BaseModel):
    key: str = Field(..., description="Cache key to retrieve (e.g., 'test_cache_key')")

@router.post(
    "/cache_get",
    summary="Get a cache value",
    description=(
        "Purpose: Retrieve a value from the cache using its key.\n\n"
        "Sample Input: { 'key': 'test_cache_key' }\n"
        "Sample Output: { 'result': { 'success': true, 'value': 'test_cache_value' } }"
    )
)
async def cache_get_endpoint(request: CacheGetRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(cache_get, key=request.key)
    return {"result": result}

class CheckRateLimitRequest(BaseModel):
    key: str = Field(..., description="Rate limit key (e.g., 'test_rate_limit')")
    max_requests: int = Field(..., description="Maximum allowed requests (e.g., 5)")
    window_seconds: int = Field(..., description="Time window in seconds (e.g., 60)")

@router.post(
    "/check_rate_limit",
    summary="Check rate limit",
    description=(
        "Purpose: Verify if the rate limit allows further requests based on a key, max requests, and time window.\n\n"
        "Sample Input: { 'key': 'test_rate_limit', 'max_requests': 5, 'window_seconds': 60 }\n"
        "Sample Output: { 'result': { 'allowed': true, 'remaining': 4 } }"
    )
)
async def check_rate_limit_endpoint(request: CheckRateLimitRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(check_rate_limit, key=request.key, max_requests=request.max_requests, window_seconds=request.window_seconds)
    return {"result": result}
