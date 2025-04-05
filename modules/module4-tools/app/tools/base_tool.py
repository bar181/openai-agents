from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: Optional[str] = None

class BaseTool:
    def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError("Subclasses must implement this method")

    def validate_input(self, **kwargs) -> bool:
        # Default validation always returns True.
        return True

    @property
    def description(self) -> str:
        raise NotImplementedError("Subclasses must implement this property")
