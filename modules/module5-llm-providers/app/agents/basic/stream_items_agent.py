"""
Streaming Items Agent Module

This module implements a streaming items agent that can generate sequences of
structured items (e.g., jokes, facts, or bullet points) in real-time.
"""

import asyncio
import random
from typing import AsyncGenerator, Dict, Any, List, Optional

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionToolParam

from app.config import OPENAI_API_KEY

# Default model to use if not specified
DEFAULT_MODEL = "gpt-3.5-turbo"

class StreamItemsAgent:
    """
    Agent capable of streaming sequences of structured items in real-time.
    
    This agent enhances dynamic content delivery by generating and streaming
    items progressively rather than waiting for the complete response.
    """
    
    def __init__(
        self,
        name: str = "ItemStreamer",
        instructions: str = "Generate items based on the request.",
        model: str = DEFAULT_MODEL,
        max_items: int = 10
    ):
        """
        Initialize the StreamItemsAgent.
        
        Args:
            name: The name of the agent
            instructions: System instructions for the agent
            model: The OpenAI model to use
            max_items: Maximum number of items to generate
        """
        self.name = name
        self.instructions = instructions
        self.model = model
        self.max_items = max_items
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    async def _determine_item_count(self, category: str) -> int:
        """
        Determine how many items to generate (1-max_items).
        
        Args:
            category: The category of items to generate
            
        Returns:
            Number of items to generate
        """
        # Define the tool for determining item count
        tools: List[ChatCompletionToolParam] = [
            {
                "type": "function",
                "function": {
                    "name": "how_many_items",
                    "description": f"Determine how many {category} items to generate (1-{self.max_items})",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "count": {
                                "type": "integer",
                                "description": f"Number of {category} items to generate (between 1 and {self.max_items})"
                            }
                        },
                        "required": ["count"]
                    }
                }
            }
        ]
        
        # Call the OpenAI API to determine the count
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": f"How many {category} items should I generate?"}
            ],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "how_many_items"}}
        )
        
        # Extract the count from the response
        tool_call = response.choices[0].message.tool_calls[0]
        tool_call_args = eval(tool_call.function.arguments)
        count = tool_call_args.get("count", random.randint(1, self.max_items))
        
        # Ensure count is within bounds
        return max(1, min(count, self.max_items))
    
    async def _generate_items(self, category: str, count: int) -> List[str]:
        """
        Generate a list of items for the specified category.
        
        Args:
            category: The category of items to generate
            count: Number of items to generate
            
        Returns:
            List of generated items
        """
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": f"Generate {count} {category} items. Format each item on a new line with a number and a dash, like '1 - Item content'."}
            ]
        )
        
        # Extract and parse the items from the response
        content = response.choices[0].message.content
        if content:
            # Split by newlines and filter out empty lines
            items = [line.strip() for line in content.split('\n') if line.strip()]
            return items[:count]  # Ensure we don't exceed the requested count
        return []
    
    async def stream_items(self, category: str, count: Optional[int] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream items based on the requested category.
        
        Args:
            category: The category of items to generate
            count: Optional number of items to generate (if not provided, the agent will decide)
            
        Yields:
            Dictionary containing event type and data
        """
        # Step 1: Determine how many items to generate
        yield {"type": "status", "message": f"Determining number of {category} items to generate..."}
        
        if count is None:
            count = await self._determine_item_count(category)
        else:
            count = max(1, min(count, self.max_items))
        
        yield {"type": "count", "count": count, "message": f"Will generate {count} {category} items."}
        
        # Step 2: Generate the items
        yield {"type": "status", "message": f"Generating {count} {category} items..."}
        
        items = await self._generate_items(category, count)
        
        # Step 3: Stream the items one by one
        for i, item in enumerate(items):
            yield {"type": "item", "index": i + 1, "content": item}
            
            # Add a small delay between items for a better streaming effect
            await asyncio.sleep(0.2)
        
        # Step 4: Signal completion
        yield {"type": "complete", "message": f"Generated {len(items)} {category} items."}
    
    async def initialize(self) -> Dict[str, Any]:
        """Initialize the agent and return its status."""
        return {"status": "initialized", "name": self.name}
    
    async def execute(self, category: str, count: Optional[int] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute the agent with the given category and count."""
        async for item in self.stream_items(category, count):
            yield item
    
    async def terminate(self) -> Dict[str, Any]:
        """Terminate the agent and clean up resources."""
        return {"status": "terminated", "name": self.name}


# Example usage
async def demo_items_streaming():
    """Demonstrate the items streaming functionality."""
    agent = StreamItemsAgent(
        instructions="You are an expert at generating creative and engaging content."
    )
    print("=== Streaming Items Agent Demo ===")
    
    # Initialize the agent
    status = await agent.initialize()
    print(f"Agent initialized: {status}")
    
    # Stream the items
    category = "jokes"
    print(f"\nStreaming {category}:\n")
    
    async for event in agent.execute(category):
        if event["type"] == "status":
            print(f"Status: {event['message']}")
        elif event["type"] == "count":
            print(f"Count: {event['count']} {category}")
        elif event["type"] == "item":
            print(f"Item {event['index']}: {event['content']}")
        elif event["type"] == "complete":
            print(f"\nComplete: {event['message']}")
    
    # Terminate the agent
    status = await agent.terminate()
    print(f"Agent terminated: {status}")
    print("=== Demo Complete ===")


if __name__ == "__main__":
    # Run the demo if this file is executed directly
    asyncio.run(demo_items_streaming())