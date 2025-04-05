# File: app/tools/echo_tools.py

from agents import function_tool

@function_tool
def echo(message: str) -> str:
    """Echoes the provided message."""
    return f"Echo: {message}"
