from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.agents.deterministic_agent import run_deterministic_agent

router = APIRouter()

class DeterministicRequest(BaseModel):
    message: str = Field(..., description="Topic for the story generation.")

class DeterministicResponse(BaseModel):
    response: str = Field(..., description="Final output from the deterministic agent.")

@router.post("/deterministic", response_model=DeterministicResponse, dependencies=[Depends(verify_api_key)])
async def deterministic_endpoint(request: DeterministicRequest):
    result = await run_deterministic_agent(request.message)
    if result.startswith("Error"):
        raise HTTPException(status_code=500, detail=result)
    return {"response": result}
