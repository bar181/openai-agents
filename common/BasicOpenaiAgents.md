

# Basic OpenAI Agents Overview

## Reference docummentation - source documents
- https://github.com/openai/openai-agents-python/blob/main/examples/basic/agent_lifecycle_example.py

- https://github.com/openai/openai-agents-python/blob/main/examples/basic/dynamic_system_prompt.py

- https://github.com/openai/openai-agents-python/blob/main/examples/basic/lifecycle_example.py

- https://github.com/openai/openai-agents-python/blob/main/examples/basic/stream_items.py

- https://github.com/openai/openai-agents-python/blob/main/examples/basic/stream_text.py

- https://github.com/openai/openai-agents-python/blob/main/examples/basic/tools.py


This document provides an overview of several basic agents implemented using the OpenAI Agents SDK. Each section includes a description, pseudocode, and key code snippets to illustrate the agent's functionality.

---

## 1. Agent Lifecycle Example

**Description:**
This example demonstrates how to manage the lifecycle of an agent, including initialization, execution, and termination. It showcases the use of hooks to monitor and log various events during the agent's operation.

**Pseudocode:**

```plaintext
Define a custom RunHooks class to handle lifecycle events:
    - on_agent_start: Log when the agent starts.
    - on_agent_end: Log when the agent ends.
    - on_tool_call: Log when a tool is called.
    - on_tool_call_output: Log the output of a tool call.

Initialize the agent with:
    - Name: "LifecycleAgent"
    - Instructions: "You are an agent demonstrating lifecycle management."
    - Tools: [example_tool]

Run the agent with the custom hooks:
    - Input: "Execute lifecycle example."
```


**Important Code Snippet:**

```python
class ExampleHooks(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        print(f"Agent {agent.name} has started.")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent) -> None:
        print(f"Agent {agent.name} has ended.")

    async def on_tool_call(self, context: RunContextWrapper, tool: Tool, input: Any) -> None:
        print(f"Tool {tool.name} called with input: {input}")

    async def on_tool_call_output(self, context: RunContextWrapper, tool: Tool, output: Any) -> None:
        print(f"Tool {tool.name} returned output: {output}")

agent = Agent(
    name="LifecycleAgent",
    instructions="You are an agent demonstrating lifecycle management.",
    tools=[example_tool],
)

result = await Runner.run(agent, input="Execute lifecycle example.", hooks=ExampleHooks())
```


---

## 2. Dynamic System Prompt

**Description:**
This agent adjusts its system prompt dynamically based on the input it receives, allowing for context-aware responses.

**Pseudocode:**

```plaintext
Define a function to generate a dynamic system prompt based on input:
    - If input contains "weather", set prompt to "You are a weather assistant."
    - Else, set prompt to "You are a general assistant."

Initialize the agent with:
    - Name: "DynamicPromptAgent"
    - Instructions: dynamic_system_prompt_function

Run the agent with varying inputs to observe dynamic prompt changes.
```


**Important Code Snippet:**

```python
def dynamic_system_prompt(input_text: str) -> str:
    if "weather" in input_text.lower():
        return "You are a weather assistant."
    else:
        return "You are a general assistant."

agent = Agent(
    name="DynamicPromptAgent",
    instructions=dynamic_system_prompt,
)

result = await Runner.run(agent, input="Tell me about the weather today.")
```


---

## 3. Stream Items

**Description:**
This example demonstrates how an agent can stream a sequence of items (e.g., jokes) to the user in real-time.

**Pseudocode:**

```plaintext
Define a function tool that returns a random number of jokes.

Initialize the agent with:
    - Name: "Joker"
    - Instructions: "First call the 'how_many_jokes' tool, then tell that many jokes."
    - Tools: [how_many_jokes]

Run the agent in a streamed manner:
    - Input: "Hello"
    - For each event in the stream:
        - If it's a tool call, log the call.
        - If it's a tool output, log the output.
        - If it's a text delta, print the text.
```


**Important Code Snippet:**

```python
@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)

agent = Agent(
    name="Joker",
    instructions="First call the 'how_many_jokes' tool, then tell that many jokes.",
    tools=[how_many_jokes],
)

result = Runner.run_streamed(agent, input="Hello")

async for event in result.stream_events():
    if event.type == "run_item_stream_event":
        if event.item.type == "tool_call_item":
            print("-- Tool was called")
        elif event.item.type == "tool_call_output_item":
            print(f"-- Tool output: {event.item.output}")
        elif event.item.type == "text_delta_item":
            print(event.item.text, end="", flush=True)
```


---

## 4. Stream Text

**Description:**
This agent streams text responses incrementally as they are generated, providing real-time feedback to the user.

**Pseudocode:**

```plaintext
Initialize the agent with:
    - Name: "Streamer"
    - Instructions: "You are a helpful assistant."

Run the agent in a streamed manner:
    - Input: "Please tell me 5 jokes."
    - For each event in the stream:
        - If it's a raw response event with text delta, print the delta.
```


**Important Code Snippet:**

```python
agent = Agent(
    name="Streamer",
    instructions="You are a helpful assistant.",
)

result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")

async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        print(event.data.delta, end="", flush=True)
```


---

## 5. Tools Integration

**Description:**
This example shows how to define and integrate tools that agents can utilize to perform specific tasks, such as fetching weather data.

**Pseudocode:**
``` plaintext
Define a Pydantic model for weather data with fields: city, temperature_range, conditions.

Define a function tool 'get_weather' that:
    - Accepts a city name.
    - Returns a Weather object with mock data.

Initialize the agent with:
    - Name: "WeatherAgent"
    - Instructions: "You are a helpful agent."
    -
::contentReference[oaicite:33]{index=33}
 ```
