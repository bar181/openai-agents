from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List
import json
import anyio
from app.dependencies import verify_api_key
from app.tools.visualization_tools import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_scatter_plot,
)

router = APIRouter(tags=["Visualization Tools"])

# Helper function to call a tool (synchronous tools are assumed to have a callable .function attribute)
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

# -----------------------------------------------------------
# Bar Chart Endpoint
# -----------------------------------------------------------
class BarChartRequest(BaseModel):
    labels: List[str] = Field(..., description="List of labels for the bar chart (e.g., ['A', 'B', 'C'])")
    values: List[float] = Field(..., description="List of numerical values (e.g., [1, 2, 3])")
    title: str = Field(..., description="Title of the bar chart (e.g., 'Sales Data')")

@router.post(
    "/bar_chart",
    summary="Create Bar Chart",
    description=(
        "Purpose: Generate a bar chart visualization.\n\n"
        "Sample Input: { 'labels': ['A', 'B', 'C'], 'values': [1,2,3], 'title': 'Test Bar Chart' }\n"
        "Sample Output: { 'chart_type': 'bar', 'chart_data': { 'labels': [...], 'values': [...], 'title': 'Test Bar Chart' } }"
    )
)
async def bar_chart_endpoint(request: BarChartRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(create_bar_chart, labels=request.labels, values=request.values, title=request.title)
    return {"result": result}

# -----------------------------------------------------------
# Line Chart Endpoint
# -----------------------------------------------------------
class LineChartRequest(BaseModel):
    x_values: List[float] = Field(..., description="X-axis values (e.g., [1,2,3,4,5])")
    y_values: List[float] = Field(..., description="Y-axis values (e.g., [2,4,6,8,10])")
    title: str = Field(..., description="Title of the line chart (e.g., 'Trend Analysis')")

@router.post(
    "/line_chart",
    summary="Create Line Chart",
    description=(
        "Purpose: Generate a line chart visualization.\n\n"
        "Sample Input: { 'x_values': [1,2,3,4,5], 'y_values': [2,4,6,8,10], 'title': 'Test Line Chart' }\n"
        "Sample Output: { 'chart_type': 'line', 'chart_data': { 'x_values': [...], 'y_values': [...], 'title': 'Test Line Chart' } }"
    )
)
async def line_chart_endpoint(request: LineChartRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(create_line_chart, x_values=request.x_values, y_values=request.y_values, title=request.title)
    return {"result": result}

# -----------------------------------------------------------
# Pie Chart Endpoint
# -----------------------------------------------------------
class PieChartRequest(BaseModel):
    labels: List[str] = Field(..., description="Labels for the pie chart (e.g., ['A', 'B', 'C'])")
    values: List[float] = Field(..., description="Values for each pie slice (e.g., [30, 40, 30])")
    title: str = Field(..., description="Title of the pie chart (e.g., 'Market Share')")

@router.post(
    "/pie_chart",
    summary="Create Pie Chart",
    description=(
        "Purpose: Generate a pie chart visualization.\n\n"
        "Sample Input: { 'labels': ['A', 'B', 'C'], 'values': [30,40,30], 'title': 'Test Pie Chart' }\n"
        "Sample Output: { 'chart_type': 'pie', 'chart_data': { 'labels': [...], 'values': [...], 'title': 'Test Pie Chart' } }"
    )
)
async def pie_chart_endpoint(request: PieChartRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(create_pie_chart, labels=request.labels, values=request.values, title=request.title)
    return {"result": result}

# -----------------------------------------------------------
# Scatter Plot Endpoint
# -----------------------------------------------------------
class ScatterPlotRequest(BaseModel):
    x_values: List[float] = Field(..., description="X-axis values (e.g., [1,2,3,4,5])")
    y_values: List[float] = Field(..., description="Y-axis values (e.g., [2,4,6,8,10])")
    title: str = Field(..., description="Title of the scatter plot (e.g., 'Data Distribution')")

@router.post(
    "/scatter_plot",
    summary="Create Scatter Plot",
    description=(
        "Purpose: Generate a scatter plot visualization.\n\n"
        "Sample Input: { 'x_values': [1,2,3,4,5], 'y_values': [2,4,6,8,10], 'title': 'Test Scatter Plot' }\n"
        "Sample Output: { 'chart_type': 'scatter', 'chart_data': { 'x_values': [...], 'y_values': [...], 'title': 'Test Scatter Plot' } }"
    )
)
async def scatter_plot_endpoint(request: ScatterPlotRequest, api_key: str = Depends(verify_api_key)):
    result = await call_tool(create_scatter_plot, x_values=request.x_values, y_values=request.y_values, title=request.title)
    return {"result": result}
