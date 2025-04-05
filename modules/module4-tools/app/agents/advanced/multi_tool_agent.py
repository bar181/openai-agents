"""
Multi-Tool Agent Module

This agent demonstrates how to call multiple tools in sequence to process input.
For this example, the agent uses:
- Math Tools (add) to add two numbers.
- String Tools (to_uppercase) to convert text to uppercase.
- Echo Tool (echo) to echo a message.

The input format is expected to be a semicolon-separated string:
"num1,num2;text_for_uppercase;message_for_echo"

For example: "2,3;hello;world"
"""

from app.tools.math_tools import add
from app.tools.string_tools import to_uppercase
from app.tools.echo_tools import echo

class MultiToolAgent:
    def __init__(self):
        # Register available tools
        self.tools = {
            "add": add,
            "to_uppercase": to_uppercase,
            "echo": echo,
        }
    
    def run(self, input_data: str) -> dict:
        try:
            parts = input_data.split(";")
            # Require exactly three parts for valid input.
            if len(parts) < 3:
                raise ValueError("Input must have three parts separated by ';'")
            
            # Part 1: Use math tool to add two numbers.
            numbers = parts[0].split(",")
            if len(numbers) < 2:
                raise ValueError("First part must include two comma-separated numbers.")
            a = float(numbers[0])
            b = float(numbers[1])
            math_result = self.tools["add"].function(a=a, b=b)
            
            # Part 2: Use string tool to convert text to uppercase.
            uppercase_result = self.tools["to_uppercase"].function(text=parts[1])
            
            # Part 3: Use echo tool.
            echo_result = self.tools["echo"].function(message=parts[2])
            
            return {
                "math_result": math_result,
                "uppercase_result": uppercase_result,
                "echo_result": echo_result,
            }
        except Exception as e:
            return {"error": str(e)}

# Create a default instance for intra-module use.
multi_tool_agent = MultiToolAgent()

if __name__ == "__main__":
    # Demonstration when running directly.
    sample_input = "2,3;hello;world"
    output = multi_tool_agent.run(sample_input)
    print("Multi-tool agent output:", output)
