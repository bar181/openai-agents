from app.tools.echo_tools import echo
from app.tools.math_tools import add, multiply

# Try different ways to call the function tool
print("Echo tool info:")
print(f"Name: {echo.name}")
print(f"Description: {echo.description}")

# Try to access the original function
try:
    # Try to call the tool directly
    result1 = echo(message="Hello World")
    print(f"Direct call result: {result1}")
except Exception as e:
    print(f"Direct call error: {e}")

try:
    # Try to call on_invoke_tool
    result2 = echo.on_invoke_tool(None, '{"message": "Hello World"}')
    print(f"on_invoke_tool result: {result2}")
except Exception as e:
    print(f"on_invoke_tool error: {e}")

# Try to access the original function through __dict__
print("\nTool attributes:")
for key, value in echo.__dict__.items():
    print(f"{key}: {value}")

# Try math tools
print("\nMath tools:")
try:
    result3 = add(a=2, b=3)
    print(f"Direct add result: {result3}")
except Exception as e:
    print(f"Direct add error: {e}")

try:
    result4 = add.on_invoke_tool(None, '{"a": 2, "b": 3}')
    print(f"add.on_invoke_tool result: {result4}")
except Exception as e:
    print(f"add.on_invoke_tool error: {e}")