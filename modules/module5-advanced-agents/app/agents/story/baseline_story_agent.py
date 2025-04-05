  # File: root/modules/module2-story-agent/app/agents/story_telling_agent.py

from agents import Agent, Runner, function_tool

@function_tool
def generate_story_outline(topic: str) -> str:
    """
    Pseudocode:
    1. Receive a topic string.
    2. Generate a simple outline for the story.
    3. Return the generated outline.
    """
    return f"Outline for {topic}: Introduction, Body, Conclusion."

# Instantiate the deterministic agent using the above tool.
story_agent = Agent(
    name="StoryDeterministicAgent",
    instructions="Based on the provided topic, generate a story outline deterministically using the given tool.",
    tools=[generate_story_outline],
)

async def run_story_agent(topic: str) -> str:
    """
    Pseudocode:
    1. Accept a topic as input.
    2. Execute the deterministic agent using the Runner.
    3. Return the agent's final output, or an error message if execution fails.
    """
    try:
        result = await Runner.run(story_agent, topic)
        return result.final_output if result else "Error: No output from the agent."
    except Exception as e:
        return f"Error: {str(e)}"
