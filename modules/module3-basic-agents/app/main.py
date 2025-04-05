# File: root/modules/module3-basic-agents/app/main.py

from fastapi import FastAPI
from app.routers import hello_world, story_router, basic_router, streaming_router

app = FastAPI(title="Module3 - Basic Agents", version="1.0.0")

app.include_router(hello_world.router, prefix="/agent")
app.include_router(story_router.router, prefix="/agents/story")
app.include_router(basic_router.router, prefix="/agents/basic")
app.include_router(streaming_router.router, prefix="/agents/streaming")


@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
