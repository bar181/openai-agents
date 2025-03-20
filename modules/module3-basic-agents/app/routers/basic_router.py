# File: root/modules/module3-basic-agents/app/routers/basic_router.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key

from app.agents.basic.lifecycle_agent import (
    initialize_agent,
    execute_agent,
    terminate_agent,
)

from app.agents.basic.dynamic_prompt_agent import (
    update_system_prompt,
    execute_dynamic_prompt_agent,
)

router = APIRouter(tags=["Basic Agents"])

# Input and Output models
class ExecuteLifecycleRequest(BaseModel):
    input: str = Field(..., description="Input data for lifecycle agent execution")

class LifecycleResponse(BaseModel):
    result: str = Field(..., description="Result of lifecycle agent execution")

class PromptUpdateRequest(BaseModel):
    new_prompt: str = Field(..., description="The new prompt for the dynamic agent")

class PromptUpdateResponse(BaseModel):
    prompt: str = Field(..., description="Updated prompt for dynamic agent")

class DynamicPromptExecuteRequest(BaseModel):
    input: str = Field(..., description="Input data for dynamic prompt agent")

class DynamicPromptExecuteResponse(BaseModel):
    response: str = Field(..., description="Agent response after executing dynamic prompt")

# Lifecycle Management Endpoints
@router.post("/lifecycle/initialize", dependencies=[Depends(verify_api_key)])
async def lifecycle_initialize():
    message = initialize_agent()
    return {"message": message}

@router.post("/lifecycle/execute",
             response_model=LifecycleResponse,
             dependencies=[Depends(verify_api_key)])
async def lifecycle_execute(request: ExecuteLifecycleRequest):
    result = execute_agent({"input": request.input})
    return LifecycleResponse(result=result)

@router.post("/lifecycle/terminate", dependencies=[Depends(verify_api_key)])
async def lifecycle_terminate():
    message = terminate_agent()
    return {"message": message}

# Dynamic Prompt Endpoints
@router.post("/dynamic-prompt/update",
             response_model=PromptUpdateResponse,
             dependencies=[Depends(verify_api_key)])
async def dynamic_prompt_update(request: PromptUpdateRequest):
    prompt = update_system_prompt(request.new_prompt)
    return PromptUpdateResponse(prompt=prompt)

@router.post("/dynamic-prompt/execute",
             response_model=DynamicPromptExecuteResponse,
             dependencies=[Depends(verify_api_key)])
async def dynamic_prompt_execute(request: DynamicPromptExecuteRequest):
    response = execute_dynamic_prompt_agent({"input": request.input})
    return DynamicPromptExecuteResponse(response=response)
