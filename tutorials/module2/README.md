# Module 2: Storytelling Agent

Welcome to Module 2! In this module, you'll extend your foundational skills from Module 1 by creating storytelling agents capable of generating compelling narratives. You'll start with a simple deterministic agent, progress to a creatively enhanced custom agent, and finally implement an advanced agent with a structured multi-step workflow. Throughout the process, you'll learn key project management practices, effective code organization, and robust testing strategies.

---

## What You'll Learn

By the end of Module 2, you'll be able to:

- Organize your codebase effectively by creating structured directories for agents.
- Develop multiple AI storytelling agents: baseline, custom, and advanced.
- Implement narrative enhancements and sophisticated logic.
- Clearly define and integrate API endpoints using FastAPI.
- Ensure your agents' reliability with comprehensive tests.

Your goal is to pass all tests by executing:
```bash
python -m pytest tests/
```

---

## Project Structure

```plaintext
module2-story-agent/
├── app/
│   ├── agents/
│   │   └── story/
│   │       ├── baseline_story_agent.py      # Simple deterministic agent
│   │       ├── custom_story_agent.py        # Enhanced creative narrative agent
│   │       └── advanced_story_agent.py      # Multi-step structured narrative agent
│   ├── routers/
│   │   └── story_router.py                  # FastAPI endpoints for agents
│   ├── config.py                            # Configuration management
│   ├── dependencies.py                      # Reusable dependencies (e.g., API keys)
│   └── main.py                              # FastAPI application entry point
├── docs/
│   ├── phase1.md                            # Baseline agent implementation
│   ├── phase2.md                            # Custom enhancements and organization
│   └── implementation_process.md            # Implementation checklist
├── tests/
│   ├── test_hello_world.py                  # Module 1 retained tests
│   └── test_mod2_story.py                   # Storytelling agents tests
└── README.md                                # This document
```

---

## Setup & Installation

Follow these steps to prepare your environment:

### Prerequisites
- Python 3.10+
- Virtual environment recommended
- Dependencies listed in `requirements.txt`

### Installation

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file at the project's root with:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
API_KEY=your_api_key_here
```

---

## Running the Application

Start your FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

Access your API docs at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

### Baseline Story Agent
- **Endpoint:** `/agents/story/baseline`
- **Description:** Generates a simple, structured outline for a provided topic.

### Custom Story Agent
- **Endpoint:** `/agents/story/custom`
- **Description:** Creates a vivid, detailed narrative outline enhancing creativity.

### Advanced Story Agent
- **Endpoint:** `/agents/story/advanced`
- **Description:** Uses a structured, multi-step process to generate a complete story from an outline.

*All endpoints require an API key provided via the `X-API-KEY` header.*

---

## Testing

Verify your implementations using provided tests:

```bash
python -m pytest tests/
```

Tests confirm:
- Successful responses (HTTP 200).
- Correct incorporation of provided topics.
- Reliable endpoint performance.

---

## Documentation & Learning Resources

Explore detailed guides in the `/docs` directory:

- **Phase 1 Documentation:** `docs/phase1.md`
- **Phase 2 Documentation:** `docs/phase2.md`
- **Implementation Checklist:** `docs/implementation_process.md`
- **Detailed Tutorials:** Located in `tutorials/module2/tutorial.md`

---

## Additional Resources

- [OpenAI Deterministic Agents Example](https://github.com/openai/openai-agents-python/blob/main/examples/agent_patterns/deterministic.py)
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)

---

## Quick Reference Commands

```bash
# Navigate to module directory
cd path/to/module2-story-agent

# Start the FastAPI server
python -m uvicorn app.main:app --reload

# Run all tests
python -m pytest tests/
```

---

Congratulations on progressing to Module 2! You're enhancing your skills in AI-driven narrative generation, effective code management, and rigorous testing—essential components for sophisticated AI agent development.

Happy storytelling!

