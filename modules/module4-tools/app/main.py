# File: root/modules/module2-story-agent/app/main.py
from fastapi import FastAPI
from app.routers import hello_world
from app.routers import story_router
from app.routers import basic_router
from app.routers import advanced_router

app = FastAPI(title="Module3 - Basic Agents", version="1.0.0")

app.include_router(hello_world.router, prefix="/agent")
app.include_router(story_router.router, prefix="/agents/story") # Mod 2 agents
app.include_router(basic_router.router, prefix="/agents/basic") # Mod 3 basic agents
app.include_router(advanced_router.router, prefix="/agents/advanced") # Mod 3 advanced agents

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
