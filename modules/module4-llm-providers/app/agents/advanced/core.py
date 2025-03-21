from enum import Enum
from typing import Any, Dict, List, Optional, Type
from app.tools.base_tool import BaseTool, ToolResult


class AgentState(Enum):
    """Enum representing the possible states of the advanced agent."""
    INITIALIZING = "initializing"
    PROCESSING = "processing"
    EXECUTING_TOOL = "executing_tool"
    ERROR = "error"
    COMPLETED = "completed"


class ToolRegistry:
    """Registry for managing and accessing tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool in the registry."""
        self._tools[tool.name] = tool
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(tool_name)
    
    def list_available_tools(self) -> List[str]:
        """List all available tool names."""
        return list(self._tools.keys())
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """Get descriptions for all registered tools."""
        return {name: tool.description for name, tool in self._tools.items()}


class ContextManager:
    """Manager for storing and retrieving context data."""
    
    def __init__(self):
        self._context: Dict[str, Any] = {}
    
    def store_context(self, key: str, value: Any) -> None:
        """Store a value in the context."""
        self._context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a value from the context."""
        return self._context.get(key, default)
    
    def clear_context(self) -> None:
        """Clear all context data."""
        self._context.clear()
    
    def get_all_context(self) -> Dict[str, Any]:
        """Get all context data."""
        return self._context.copy()


class StateMachine:
    """State machine for managing agent state transitions."""
    
    def __init__(self, initial_state: AgentState = AgentState.INITIALIZING):
        self._current_state = initial_state
        self._state_history: List[AgentState] = [initial_state]
    
    @property
    def current_state(self) -> AgentState:
        """Get the current state."""
        return self._current_state
    
    @property
    def state_history(self) -> List[AgentState]:
        """Get the state history."""
        return self._state_history.copy()
    
    def transition_to(self, new_state: AgentState) -> None:
        """Transition to a new state."""
        self._current_state = new_state
        self._state_history.append(new_state)
    
    def can_transition_to(self, new_state: AgentState) -> bool:
        """Check if transition to a new state is valid."""
        # Define valid state transitions
        valid_transitions = {
            AgentState.INITIALIZING: [AgentState.PROCESSING, AgentState.ERROR],
            AgentState.PROCESSING: [AgentState.EXECUTING_TOOL, AgentState.COMPLETED, AgentState.ERROR],
            AgentState.EXECUTING_TOOL: [AgentState.PROCESSING, AgentState.ERROR],
            AgentState.ERROR: [AgentState.INITIALIZING, AgentState.PROCESSING],
            AgentState.COMPLETED: [AgentState.INITIALIZING]
        }
        
        return new_state in valid_transitions.get(self._current_state, [])