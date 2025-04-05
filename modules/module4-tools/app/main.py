from fastapi import FastAPI
from app.routers import basic_router, streaming_router, story_router, hello_world, tools_router  # NEW import

app = FastAPI(title="Module4 - Tools", version="1.0.0")

app.include_router(hello_world.router, prefix="/agent")           # Module 1
app.include_router(story_router.router, prefix="/agents/story")     # Module 2
app.include_router(basic_router.router, prefix="/agents/basic")     # Module 3
app.include_router(streaming_router.router, prefix="/agents/streaming")  # Module 3
app.include_router(tools_router.router, prefix="/tools")            # Module 4 (New)

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
