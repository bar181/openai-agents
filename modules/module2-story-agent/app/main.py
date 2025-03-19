# File: root/modules/module2-story-agent/app/main.py
from fastapi import FastAPI
from app.routers import hello_world
from app.routers import story_telling_router

app = FastAPI(title="Module2 - Story Telling Agent", version="1.0.0")

app.include_router(hello_world.router, prefix="/agent") # Added a prefix
app.include_router(story_telling_router.router, prefix="/agents/story")

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
