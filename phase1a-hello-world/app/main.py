# backend/app/main.py
from fastapi import FastAPI
from app.routers import hello_world

app = FastAPI()

app.include_router(hello_world.router, prefix="/agent") # Added a prefix

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}