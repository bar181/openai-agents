<!-- File: README.md -->

# OpenAI Agents MonoRepo for FastAPI

Welcome to the OpenAI Agents MonoRepo, a structured, self-paced course designed to teach you how to build, enhance, and deploy intelligent AI agents using the OpenAI Agents SDK and FastAPI. This repository is organized into clearly defined modules, each progressively introducing more complex agent functionalities and patterns.
 
---

## Current Status

### Completed Modules

**Module 1: Hello World Agent**
- **Agent:** `hello_world_agent.py`
- **Skills Learned:** Basic environment setup, agent implementation with OpenAI SDK, FastAPI integration, endpoint testing.

**Module 2: Story Telling Agent**
- **Agents:**
  - `baseline_story_agent.py`: Generates basic deterministic outlines.
  - `custom_story_agent.py`: Provides creatively enhanced outlines.
  - `advanced_story_agent.py`: Implements a structured, multi-step story generation workflow.
- **Skills Learned:** Project reorganization, advanced narrative generation, comprehensive API documentation, structured testing.

**Module 3: Basic and Advanced OpenAI Agents**
- **Agents:**
  - Basic Agents:
    - `lifecycle_agent.py`: Implements agent lifecycle management (initialization, execution, termination).
    - `dynamic_prompt_agent.py`: Enables runtime updates to system prompts.
    - `stream_text_agent.py`: Provides real-time streaming text responses.
    - `stream_items_agent.py`: Delivers structured item sequences incrementally.
  - Advanced Agents:
    - `generic_lifecycle_agent.py`: Enhanced agent with comprehensive tool integration.
    - `multi_tool_agent.py`: Advanced agent with multiple tool capabilities and context management.
- **Tools:** Extensive tool suite including math operations, string manipulation, data handling, JSON processing, CSV handling, database operations, text analysis, API integration, and data visualization.
- **Skills Learned:** Agent lifecycle management, dynamic system prompts, real-time streaming, tool integration, context management, comprehensive testing strategies.

---

## Upcoming Modules

### Module 4: Custom LLM Providers
- **Agent:** `custom_llm_agent.py`

### Module 5: Supabase Integration
- **Agent:** `supabase_agent.py`

### Module 6: OpenAI Agent Tools
- **Agents:** `file_search_agent.py`, `web_search_agent.py`

### Module 7: Handoffs
- **Agents:** `handoff_agent.py`, `message_filter.py`, `message_filter_streaming.py`

### Module 8: Agent Patterns
- **Agents:** `routing_agent.py`, `parallelization_agent.py`, `input_guardrails.py`, `output_guardrails.py`, `agents_as_tools.py`

### Module 9: Research Agent
- **Agent:** `research_agent.py`

### Module 10: Edge Function Agents
- **Agents:** To be determined (TypeScript to Python conversions)

### Module 11: DSPy Integration
- **Agent:** `dspy_agent.py`

### Module 12: Single POST Endpoint Agents
- **Agent:** `post_endpoint_agent.py`

### Module 13: Dynamic Agents
- **Agent:** `dynamic_creation_agent.py`

### Advanced Modules
- **Agents:** `chain_of_thought_agent.py`, `agent_swarm.py`, `reflection_agent.py`

---

## Repository Structure

```
monorepo/
├── modules/
│   └── module1-hello-world/
│       ├── app/
│       │   ├── agents/
│       │   │   ├── hello_world_agent.py
│       │   ├── routers/hello_world.py
│       │   ├── config.py
│       │   ├── dependencies.py
│       │   └── main.py
│       ├── docs/
│       └── tests/
│   └── module3-basic-agents/
│       ├── app/
│       │   ├── agents/
│       │   │   ├── basic/
│       │   │   │   ├── lifecycle_agent.py
│       │   │   │   ├── dynamic_prompt_agent.py
│       │   │   │   ├── stream_text_agent.py
│       │   │   │   └── stream_items_agent.py
│       │   │   └── advanced/
│       │   │       ├── generic_lifecycle_agent.py
│       │   │       └── multi_tool_agent.py
│       │   ├── routers/
│       │   │   ├── basic_router.py
│       │   │   └── advanced_router.py
│       │   ├── tools/
│       │   │   ├── base_tool.py
│       │   │   ├── math_tools.py
│       │   │   ├── string_tools.py
│       │   │   ├── data_tools.py
│       │   │   ├── datetime_tools.py
│       │   │   ├── echo_tools.py
│       │   │   ├── json_tools.py
│       │   │   ├── csv_tools.py
│       │   │   ├── database_tools.py
│       │   │   ├── analysis_tools.py
│       │   │   ├── api_tools.py
│       │   │   └── visualization_tools.py
│       │   ├── config.py
│       │   ├── dependencies.py
│       │   └── main.py
│       ├── docs/
│       └── tests/
│   └── module2-story-agent/
│       ├── app/
│       │   ├── agents/story/
│       │   │   ├── baseline_story_agent.py
│       │   │   ├── custom_story_agent.py
│       │   │   └── advanced_story_agent.py
│       │   ├── routers/story_router.py
│       │   ├── config.py
│       │   ├── dependencies.py
│       │   └── main.py
│       ├── docs/
│       └── tests/
├── tutorials/
│   ├── module1/tutorial.md
│   ├── module2/tutorial.md
│   └── module3/tutorial.md
└── README.md
```

---

## Getting Started

**1. Clone the Repository:**
```bash
git clone <repository_url>
cd monorepo
```

**2. Set Up Your Environment:**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r modules/module1-hello-world/requirements.txt
```

**3. Run the FastAPI Server:**
```bash
cd modules/module1-hello-world
python -m uvicorn app.main:app --reload
```

Access Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs).

**4. Execute Tests:**
```bash
python -m pytest tests/
```

Repeat these steps within each module folder as you progress.

---

## Documentation and Learning Resources

Each module includes comprehensive documentation:
- **Implementation Plans:** Detailed setup and coding instructions.
- **Phase Guides:** Step-by-step implementation with code snippets.
- **Tutorials:** In-depth explanations, pseudocode, and examples in a guided format.

---

## About the Instructor

**Bradley Ross** is an experienced Agentics Engineer and Technical Lead, currently pursuing a Master's degree at Harvard University. Bradley has served as a Teaching Fellow/Course Assistant for Harvard's CS50 course for ten terms.  He mentors students and developers in software engineering, AI development, and web programming.

---

## Acknowledgements
[OpenAI Agents Python](https://github.com/openai/openai-agents-python) [MIT License](https://github.com/openai/openai-agents-python/blob/main/LICENSE)


---

## Conclusion

This structured approach offers a robust framework for learning and building increasingly sophisticated AI agents. Whether you're developing practical skills or exploring advanced AI integration, this repository will serve as your comprehensive resource.

Happy coding and exploring AI agents!

