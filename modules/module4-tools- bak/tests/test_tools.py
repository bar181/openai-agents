"""
Test module for the tool implementations.

This module contains tests for the various tools used by the agents,
testing them directly rather than through the agent interfaces.
"""

import pytest
import json
from datetime import datetime, timedelta

from app.tools.base_tool import BaseTool, ToolResult
from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase, concatenate
from app.tools.datetime_tools import current_time, add_days
from app.tools.data_tools import get_item, summarize_list, fetch_mock_data
from app.tools.echo_tools import echo
from app.tools.json_tools import validate_json, transform_json
from app.tools.csv_tools import parse_csv, generate_csv
from app.tools.database_tools import (
    store_data, retrieve_data, list_keys, delete_data, clear_database
)
from app.tools.analysis_tools import (
    analyze_sentiment, extract_entities, extract_keywords,
    calculate_basic_stats, perform_correlation, find_patterns, apply_regex
)
from app.tools.api_tools import make_request, cache_get, cache_set, check_rate_limit
from app.tools.visualization_tools import (
    create_bar_chart, create_line_chart, create_pie_chart, create_scatter_plot
)

# Base Tool Tests
def test_base_tool():
    """Test the BaseTool abstract class."""
    class TestTool(BaseTool):
        def execute(self, **kwargs):
            return ToolResult(success=True, output="Test output")
    
    tool = TestTool()
    result = tool.execute()
    assert result.success
    assert result.output == "Test output"

def test_tool_result():
    """Test the ToolResult class."""
    result = ToolResult(success=True, output="Test output", metadata={"key": "value"})
    assert result.success
    assert result.output == "Test output"
    assert result.metadata == {"key": "value"}

# Math Tools Tests
def test_add_tool():
    """Test the add tool."""
    result = add(a=2, b=3)
    assert result.success
    assert result.output == 5

def test_multiply_tool():
    """Test the multiply tool."""
    result = multiply(a=4, b=5)
    assert result.success
    assert result.output == 20

# String Tools Tests
def test_to_uppercase_tool():
    """Test the to_uppercase tool."""
    result = to_uppercase(text="hello")
    assert result.success
    assert result.output == "HELLO"

def test_concatenate_tool():
    """Test the concatenate tool."""
    result = concatenate.execute(text1="hello", text2="world")
    assert result.success
    assert result.output == "helloworld"

# Datetime Tools Tests
def test_current_time_tool():
    """Test the current_time tool."""
    result = current_time.execute()
    assert result.success
    # Verify the output is a valid ISO format datetime string
    try:
        datetime.fromisoformat(result.output.replace('Z', '+00:00'))
        valid_datetime = True
    except ValueError:
        valid_datetime = False
    assert valid_datetime

def test_add_days_tool():
    """Test the add_days tool."""
    date_str = "2023-01-01"
    result = add_days.execute(date=date_str, days=5)
    assert result.success
    assert result.output == "2023-01-06"

# Data Tools Tests
def test_get_item_tool():
    """Test the get_item tool."""
    result = get_item.execute(items=["a", "b", "c"], index=1)
    assert result.success
    assert result.output == "b"

def test_summarize_list_tool():
    """Test the summarize_list tool."""
    result = summarize_list.execute(items=[1, 2, 3, 4, 5])
    assert result.success
    assert "count" in result.output
    assert "min" in result.output
    assert "max" in result.output
    assert "average" in result.output

def test_fetch_mock_data_tool():
    """Test the fetch_mock_data tool."""
    result = fetch_mock_data.execute(source="source1")
    assert result.success
    assert "sample data" in result.output

# Echo Tool Test
def test_echo_tool():
    """Test the echo tool."""
    result = echo.execute(text="Hello World")
    assert result.success
    assert result.output == "Echo: Hello World"

# JSON Tools Tests
def test_validate_json_tool():
    """Test the validate_json tool."""
    valid_json = '{"name": "test", "value": 123}'
    result = validate_json.execute(json_str=valid_json)
    assert result.success
    assert result.output["valid"]
    
    invalid_json = '{"name": "test", value: 123}'
    result = validate_json.execute(json_str=invalid_json)
    assert not result.success
    assert not result.output["valid"]

def test_transform_json_tool():
    """Test the transform_json tool."""
    json_str = '{"name": "test", "value": 123}'
    transformation = "uppercase_keys"
    result = transform_json.execute(json_str=json_str, transformation=transformation)
    assert result.success
    assert "NAME" in result.output
    assert "VALUE" in result.output

# CSV Tools Tests
def test_parse_csv_tool():
    """Test the parse_csv tool."""
    csv_data = "name,age,city\nJohn,30,New York\nJane,25,San Francisco"
    result = parse_csv.execute(csv_str=csv_data)
    assert result.success
    assert len(result.output) == 2
    assert result.output[0]["name"] == "John"
    assert result.output[1]["city"] == "San Francisco"

def test_generate_csv_tool():
    """Test the generate_csv tool."""
    data = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "San Francisco"}
    ]
    result = generate_csv.execute(data=data)
    assert result.success
    assert "name,age,city" in result.output
    assert "John,30,New York" in result.output
    assert "Jane,25,San Francisco" in result.output

# Database Tools Tests
def test_database_operations():
    """Test the database operations tools."""
    # Clear the database first
    clear_result = clear_database.execute()
    assert clear_result.success
    
    # Store data
    store_result = store_data.execute(key="test_key", value="test_value")
    assert store_result.success
    
    # Retrieve data
    retrieve_result = retrieve_data.execute(key="test_key")
    assert retrieve_result.success
    assert retrieve_result.output == "test_value"
    
    # List keys
    list_result = list_keys.execute()
    assert list_result.success
    assert "test_key" in list_result.output
    
    # Delete data
    delete_result = delete_data.execute(key="test_key")
    assert delete_result.success
    
    # Verify deletion
    retrieve_after_delete = retrieve_data.execute(key="test_key")
    assert not retrieve_after_delete.success

# Analysis Tools Tests
def test_analyze_sentiment_tool():
    """Test the analyze_sentiment tool."""
    result = analyze_sentiment.execute(text="Great product!")
    assert result.success
    assert "sentiment" in result.output
    assert result.output["sentiment"] == "positive"

def test_extract_entities_tool():
    """Test the extract_entities tool."""
    result = extract_entities.execute(text="John Smith works at Microsoft in Seattle.")
    assert result.success
    assert "entities" in result.output
    entities = result.output["entities"]
    assert any(e["text"] == "John Smith" and e["type"] == "PERSON" for e in entities)
    assert any(e["text"] == "Microsoft" and e["type"] == "ORG" for e in entities)
    assert any(e["text"] == "Seattle" and e["type"] == "GPE" for e in entities)

def test_extract_keywords_tool():
    """Test the extract_keywords tool."""
    result = extract_keywords.execute(text="Artificial intelligence is transforming the technology industry.")
    assert result.success
    assert "keywords" in result.output
    keywords = result.output["keywords"]
    assert "artificial intelligence" in keywords
    assert "technology" in keywords

def test_calculate_basic_stats_tool():
    """Test the calculate_basic_stats tool."""
    result = calculate_basic_stats.execute(data=[1, 2, 3, 4, 5])
    assert result.success
    assert "mean" in result.output
    assert "median" in result.output
    assert "mode" in result.output
    assert "std_dev" in result.output
    assert result.output["mean"] == 3.0
    assert result.output["median"] == 3.0

def test_perform_correlation_tool():
    """Test the perform_correlation tool."""
    result = perform_correlation.execute(
        x=[1, 2, 3, 4, 5],
        y=[2, 4, 6, 8, 10]
    )
    assert result.success
    assert "correlation" in result.output
    assert result.output["correlation"] == 1.0

def test_find_patterns_tool():
    """Test the find_patterns tool."""
    result = find_patterns.execute(data=[1, 2, 3, 1, 2, 3, 1, 2, 3])
    assert result.success
    assert "patterns" in result.output
    assert [1, 2, 3] in result.output["patterns"]

def test_apply_regex_tool():
    """Test the apply_regex tool."""
    result = apply_regex.execute(
        text="Contact us at info@example.com or support@example.org",
        pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    assert result.success
    assert "matches" in result.output
    assert "info@example.com" in result.output["matches"]
    assert "support@example.org" in result.output["matches"]

# API Tools Tests
def test_make_request_tool():
    """Test the make_request tool."""
    # Mock API endpoint
    result = make_request.execute(
        url="https://jsonplaceholder.typicode.com/todos/1",
        method="GET"
    )
    assert result.success
    assert "userId" in result.output
    assert "title" in result.output

def test_cache_operations():
    """Test the cache operations tools."""
    # Set cache
    set_result = cache_set.execute(key="test_cache_key", value="test_cache_value", ttl=60)
    assert set_result.success
    
    # Get cache
    get_result = cache_get.execute(key="test_cache_key")
    assert get_result.success
    assert get_result.output == "test_cache_value"

def test_check_rate_limit_tool():
    """Test the check_rate_limit tool."""
    result = check_rate_limit.execute(key="test_rate_limit", max_requests=5, window_seconds=60)
    assert result.success
    assert "allowed" in result.output
    assert result.output["allowed"]
    assert "remaining" in result.output
    assert result.output["remaining"] == 4

# Visualization Tools Tests
def test_create_bar_chart_tool():
    """Test the create_bar_chart tool."""
    result = create_bar_chart.execute(
        labels=["A", "B", "C"],
        values=[1, 2, 3],
        title="Test Bar Chart"
    )
    assert result.success
    assert "chart_data" in result.output
    assert result.output["chart_type"] == "bar"

def test_create_line_chart_tool():
    """Test the create_line_chart tool."""
    result = create_line_chart.execute(
        x_values=[1, 2, 3, 4, 5],
        y_values=[2, 4, 6, 8, 10],
        title="Test Line Chart"
    )
    assert result.success
    assert "chart_data" in result.output
    assert result.output["chart_type"] == "line"

def test_create_pie_chart_tool():
    """Test the create_pie_chart tool."""
    result = create_pie_chart.execute(
        labels=["A", "B", "C"],
        values=[30, 40, 30],
        title="Test Pie Chart"
    )
    assert result.success
    assert "chart_data" in result.output
    assert result.output["chart_type"] == "pie"

def test_create_scatter_plot_tool():
    """Test the create_scatter_plot tool."""
    result = create_scatter_plot.execute(
        x_values=[1, 2, 3, 4, 5],
        y_values=[2, 4, 6, 8, 10],
        title="Test Scatter Plot"
    )
    assert result.success
    assert "chart_data" in result.output
    assert result.output["chart_type"] == "scatter"