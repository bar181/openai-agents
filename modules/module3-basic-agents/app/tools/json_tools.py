from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ValidationError
from app.tools.base_tool import BaseTool, ToolResult
from agents import function_tool


class ValidationResult(BaseModel):
    """Result of JSON validation."""
    is_valid: bool
    errors: Optional[List[str]] = None


@function_tool
def validate_json(data: Dict[str, Any]) -> ValidationResult:
    """Validates JSON data structure."""
    try:
        # Simple validation - just check if it's a valid dict
        if not isinstance(data, dict):
            return ValidationResult(is_valid=False, errors=["Input is not a valid JSON object"])
        return ValidationResult(is_valid=True)
    except Exception as e:
        return ValidationResult(is_valid=False, errors=[str(e)])


@function_tool
def transform_json(data: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
    """Transforms JSON according to template."""
    result = {}
    
    # Apply template transformations
    for key, value in template.items():
        if key in data:
            # If template value is a string starting with "$", it's a reference to another field
            if isinstance(value, str) and value.startswith("$"):
                field_ref = value[1:]
                if field_ref in data:
                    result[key] = data[field_ref]
            # If template value is a dict, recursively transform
            elif isinstance(value, dict) and isinstance(data[key], dict):
                result[key] = transform_json(data[key], value)
            # Otherwise, use the template value directly
            else:
                result[key] = data[key]
    
    return result


class JsonTool(BaseTool):
    """Tool for JSON processing operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation == "validate":
            return "data" in kwargs
        elif operation == "transform":
            return "data" in kwargs and "template" in kwargs
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the JSON tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "validate":
                result = validate_json(kwargs["data"])
                return ToolResult(success=True, data=result)
            
            elif operation == "transform":
                result = transform_json(kwargs["data"], kwargs["template"])
                return ToolResult(success=True, data=result)
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing JSON tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Processes JSON data with operations like validation and transformation. "
            "Operations: validate, transform."
        )