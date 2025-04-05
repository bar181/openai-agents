"""
Test module for the completed tool implementations.

This module tests the following tools:
- Base Tool functionality (BaseTool and ToolResult)
- Math Tools: add and multiply
- String Tools: to_uppercase and concatenate
- Datetime Tools: current_time and add_days
- Echo Tool: echo
"""

import asyncio
import json
import pytest
from datetime import datetime

from app.tools.base_tool import BaseTool, ToolResult
from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase, concatenate
from app.tools.datetime_tools import current_time, add_days
from app.tools.echo_tools import echo

def call_tool(tool, **kwargs):
    """
    Call the given tool with provided keyword arguments.
    
    For tools decorated with @function_tool (which have an "on_invoke_tool" attribute),
    serialize the kwargs as JSON and call the async on_invoke_tool function.
    For plain tools with a callable 'function' attribute, call that.
    Otherwise, if the tool is callable, call it directly.
    """
    if hasattr(tool, "function") and callable(tool.function):
        return tool.function(**kwargs)
    elif hasattr(tool, "on_invoke_tool"):
        ctx = {}  # Empty context for testing
        args_json = json.dumps(kwargs)
        return asyncio.run(tool.on_invoke_tool(ctx, args_json))
    elif callable(tool):
        return tool(**kwargs)
    else:
        raise ValueError("Tool is not callable")

# --- Base Tool Tests ---
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

# --- Math Tools Tests ---
def test_add_tool():
    """Test the add tool."""
    result = call_tool(add, a=2, b=3)
    assert result == 5

def test_multiply_tool():
    """Test the multiply tool."""
    result = call_tool(multiply, a=4, b=5)
    assert result == 20

# --- String Tools Tests ---
def test_to_uppercase_tool():
    """Test the to_uppercase tool."""
    result = call_tool(to_uppercase, text="hello")
    assert result == "HELLO"

def test_concatenate_tool():
    """Test the concatenate tool."""
    result = call_tool(concatenate, text1="hello", text2="world")
    assert result == "helloworld"

# --- Datetime Tools Tests ---
def test_current_time_tool():
    """Test the current_time tool."""
    result = call_tool(current_time)
    try:
        # datetime.fromisoformat expects a timezone offset; our current_time returns one.
        datetime.fromisoformat(result)
        valid_datetime = True
    except ValueError:
        valid_datetime = False
    assert valid_datetime

def test_add_days_tool():
    """Test the add_days tool."""
    date_str = "2023-01-01"
    # Note: the updated add_days tool expects a parameter named 'base_date'
    result = call_tool(add_days, base_date=date_str, days=5)
    # We check that the result starts with the expected date string.
    assert result.startswith("2023-01-06")

# --- Echo Tool Test ---
def test_echo_tool():
    """Test the echo tool."""
    result = call_tool(echo, message="Hello World")
    assert result == "Echo: Hello World"
