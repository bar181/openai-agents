import re
from typing import Any, Optional, Callable
from pydantic import BaseModel, ConfigDict
from agents import Agent, Runner, RunHooks, Tool
from app.tools import (
    echo,
    add,
    multiply,
    to_uppercase,
    current_time,
    fetch_mock_data
)

class GenericLifecycleHooks(RunHooks):
    def __init__(self, logger: Optional[Callable[[str], None]] = print):
        self.logger = logger

    async def on_agent_start(self, context, agent: Agent):
        self.logger(f"[START] Agent '{agent.name}' started.")

    async def on_agent_end(self, context, agent: Agent, output: Any):
        self.logger(f"[END] Agent '{agent.name}' ended with output: {output}")

    async def on_tool_start(self, context, agent: Agent, tool: Tool):
        self.logger(f"[TOOL START] '{tool.name}' started.")

    async def on_tool_end(self, context, agent: Agent, tool: Tool, result: Any):
        self.logger(f"[TOOL END] '{tool.name}' ended with result: {result}")


class GenericAgentConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    instructions: str
    tools: Optional[list[Tool]] = None
    output_type: Optional[Any] = None


class GenericLifecycleAgent:
    def __init__(self, config: GenericAgentConfig, hooks: Optional[RunHooks] = None):
        self.agent = Agent(
            name=config.name,
            instructions=config.instructions,
            tools=config.tools or [],
            output_type=config.output_type
        )
        self.hooks = hooks or GenericLifecycleHooks()

    async def run(self, input_data: Any):
        text_lower = input_data.lower()
        if "fetch" in text_lower or "retrieve" in text_lower:
            match = re.search(r"[Ff]rom\s+'([^']+)'", input_data)
            source = match.group(1) if match else "unknown"
            
        # Use Runner.run for all tasks, let the agent handle tool selection
        return await Runner.run(
            self.agent,
            hooks=self.hooks,
            input=input_data
        )


# Example agent setup with tools
agent_config = GenericAgentConfig(
    name="GenericLifecycleAgent",
    instructions=(
        "You have access to the following INTERNAL tools only:\n"
        "- echo(message: str): echoes a message.\n"
        "- add(a: float, b: float): returns the sum of two numbers.\n"
        "- multiply(a: float, b: float): returns the product of two numbers.\n"
        "- to_uppercase(text: str): converts text to uppercase.\n"
        "- current_time(): returns current UTC time.\n"
        "- fetch_mock_data(source: str): retrieves MOCK data from a simulated internal database.\n\n"
        "When a user requests to fetch or retrieve data from any source, use fetch_mock_data to get the data "
        "and return the data value from the result."
    ),
    tools=[echo, add, multiply, to_uppercase, current_time, fetch_mock_data]
)

generic_agent = GenericLifecycleAgent(agent_config)
