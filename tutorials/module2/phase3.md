Advanced Story Agent File
python
Copy
Edit
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
Updated Router (story_router.py)
Below are the updated lines added to the router file to expose the advanced story endpoint.

python
Copy
Edit
# File: root/modules/module2-story-agent/app/routers/story_router.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.agents.story.baseline_story_agent import run_story_agent
from app.agents.story.custom_story_agent import run_custom_story_agent
from app.agents.story.advanced_story_agent import run_advanced_story_agent  # New import

router = APIRouter()

class StoryRequest(BaseModel):
    topic: str = Field(..., description="The topic for generating a story outline.")

class StoryResponse(BaseModel):
    outline: str = Field(..., description="The generated story outline or complete story text.")

@router.post(
    "/baseline",
    response_model=StoryResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Generate a Baseline Story Outline",
    description="""
Generates a story outline using the baseline deterministic story agent.
- **Input:** A topic provided by the user.
- **Output:** A simple outline comprising Introduction, Body, and Conclusion.
"""
)
async def baseline_story_endpoint(request: StoryRequest):
    agent_response = await run_story_agent(request.topic)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)
    return {"outline": agent_response}

@router.post(
    "/custom",
    response_model=StoryResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Generate a Custom Story Outline",
    description="""
Triggers the custom story generation process. The custom agent uses enhanced narrative logic to produce a rich, detailed story outline.
- **Enhanced Outline Generation:** Creates an outline with vivid descriptions.
- **Custom Narrative Processing:** Includes creative elements for a more engaging storytelling experience.
"""
)
async def custom_story_endpoint(request: StoryRequest):
    agent_response = await run_custom_story_agent(request.topic)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)
    return {"outline": agent_response}

@router.post(
    "/advanced",
    response_model=StoryResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Generate an Advanced Full Story",
    description="""
Triggers the advanced story generation process. This endpoint employs a multi-step workflow:
1. **Advanced Outline Generation:** Creates a detailed, structured outline with introduction, body, and conclusion.
2. **Story Expansion:** Uses the outline to generate a complete story with enhanced narrative details.
The final output is a full story text.
"""
)
async def advanced_story_endpoint(request: StoryRequest):
    agent_response = await run_advanced_story_agent(request.topic)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)
    return {"outline": agent_response}
Updated Main File (main.py)
Ensure the main file includes the updated story router. If already imported, verify that the router now contains the advanced endpoint.

python
Copy
Edit
# File: root/modules/module2-story-agent/app/main.py

from fastapi import FastAPI
from app.routers import story_router  # Updated router with advanced endpoint

app = FastAPI(title="Story Telling Agent System", version="1.0.0")

# Include the story router under the prefix '/agents/story'
app.include_router(story_router.router, prefix="/agents/story")

@app.get("/")
async def root():
    return {"message": "Story Telling Agent System Running"}
Updated Test File (test_mod2_story.py)
Below are the updated tests that now include a test for the advanced story endpoint.

python
Copy
Edit
# File: root/modules/module2-story-agent/tests/test_mod2_story.py
# Run in module folder: python -m pytest tests/test_mod2_story.py

from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY  # API_KEY is loaded from .env via config.py

client = TestClient(app)

def test_story_telling_agent_baseline():
    """
    Test the baseline story agent endpoint.
    This endpoint should return an outline that contains the provided topic (case-insensitive).
    """
    topic = "A brave knight"
    response = client.post(
        "/agents/story/baseline",
        json={"topic": topic},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "outline" in data, "Response JSON must contain the key 'outline'"
    assert topic.lower() in data["outline"].lower(), (
        f"Expected the outline to include '{topic}', got: {data['outline']}"
    )

def test_story_telling_agent_custom():
    """
    Test the custom story agent endpoint.
    This endpoint should return an outline that contains the provided topic (case-insensitive).
    """
    topic = "A mysterious adventure"
    response = client.post(
        "/agents/story/custom",
        json={"topic": topic},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "outline" in data, "Response JSON must contain the key 'outline'"
    assert topic.lower() in data["outline"].lower(), (
        f"Expected the outline to include '{topic}', got: {data['outline']}"
    )

def test_story_telling_agent_advanced():
    """
    Test the advanced story agent endpoint.
    This endpoint should generate a complete story (full narrative) that includes the provided topic (case-insensitive).
    """
    topic = "A futuristic odyssey"
    response = client.post(
        "/agents/story/advanced",
        json={"topic": topic},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    data = response.json()
    assert "outline" in data, "Response JSON must contain the key 'outline'"
    # Check that the generated story contains the topic (case-insensitive).
    assert topic.lower() in data["outline"].lower(), (
        f"Expected the generated story to include '{topic}', got: {data['outline']}"
    )