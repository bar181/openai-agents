# File: root/modules/module2-story-agent/app/agents/story/custom_story_agent.py
from agents import Agent, Runner, function_tool
 

@function_tool
def generate_custom_outline(topic: str) -> str:
    """
    Generate a creative, detailed story outline based on a topic.
    
    Accepts a topic string and returns a multi-part outline with creative elements.
    """
    return (
        f"Custom Story Outline for '{topic}':\n"
        "1. **Introduction:** Set stage with vivid imagery and mood.\n"
        "2. **Conflict:** Present a compelling challenge or dilemma.\n"
        "3. **Climax:** Build suspense with dynamic, unexpected turns.\n"
        "4. **Conclusion:** Deliver a satisfying resolution that inspires reflection."
    )


custom_story_agent = Agent(
    name="CustomStoryAgent",
    instructions="Generate a creative and detailed story outline with enhanced narrative flair.",
    tools=[generate_custom_outline],
)


async def run_custom_story_agent(topic: str) -> str:
    """
    Run the custom story agent using the provided topic.
    
    Returns the generated outline or an error message if execution fails.
    """
    try:
        result = await Runner.run(custom_story_agent, topic)
        return result.final_output if result else "Error: No output from custom agent."
    except Exception as e:
        return f"Error: {str(e)}"
