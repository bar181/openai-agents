# app/tools/__init__.py

from .math_tools import add, multiply
from .data_tools import get_item, summarize_list, fetch_mock_data
from .string_tools import concatenate, to_uppercase
from .datetime_tools import current_time, add_days
from .echo_tools import echo

all_tools = [
    add, multiply, get_item, summarize_list, fetch_mock_data,
    concatenate, to_uppercase, current_time,
    add_days, echo
]

__all__ = [
    "add",
    "multiply",
    "get_item",
    "summarize_list",
    "fetch_mock_data",
    "concatenate",
    "to_uppercase",
    "current_time",
    "add_days",
    "echo",
    "all_tools"
]
