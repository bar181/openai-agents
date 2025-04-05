from typing import Any

def echo_function(message: str) -> str:
    """
    Echo the provided message.

    Args:
        message (str): The message to echo.

    Returns:
        str: A string echoing the message.
    """
    return f"Echo: {message}"

class EchoTool:
    @staticmethod
    def function(**kwargs: Any) -> str:
        message = kwargs.get("message", "")
        return echo_function(message)

# Expose tool instance.
echo = EchoTool()
