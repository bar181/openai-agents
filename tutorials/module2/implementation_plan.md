
<!-- File: root/modules/module2-story-agent/docs/implementation_plan.md -->

# Module 2 Implementation Plan: Story Telling Agent

This document outlines the step-by-step plan to implement Module 2, which focuses on creating a Story Telling Agent. This module builds upon the concepts from Module 1 and uses the OpenAI Agents deterministic example as its foundation. In this module, you will first create a baseline deterministic agent and then extend it with custom narrative enhancements. In addition, you will reorganize the agents folder for better maintainability. Finally, you will add an advanced story agent that leverages a multi-step workflow to generate a complete story.

---

## 1. Overview

**Module Goal:**  
Develop a functional Story Telling Agent that initially replicates the behavior of the deterministic agent example and then customizes it to generate coherent, engaging stories based on user input. The module concludes with the creation of an advanced agent that produces a full narrative using a multi-step process.

**Key Components:**
- **Baseline Implementation:**  
  Use the deterministic agent pattern from [OpenAI Agents deterministic.py](https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/deterministic.py) to create a baseline agent that generates a simple story outline.
- **Custom Enhancements:**  
  Extend and customize the baseline agent to include creative narrative logic. This involves adding detailed descriptions, vivid imagery, and more dynamic story components.
- **Reorganization:**  
  Improve the project structure by reorganizing the agents folder. Move the existing baseline agent into a dedicated subfolder (`/agents/story`) and rename it for clarity. Introduce a new custom story agent in the same subfolder.
- **Advanced Agent:**  
  Add a new advanced story agent that implements a multi-step workflow:
  - Generate a detailed, structured outline.
  - Expand the outline into a full story with enhanced narrative details.
- **API Exposure:**  
  Integrate all three agents (baseline, custom, and advanced) into FastAPI endpoints with comprehensive Swagger documentation.
- **Testing & Documentation:**  
  Develop tests and update documentation to reflect these changes.

---

## 2. Prerequisites

- **Python Version:** 3.10+
- **Environment:** Virtual environment set up with dependencies (as listed in the module's `requirements.txt`)
- **Dependencies:** FastAPI, Uvicorn, python-dotenv, openai, pydantic, openai-agents, pytest, pytest-asyncio
- **Configuration:** Properly configured environment variables in the `.env` file (e.g., `OPENAI_API_KEY`, `API_KEY`)

---

## 3. Implementation Phases

### Phase 1: Create a Working Deterministic Agent
- **Objective:**  
  - Implement a working agent based on the deterministic agent pattern.
  - Adapt the code from the OpenAI deterministic example so that it functions as a baseline agent.
- **Tasks:**
  - Review and analyze the code from `deterministic.py` in the OpenAI Agents examples.
  - Create the agent file (e.g., `story_telling_agent.py`) under `app/agents/` that replicates the deterministic behavior.
  - Set up the corresponding FastAPI router in `app/routers/` (e.g., `story_telling_router.py`) to expose the agent via an API endpoint.
  - Ensure all configurations, dependencies, and testing utilities are in place.
- **Milestones:**
  - A fully functional deterministic agent that responds correctly to user input.
  - End-to-end API testing for the baseline agent functionality.

### Phase 2: Customize and Reorganize for a Story Telling Agent
- **Objective:**  
  - Extend and customize the baseline deterministic agent to generate story outlines, story bodies, and endings with creative enhancements.
  - Reorganize the agents directory by creating a dedicated subfolder for story-related agents, renaming the existing baseline agent, and adding a new custom story agent.
- **Tasks:**
  - **Reorganize Agents Directory:**
    - Create a subfolder named `story` within `app/agents/`.
    - Move the existing baseline agent file (`story_telling_agent.py`) into `app/agents/story/` and rename it to `baseline_story_agent.py`.
  - **Implement the Custom Story Agent:**
    - Create a new file `custom_story_agent.py` in `app/agents/story/`.
    - Implement a new function tool (e.g., `generate_custom_outline`) that includes enhanced narrative elements.
    - Instantiate a custom agent (`custom_story_agent`) with refined instructions.
    - Develop an asynchronous runner function (`run_custom_story_agent`) to execute the custom agent.
  - **Update the Router:**
    - Rename the router file to `story_router.py` if needed.
    - Update import statements to reflect the new file structure.
    - Add two endpoints: one for the baseline story agent (`/baseline`) and one for the custom story agent (`/custom`).
    - Enhance Swagger documentation for both endpoints with detailed descriptions.
  - **Testing:**
    - Update test files to target the new endpoints (`/agents/story/baseline` and `/agents/story/custom`).
- **Milestones:**
  - A reorganized agents folder with:
    - `baseline_story_agent.py` (moved and renamed from Phase 1)
    - `custom_story_agent.py` (new file with creative enhancements)
  - Updated API endpoints in the router that are fully documented.
  - Passing tests for both baseline and custom endpoints.

### Phase 3: Add an Advanced Story Agent
- **Objective:**  
  - Develop an advanced story agent that implements a multi-step workflow to generate a complete narrative.
  - This agent will first generate a detailed, structured story outline, and then expand it into a full story with enhanced narrative details.
- **Tasks:**
  - **Implement the Advanced Story Agent:**
    - Create a new file `advanced_story_agent.py` in `app/agents/story/`.
    - Define structured output using Pydantic models (e.g., `StoryOutline`) to enforce consistency.
    - Implement two function tools:
      - One for generating an advanced outline (`generate_advanced_outline`).
      - One for expanding the outline into a full story (`generate_advanced_story_body`).
    - Instantiate the advanced agent (`advanced_story_agent`) with detailed instructions.
    - Develop an asynchronous runner function (`run_advanced_story_agent`) that executes the multi-step workflow within a trace context.
  - **Update the Router:**
    - Update the router file (`story_router.py`) to add a new endpoint `/advanced` for the advanced story agent.
    - Enhance Swagger documentation for this endpoint with a comprehensive description that details the multi-step workflow.
  - **Update Tests:**
    - Add or update tests in `tests/test_mod2_story.py` to target the new `/agents/story/advanced` endpoint.
    - Ensure that the tests validate that the complete narrative contains the input topic (case-insensitive) and meets expected structure.
- **Milestones:**
  - A new advanced story agent file (`advanced_story_agent.py`) that implements the multi-step narrative workflow.
  - An updated router with an `/advanced` endpoint that is fully documented.
  - Passing tests for the advanced endpoint, ensuring the complete story is generated as expected.

---

## 4. Testing Strategy

- **Unit Testing:**  
  Validate individual functions and tool methods used in all agents for correctness.
- **Integration Testing:**  
  Use FastAPI's `TestClient` to simulate API requests and verify that endpoints for the baseline, custom, and advanced agents work correctly.
- **Error Handling:**  
  Ensure proper error messages are returned for invalid input or failed agent processing.
- **Milestones:**
  - All tests pass for the deterministic baseline, customized, and advanced story agents.

---

## 5. Documentation and Resources

- **Code Documentation:**  
  Each file should include the file name and path as a header comment. Ensure that functions have clear docstrings and inline comments.
- **Tutorial and Guidance:**  
  Update module-specific tutorials and code snippets in the `docs/` folder as development progresses.
- **Reference Materials:**  
  Consult the [OpenAI Agents deterministic example](https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/deterministic.py) for baseline logic and implementation ideas.

---

## 6. Deployment

- **Local Deployment:**  
  Use Uvicorn to run the FastAPI server and verify that endpoints are accessible via Swagger UI.
- **Validation:**  
  Confirm that the environment variables load correctly and that all agents respond as expected to various inputs.

---

## 7. Next Steps

- **Phase Documentation:**  
  Later, two additional `/plans` documents will be created, detailing code snippets for `main.py`, routers, agents, and tests.
- **Feedback & Iteration:**  
  Gather feedback on the agents' performance and make iterative improvements.
- **Preparation for Advanced Features:**  
  Begin planning for future modules that might extend or build upon the story telling agent.

---
