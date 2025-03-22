<!-- File: root/tutorials/module2/tutorial.md -->

# Module 2 Tutorial: Storytelling Agent

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Director @ Agentics Foundation, Programmer and Data Scientist with over 20 years of experience, Master's Student at Harvard University, CS50 Teaching Fellow/Course Assistant, Instructor and Course Designer*

---

## Welcome to Module 2!

Welcome back! Bradley Ross here, ready to guide you through Module 2. In this module, you'll build upon the skills from Module 1 (Hello World Agent) by creating a Storytelling Agent. This project will introduce you to generating creative, engaging narratives using OpenAI-powered agents. You'll also learn structured project management, effective code organization, and rigorous testing techniques.

**Important:** To maintain consistency, start by copying your Module 1 directory and rename it appropriately. The detailed documents in `/docs` (`phase1.md`, `phase2.md`, and `implementation_process.md`) will serve as your roadmap.

---

## What You'll Achieve

By completing this module, you will:

- Develop three distinct types of storytelling agents: Baseline, Custom, and Advanced.
- Organize your project's files and directories for clarity and scalability.
- Integrate creative narrative elements into your AI agents.
- Define clear and robust API endpoints using FastAPI.
- Write thorough tests to validate the reliability of your agents.

---

## Recommended Workflow

Follow this structured path for optimal results:

1. **Start Fresh:** Copy your completed Module 1 folder as a new starting point.
2. **Review `/docs` Files:** Regularly consult these documents as you progress.
3. **Analyze Provided Code:** Carefully examine the provided examples (`baseline_story_agent.py`, `custom_story_agent.py`, `advanced_story_agent.py`).
4. **Consult This Tutorial Frequently:** Use this tutorial alongside your coding to stay on track.

*Pro tip:* Use AI coding assistants by pointing them to the provided agent files to speed up customizations.

---

## Module Breakdown

This module covers three increasingly sophisticated agents:

### 1. **Baseline Story Agent (`baseline_story_agent.py`)**

- **Objective:** Generate simple, structured story outlines.
- **Approach:** Deterministic output following a clear, predictable structure.

**Pseudocode:**
```python
function generate_outline(topic):
    return simple structured outline

async function run_baseline_agent(topic):
    return agent-generated outline
```

### 2. **Custom Story Agent (`custom_story_agent.py`)**

- **Objective:** Produce vivid, creatively enhanced narratives.
- **Approach:** Extend baseline functionality with richer, descriptive content.

**Pseudocode:**
```python
function generate_custom_outline(topic):
    return detailed and vivid story outline

async function run_custom_agent(topic):
    return enhanced narrative outline
```

### 3. **Advanced Story Agent (`advanced_story_agent.py`)**

- **Objective:** Create complex, structured stories using advanced workflows.
- **Approach:** Two-step narrative creation leveraging structured Pydantic models.

**Pseudocode:**
```python
class StoryOutline(BaseModel):
    introduction: str
    body: str
    conclusion: str

function generate_advanced_outline(topic):
    return structured StoryOutline

function generate_story_body(outline):
    return expanded complete story

async function run_advanced_agent(topic):
    outline = generate_advanced_outline(topic)
    story = generate_story_body(outline)
    return complete narrative
```

---

## Project Structure

Your project should match this clear, scalable structure:

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

## FastAPI Integration

Integrate your storytelling agents into clear FastAPI endpoints (`routers/story_router.py`):

- `/agents/story/baseline`
- `/agents/story/custom`
- `/agents/story/advanced`

**Pseudocode Example:**
```python
@app.post("/agents/story/baseline")
async def baseline_endpoint(topic: str):
    return await run_baseline_agent(topic)

@app.post("/agents/story/custom")
async def custom_endpoint(topic: str):
    return await run_custom_agent(topic)

@app.post("/agents/story/advanced")
async def advanced_endpoint(topic: str):
    return await run_advanced_agent(topic)
```

---

## Testing Your Work

Quality assurance is vital. Use provided test cases in `tests/test_mod2_story.py` to confirm:

- Correct HTTP responses (expecting status code 200).
- Outputs properly reflect the provided topics.

Execute tests regularly:
```bash
python -m pytest tests/
```

Ensure all tests pass successfully.

---

## Best Practices for Learning

- **Make Small Changes:** Incremental updates make debugging simpler.
- **Review Often:** Regularly check `/docs` files for alignment.
- **Leverage AI Tools:** Use AI-powered coding tools to streamline your work.

---

## Next Steps

Congratulations on completing Module 2! You're now capable of developing engaging storytelling agents, structuring clear codebases, and implementing rigorous testing. Module 3 will take your skills even further into the world of complex agent systems and advanced integrations.

Keep innovating, and see you in the next module!

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Director @ Agentics Foundation*

