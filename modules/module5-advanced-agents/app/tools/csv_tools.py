import csv
from io import StringIO
from typing import Dict, Any, List, Optional
from app.tools.base_tool import BaseTool, ToolResult
from agents import function_tool


@function_tool
def parse_csv(content: str, has_header: bool = True) -> List[Dict[str, Any]]:
    """Parses CSV content into structured data."""
    try:
        csv_file = StringIO(content)
        if has_header:
            reader = csv.DictReader(csv_file)
            return [row for row in reader]
        else:
            reader = csv.reader(csv_file)
            rows = [row for row in reader]
            return [{"column_" + str(i): value for i, value in enumerate(row)} for row in rows]
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")


@function_tool
def generate_csv(data: List[Dict[str, Any]], include_header: bool = True) -> str:
    """Generates CSV from structured data."""
    if not data:
        return ""
    
    output = StringIO()
    fieldnames = data[0].keys()
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    if include_header:
        writer.writeheader()
    
    writer.writerows(data)
    return output.getvalue()


class CsvTool(BaseTool):
    """Tool for CSV processing operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation == "parse":
            return "content" in kwargs
        elif operation == "generate":
            return "data" in kwargs and isinstance(kwargs["data"], list)
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the CSV tool operation."""
        try:
            operation = kwargs["operation"]
            
            if operation == "parse":
                has_header = kwargs.get("has_header", True)
                result = parse_csv(kwargs["content"], has_header)
                return ToolResult(success=True, data=result)
            
            elif operation == "generate":
                include_header = kwargs.get("include_header", True)
                result = generate_csv(kwargs["data"], include_header)
                return ToolResult(success=True, data=result)
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing CSV tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Processes CSV data with operations like parsing and generation. "
            "Operations: parse, generate."
        )