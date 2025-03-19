```markdown
<!-- File: README.md -->

# OpenAI Agents MonoRepo for FastAPI

Welcome to the OpenAI Agents MonoRepo, a self-paced course project that demonstrates how to build and extend intelligent agents using the OpenAI Agents SDK and FastAPI. This repository is organized as a monorepo with multiple modules, each focusing on specific agent functionalities and design patterns.

---

## Highlights

- **Module 1: Hello World Agent**  
  - **Status:** Complete  
  - **Agent:** `hello_world_agent.py` (a simple agent that returns "Hello, world!")  
  - **Key Learnings:** Environment setup, basic FastAPI integration, and initial agent structure.

- **Module 2: Story Telling Agent**  
  - **Status:** Complete  
  - **Agents:**  
    - `baseline_story_agent.py` – A baseline deterministic agent that generates a simple story outline.
    - `custom_story_agent.py` – A custom story agent with enhanced narrative creativity.
    - `advanced_story_agent.py` – An advanced story agent implementing a multi-step workflow to generate a full narrative.
  - **Key Learnings:** Code reorganization, multi-endpoint API integration, advanced agent workflows, and comprehensive testing.

---

## Future Modules

Below is an outline of future modules along with the specific list of agents to be implemented in each module.

### Module 3: Basic OpenAI Agents
- **Focus:** Introduce various basic agent functionalities, including streaming responses and agent lifecycle management.
- **Planned Agents:**
  - `agent_lifecycle_example.py`
  - `dynamic_system_prompt.py`
  - `stream_items.py`
  - `stream_text.py`

### Module 4: Custom LLM Providers
- **Focus:** Integrate custom Large Language Model (LLM) providers.
- **Planned Agent:**
  - `custom_llm_agent.py` – An agent that selects and uses custom LLM providers based on user input or flags.

### Module 5: Supabase Integration
- **Focus:** Incorporate Supabase for state management, logging, and database interactions.
- **Planned Agent:**
  - `supabase_agent.py` – An agent that integrates Supabase for enhanced functionality and persistence.

### Module 6: OpenAI Agent Tools
- **Focus:** Leverage tools such as file search and web search.
- **Planned Agents:**
  - `file_search_agent.py`
  - `web_search_agent.py`

### Module 7: Handoffs
- **Focus:** Implement mechanisms for agent handoffs and task delegation.
- **Planned Agents:**
  - `handoff_agent.py`
  - `message_filter.py`
  - `message_filter_streaming.py`

### Module 8: Agent Patterns
- **Focus:** Explore advanced design patterns for agents.
- **Planned Agents:**
  - `routing_agent.py`
  - `parallelization_agent.py`
  - `input_guardrails.py`
  - `output_guardrails.py`
  - `agents_as_tools.py`

### Module 9: Research Agent
- **Focus:** Develop a multi-agent research bot for in-depth information gathering.
- **Planned Agent:**
  - `research_agent.py`

### Module 10: Edge Function Agents
- **Focus:** Convert select agents from the Edge Functions repository from TypeScript to Python.
- **Planned Agents:**
  - Agents to be determined (conversion of select edge function agents).

### Module 11: DSPy Integration
- **Focus:** Integrate DSPy for data visualization and enhanced agent analytics.
- **Planned Agent:**
  - `dspy_agent.py`

### Module 12: Single POST Endpoint Agents
- **Focus:** Develop agents that can be invoked via a single POST endpoint specifying agent names and inputs.
- **Planned Agent:**
  - `post_endpoint_agent.py`

### Module 13: Dynamic Agents
- **Focus:** Create agents dynamically based on user-defined parameters.
- **Planned Agent:**
  - `dynamic_creation_agent.py`

### Advanced Modules
- **Focus:** Explore cutting-edge agent functionalities.
- **Planned Agents:**
  - `chain_of_thought_agent.py`
  - `agent_swarm.py`
  - `reflection_agent.py`

---

## Repository Structure

```
monorepo/
├── modules/
│   ├── module1-hello-world/       # Module 1 (Complete)
│   └── module2-story-agent/       # Module 2 (Complete)
│       ├── app/
│       │   ├── agents/
│       │   │   └── story/
│       │   │       ├── baseline_story_agent.py
│       │   │       ├── custom_story_agent.py
│       │   │       └── advanced_story_agent.py
│       │   ├── routers/
│       │   │   └── story_router.py
│       │   ├── config.py
│       │   ├── dependencies.py
│       │   └── main.py
│       ├── docs/
│       │   ├── phase1.md
│       │   ├── phase2.md
│       │   └── implementation_process.md
│       └── tests/
│           ├── test_hello_world.py
│           └── test_mod2_story.py
├── tutorials/                    # Tutorials for each module
│   ├── module1/
│   │   └── tutorial.md
│   └── module2/
│       └── tutorial.md
└── README.md                     # Master readme (this file)
```

---

## How to Get Started

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Navigate to a Module:**
   - For Module 1 (Hello World Agent):
     ```bash
     cd modules/module1-hello-world
     ```
   - For Module 2 (Story Telling Agent):
     ```bash
     cd modules/module2-story-agent
     ```

3. **Set Up the Environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run the Server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   - Access Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs).

5. **Run Tests:**
   ```bash
   python -m pytest tests/
   ```

---

## Conclusion

This monorepo provides a structured, modular approach to building and extending AI agents using FastAPI and the OpenAI Agents SDK. With Module 1 and Module 2 complete, you now have a foundation that demonstrates basic agent functionality, custom narrative enhancements, and advanced multi-step workflows. Future modules will continue to build on this foundation, introducing a variety of agent types and integrations to expand the system’s capabilities.

Enjoy exploring and building your AI agent solutions!
```