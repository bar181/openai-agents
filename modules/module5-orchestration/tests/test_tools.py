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
            return ToolResult(success=True, data="Test output")
        
        def validate_input(self, **kwargs):
            return True
        
        @property
        def description(self):
            return "Test tool description"
    
    tool = TestTool()
    result = tool.execute()
    assert result.success
    assert result.data == "Test output"

def test_tool_result():
    """Test the ToolResult class."""
    result = ToolResult(success=True, data="Test output", error=None)
    assert result.success
    assert result.data == "Test output"
    assert result.error is None

# Math Tools Tests
def test_add_tool():
    """Test the add tool."""
    result = add.function(a=2, b=3)
    assert result == 5

def test_multiply_tool():
    """Test the multiply tool."""
    result = multiply.function(a=4, b=5)
    assert result == 20

# String Tools Tests
def test_to_uppercase_tool():
    """Test the to_uppercase tool."""
    result = to_uppercase.function(text="hello")
    assert result == "HELLO"

def test_concatenate_tool():
    """Test the concatenate tool."""
    result = concatenate.function(text1="hello", text2="world")
    assert result == "helloworld"

# Datetime Tools Tests
def test_current_time_tool():
    """Test the current_time tool."""
    result = current_time.function()
    # Verify the output is a valid ISO format datetime string
    try:
        datetime.fromisoformat(result.replace('Z', '+00:00'))
        valid_datetime = True
    except ValueError:
        valid_datetime = False
    assert valid_datetime

def test_add_days_tool():
    """Test the add_days tool."""
    date_str = "2023-01-01"
    result = add_days.function(date=date_str, days=5)
    assert result == "2023-01-06"

# Data Tools Tests
def test_get_item_tool():
    """Test the get_item tool."""
    result = get_item.function(items=["a", "b", "c"], index=1)
    assert result == "b"

def test_summarize_list_tool():
    """Test the summarize_list tool."""
    result = summarize_list.function(items=[1, 2, 3, 4, 5])
    assert "count" in result
    assert "min" in result
    assert "max" in result
    assert "average" in result

def test_fetch_mock_data_tool():
    """Test the fetch_mock_data tool."""
    result = fetch_mock_data.function(source="source1")
    assert "sample data" in result

# Echo Tool Test
def test_echo_tool():
    """Test the echo tool."""
    result = echo.function(message="Hello World")
    assert result == "Echo: Hello World"

# JSON Tools Tests
def test_validate_json_tool():
    """Test the validate_json tool."""
    valid_json = '{"name": "test", "value": 123}'
    result = validate_json.function(json_str=valid_json)
    assert result["valid"]
    
    invalid_json = '{"name": "test", value: 123}'
    result = validate_json.function(json_str=invalid_json)
    assert not result["valid"]

def test_transform_json_tool():
    """Test the transform_json tool."""
    json_str = '{"name": "test", "value": 123}'
    transformation = "uppercase_keys"
    result = transform_json.function(json_str=json_str, transformation=transformation)
    assert "NAME" in result
    assert "VALUE" in result

# CSV Tools Tests
def test_parse_csv_tool():
    """Test the parse_csv tool."""
    csv_data = "name,age,city\nJohn,30,New York\nJane,25,San Francisco"
    result = parse_csv.function(csv_str=csv_data)
    assert len(result) == 2
    assert result[0]["name"] == "John"
    assert result[1]["city"] == "San Francisco"

def test_generate_csv_tool():
    """Test the generate_csv tool."""
    data = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "San Francisco"}
    ]
    result = generate_csv.function(data=data)
    assert "name,age,city" in result
    assert "John,30,New York" in result
    assert "Jane,25,San Francisco" in result

# Database Tools Tests
def test_database_operations():
    """Test the database operations tools."""
    # Clear the database first
    clear_result = clear_database.function()
    assert clear_result["success"]
    
    # Store data
    store_result = store_data.function(key="test_key", value="test_value")
    assert store_result["success"]
    
    # Retrieve data
    retrieve_result = retrieve_data.function(key="test_key")
    assert retrieve_result["success"]
    assert retrieve_result["value"] == "test_value"
    
    # List keys
    list_result = list_keys.function()
    assert list_result["success"]
    assert "test_key" in list_result["keys"]
    
    # Delete data
    delete_result = delete_data.function(key="test_key")
    assert delete_result["success"]
    
    # Verify deletion
    retrieve_after_delete = retrieve_data.function(key="test_key")
    assert not retrieve_after_delete["success"]

# Analysis Tools Tests
def test_analyze_sentiment_tool():
    """Test the analyze_sentiment tool."""
    result = analyze_sentiment.function(text="Great product!")
    assert "sentiment" in result
    assert result["sentiment"] == "positive"

def test_extract_entities_tool():
    """Test the extract_entities tool."""
    result = extract_entities.function(text="John Smith works at Microsoft in Seattle.")
    assert "entities" in result
    entities = result["entities"]
    assert any(e["text"] == "John Smith" and e["type"] == "PERSON" for e in entities)
    assert any(e["text"] == "Microsoft" and e["type"] == "ORG" for e in entities)
    assert any(e["text"] == "Seattle" and e["type"] == "GPE" for e in entities)

def test_extract_keywords_tool():
    """Test the extract_keywords tool."""
    result = extract_keywords.function(text="Artificial intelligence is transforming the technology industry.")
    assert "keywords" in result
    keywords = result["keywords"]
    assert "artificial intelligence" in keywords
    assert "technology" in keywords

def test_calculate_basic_stats_tool():
    """Test the calculate_basic_stats tool."""
    result = calculate_basic_stats.function(data=[1, 2, 3, 4, 5])
    assert "mean" in result
    assert "median" in result
    assert "mode" in result
    assert "std_dev" in result
    assert result["mean"] == 3.0
    assert result["median"] == 3.0

def test_perform_correlation_tool():
    """Test the perform_correlation tool."""
    result = perform_correlation.function(
        x=[1, 2, 3, 4, 5],
        y=[2, 4, 6, 8, 10]
    )
    assert "correlation" in result
    assert result["correlation"] == 1.0

def test_find_patterns_tool():
    """Test the find_patterns tool."""
    result = find_patterns.function(data=[1, 2, 3, 1, 2, 3, 1, 2, 3])
    assert "patterns" in result
    assert [1, 2, 3] in result["patterns"]

def test_apply_regex_tool():
    """Test the apply_regex tool."""
    result = apply_regex.function(
        text="Contact us at info@example.com or support@example.org",
        pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    assert "matches" in result
    assert "info@example.com" in result["matches"]
    assert "support@example.org" in result["matches"]

# API Tools Tests
def test_make_request_tool():
    """Test the make_request tool."""
    # Mock API endpoint
    result = make_request.function(
        url="https://jsonplaceholder.typicode.com/todos/1",
        method="GET"
    )
    assert "userId" in result
    assert "title" in result

def test_cache_operations():
    """Test the cache operations tools."""
    # Set cache
    set_result = cache_set.function(key="test_cache_key", value="test_cache_value", ttl=60)
    assert set_result["success"]
    
    # Get cache
    get_result = cache_get.function(key="test_cache_key")
    assert get_result["success"]
    assert get_result["value"] == "test_cache_value"

def test_check_rate_limit_tool():
    """Test the check_rate_limit tool."""
    result = check_rate_limit.function(key="test_rate_limit", max_requests=5, window_seconds=60)
    assert "allowed" in result
    assert result["allowed"]
    assert "remaining" in result
    assert result["remaining"] == 4

# Visualization Tools Tests
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