```markdown
<!-- File: root/modules/module2-story-agent/README.md -->

# Module 2: Story Telling Agent

## Overview

Module 2 builds upon the foundational work of Module 1 by introducing a Story Telling Agent. In this module, we start with a baseline deterministic agent (Phase 1) and then extend it with custom narrative enhancements (Phase 2). In Phase 3, an advanced story agent is added that leverages a multi-step workflow to generate a complete narrative. This module teaches you how to reorganize your code for better clarity, split agents into subfolders, and implement creative custom logic. You will learn how to:
- Reorganize the agents directory by creating a dedicated subfolder for story agents.
- Rename and move the baseline agent for improved maintainability.
- Implement a new custom story agent with enhanced narrative output.
- Add an advanced story agent that generates a full narrative using a multi-step process.
- Update API endpoints and tests to accommodate these changes.
- Validate your work through passing tests.

The definition of done for this module is achieving a working test suite where all tests pass using `python -m pytest tests/`.

---

## Folder Structure

```
module2-story-agent/
├── app/
│   ├── agents/
│   │   └── story/
│   │       ├── baseline_story_agent.py   # Baseline deterministic story agent (from Phase 1, moved and renamed)
│   │       ├── custom_story_agent.py       # Custom story agent with narrative enhancements (Phase 2)
│   │       └── advanced_story_agent.py     # Advanced story agent with a multi-step narrative workflow (Phase 3)
│   ├── routers/
│   │   └── story_router.py                 # API endpoints for story agents
│   ├── config.py                           # Environment variable and configuration management
│   ├── dependencies.py                     # Reusable dependencies (e.g., API key validation)
│   └── main.py                             # FastAPI application entry point
├── docs/
│   ├── phase1.md                           # Phase 1 Implementation Document (baseline implementation)
│   ├── phase2.md                           # Phase 2 Implementation Document (custom enhancements and reorganization)
│   └── implementation_process.md         # Checklist of activities completed for Module 2
├── tests/
│   ├── test_hello_world.py                 # Module 1 tests (retained)
│   └── test_mod2_story.py                  # Tests for baseline, custom, and advanced story endpoints
└── README.md                               # This file
```

---

## Setup & Installation

1. **Prerequisites:**
   - Python 3.10 or higher.
   - A virtual environment is recommended.
   - Required packages are listed in the module’s `requirements.txt`.

2. **Installation:**
   - Create and activate a virtual environment:
     ```bash
     python -m venv env
     source env/bin/activate  # On Windows: env\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Environment Configuration:**
   - Ensure a `.env` file is present at the root level with the following variables:
     ```dotenv
     OPENAI_API_KEY=your_openai_api_key_here
     API_KEY=your_api_key_here
     ```

---

## Running the Application

To start the FastAPI server, navigate to the module root and run:

```bash
python -m uvicorn app.main:app --reload
```

Access the API documentation at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

This module exposes three main endpoints under the `/agents/story` prefix:

1. **Baseline Story Agent**
   - **Endpoint:** `/agents/story/baseline`
   - **Description:** Generates a simple story outline based on the input topic using the baseline deterministic agent.
   
2. **Custom Story Agent**
   - **Endpoint:** `/agents/story/custom`
   - **Description:** Generates a story outline with enhanced narrative creativity using the custom story agent.

3. **Advanced Story Agent**
   - **Endpoint:** `/agents/story/advanced`
   - **Description:** Generates a complete story using a multi-step workflow that first creates a detailed, structured outline and then expands it into a full narrative with enhanced storytelling elements.

All endpoints require an API key provided via the `X-API-KEY` header.

---

## Testing

To run tests for this module, execute:

```bash
python -m pytest tests/
```

The tests verify that:
- The endpoints return a 200 status code.
- The generated outlines and stories contain the expected story topic.
- All endpoints (baseline, custom, and advanced) are functioning as intended.

---

## Documentation & Learning Resources

- **Phase 1 Documentation:** Detailed in `docs/phase1.md`
- **Phase 2 Documentation:** Custom enhancements and folder reorganization are described in `docs/phase2.md`
- **Implementation Process:** Activities and checklist are outlined in `docs/implementation_process.md`
- **Tutorials:** Additional step-by-step tutorials for Module 2 can be found in the root-level `tutorials/` directory under the appropriate module folder.

---

## Additional Resources

- [OpenAI Agents Deterministic Example](https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/deterministic.py)
- FastAPI Documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

---

## Terminal Instructions

1. **Navigate to the Module Directory:**
   ```bash
   cd path/to/module2-story-agent
   ```

2. **Run the FastAPI Server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

3. **Run the Tests:**
   ```bash
   python -m pytest tests/
   ```

---

This module provides a comprehensive learning experience that guides you from a simple deterministic agent to a fully customized and advanced story generation system. Through reorganizing code, implementing new features, and updating tests and documentation, you will enhance both your technical skills and your ability to manage scalable projects.

Enjoy exploring and enhancing your AI agent capabilities!
```