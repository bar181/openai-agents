```markdown
# Module 2 – Core Research Agents & Advanced Patterns

This module is the second part of our multi-module project to build OpenAI agents using FastAPI and the OpenAI Agents SDK. In this module, we extend the basic "Hello World" agent (from Module 1) to introduce more sophisticated agent patterns. You will learn how to implement agents that perform multi-step deterministic tasks, route requests to specialized sub-agents, and combine these patterns into a unified workflow.  This is a *mono-repo* structure, so this module builds directly upon Module 1.

The agents in this module include:

1.  **Deterministic Agent** – Breaks a complex task into sequential steps (e.g., generate an outline, then a story, then an ending). The agent executes a series of function calls in a predefined order, using the output of one step as the input to the next.  This demonstrates how to create agents that perform tasks requiring a specific, predictable execution path.

2.  **Routing (Handoff) Agent** – Acts as a triage agent that examines the incoming request and delegates it to a specialized sub-agent.  The routing logic can be based on any characteristic of the request, such as the language used, the type of task, or the presence of specific keywords. This agent showcases how to create a flexible system where different agents handle different types of requests. The implementation uses the `handoff` functionality of the OpenAI Agents SDK.

3.  **Combined Agent** – Integrates both deterministic and routing patterns. This agent demonstrates a more complex workflow where the agent might first perform some deterministic steps and then, based on the intermediate results or user input, hand off part of the task to a specialized sub-agent.  This combines the predictability of deterministic execution with the flexibility of dynamic routing.

Each agent is implemented as a separate file within the `app/agents` directory and is exposed via its own FastAPI router in the `app/routers` directory. Unit tests accompany each agent to ensure they work as expected, and are located in the `tests` directory.

---

## Project Structure

```
module2-core-research-agents/  <-- This is the root of the current module
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application initialization
│   ├── config.py              # Loads environment variables (from .env)
│   ├── dependencies.py        # API key authentication for endpoints
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── deterministic_agent.py  # Implements the deterministic multi-step agent
│   │   ├── routing_agent.py          # Implements the handoff/routing agent
│   │   └── combined_agent.py         # Combines deterministic and routing patterns
│   └── routers/
│       ├── __init__.py
│       ├── deterministic.py          # Exposes deterministic agent endpoints
│       ├── routing.py                # Exposes routing agent endpoints
│       └── combined.py               # Exposes combined agent endpoints
├── .env                       # Environment variables file (API keys)
├── requirements.txt           # Lists all project dependencies
├── tests/
│   ├── test_deterministic.py  # Unit tests for deterministic agent endpoints
│   ├── test_routing.py        # Unit tests for routing agent endpoints
│   └── test_combined.py       # Unit tests for combined agent endpoints
├── tutorial.md                # Detailed, step-by-step guide for Module2
└── README.md                  # This overview and usage instructions for Module2

#  Files from Module 1 (included because this is a mono-repo):
module1-hello-world/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── hello_world_agent.py
│   └── routers/
│       ├── __init__.py
│       └── hello_world.py
├── .env
├── requirements.txt
├── tests/
│   └── test_hello_world.py
├── module1-tutorial.md
└── README.md
```

---

## Getting Started

### 1. Clone and Setup

-   Clone the repository (if you haven't already) and navigate to the `module2-core-research-agents` folder.  *Important:*  This assumes you are working within a single repository (mono-repo) that contains both `module1-hello-world` and `module2-core-research-agents`.
-   Create and activate your virtual environment (it's recommended to create a new virtual environment for each module):
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows: env\Scripts\activate
    ```
-   Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Configure Environment

-   Create a `.env` file in the root of the `module2-core-research-agents` directory (or rename an existing `.env.sample` to `.env`).  *Note:*  If you already have a `.env` file from Module 1, you can either use that same file (and add any new variables needed for Module 2) or create a separate `.env` file specifically for Module 2.  If you use separate files, make sure you're loading the correct one when running Module 2's code.
-   Add your keys:
    ```dotenv
    OPENAI_API_KEY=sk-YourOpenAIKeyHere
    API_KEY=mysecretkey
    ```

### 3. Running the Server

-   Start the FastAPI server with Uvicorn:
    ```bash
    python -m uvicorn app.main:app --reload
    ```
-   Open your browser at [http://localhost:8000/docs](http://localhost:8000/docs) to view the interactive API documentation. Make sure to authorize with your `API_KEY` from the `.env` file.

### 4. Running Tests

-   To run all unit tests for Module 2, execute:
    ```bash
    python -m pytest tests/
    ```

---

## Overview of Agents in This Module

### Deterministic Agent

-   **Purpose:** Demonstrates a multi-step process by sequentially executing tasks (e.g., generate outline → story → ending).  This agent provides a predictable and controlled workflow.
-   **Implementation:**
    -   Located in `app/agents/deterministic_agent.py`
    -   Exposed via `app/routers/deterministic.py`
    -   Uses the `@function_tool` decorator to define the individual steps as tools.
    -   The agent's instructions guide it to call these tools in the correct sequence.
-   **Testing:** Unit tests in `tests/test_deterministic.py` verify the correct execution order and data flow between steps.

### Routing (Handoff) Agent

-   **Purpose:** Uses triage logic to examine the request and delegate processing to specialized sub-agents (e.g., based on language). This allows for a more flexible and scalable system.
-   **Implementation:**
    -   Located in `app/agents/routing_agent.py`
    -   Exposed via `app/routers/routing.py`
    -   Uses the `handoff` functionality of the OpenAI Agents SDK to delegate to sub-agents.
    -   Defines multiple sub-agents (e.g., `EnglishAgent`, `SpanishAgent`).
    -   The main routing agent's instructions determine which sub-agent to call.
-   **Testing:** Unit tests in `tests/test_routing.py` verify that the routing logic correctly selects the appropriate sub-agent based on the input.

### Combined Agent

-   **Purpose:** Integrates both deterministic multi-step processing and dynamic handoff patterns into a single agent workflow. This demonstrates a more complex and powerful agent design.
-   **Implementation:**
    -   Located in `app/agents/combined_agent.py`
    -   Exposed via `app/routers/combined.py`
    -   Combines the techniques used in the deterministic and routing agents.
    -   Might have some initial deterministic steps, followed by a handoff to a specialized sub-agent based on the results of those steps.
-   **Testing:** Unit tests in `tests/test_combined.py` verify both the deterministic execution and the correct handoff behavior.

---

## QUICK GUIDE

### Create your .env file
Rename the `.env.sample` file to `.env` (or create a new one) and add your OpenAI API key (visit openai.com for details) and a custom `API_KEY` for authorization.

### In the terminal:
```bash
#  Make sure you are in the module2-core-research-agents directory
cd module2-core-research-agents

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Start the FastAPI server with Uvicorn
python -m uvicorn app.main:app --reload

# View FastAPI API documentation (authorize with the API_KEY in your .env file)
http://localhost:8000/docs

# Run tests
python -m pytest tests/
```

---

## Future Plans

-   **Module 3:**
    Introduce additional advanced features such as:
    -   Function Tool Agent (e.g., `get_weather` - expanding on the basic function calling).
    -   LLM-as-a-Judge Agent for self-refinement and evaluation.
    -   Parallelization of agent calls using `asyncio.gather` for improved performance.
    -   Guardrails for input and output safety to prevent undesirable agent behavior.

-   **Module 4:**
    Build a composite multi-agent research system that integrates planner, search, and writer agents with advanced orchestration, persistent state, and additional tools (e.g., vector stores, file search). This will demonstrate a more complete and realistic agent application.

Each new module will build cumulatively on the previous ones, ensuring that the earlier agents remain available and new functionality is added incrementally within the mono-repo structure.

---

Happy coding, and enjoy building your core research agents!
```

Key changes and improvements:

*   **Mono-Repo Context:**  Explicitly states that this is a mono-repo and that Module 2 builds on Module 1. Includes the Module 1 file structure to show the relationship.
*   **Detailed Agent Descriptions:** Provides more in-depth explanations of each agent's purpose, implementation details, and how they use the OpenAI Agents SDK features.
*   **Clearer Instructions:**  Provides more precise instructions for setting up the environment and running the code, specifically addressing the mono-repo structure.
*   **Emphasis on Key Concepts:** Highlights important concepts like `@function_tool`, `handoff`, and the role of agent instructions.
*   **Testing Details:**  Explains what aspects of each agent are tested.
*   **Future Plans:**  Provides a more detailed roadmap for future modules, outlining the specific features that will be added.
*   **Virtual Environment:** Specifically recommends creating a new virtual environment.
*   **`.env` File Handling:** Clarifies the options for handling the `.env` file in a mono-repo context.
*   **Navigation:** Clarifies the user should navigate to the `module2-core-research-agents` folder.

This revised README provides a much more comprehensive and user-friendly guide to Module 2, taking into account the mono-repo structure and the specific features of the OpenAI Agents SDK. It's ready to be used as the main documentation for your project.
