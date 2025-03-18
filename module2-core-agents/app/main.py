# backend/app/main.py
from fastapi import FastAPI
from app.routers import hello_world, deterministic

app = FastAPI(title="FastAPI OpenAI Agents - Module 2", version="2.0.0")

# Mount routers under the /agent path.
app.include_router(hello_world.router, prefix="/agent")
app.include_router(deterministic.router, prefix="/agent")

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}