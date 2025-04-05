Below is the updated README that incorporates all the changes. In this version, the hello_world and story agents are retained as Module 2 components, while Module 3 introduces the basic agents (lifecycle, dynamic prompt) and streaming agents (both text and items). Comments indicate which files and endpoints are updated or new for Module 3.

---

# Module 3: Basic OpenAI Agents

Welcome to **Module 3**! In this module, you’ll build foundational AI agents using OpenAI's API. You'll start with simple agent functionalities like lifecycle management and dynamic prompt updates, then progress to real-time streaming agents for text and structured items.

> **Note:**  
> - **Module 2:** Contains the `hello_world` and story agents (Module 2 files remain unchanged).  
> - **Module 3:** Introduces the new basic agents (lifecycle, dynamic prompt, streaming text, streaming items). Advanced agents and integrated tool support have been removed to keep the focus on core functionalities.

---

## Features

### Module 2 (Existing)
- **Hello World Agent:**  
  A simple agent demonstrating basic endpoint usage.
- **Story Agents:**  
  Agents that generate narrative content.

### Module 3 (New/Updated)
- **Lifecycle Management:**  
  Initialize, execute, and terminate basic agents.
- **Dynamic System Prompts:**  
  Update an agent’s system prompt at runtime.
- **Streaming Text Agent:**  
  Incrementally stream text responses for real-time interactions.
- **Streaming Items Agent:**  
  Stream structured items (like jokes or facts) sequentially in real time.

---

## Project Structure

Below is a comprehensive folder layout with annotations indicating which files belong to Module 2 and which are new/updated for Module 3.

```plaintext
module3-basic-agents/                          # Root for Module 3 (Basic Agents)
├── app/
│   ├── agents/
│   │   ├── basic/                           # Module 3 - Basic Agents (New/Updated)
│   │   │   ├── lifecycle_agent.py           # Module 3 (New): Basic lifecycle management agent
│   │   │   ├── dynamic_prompt_agent.py      # Module 3 (New): Dynamic prompt update & execution
│   │   │   ├── stream_text_agent.py         # Module 3 (New): Streaming text responses
│   │   │   └── stream_items_agent.py        # Module 3 (New): Streaming structured items
│   │   ├── story/                           # Module 2 - Story Agents (Existing)
│   │   │   ├── advanced_story_agent.py      # Module 2: Advanced story agent
│   │   │   ├── baseline_story_agent.py      # Module 2: Baseline story agent
│   │   │   └── custom_story_agent.py        # Module 2: Custom story agent
│   │   └── hello_world/                     # Module 2 - Hello World Agent (Existing)
│   │       └── hello_world_agent.py         # Module 2: Simple hello world agent
│   ├── routers/
│   │   ├── basic_router.py                  # Module 3 (New): Endpoints for lifecycle and dynamic prompt agents
│   │   ├── streaming_router.py              # Module 3 (New): Combined endpoints for streaming agents
│   │   ├── story_router.py                  # Module 2: Endpoints for story agents
│   │   └── hello_world.py                   # Module 2: Endpoints for hello world agent
│   ├── config.py                            # Module 3 (New): Configuration settings
│   └── dependencies.py                      # Module 3 (New): Shared dependencies (e.g., API key verification)
├── docs/                                    # Documentation, tutorials, and implementation notes
│   ├── implementation_plan.md               # Module 3: Implementation plan for basic agents
│   ├── implementation_process.md            # Module 3: Step-by-step guide for building agents
│   ├── phase1.md                            # Module 3: Phase 1 details
│   ├── tutorial.md                          # Comprehensive tutorial for Module 3
│   └── (other docs as needed)
└── tests/                                   # Tests for all modules
    ├── test_basic_agents.py                # Module 3: Tests for lifecycle & dynamic prompt agents
    ├── test_streaming_agents.py            # Module 3: Tests for streaming text & items agents
    └── (other test files as needed)
```

> **Legend:**  
> - Files marked with **Module 3 (New/Updated)** are introduced or revised in Module 3.  
> - Files under **Module 2** remain unchanged.

---

## Getting Started

### Environment Setup

Clone the repository and set up your Python virtual environment:

```bash
git clone <repository-url>
cd openai-agents/modules/module3-basic-agents

python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
.\venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Configuration

Copy the sample environment file and update it with your OpenAI API key:

```bash
cp .env.sample .env
# Update the .env file with your OPENAI_API_KEY
```

### Running the Server

Launch the FastAPI server with:

```bash
python -m uvicorn app.main:app --reload
```

---

## API Endpoints

### Module 2 Endpoints (Existing)
- **Hello World Agent:**  
  - `/agent`  
- **Story Agents:**  
  - `/agents/story`

### Module 3 Endpoints (New/Updated)
- **Lifecycle Agent Endpoints:**
  - `/agents/basic/lifecycle/initialize`
  - `/agents/basic/lifecycle/execute`
  - `/agents/basic/lifecycle/terminate`
- **Dynamic Prompt Agent Endpoints:**
  - `/agents/basic/dynamic-prompt/update`
  - `/agents/basic/dynamic-prompt/execute`
- **Streaming Agents:** (Grouped under `/agents/streaming`)
  - **Streaming Items:**
    - `/agents/streaming/items/initialize`
    - `/agents/streaming/items/execute`
    - `/agents/streaming/items/terminate`
  - **Streaming Text:**
    - `/agents/streaming/text/initialize`
    - `/agents/streaming/text/execute`
    - `/agents/streaming/text/terminate`

---

## Running Tests

Execute all tests using:

```bash
python -m pytest tests/
```

> **Individual Tests:**  
> - `python -m pytest tests/test_basic_agents.py`  
> - `python -m pytest tests/test_streaming_agents.py`

---

## Documentation

Refer to the `/docs` directory for detailed guides, including:
- **Implementation Plan:** `implementation_plan.md`
- **Step-by-Step Process:** `implementation_process.md`
- **Phase Documents:** `phase1.md`, etc.
- **Comprehensive Tutorial:** `tutorial.md`

---

## Development Workflow

1. **Start with Basic Agents:**  
   Develop and test lifecycle and dynamic prompt agents.
2. **Explore Streaming Capabilities:**  
   Implement and validate real-time streaming for both text and structured items.
3. **Test Frequently:**  
   Use the provided test suite to ensure all endpoints function correctly.
4. **Iterate and Expand:**  
   Use feedback to further refine your agents. Advanced topics are planned for future modules.

---

## Contributing

1. Fork and clone the repository.
2. Create a new feature branch.
3. Make clear, concise commits.
4. Push your branch and open a Pull Request.

---

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.

---

By completing Module 3, you'll gain essential skills in creating interactive AI agents capable of dynamic behavior and real-time interactions. For detailed instructions and further guidance, refer to the comprehensive documentation in the `/docs` directory.

Feel free to reach out if you have any questions or need further assistance!