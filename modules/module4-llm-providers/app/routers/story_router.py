# File: root/modules/module2-story-agent/app/routers/story_router.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.agents.story.baseline_story_agent import run_story_agent
from app.agents.story.custom_story_agent import run_custom_story_agent
from app.agents.story.advanced_story_agent import run_advanced_story_agent  # phase 3

router = APIRouter(tags=["Create a Story Agents"])

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
- **Enhanced Outline Generation:** The custom agent creates an outline with vivid descriptions.
- **Custom Narrative Processing:** The agent includes creative elements for a more engaging storytelling experience.
- **uses function_tool** generate_custom_outline

Accepts a topic string and returns a multi-part outline with creative elements
1. **Introduction:** Set stage with vivid imagery and mood.
2. **Conflict:** Present a compelling challenge or dilemma
3. **Climax:** Build suspense with dynamic, unexpected turns.
4. **Conclusion:** Deliver a satisfying resolution that inspires reflection

"""
)
async def custom_story_endpoint(request: StoryRequest):
    """
    Endpoint for the custom story agent.
    This endpoint triggers the custom story generation process, returning a story outline with creative enhancements.
    """
    agent_response = await run_custom_story_agent(request.topic)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)
    return {"outline": agent_response}

# phase 3
@router.post(
    "/advanced",
    response_model=StoryResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Generate an Advanced Full Story",
    description="""
Triggers the advanced story generation process which follows a multi-step workflow to produce a complete narrative. The process includes:

1. **Advanced Outline Generation:**  
   - Uses a dedicated function tool to create a detailed, structured outline.  
   - The outline is divided into:
     - **Introduction:** Sets the scene with evocative descriptions and establishes key characters.
     - **Body:** Develops the central conflict and narrative through dynamic events.
     - **Conclusion:** Provides a thoughtful and memorable resolution.

2. **Story Expansion:**  
   - The generated outline is then processed by another function tool to expand it into a full story.
   - The resulting story integrates enhanced narrative details, ensuring a rich and engaging storytelling experience.

3. **Workflow Tracing:**  
   - The entire process is executed within a trace context to aid in debugging and performance monitoring.

**Implementation Details:**  
- Utilizes function tools `generate_advanced_outline` and `generate_advanced_story_body` to perform the multi-step narrative generation.
- Accepts a topic string and returns a complete story text that includes all narrative components.

The final output is a comprehensive, full-length story that not only outlines the narrative structure but also delivers an immersive storytelling experience.
"""
)
async def advanced_story_endpoint(request: StoryRequest):
    agent_response = await run_advanced_story_agent(request.topic)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)
    return {"outline": agent_response}