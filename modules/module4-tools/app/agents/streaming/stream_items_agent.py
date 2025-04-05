# app/agents/streaming/stream_items_agent.py

import asyncio
import random
from typing import AsyncGenerator, Dict, Any, List, Optional

from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY

# Default model to use if not specified
DEFAULT_MODEL = "gpt-4o-mini"


class StreamItemsAgent:
    """
    Agent capable of streaming sequences of structured items in real-time.

    This agent generates and streams items progressively. It is designed
    to be invoked from HTTP endpoints as well as directly from within the system.
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
            name: The name of the agent.
            instructions: System instructions for the agent.
            model: The OpenAI model to use.
            max_items: Maximum number of items to generate.
        """
        self.name = name
        self.instructions = instructions
        self.model = model
        self.max_items = max_items
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def _determine_item_count(self, category: str) -> int:
        """
        Determine how many items to generate (1-max_items).

        For simplicity, we now choose a random count rather than calling any tools.

        Args:
            category: The category of items to generate.
            
        Returns:
            Number of items to generate.
        """
        return random.randint(1, self.max_items)

    async def _generate_items(self, category: str, count: int) -> List[str]:
        """
        Generate a list of items for the specified category.

        Args:
            category: The category of items to generate.
            count: Number of items to generate.
            
        Returns:
            List of generated items.
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
            category: The category of items to generate.
            count: Optional number of items to generate (if not provided, the agent will decide).
            
        Yields:
            Dictionary containing event type and data.
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
        async for event in self.stream_items(category, count):
            yield event

    async def terminate(self) -> Dict[str, Any]:
        """Terminate the agent and clean up resources."""
        return {"status": "terminated", "name": self.name}


# Global instance for use across the application
stream_items_agent = StreamItemsAgent()


async def initialize_stream_items_agent() -> Dict[str, Any]:
    """
    Convenience function to initialize the global streaming items agent.

    Returns:
        A dictionary indicating the initialization status.
    """
    return await stream_items_agent.initialize()


async def execute_stream_items_agent(category: str, count: Optional[int] = None) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Convenience function to execute the global streaming items agent.

    Args:
        category: The category of items to generate.
        count: Optional number of items to generate.

    Yields:
        A dictionary representing streaming events.
    """
    async for event in stream_items_agent.execute(category, count):
        yield event


async def terminate_stream_items_agent() -> Dict[str, Any]:
    """
    Convenience function to terminate the global streaming items agent.

    Returns:
        A dictionary indicating the termination status.
    """
    return await stream_items_agent.terminate()
