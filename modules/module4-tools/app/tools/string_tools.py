from typing import Any

def to_uppercase_function(text: str) -> str:
    """
    Convert text to uppercase.

    Args:
        text (str): Input text.

    Returns:
        str: Uppercase version of the text.
    """
    return text.upper()

def concatenate_function(text1: str, text2: str) -> str:
    """
    Concatenate two strings.

    Args:
        text1 (str): The first string.
        text2 (str): The second string.

    Returns:
        str: The concatenated result.
    """
    return f"{text1}{text2}"

class ToUppercaseTool:
    @staticmethod
    def function(**kwargs: Any) -> str:
        text = kwargs.get("text", "")
        return to_uppercase_function(text)

class ConcatenateTool:
    @staticmethod
    def function(**kwargs: Any) -> str:
        text1 = kwargs.get("text1", "")
        text2 = kwargs.get("text2", "")
        return concatenate_function(text1, text2)

# Expose tool instances.
to_uppercase = ToUppercaseTool()
concatenate = ConcatenateTool()
