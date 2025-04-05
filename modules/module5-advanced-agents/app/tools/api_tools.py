import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.tools.base_tool import BaseTool, ToolResult
from agents import function_tool


class Response(BaseModel):
    """Mock API response."""
    status_code: int
    headers: Dict[str, str]
    body: Any


# Mock rate limiter
class _RateLimiter:
    def __init__(self):
        self._request_counts: Dict[str, List[float]] = {}
        self._window_size = 60  # 1 minute window
        self._max_requests = 10  # 10 requests per minute
    
    def check_limit(self, key: str) -> bool:
        """Check if rate limit is exceeded."""
        now = time.time()
        
        # Initialize if key doesn't exist
        if key not in self._request_counts:
            self._request_counts[key] = []
        
        # Remove timestamps outside the window
        self._request_counts[key] = [t for t in self._request_counts[key] if now - t < self._window_size]
        
        # Check if limit is exceeded
        return len(self._request_counts[key]) < self._max_requests
    
    def update_count(self, key: str) -> None:
        """Update request count."""
        now = time.time()
        
        # Initialize if key doesn't exist
        if key not in self._request_counts:
            self._request_counts[key] = []
        
        # Add current timestamp
        self._request_counts[key].append(now)


# Mock cache
class _Cache:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        # Check if entry is expired
        if entry["expires"] < time.time():
            del self._cache[key]
            return None
        
        return entry["value"]
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache with TTL."""
        self._cache[key] = {
            "value": value,
            "expires": time.time() + ttl
        }


# Singleton instances
_rate_limiter = _RateLimiter()
_cache = _Cache()


@function_tool
def make_request(url: str, method: str = "GET", headers: Dict[str, str] = None, data: Any = None) -> Response:
    """Makes a mock HTTP request."""
    # Check rate limit
    if not _rate_limiter.check_limit(url):
        return Response(
            status_code=429,
            headers={"Content-Type": "application/json"},
            body={"error": "Rate limit exceeded"}
        )
    
    # Update rate limit counter
    _rate_limiter.update_count(url)
    
    # Generate mock response based on URL and method
    if url.startswith("https://api.example.com/data"):
        return Response(
            status_code=200,
            headers={"Content-Type": "application/json"},
            body={"data": "Sample data from API", "timestamp": time.time()}
        )
    elif url.startswith("https://api.example.com/users"):
        return Response(
            status_code=200,
            headers={"Content-Type": "application/json"},
            body={"users": [{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}]}
        )
    elif url.startswith("https://api.example.com/error"):
        return Response(
            status_code=500,
            headers={"Content-Type": "application/json"},
            body={"error": "Internal server error"}
        )
    else:
        return Response(
            status_code=404,
            headers={"Content-Type": "application/json"},
            body={"error": "Not found"}
        )


@function_tool
def cache_get(key: str) -> Optional[Any]:
    """Gets a value from the cache."""
    return _cache.get(key)


@function_tool
def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """Sets a value in the cache with TTL."""
    try:
        _cache.set(key, value, ttl)
        return True
    except Exception:
        return False


@function_tool
def check_rate_limit(key: str) -> bool:
    """Checks if rate limit is exceeded."""
    return _rate_limiter.check_limit(key)


class ApiTool(BaseTool):
    """Tool for API operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation == "request":
            return "url" in kwargs
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the API tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "request":
                method = kwargs.get("method", "GET")
                headers = kwargs.get("headers", {})
                data = kwargs.get("data", None)
                
                result = make_request(kwargs["url"], method, headers, data)
                return ToolResult(success=result.status_code < 400, data=result)
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing API tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Makes mock HTTP requests to APIs. "
            "Operations: request."
        )


class CacheTool(BaseTool):
    """Tool for cache operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation == "get":
            return "key" in kwargs
        elif operation == "set":
            return "key" in kwargs and "value" in kwargs
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the cache tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "get":
                result = cache_get(kwargs["key"])
                return ToolResult(success=True, data=result)
            
            elif operation == "set":
                ttl = kwargs.get("ttl", 3600)
                result = cache_set(kwargs["key"], kwargs["value"], ttl)
                return ToolResult(success=result, data={"cached": result})
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing cache tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Manages cache for storing and retrieving data with TTL. "
            "Operations: get, set."
        )


class RateLimiterTool(BaseTool):
    """Tool for rate limiting operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation == "check":
            return "key" in kwargs
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the rate limiter tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "check":
                result = check_rate_limit(kwargs["key"])
                return ToolResult(
                    success=True,
                    data={"allowed": result}
                )
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing rate limiter tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Manages rate limiting for API requests. "
            "Operations: check."
        )