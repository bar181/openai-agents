from agents import function_tool

@function_tool
def concatenate(str1: str, str2: str) -> str:
    """Concatenate two strings."""
    return str1 + str2

@function_tool
def to_uppercase(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()
