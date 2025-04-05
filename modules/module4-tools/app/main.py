from fastapi import FastAPI
from app.routers import (
    hello_world, story_router, basic_router, streaming_router,
    math_router, string_router, datetime_router, echo_router, multi_tool_router,
    additional_tools_router, visualization_router
)

app = FastAPI(title="Module4 - Tools", version="1.0.0")

# Module 1: Hello World
app.include_router(hello_world.router, prefix="/agent")
# Module 2: Story Agents
app.include_router(story_router.router, prefix="/agents/story")
# Module 3: Basic & Streaming Agents
app.include_router(basic_router.router, prefix="/agents/basic")
app.include_router(streaming_router.router, prefix="/agents/streaming")
# Module 4: Tools
app.include_router(math_router.router, prefix="/tools/math")
app.include_router(string_router.router, prefix="/tools/string")
app.include_router(datetime_router.router, prefix="/tools/datetime")
app.include_router(echo_router.router, prefix="/tools/echo")
app.include_router(multi_tool_router.router, prefix="/tools/multi-tool")
app.include_router(additional_tools_router.router, prefix="/tools/additional")
app.include_router(visualization_router.router, prefix="/tools/visualization")

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
