# File: root/modules/module4-llm-providers/app/main.py
from fastapi import FastAPI
from app.routers import hello_world
from app.routers import story_router
from app.routers import basic_router
from app.routers import advanced_router
from app.routers import llm_router

app = FastAPI(title="Module4 - LLM Providers", version="1.0.0")

app.include_router(hello_world.router, prefix="/agent")
app.include_router(story_router.router, prefix="/agents/story") # Mod 2 agents
app.include_router(basic_router.router, prefix="/agents/basic") # Mod 3 basic agents
app.include_router(advanced_router.router, prefix="/agents/advanced") # Mod 3 advanced agents
app.include_router(llm_router.router, prefix="/agents/llm-provider") # Mod 4 llm providers

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
