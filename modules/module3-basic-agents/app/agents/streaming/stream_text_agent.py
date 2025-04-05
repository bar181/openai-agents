#app/agents/streaming/stream_text_agent.py

import asyncio
from typing import AsyncGenerator, Dict, Any, Optional

from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

from app.config import OPENAI_API_KEY

# Default model to use if not specified
DEFAULT_MODEL = "gpt-4o-mini"


class StreamTextAgent:
    """
    Agent capable of streaming text responses incrementally to users.

    This agent enhances real-time interaction by generating and streaming
    text progressively rather than waiting for the complete response.
    """

    def __init__(
        self,
        name: str = "TextStreamer",
        instructions: str = "You are a helpful assistant.",
        model: str = DEFAULT_MODEL
    ):
        """
        Initialize the StreamTextAgent.

        Args:
            name: The name of the agent.
            instructions: System instructions for the agent.
            model: The OpenAI model to use.
        """
        self.name = name
        self.instructions = instructions
        self.model = model
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def stream_response(self, user_input: str) -> AsyncGenerator[str, None]:
        """
        Stream the agent's response to the user input.

        Args:
            user_input: The user's input message.
            
        Yields:
            Text chunks as they are generated.
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": user_input}
            ],
            stream=True
        )

        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def initialize(self) -> Dict[str, Any]:
        """Initialize the agent and return its status."""
        return {"status": "initialized", "name": self.name}

    async def execute(self, input_data: str) -> AsyncGenerator[str, None]:
        """Execute the agent with the given input data."""
        async for chunk in self.stream_response(input_data):
            yield chunk

    async def terminate(self) -> Dict[str, Any]:
        """Terminate the agent and clean up resources."""
        return {"status": "terminated", "name": self.name}


# Global instance for consistent usage across the application
stream_text_agent = StreamTextAgent()


async def initialize_stream_text_agent() -> Dict[str, Any]:
    """
    Convenience function to initialize the global streaming text agent.

    Returns:
        A dictionary indicating the initialization status.
    """
    return await stream_text_agent.initialize()


async def execute_stream_text_agent(input_data: dict) -> AsyncGenerator[str, None]:
    """
    Convenience function to execute the global streaming text agent.

    Args:
        input_data (dict): A dictionary containing the key 'input'.
    
    Yields:
        Text chunks as they are generated.
    """
    async for chunk in stream_text_agent.execute(input_data["input"]):
        yield chunk


async def terminate_stream_text_agent() -> Dict[str, Any]:
    """
    Convenience function to terminate the global streaming text agent.

    Returns:
        A dictionary indicating the termination status.
    """
    return await stream_text_agent.terminate()
