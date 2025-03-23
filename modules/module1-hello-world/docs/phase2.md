# Module 1 - Phase 2: Agent Implementation

In this phase, you'll implement the logic for your basic "Hello World" AI agent. This document guides you through creating an agent using the OpenAI Python SDK, specifically using the provided `function_tool` decorator to build agent tools.

---

## Step 1: Creating the Agent File

Navigate to `app/agents/` and create a file named `hello_world_agent.py`.

Your file should start with the necessary imports:

```python
from agents import Agent, Runner, function_tool
```

---

## Step 2: Defining the Tool Function

Define a simple tool function that the agent can use. Here, you'll create a basic tool that returns the string "Hello, world!":

```python
@function_tool
def hello_world_tool() -> str:
    """Returns a 'Hello, world!' string."""
    return "Hello, world!"
```

- **Explanation:**
  - The `@function_tool` decorator registers this function as a usable tool by the agent.
  - The function returns a simple greeting message.

---

## Step 3: Creating the Agent

Next, define your agent by specifying its name, instructions, and tools:

```python
hello_agent = Agent(
    name="HelloAgent",
    instructions="You are a friendly agent that greets the user.",
    tools=[hello_world_tool],
)
```

- **Explanation:**
  - `name`: A descriptive name for your agent.
  - `instructions`: These guide the agent's responses and interactions.
  - `tools`: A list of tools (functions) your agent can use.

---

## Step 4: Implementing the Runner

Define an asynchronous function to run the agent. This function manages the execution and output of your agent:

```python
async def run_hello_agent(user_message: str) -> str:
    """
    Executes the hello_agent asynchronously and returns its response.
    """
    try:
        result = await Runner.run(hello_agent, user_message)
        return result.final_output if result else "Error: No response from agent."
    except Exception as e:
        return f"Error: {str(e)}"
```

- **Explanation:**
  - Receives `user_message` and processes it using the defined agent.
  - Provides basic error handling to gracefully handle potential issues.

---

## Step 5: Verifying Your Implementation

Perform a quick verification to ensure the agent logic is error-free. You can run a simple Python check from your terminal:

```bash
python -c "import asyncio; from app.agents.hello_world_agent import run_hello_agent; print(asyncio.run(run_hello_agent('Test message')))"
```

You should see:

```
Hello, world!
```

---

## Completion of Phase 2

After completing this phase, you'll have:

- Defined a functional tool for your agent.
- Implemented your basic agent with clear instructions.
- Verified basic execution logic.

You're now ready to proceed to **Phase 3: API Router and Endpoint Creation**.