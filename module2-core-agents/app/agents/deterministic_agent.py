import asyncio
from typing import Optional

from pydantic import BaseModel

from agents import Agent, Runner, function_tool, trace

class StoryOutline(BaseModel):
    """Represents a story outline with distinct sections."""
    introduction: str
    body: str
    conclusion: str

class FullStory(BaseModel):
    """Represents the full story"""
    outline: StoryOutline
    story_text: str
    ending: str

@function_tool
def generate_outline(topic: str) -> StoryOutline:
    """Generates a story outline based on the user's input topic.

    Args:
        topic: The topic or theme for the story.

    Returns:
        A StoryOutline object.
    """
    # In a real application, you'd use an LLM call here.
    return StoryOutline(
        introduction=f"Introduction for {topic}: Introduce main character and setting.",
        body=f"Body for {topic}: Character faces a challenge or goes on an adventure.",
        conclusion=f"Conclusion for {topic}: Resolution of the challenge and character's fate.",
    )
@function_tool
def generate_story(outline: StoryOutline) -> str:
    """Generates a short story based on the provided story outline.

    Args:
        outline: The StoryOutline object to base the story on.

    Returns:
        The full text of the story (without the ending).
    """
    # In a real application, you'd use an LLM call here.
    return (
        f"{outline.introduction}\n\n{outline.body}"
    )
@function_tool
def generate_ending(story: str) -> str:
    """Generates an ending for the provided story.

    Args:
        story: The story text (without the ending).

    Returns:
        The ending of the story.
    """
    # In a real application, you'd use an LLM call here.
    return f"{story}.\n\nAnd they all lived happily ever after. The End."


story_outline_agent = Agent(
    name="StoryOutlineAgent",
    instructions="Generate a very short story outline based on the user's input.",
    tools=[generate_outline],
)

story_agent = Agent(
    name="StoryAgent",
    instructions="Write a short story based on the given outline.",
    tools=[generate_story],
)

ending_agent = Agent(
    name="EndingAgent",
    instructions="Write a short ending based on the given story.",
    tools=[generate_ending],
)

deterministic_agent = Agent(
    name="DeterministicAgent",
    instructions="You are a story writing agent.  Your task is to generate a complete short story based on a topic provided by the user. You MUST proceed in the following STRICT sequence: 1. Generate an outline using the StoryOutlineAgent. 2. Generate the main story body based on the outline using the StoryAgent. 3. Generate an ending for the story using the EndingAgent.",
    tools=[generate_outline, generate_story, generate_ending] #Include the tools for the runner.
)



async def run_deterministic_agent(user_input: str) -> str:
    """
    Runs the deterministic story generation process.  This function orchestrates the
    interaction between the three sub-agents (outline generation, story generation,
    and ending generation) to produce a complete story.

    Args:
        user_input: The topic or theme for the story, provided by the user.

    Returns:
        The complete story, including the outline, main body, and ending.  Returns
        an error message if any step fails.

    Raises:
        Exception: If any of the agent calls fail.

    Swagger Description:
        This endpoint triggers a deterministic story generation process.  The user
        provides a topic, and the system generates a story in three distinct steps:

        1. **Outline Generation:** An outline is created based on the user's topic.
        2. **Story Body Generation:**  A story body is written based on the generated outline.
        3. **Ending Generation:** An ending is added to complete the story.

        The process is deterministic, meaning the steps always occur in the same order.
        The final output is the complete story.
    """
    try:
        with trace("Deterministic Story Flow"):
            # 1. Generate the outline using the dedicated agent
            outline_result = await Runner.run(story_outline_agent, user_input)
            if not outline_result or not outline_result.final_output:
                return "Error: Outline generation failed."
            outline: StoryOutline = outline_result.final_output

            # 2. Generate the story body using the dedicated agent
            story_result = await Runner.run(story_agent, outline)
            if not story_result or not story_result.final_output:
                return "Error: Story generation failed."
            story_body: str = story_result.final_output

            # 3. Generate the ending using the dedicated agent.
            ending_result = await Runner.run(ending_agent, story_body)
            if not ending_result or not ending_result.final_output:
                 return "Error: Ending generation failed."
            story_ending: str = ending_result.final_output
            full_story = FullStory(outline=outline, story_text=story_body, ending=story_ending)

            return str(full_story) #Return the full story

    except Exception as e:
        return f"Error: {str(e)}"