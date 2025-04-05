# File: root/modules/module2-story-agent/app/agents/story/advanced_story_agent.py
"""
This file implements an advanced story agent that uses a multi-step workflow:
1. Generate a detailed, structured story outline using a function tool.
2. Expand the outline into a full story with enhanced narrative details.
The workflow is traced for debugging purposes, and comprehensive comments explain each step.
"""

from agents import Agent, Runner, function_tool, trace
from pydantic import BaseModel

# Define a structured model for the story outline.
class StoryOutline(BaseModel):
    introduction: str
    body: str
    conclusion: str

@function_tool
def generate_advanced_outline(topic: str) -> StoryOutline:
    """
    Generate a detailed story outline based on the provided topic.
    
    This function creates a structured outline consisting of three parts:
    - Introduction: Sets the stage with vivid descriptions.
    - Body: Develops the central narrative with conflict and adventure.
    - Conclusion: Provides a satisfying resolution to the story.
    
    Args:
        topic (str): The topic or theme for the story.
        
    Returns:
        StoryOutline: A structured outline with introduction, body, and conclusion.
    """
    return StoryOutline(
        introduction=f"Introduction for '{topic}': Begin with an evocative setting and compelling characters.",
        body=f"Body for '{topic}': Develop the conflict and outline the journey with dynamic events.",
        conclusion=f"Conclusion for '{topic}': Resolve the conflict with a memorable and thoughtful ending."
    )

@function_tool
def generate_advanced_story_body(outline: StoryOutline) -> str:
    """
    Expand the given story outline into a complete story.
    
    This function takes a structured StoryOutline and converts it into a full narrative.
    
    Args:
        outline (StoryOutline): The structured outline for the story.
        
    Returns:
        str: The complete story text, combining the introduction, body, and conclusion.
    """
    return (
        f"{outline.introduction}\n\n"
        f"{outline.body}\n\n"
        f"{outline.conclusion}"
    )

# Create the advanced story agent with both function tools.
advanced_story_agent = Agent(
    name="AdvancedStoryAgent",
    instructions=(
        "Generate a complete story by first creating a detailed outline and then expanding it into a full narrative. "
        "The outline should include an evocative introduction, a dynamic body, and a satisfying conclusion."
    ),
    tools=[generate_advanced_outline, generate_advanced_story_body],
)

async def run_advanced_story_agent(topic: str) -> str:
    """
    Execute the advanced story agent using a multi-step workflow:
    
    1. Generate a detailed story outline using the 'generate_advanced_outline' tool.
    2. Expand the outline into a full story using the 'generate_advanced_story_body' tool.
    
    The entire process is wrapped in a trace context for debugging.
    
    Args:
        topic (str): The topic or theme for the story.
        
    Returns:
        str: The complete story text, or an error message if any step fails.
    """
    try:
        with trace("Advanced Story Flow"):
            # Step 1: Generate the advanced outline.
            outline_result = await Runner.run(advanced_story_agent, topic)
            if not outline_result or not outline_result.final_output:
                return "Error: No output from advanced outline generation."
            
            # Extract the structured outline.
            outline = outline_result.final_output
            
            # Step 2: Generate the full story using the outline.
            story_result = await Runner.run(advanced_story_agent, outline)
            if not story_result or not story_result.final_output:
                return "Error: No output from advanced story body generation."
            
            return story_result.final_output
    except Exception as e:
        return f"Error: {str(e)}"
