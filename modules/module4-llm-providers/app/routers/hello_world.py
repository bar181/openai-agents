# backend/app/routers/hello_world.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.agents.hello_world_agent import run_hello_agent

router = APIRouter(tags=["Get Started Agents"])

class HelloRequest(BaseModel):
    message: str = Field(..., description="The user's message to the agent.")

class HelloResponse(BaseModel):
    response: str = Field(..., description="The agent's response.")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message.")

@router.post("/hello", response_model=HelloResponse, dependencies=[Depends(verify_api_key)])
async def hello_endpoint(request: HelloRequest):
    """
    A simple endpoint that greets the user using the Hello World agent.
    """
    agent_response = await run_hello_agent(request.message)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)

    return {"response": agent_response}
