"""
Tools package initialization.

This module initializes the tools package and applies adapters to function tools.
"""

# Import individual tools so they can be imported from app.tools
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

# Import tool modules for advanced_router.py
import app.tools.json_tools as json_tool
import app.tools.csv_tools as csv_tool
import app.tools.database_tools as database_tool
import app.tools.analysis_tools as text_analysis_tool
import app.tools.analysis_tools as statistics_tool
import app.tools.analysis_tools as pattern_tool
import app.tools.api_tools as api_tool
import app.tools.api_tools as cache_tool
import app.tools.api_tools as rate_limiter_tool
import app.tools.visualization_tools as visualization_tool

# Import the adapter application function
from app.tools.tool_adapter import adapt_all_tools

# Apply adapters to all function tools
adapt_all_tools()
