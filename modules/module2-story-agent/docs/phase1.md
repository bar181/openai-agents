```markdown
<!-- File: root/modules/module2-story-agent/docs/phase1.md -->

# Module 2 - Phase 1: Baseline Deterministic Agent Implementation

This document provides a detailed plan for Phase 1 of Module 2: creating a working deterministic agent that will serve as the basis for our Story Telling Agent. In this phase, we replicate the behavior of the deterministic agent from the OpenAI Agents example and expose it via a FastAPI endpoint. In later phases, we will customize the agent for enhanced story generation.

---

## 1. Objective

- **Goal:**  
  Develop a baseline deterministic agent that accepts a story topic and returns a generated outline. This phase sets up the core functionality using the existing deterministic pattern.

- **Key Deliverables:**
  - A working agent located in `app/agents/story_telling_agent.py`.
  - A FastAPI router in `app/routers/story_telling_router.py` that calls the agent.
  - An updated `app/main.py` file that includes the new router.
  - Detailed instructions, pseudocode, and example code for each file.

---

## 2. Folder Structure and File Changes

Ensure that the following structure exists under `root/modules/module2-story-agent/`:

```
module2-story-agent/
├── app/
│   ├── agents/
│   │   └── story_telling_agent.py
│   ├── routers/
│   │   └── story_telling_router.py
│   ├── config.py         # (Copied from Module 1, ensure environment variables are loaded)
│   ├── dependencies.py   # (Copied from Module 1, includes API key authentication)
│   └── main.py
├── docs/
│   └── phase1.md         # (This document)
└── tests/                # (Will be updated in later phases)
```

---

## 3. Detailed File Instructions and Code

### A. Agent Implementation

**File:** `root/modules/module2-story-agent/app/agents/story_telling_agent.py`

- **Purpose:**  
  Implement a baseline deterministic agent that generates a simple story outline based on a given topic.

- **Pseudocode:**
  1. Define a function tool (`generate_story_outline`) that takes a topic as input and returns a generated outline.
  2. Create an agent (`story_agent`) using this tool.
  3. Implement an asynchronous function (`run_story_agent`) that runs the agent with the provided topic and returns the output.

- **Code:**

  ```python
  # File: root/modules/module2-story-agent/app/agents/story_telling_agent.py

  from agents import Agent, Runner, function_tool

  @function_tool
  def generate_story_outline(topic: str) -> str:
      """
      Pseudocode:
      1. Receive a topic string.
      2. Generate a simple outline for the story.
      3. Return the generated outline.
      """
      return f"Outline for {topic}: Introduction, Body, Conclusion."

  # Instantiate the deterministic agent using the above tool.
  story_agent = Agent(
      name="StoryDeterministicAgent",
      instructions="Based on the provided topic, generate a story outline deterministically using the given tool.",
      tools=[generate_story_outline],
  )

  async def run_story_agent(topic: str) -> str:
      """
      Pseudocode:
      1. Accept a topic as input.
      2. Execute the deterministic agent using the Runner.
      3. Return the agent's final output, or an error message if execution fails.
      """
      try:
          result = await Runner.run(story_agent, topic)
          return result.final_output if result else "Error: No output from the agent."
      except Exception as e:
          return f"Error: {str(e)}"
  ```

---

### B. Router Implementation

**File:** `root/modules/module2-story-agent/app/routers/story_telling_router.py`

- **Purpose:**  
  Create an API endpoint that receives a topic from the user, invokes the deterministic agent, and returns the generated outline.

- **Pseudocode:**
  1. Define a Pydantic model (`StoryRequest`) with a `topic` field.
  2. Define a Pydantic model (`StoryResponse`) to encapsulate the output.
  3. Create a POST endpoint that:
     - Validates the API key via dependency injection.
     - Extracts the topic from the request.
     - Calls `run_story_agent` to generate the outline.
     - Returns the outline or an error message.

- **Code:**

  ```python
  # File: root/modules/module2-story-agent/app/routers/story_telling_router.py

  from fastapi import APIRouter, Depends, HTTPException
  from pydantic import BaseModel, Field
  from app.dependencies import verify_api_key
  from app.agents.story_telling_agent import run_story_agent

  router = APIRouter()

  class StoryRequest(BaseModel):
      topic: str = Field(..., description="The topic for generating a story outline.")

  class StoryResponse(BaseModel):
      outline: str = Field(..., description="The generated story outline.")

  @router.post("/story", response_model=StoryResponse, dependencies=[Depends(verify_api_key)])
  async def story_endpoint(request: StoryRequest):
      """
      Pseudocode:
      1. Extract the 'topic' from the request.
      2. Call the 'run_story_agent' function with the provided topic.
      3. If the agent returns an error, raise an HTTPException.
      4. Otherwise, return the generated outline in the response.
      """
      agent_response = await run_story_agent(request.topic)
      if agent_response.startswith("Error"):
          raise HTTPException(status_code=500, detail=agent_response)
      return {"outline": agent_response}
  ```

---

### C. Main Application Update

**File:** `root/modules/module2-story-agent/app/main.py`

- **Purpose:**  
  Update the main FastAPI application to include the new story telling router.

- **Pseudocode:**
  1. Import the story telling router.
  2. Include the router with a suitable prefix (e.g., `/agents/story`).
  3. Define a root endpoint that confirms the application is running.

- **Code:**

  ```python
  # File: root/modules/module2-story-agent/app/main.py
  # keep existing module 1 router and agent
  
  from fastapi import FastAPI
  from app.routers import story_telling_router

  app = FastAPI(title="Story Telling Agent System", version="1.0.0")

  # Include the story telling router under the prefix '/agents/story'
  app.include_router(story_telling_router.router, prefix="/agents/story")

  @app.get("/")
  async def root():
      return {"message": "Story Telling Agent System Running"}
  ```

---

## 4. Summary and Next Steps

- **Phase 1 Deliverables:**
  - A baseline deterministic agent in `app/agents/story_telling_agent.py` that generates a simple outline.
  - An API endpoint in `app/routers/story_telling_router.py` that accepts a topic and returns the outline.
  - An updated `app/main.py` that includes the new router.
- **Next Steps:**
  - Validate the implementation using FastAPI's Swagger UI.
  - Write initial tests for the new endpoint (to be covered in later phases).
  - In Phase 2, further customize the agent to handle more sophisticated story generation.

---

*End of Module 2 Phase 1 Implementation Document.*
```