# File: app/agents/basic/dynamic_prompt_agent.py

class DynamicPromptAgent:
    """
    Unified agent for dynamic prompt management and execution.
    It can be used both from HTTP endpoints and internally by an orchestrator.
    """

    def __init__(self, initial_prompt: str = "You are a helpful assistant."):
        self.system_prompt = initial_prompt

    def update(self, new_prompt: str) -> str:
        """Update the system prompt with a new value."""
        self.system_prompt = new_prompt
        return self.system_prompt

    def execute(self, input_data: str) -> str:
        """Execute agent logic using the current system prompt and provided input."""
        return f"Prompt: {self.system_prompt}, Input: {input_data}"


# Global instance available application-wide
dynamic_agent = DynamicPromptAgent()


def update_system_prompt(new_prompt: str) -> str:
    """Convenience function to update the global agent's system prompt."""
    return dynamic_agent.update(new_prompt)


def execute_dynamic_prompt_agent(input_data: dict) -> str:
    """Convenience function to execute the global agent using the provided input data."""
    return dynamic_agent.execute(input_data["input"])
