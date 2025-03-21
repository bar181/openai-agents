from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ToolResult(BaseModel):
    """Base class for tool execution results."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


class BaseTool(ABC):
    """Abstract base class for all advanced tools."""
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Executes the tool's primary function."""
        pass
    
    @abstractmethod
    def validate_input(self, **kwargs) -> bool:
        """Validates input parameters."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Returns tool description for agent."""
        pass
    
    @property
    def name(self) -> str:
        """Returns the name of the tool."""
        return self.__class__.__name__