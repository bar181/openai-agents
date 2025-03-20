<!-- File: root/tutorials/module3/tutorial.md -->

# Module 2 Tutorial: Story Telling Agent

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Master's Student at Harvard University, CS50 Teaching Fellow for 10 Terms*

---

## Welcome to Module 2!

Welcome back! Bradley Ross here. In Module 2, we're expanding on the basics from Module 1 (Hello World Agent) by diving deeper into more advanced concepts through building a Story Telling Agent. By the end of this module, you'll understand how to enhance a simple deterministic agent into creative narrative generators, using structured project management and thoughtful design.

**Note:** All files from Module 1 are retained in this module. A good practice to follow is copying the entire Module 1 directory and renaming it as your starting point. The detailed `/docs` files (`phase1.md`, `phase2.md`, and `implementation_process.md`) will guide your modifications.

---

## Learning Goals

In this module, you will:

- Create multiple AI agents: Baseline, Custom, and Advanced story agents.
- Reorganize and structure project folders effectively for scalability.
- Integrate creative narrative enhancements into your agent.
- Clearly define API endpoints using FastAPI.
- Write comprehensive tests to ensure agent reliability.

---

## Recommended Workflow

1. **Start by copying Module 1** and renaming it to a new working folder.
2. **Follow the `/docs` files closely**—these documents serve as your roadmap.
3. **Review the example agent files** (`baseline_story_agent.py`, `custom_story_agent.py`, and `advanced_story_agent.py`) carefully.
4. **Consult this tutorial frequently**, referring to the code files as you proceed.

*For advanced users:* Point your AI coding tools to these existing files to expedite customizing or extending your agents.

---

## Detailed Module Structure

This module introduces three agents with increasing complexity:

### 1. **Baseline Story Agent** (`baseline_story_agent.py`)

- **Purpose:** Generate a deterministic, simple story outline.
- **Implementation:** Based on the OpenAI deterministic pattern.
- **Pseudocode:**
  ```
  function generate_outline(topic):
      return simple structured outline

  create baseline agent using generate_outline tool

  async run_baseline_agent(topic):
      return agent-generated outline
  ```

### 2. **Custom Story Agent** (`custom_story_agent.py`)

- **Purpose:** Enhance narrative creativity with detailed, vivid outlines.
- **Implementation:** Extends baseline logic with more creative narrative instructions.
- **Pseudocode:**
  ```
  function generate_custom_outline(topic):
      return detailed, vivid story outline

  create custom agent with generate_custom_outline tool

  async run_custom_agent(topic):
      return enhanced narrative outline
  ```

### 3. **Advanced Story Agent** (`advanced_story_agent.py`)

- **Purpose:** Generate structured, multi-step stories using Pydantic models and a sophisticated workflow.
- **Implementation:**
  - Step 1: Structured outline generation.
  - Step 2: Expand into full story.
- **Pseudocode:**
  ```
  define StoryOutline model:
      introduction, body, conclusion

  function generate_advanced_outline(topic):
      return structured StoryOutline

  function generate_story_body(outline):
      return complete story based on outline

  create advanced agent with both tools

  async run_advanced_agent(topic):
      generate outline
      generate full story from outline
      return complete narrative
  ```

---

## Project Structure Overview

```
module2-story-agent/
├── app/
│   ├── agents/
│   │   └── story/
│   │       ├── baseline_story_agent.py
│   │       ├── custom_story_agent.py
│   │       └── advanced_story_agent.py
│   ├── routers/
│   │   └── story_router.py
│   ├── config.py
│   ├── dependencies.py
│   └── main.py
├── docs/
│   ├── phase1.md
│   ├── phase2.md
│   └── implementation_process.md
├── tests/
│   ├── test_hello_world.py
│   └── test_mod2_story.py
└── tutorials/
    └── module2/
        └── tutorial.md (this file)
```

---

## Integrating Your Agents into FastAPI

### File: `routers/story_router.py`

Define clear API endpoints for each agent:

- **Baseline Endpoint:** `/agents/story/baseline`
- **Custom Endpoint:** `/agents/story/custom`
- **Advanced Endpoint:** `/agents/story/advanced`

*Pseudocode:*
```
define endpoint /baseline:
    return baseline agent output

define endpoint /custom:
    return custom agent output

define endpoint /advanced:
    return advanced agent output
```

Refer to `story_router.py` for complete FastAPI integration details.

---

## Testing Your Agents

Testing is critical. All three endpoints are thoroughly tested in `tests/test_mod2_story.py`.

- **Test coverage includes:**
  - Endpoint status code checks (expecting HTTP 200)
  - Verifying returned outlines/stories include provided topics (case-insensitive)

To run tests:

```bash
python -m pytest tests/
```

Ensure all tests pass successfully.

---

## Tips for Effective Learning

- **Incremental Changes:** Make small, frequent changes and test each step thoroughly.
- **Frequent Reviews:** Regularly revisit `/docs` files to confirm your implementation aligns with intended structure.
- **Utilize AI Assistance:** Leverage AI code-writing tools by providing these module files as references.

---

## Wrapping Up

Great job completing Module 2! You've significantly expanded your understanding of agent complexity, code structure, API integration, and testing.

Module 3 will further deepen your skills with more complex agent workflows and functionalities, preparing you for real-world agent development.

Thank you, and keep building amazing agents!

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, CS50 Teaching Fellow*

