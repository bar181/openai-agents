"""
Streaming Text Agent Module

This module implements a streaming text agent that can generate text responses
incrementally, enhancing real-time interaction and feedback.
"""

import asyncio
from typing import AsyncGenerator, Dict, Any, Optional

from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

from app.config import OPENAI_API_KEY

# Default model to use if not specified
DEFAULT_MODEL = "gpt-3.5-turbo"

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
            name: The name of the agent
            instructions: System instructions for the agent
            model: The OpenAI model to use
        """
        self.name = name
        self.instructions = instructions
        self.model = model
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    async def stream_response(self, user_input: str) -> AsyncGenerator[str, None]:
        """
        Stream the agent's response to the user input.
        
        Args:
            user_input: The user's input message
            
        Yields:
            Text chunks as they are generated
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


# Example usage
async def demo_text_streaming():
    """Demonstrate the text streaming functionality."""
    agent = StreamTextAgent()
    print("=== Streaming Text Agent Demo ===")
    
    # Initialize the agent
    status = await agent.initialize()
    print(f"Agent initialized: {status}")
    
    # Stream the response
    user_input = "Please tell me a short story about a space adventure."
    print(f"\nUser: {user_input}\n")
    print("Agent: ", end="", flush=True)
    
    async for text_chunk in agent.execute(user_input):
        print(text_chunk, end="", flush=True)
    print("\n")
    
    # Terminate the agent
    status = await agent.terminate()
    print(f"Agent terminated: {status}")
    print("=== Demo Complete ===")


if __name__ == "__main__":
    # Run the demo if this file is executed directly
    asyncio.run(demo_text_streaming())