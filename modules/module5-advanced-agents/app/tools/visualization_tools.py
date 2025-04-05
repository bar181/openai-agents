import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.tools.base_tool import BaseTool, ToolResult
from agents import function_tool


class ChartResult(BaseModel):
    """Result of chart generation."""
    chart_id: str
    url: str
    type: str
    title: Optional[str] = None


@function_tool
def create_bar_chart(data: List[Dict[str, Any]], title: Optional[str] = None) -> ChartResult:
    """Creates a mock bar chart visualization."""
    chart_id = str(uuid.uuid4())
    return ChartResult(
        chart_id=chart_id,
        url=f"mock://charts/bar/{chart_id}",
        type="bar",
        title=title
    )


@function_tool
def create_line_chart(data: List[Dict[str, Any]], title: Optional[str] = None) -> ChartResult:
    """Creates a mock line chart visualization."""
    chart_id = str(uuid.uuid4())
    return ChartResult(
        chart_id=chart_id,
        url=f"mock://charts/line/{chart_id}",
        type="line",
        title=title
    )


@function_tool
def create_pie_chart(data: List[Dict[str, Any]], title: Optional[str] = None) -> ChartResult:
    """Creates a mock pie chart visualization."""
    chart_id = str(uuid.uuid4())
    return ChartResult(
        chart_id=chart_id,
        url=f"mock://charts/pie/{chart_id}",
        type="pie",
        title=title
    )


@function_tool
def create_scatter_plot(x_data: List[float], y_data: List[float], title: Optional[str] = None) -> ChartResult:
    """Creates a mock scatter plot visualization."""
    if len(x_data) != len(y_data):
        raise ValueError("x_data and y_data must have the same length")
    
    chart_id = str(uuid.uuid4())
    return ChartResult(
        chart_id=chart_id,
        url=f"mock://charts/scatter/{chart_id}",
        type="scatter",
        title=title
    )


class VisualizationTool(BaseTool):
    """Tool for data visualization operations."""
    
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        if "operation" not in kwargs:
            return False
        
        operation = kwargs["operation"]
        
        if operation in ["bar", "line", "pie"]:
            return "data" in kwargs and isinstance(kwargs["data"], list)
        elif operation == "scatter":
            return ("x_data" in kwargs and isinstance(kwargs["x_data"], list) and
                    "y_data" in kwargs and isinstance(kwargs["y_data"], list))
        
        return False
    
    def execute(self, **kwargs) -> ToolResult:
        """Executes the visualization tool operation."""
        try:
            operation = kwargs["operation"]
            title = kwargs.get("title")
            
            if operation == "bar":
                result = create_bar_chart(kwargs["data"], title)
                return ToolResult(success=True, data=result)
            
            elif operation == "line":
                result = create_line_chart(kwargs["data"], title)
                return ToolResult(success=True, data=result)
            
            elif operation == "pie":
                result = create_pie_chart(kwargs["data"], title)
                return ToolResult(success=True, data=result)
            
            elif operation == "scatter":
                result = create_scatter_plot(kwargs["x_data"], kwargs["y_data"], title)
                return ToolResult(success=True, data=result)
            
            return ToolResult(
                success=False,
                error=f"Unknown operation: {operation}"
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing visualization tool: {str(e)}"
            )
    
    @property
    def description(self) -> str:
        """Returns tool description."""
        return (
            "Creates mock data visualizations. "
            "Operations: bar, line, pie, scatter."
        )