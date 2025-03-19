
<!-- File: root/modules/module2-story-agent/docs/phase2.md -->

# Module 2 - Phase 2: Custom Story Telling Agent Enhancements

## Purpose and Learnings

In Phase 2 we build on the successful implementation of the baseline deterministic story agent (Phase 1) by introducing custom narrative enhancements and improving our code organization. This phase focuses on:
- **Reorganizing the Agents Folder:** We will create a dedicated subfolder for all story-related agents. This involves moving the existing story agent to a new location and renaming it for clarity.
- **Introducing a Custom Story Agent:** We develop a new custom agent that enriches narrative generation with creative enhancements.
- **API Enhancements:** The FastAPI router will be updated to expose separate endpoints for both the baseline and custom agents.
- **Key Learnings:**  
  - How to reorganize and rename files to improve maintainability.
  - Extending a baseline implementation with creative custom logic.
  - Updating API endpoints and tests to reflect new structure.
  
The **definition of done** for this phase is achieving a working test (i.e., all tests pass when running `python -m pytest tests/`).

---

## Phase 2 Updates: Detailed Step 1

### Step 1: Reorganizing the Agents Directory and Renaming Files

#### A. Create a Subfolder for Story Agents
- **Action:**  
  In the `app/agents/` directory, create a new subfolder named `story`.

- **New Structure:**
  ```
  app/
  ├── agents/
  │   └── story/
  │       ├── baseline_story_agent.py   # Formerly: story_telling_agent.py
  │       └── custom_story_agent.py       # New custom agent file
  ```

#### B. Move and Rename the Existing Story Agent
- **Current File:**  
  `app/agents/story_telling_agent.py` (from Phase 1)

- **New Location and Name:**  
  Move the file into `app/agents/story/` and rename it to `baseline_story_agent.py`.

- **File Content Changes (if needed):**
  - Update any internal references (e.g., module-level docstrings) to reflect the new filename.
  - Confirm that function names remain unchanged unless required.

  **Example Header Update:**
  ```python
  # File: root/modules/module2-story-agent/app/agents/story/baseline_story_agent.py
  # This file contains the baseline deterministic story agent from Phase 1.
  ```

#### C. Update the Router to Reflect New File Structure

- **Old Import Statement in Router (before Phase 2):**
  ```python
  from app.agents.story_telling_agent import run_story_agent
  ```
- **New Import Statement in Router:**
  ```python
  from app.agents.story.baseline_story_agent import run_story_agent
  ```

- **File to Update:**  
  `app/routers/story_telling_router.py`

- **Updated Router Code Snippet:**
  ```python
  # File: root/modules/module2-story-agent/app/routers/story_telling_router.py

  from fastapi import APIRouter, Depends, HTTPException
  from pydantic import BaseModel, Field
  from app.dependencies import verify_api_key
  # Import the baseline agent from the new subfolder
  from app.agents.story.baseline_story_agent import run_story_agent
  # Import the custom agent (to be added in Phase 2)
  from app.agents.story.custom_story_agent import run_custom_story_agent

  router = APIRouter()

  class StoryRequest(BaseModel):
      topic: str = Field(..., description="The topic for generating a story outline.")

  class StoryResponse(BaseModel):
      outline: str = Field(..., description="The generated story outline.")

  @router.post("/story", response_model=StoryResponse, dependencies=[Depends(verify_api_key)])
  async def story_endpoint(request: StoryRequest):
      """
      Endpoint for the baseline story agent.
      """
      agent_response = await run_story_agent(request.topic)
      if agent_response.startswith("Error"):
          raise HTTPException(status_code=500, detail=agent_response)
      return {"outline": agent_response}

  @router.post("/story/custom", response_model=StoryResponse, dependencies=[Depends(verify_api_key)])
  async def custom_story_endpoint(request: StoryRequest):
      """
      Endpoint for the custom story agent.
      """
      agent_response = await run_custom_story_agent(request.topic)
      if agent_response.startswith("Error"):
          raise HTTPException(status_code=500, detail=agent_response)
      return {"outline": agent_response}
  ```

- Test within the module folder:
``` bash
python -m pytest tests/test_mod2_story.py
```

#### D. Update Tests to Reflect New Endpoints and Structure

- **Old Test File:**  
  The test for the story agent was previously targeting the endpoint `/agents/story/story`.

- **New Test Adjustments:**
  - Ensure tests are still correctly targeting `/agents/story/story` for the baseline agent and add tests for `/agents/story/custom` for the custom agent.
  - Update any file paths if the test file itself has moved (if necessary).

- **Sample Test Update:**
  ```python
  # File: root/modules/module2-story-agent/tests/test_mod2_story.py
  # Updated to use new endpoints from the reorganized structure

  from fastapi.testclient import TestClient
  from app.main import app
  from app.config import API_KEY  # API_KEY is loaded from .env via config.py

  client = TestClient(app)

  def test_story_telling_agent_baseline():
      """
      Test the baseline story agent endpoint.
      """
      topic = "A brave knight"
      response = client.post(
          "/agents/story/story",
          json={"topic": topic},
          headers={"X-API-KEY": API_KEY}
      )
      assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
      data = response.json()
      assert "outline" in data, "Response JSON must contain the key 'outline'"
      assert topic.lower() in data["outline"].lower(), f"Expected the outline to include '{topic}', got: {data['outline']}"

  def test_story_telling_agent_custom():
      """
      Test the custom story agent endpoint.
      """
      topic = "A mysterious adventure"
      response = client.post(
          "/agents/story/custom",
          json={"topic": topic},
          headers={"X-API-KEY": API_KEY}
      )
      assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
      data = response.json()
      assert "outline" in data, "Response JSON must contain the key 'outline'"
      assert topic.lower() in data["outline"].lower(), f"Expected the outline to include '{topic}', got: {data['outline']}"
  ```

---

## 5. Definition of Done

Phase 2 is considered complete when:
- The baseline story agent has been successfully moved and renamed to `baseline_story_agent.py` within the `/agents/story` subfolder.
- The FastAPI router (`story_telling_router.py`) has been updated to import from the new location.
- A new custom story agent (`custom_story_agent.py`) has been implemented and its endpoint is added to the router.
- All tests (both baseline and custom endpoints) pass when running:
  ```bash
  python -m pytest tests/
  ```
- The working test serves as the definition of done for Phase 2.

---

*End of Phase 2 Updates for Module 2.*
