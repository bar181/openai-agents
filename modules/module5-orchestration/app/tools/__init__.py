"""
Tools package initialization.

This module initializes the tools package and applies adapters to function tools.
"""

# Import the adapter application function
from app.tools.tool_adapter import adapt_all_tools

# Apply adapters to all function tools
adapt_all_tools()
