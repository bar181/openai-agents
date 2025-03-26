# File: root/modules/module5-orchestration/app/main.py
from fastapi import FastAPI
from app.routers import hello_world
from app.routers import story_router
from app.routers import basic_router
from app.routers import advanced_router
from app.routers import llm_router
from app.routers import orchestration_router
from app.agents.orchestration.trace_processor import trace_processor

# The trace processor is already registered in the trace_processor.py file

app = FastAPI(title="Module5 - Orchestration", version="1.0.0")

app.include_router(hello_world.router, prefix="/agent")
app.include_router(story_router.router, prefix="/agents/story") # Mod 2 agents
app.include_router(basic_router.router, prefix="/agents/basic") # Mod 3 basic agents
app.include_router(advanced_router.router, prefix="/agents/advanced") # Mod 3 advanced agents
app.include_router(llm_router.router, prefix="/agents/llm-provider") # Mod 4 llm providers
app.include_router(orchestration_router.router) # Mod 5 orchestration (prefix already in router)

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running with Orchestration"}
