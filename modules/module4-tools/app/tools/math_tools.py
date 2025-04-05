from app.tools.base_tool import ToolResult
from typing import Any

def add_function(a: float, b: float) -> float:
    """
    Add two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.
    """
    return a + b

def multiply_function(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.
    """
    return a * b

class AddTool:
    @staticmethod
    def function(**kwargs: Any) -> float:
        a = kwargs.get("a")
        b = kwargs.get("b")
        return add_function(a, b)

class MultiplyTool:
    @staticmethod
    def function(**kwargs: Any) -> float:
        a = kwargs.get("a")
        b = kwargs.get("b")
        return multiply_function(a, b)

# Expose tool instances.
add = AddTool()
multiply = MultiplyTool()
