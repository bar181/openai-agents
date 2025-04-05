import re
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Union
from pydantic import BaseModel, Field, ConfigDict

from agents import Agent, Runner, RunHooks, Tool
from app.agents.advanced.core import AgentState, ToolRegistry, ContextManager, StateMachine
from app.tools.base_tool import BaseTool, ToolResult

# Import existing tools
from app.tools.echo_tools import echo
from app.tools.math_tools import add, multiply
from app.tools.string_tools import to_uppercase
from app.tools.datetime_tools import current_time
from app.tools.data_tools import fetch_mock_data


class MultiToolAgentConfig(BaseModel):
    """Configuration for the Multi-Tool Agent."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = Field(..., description="Name of the agent")
    instructions: str = Field(..., description="Instructions for the agent")
    tools: List[Any] = Field(default_factory=list, description="List of tools available to the agent")
    output_type: Optional[Any] = Field(None, description="Expected output type")
    max_iterations: int = Field(10, description="Maximum number of iterations")
    debug_mode: bool = Field(False, description="Enable debug mode")


class MultiToolAgentHooks(RunHooks):
    """Hooks for the Multi-Tool Agent execution lifecycle."""
    
    def __init__(
        self, 
        context_manager: ContextManager,
        state_machine: StateMachine,
        logger: Optional[Callable[[str], None]] = print
    ):
        self.context_manager = context_manager
        self.state_machine = state_machine
        self.logger = logger
    
    async def on_agent_start(self, context, agent: Agent):
        """Called when the agent starts."""
        self.state_machine.transition_to(AgentState.INITIALIZING)
        self.logger(f"[START] Agent '{agent.name}' started.")
        self.context_manager.store_context("agent_start_time", current_time())
    
    async def on_agent_end(self, context, agent: Agent, output: Any):
        """Called when the agent ends."""
        self.state_machine.transition_to(AgentState.COMPLETED)
        self.logger(f"[END] Agent '{agent.name}' ended with output: {output}")
        self.context_manager.store_context("agent_end_time", current_time())
        self.context_manager.store_context("agent_output", output)
    
    async def on_tool_start(self, context, agent: Agent, tool: Tool):
        """Called when a tool starts."""
        self.state_machine.transition_to(AgentState.EXECUTING_TOOL)
        self.logger(f"[TOOL START] '{tool.name}' started.")
        self.context_manager.store_context("current_tool", tool.name)
    
    async def on_tool_end(self, context, agent: Agent, tool: Tool, result: Any):
        """Called when a tool ends."""
        self.state_machine.transition_to(AgentState.PROCESSING)
        self.logger(f"[TOOL END] '{tool.name}' ended with result: {result}")
        
        # Store tool results in context
        tool_results = self.context_manager.get_context("tool_results", {})
        tool_results[tool.name] = result
        self.context_manager.store_context("tool_results", tool_results)


class MultiToolAgent:
    """Multi-Tool Agent with enhanced capabilities."""
    
    def __init__(self, config: MultiToolAgentConfig):
        self.config = config
        self.context_manager = ContextManager()
        self.state_machine = StateMachine()
        self.tool_registry = ToolRegistry()
        
        # Filter tools to only include those compatible with Agent
        agent_compatible_tools = []
        for tool in config.tools:
            if isinstance(tool, (Tool, BaseTool)):
                if isinstance(tool, Tool):
                    agent_compatible_tools.append(tool)
                # BaseTool instances are registered but not passed to Agent
        
        # Initialize the agent
        self.agent = Agent(
            name=config.name,
            instructions=self._build_instructions(),
            tools=agent_compatible_tools,
            output_type=config.output_type
        )
        
        # Initialize hooks
        self.hooks = MultiToolAgentHooks(
            context_manager=self.context_manager,
            state_machine=self.state_machine,
            logger=print if config.debug_mode else lambda _: None
        )
        
        # Register tools
        for tool in config.tools:
            if isinstance(tool, BaseTool):
                self.tool_registry.register_tool(tool)
    
    def _build_instructions(self) -> str:
        """Build the instructions for the agent."""
        base_instructions = self.config.instructions
        
        # Add tool descriptions
        tool_descriptions = "\n\nAvailable tools:\n"
        for tool in self.config.tools:
            if isinstance(tool, Tool) and hasattr(tool, "description"):
                tool_descriptions += f"- {tool.name}: {tool.description}\n"
            elif isinstance(tool, BaseTool):
                tool_descriptions += f"- {tool.__class__.__name__}: {tool.description}\n"
        
        return base_instructions + tool_descriptions
    
    async def run(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> Any:
        """Run the agent with the given input."""
        # Initialize context if provided
        if context:
            for key, value in context.items():
                self.context_manager.store_context(key, value)
        
        # Store input in context
        self.context_manager.store_context("input", input_data)
        
        # Transition to processing state
        self.state_machine.transition_to(AgentState.PROCESSING)
        
        try:
            # Run the agent
            result = await Runner.run(
                self.agent,
                hooks=self.hooks,
                input=input_data
            )
            
            # Store result in context
            self.context_manager.store_context("result", result)
            
            return {
                "final_output": result.final_output,
                "context": self.context_manager.get_all_context()
            }
        
        except Exception as e:
            # Handle errors
            self.state_machine.transition_to(AgentState.ERROR)
            error_message = f"Error during agent execution: {str(e)}"
            self.context_manager.store_context("error", error_message)
            
            return {
                "final_output": f"Error: {error_message}",
                "context": self.context_manager.get_all_context()
            }


# Create default configuration with all available tools
default_config = MultiToolAgentConfig(
    name="MultiToolAgent",
    instructions=(
        "You are a multi-tool agent with access to various tools for data processing, "
        "analysis, and integration. You can handle complex tasks by breaking them down "
        "into steps and using the appropriate tools for each step.\n\n"
        "When processing user requests, identify the required tools and execute them "
        "in the correct sequence. Maintain context between steps and handle errors gracefully."
    ),
    tools=[echo, add, multiply, to_uppercase, current_time, fetch_mock_data],
    debug_mode=True
)

# Create default instance
multi_tool_agent = MultiToolAgent(default_config)