"""
Test module for the phase2 tool implementations.

This module tests the following tools:
- Data Tools: get_item, summarize_list, fetch_mock_data
- JSON Tools: validate_json, transform_json
- CSV Tools: parse_csv, generate_csv
- Database Tools: (tests skipped as not implemented yet)
- Analysis Tools: analyze_sentiment, extract_entities, extract_keywords,
  calculate_basic_stats, perform_correlation, find_patterns, apply_regex
- API Tools: make_request, cache_get, cache_set, check_rate_limit

Note: Visualization Tools tests are removed and will be implemented separately.
"""

import pytest
import json
from datetime import datetime

# Data Tools Tests
from app.tools.data_tools import get_item, summarize_list, fetch_mock_data

def test_get_item_tool():
    """Test the get_item tool."""
    result = get_item.function(items=["a", "b", "c"], index=1)
    assert result == "b"

def test_summarize_list_tool():
    """Test the summarize_list tool."""
    result = summarize_list.function(items=[1, 2, 3, 4, 5])
    # Expect result to be a dictionary with keys: count, min, max, average
    assert "count" in result
    assert "min" in result
    assert "max" in result
    assert "average" in result

def test_fetch_mock_data_tool():
    """Test the fetch_mock_data tool."""
    result = fetch_mock_data.function(source="source1")
    assert "sample data" in result

# JSON Tools Tests
from app.tools.json_tools import validate_json, transform_json

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
from app.tools.csv_tools import parse_csv, generate_csv

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

# Database Tools Tests (Skipped)
# from app.tools.database_tools import store_data, retrieve_data, list_keys, delete_data, clear_database

# @pytest.mark.skip(reason="Database connectivity not implemented yet")
# def test_database_tools():
#     """Placeholder test for database tools."""
#     pass

# Analysis Tools Tests
from app.tools.analysis_tools import (
    analyze_sentiment, extract_entities, extract_keywords,
    calculate_basic_stats, perform_correlation, find_patterns, apply_regex
)

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
    # Instead of expecting the phrase "artificial intelligence",
    # check that both "artificial" and "intelligence" appear in the keywords list.
    assert "artificial" in keywords
    assert "intelligence" in keywords
    # Also check that "technology" is in the keywords
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
from app.tools.api_tools import make_request, cache_get, cache_set, check_rate_limit

def test_make_request_tool():
    """Test the make_request tool."""
    result = make_request.function(
        url="https://jsonplaceholder.typicode.com/todos/1",
        method="GET"
    )
    assert "userId" in result
    assert "title" in result

def test_cache_operations():
    """Test the cache operations tools."""
    set_result = cache_set.function(key="test_cache_key", value="test_cache_value", ttl=60)
    assert set_result["success"]
    
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
