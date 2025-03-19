# File: root/modules/module2-story-agent/app/routers/story_telling_router.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.agents.story_telling_agent import run_story_agent

router = APIRouter()

class StoryRequest(BaseModel):
    topic: str = Field(..., description="The topic for generating a story outline.")

class StoryResponse(BaseModel):
    outline: str = Field(..., description="The generated story outline.")

@router.post("/story", response_model=StoryResponse, dependencies=[Depends(verify_api_key)])
async def story_endpoint(request: StoryRequest):
    """
    Pseudocode:
    1. Extract the 'topic' from the request.
    2. Call the 'run_story_agent' function with the provided topic.
    3. If the agent returns an error, raise an HTTPException.
    4. Otherwise, return the generated outline in the response.
    """
    agent_response = await run_story_agent(request.topic)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)
    return {"outline": agent_response}
