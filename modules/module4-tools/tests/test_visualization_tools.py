"""
Test module for the visualization tool implementations.

This module tests the following visualization tools:
- create_bar_chart
- create_line_chart
- create_pie_chart
- create_scatter_plot
"""

from app.tools.visualization_tools import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_scatter_plot,
)

def test_create_bar_chart_tool():
    """Test the create_bar_chart tool."""
    result = create_bar_chart.function(
        labels=["A", "B", "C"],
        values=[1, 2, 3],
        title="Test Bar Chart"
    )
    assert "chart_data" in result
    assert result["chart_type"] == "bar"

def test_create_line_chart_tool():
    """Test the create_line_chart tool."""
    result = create_line_chart.function(
        x_values=[1, 2, 3, 4, 5],
        y_values=[2, 4, 6, 8, 10],
        title="Test Line Chart"
    )
    assert "chart_data" in result
    assert result["chart_type"] == "line"

def test_create_pie_chart_tool():
    """Test the create_pie_chart tool."""
    result = create_pie_chart.function(
        labels=["A", "B", "C"],
        values=[30, 40, 30],
        title="Test Pie Chart"
    )
    assert "chart_data" in result
    assert result["chart_type"] == "pie"

def test_create_scatter_plot_tool():
    """Test the create_scatter_plot tool."""
    result = create_scatter_plot.function(
        x_values=[1, 2, 3, 4, 5],
        y_values=[2, 4, 6, 8, 10],
        title="Test Scatter Plot"
    )
    assert "chart_data" in result
    assert result["chart_type"] == "scatter"
