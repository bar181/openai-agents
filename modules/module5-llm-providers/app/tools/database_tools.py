from typing import Dict, Any, List, Optional
from app.tools.base_tool import BaseTool, ToolResult
from agents import function_tool


# Mock in-memory database
_mock_db: Dict[str, Any] = {}


@function_tool
def store_data(key: str, value: Any) -> bool:
    """Stores data in mock database."""
    try:
        _mock_db[key] = value
        return True
    except Exception:
        return False


@function_tool
def retrieve_data(key: str) -> Any:
    """Retrieves data from mock database."""
    return _mock_db.get(key)


@function_tool
def list_keys() -> List[str]:
    """Lists all keys in the mock database."""
    return list(_mock_db.keys())


@function_tool
def delete_data(key: str) -> bool:
    """Deletes data from mock database."""
    if key in _mock_db:
        del _mock_db[key]
        return True
    return False


@function_tool
def clear_database() -> bool:
    """Clears all data from mock database."""
    _mock_db.clear()
    return True


class DatabaseTool(BaseTool):
    """Tool for mock database operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation == "store":
            return "key" in kwargs and "value" in kwargs
        elif operation == "retrieve":
            return "key" in kwargs
        elif operation == "list":
            return True
        elif operation == "delete":
            return "key" in kwargs
        elif operation == "clear":
            return True
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the database tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "store":
                result = store_data(kwargs["key"], kwargs["value"])
                return ToolResult(
                    success=result,
                    data={"stored": result}
                )
            
            elif operation == "retrieve":
                result = retrieve_data(kwargs["key"])
                return ToolResult(
                    success=True,
                    data=result
                )
            
            elif operation == "list":
                result = list_keys()
                return ToolResult(
                    success=True,
                    data=result
                )
            
            elif operation == "delete":
                result = delete_data(kwargs["key"])
                return ToolResult(
                    success=result,
                    data={"deleted": result}
                )
            
            elif operation == "clear":
                result = clear_database()
                return ToolResult(
                    success=result,
                    data={"cleared": result}
                )
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing database tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Performs mock database operations for storing and retrieving data. "
            "Operations: store, retrieve, list, delete, clear."
        )