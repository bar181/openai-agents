# app/tools/__init__.py

# Base tool
from .base_tool import BaseTool, ToolResult

# Basic tools
from .math_tools import add, multiply
from .data_tools import get_item, summarize_list, fetch_mock_data
from .string_tools import concatenate, to_uppercase
from .datetime_tools import current_time, add_days
from .echo_tools import echo

# Advanced tools
from .json_tools import JsonTool, validate_json, transform_json
from .csv_tools import CsvTool, parse_csv, generate_csv
from .database_tools import DatabaseTool, store_data, retrieve_data, list_keys, delete_data, clear_database
from .analysis_tools import (
    TextAnalysisTool, analyze_sentiment, extract_entities, extract_keywords,
    StatisticsTool, calculate_basic_stats, perform_correlation,
    PatternTool, find_patterns, apply_regex
)
from .api_tools import ApiTool, make_request, CacheTool, cache_get, cache_set, RateLimiterTool, check_rate_limit
from .visualization_tools import VisualizationTool, create_bar_chart, create_line_chart, create_pie_chart, create_scatter_plot

# Basic tool list
basic_tools = [
    add, multiply, get_item, summarize_list, fetch_mock_data,
    concatenate, to_uppercase, current_time,
    add_days, echo
]

# Advanced tool instances
json_tool = JsonTool()
csv_tool = CsvTool()
database_tool = DatabaseTool()
text_analysis_tool = TextAnalysisTool()
statistics_tool = StatisticsTool()
pattern_tool = PatternTool()
api_tool = ApiTool()
cache_tool = CacheTool()
rate_limiter_tool = RateLimiterTool()
visualization_tool = VisualizationTool()

# Advanced tool list
advanced_tools = [
    json_tool, csv_tool, database_tool,
    text_analysis_tool, statistics_tool, pattern_tool,
    api_tool, cache_tool, rate_limiter_tool, visualization_tool
]

# All tools
all_tools = basic_tools + advanced_tools

__all__ = [
    # Base classes
    "BaseTool",
    "ToolResult",
    
    # Basic tools
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
    
    # Advanced tools - JSON
    "JsonTool",
    "validate_json",
    "transform_json",
    
    # Advanced tools - CSV
    "CsvTool",
    "parse_csv",
    "generate_csv",
    
    # Advanced tools - Database
    "DatabaseTool",
    "store_data",
    "retrieve_data",
    "list_keys",
    "delete_data",
    "clear_database",
    
    # Advanced tools - Analysis
    "TextAnalysisTool",
    "analyze_sentiment",
    "extract_entities",
    "extract_keywords",
    "StatisticsTool",
    "calculate_basic_stats",
    "perform_correlation",
    "PatternTool",
    "find_patterns",
    "apply_regex",
    
    # Advanced tools - API
    "ApiTool",
    "make_request",
    "CacheTool",
    "cache_get",
    "cache_set",
    "RateLimiterTool",
    "check_rate_limit",
    
    # Advanced tools - Visualization
    "VisualizationTool",
    "create_bar_chart",
    "create_line_chart",
    "create_pie_chart",
    "create_scatter_plot",
    
    # Tool collections
    "basic_tools",
    "advanced_tools",
    "all_tools"
]
