from agents import function_tool

@function_tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@function_tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
