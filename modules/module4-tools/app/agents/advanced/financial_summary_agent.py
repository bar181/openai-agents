"""
Financial Summary Agent Module

This agent calculates simple interest and total amount using a simple interest formula,
and then processes a message. It expects input in the format:
    "principal,rate,time;message"

For example, given the input "1000,0.05,2;thank you":
  - Computes the simple interest: interest = principal * rate * time
      1000 * 0.05 * 2 = 100
  - Computes the total amount: total = principal + interest
      1000 + 100 = 1100
  - Processes the message by converting it to uppercase and echoing it.
  
Final Output:
    {
        "interest": 100.0,
        "total": 1100.0,
        "message": "Echo: THANK YOU"
    }
"""

from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase
from app.tools.echo_tools import echo

class FinancialSummaryAgent:
    def __init__(self):
        # Register available tools
        self.tools = {
            "add": add,
            "multiply": multiply,
            "to_uppercase": to_uppercase,
            "echo": echo,
        }
    
    def run(self, input_data: str) -> dict:
        try:
            parts = input_data.split(";")
            if len(parts) < 2:
                raise ValueError("Input must have two parts separated by ';'")
            
            # Parse the first part: "principal,rate,time"
            numbers = parts[0].split(",")
            if len(numbers) < 3:
                raise ValueError("First part must include three comma-separated numbers: principal, rate, time")
            principal = float(numbers[0])
            rate = float(numbers[1])
            time = float(numbers[2])
            
            # Compute interest = principal * rate * time
            # Using multiply twice for the calculation
            interest_partial = self.tools["multiply"].function(a=principal, b=rate)
            interest = self.tools["multiply"].function(a=interest_partial, b=time)
            
            # Compute total = principal + interest
            total = self.tools["add"].function(a=principal, b=interest)
            
            # Process the message: convert to uppercase then echo it
            message_upper = self.tools["to_uppercase"].function(text=parts[1])
            final_message = self.tools["echo"].function(message=message_upper)
            
            return {
                "interest": interest,
                "total": total,
                "message": final_message,
            }
        except Exception as e:
            return {"error": str(e)}

# Create a default instance for intra-module use.
financial_summary_agent = FinancialSummaryAgent()

if __name__ == "__main__":
    sample_input = "1000,0.05,2;thank you"
    output = financial_summary_agent.run(sample_input)
    print("Financial Summary Agent output:", output)
