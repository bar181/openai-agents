
# module1-hello-world/app/agents/hello_world_agent.py


from agents import Agent, Runner, function_tool

@function_tool
def hello_world_tool() -> str:
    """Returns a 'Hello, world!' string."""
    return "Hello, world!"

# Create the agent using the function_tool-decorated function.
hello_agent = Agent(
    name="HelloAgent",
    instructions="You are a friendly agent that greets the user.",
    tools=[hello_world_tool],  # Pass a list of tool functions.
)

async def run_hello_agent(user_message: str) -> str:
    """
    Runs the hello_agent with the provided user message using an async runner.
    Returns the final output from the agent.
    """
    try:
        result = await Runner.run(hello_agent, user_message)
        return result.final_output if result else "Error: No response from agent."
    except Exception as e:
        return f"Error: {str(e)}"
