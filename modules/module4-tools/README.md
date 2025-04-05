
# Module 4: Tools

Welcome to **Module 4: Tools**! This module builds on the functionality from Module 3 by introducing tools. In this module, you will learn to:

- Create endpoints to call tools both from HTTP and within your application.
- Organize tool implementations in a dedicated `/tools` folder.
- Develop at least one multi-tool agent that can orchestrate multiple tools.
- Write tests for all tool implementations and the multi-tool agent.

> **Note:**  
> - **Module 1:** Contains the Hello World agent.  
> - **Module 2:** Contains the Story agents.  
> - **Module 3:** Introduces the Basic Agents (lifecycle, dynamic prompt) and Streaming Agents (text and items).  
> - **Module 4 (New):** Adds tool functionality – endpoints, tools implementations, and a multi-tool agent.

---

## Features

### Module 4 (Tools)

- **Tools Endpoints:**  
  Create separate endpoints for each tool so they can be called directly via HTTP.
  
- **Intra-Module Tool Calls:**  
  Tools can also be called from within the module by agents.
  
- **Tools Implementations:**  
  All tool implementations reside in the `/tools` folder.
  
- **Multi-Tool Agent:**  
  At least one agent demonstrates how to call multiple tools sequentially to accomplish complex tasks.
  
- **Comprehensive Tests:**  
  Unit tests cover each tool’s functionality as well as the multi-tool agent’s orchestration.

---

## Project Structure

Below is a comprehensive folder layout with annotations for each module. Files marked with **Module 4 (New)** or similar indicate additions/updates for this module.

```plaintext
module4-tools/                          # Root for Module 4 (Tools)
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
│   │   ├── hello_world/                     # Module 1 - Hello World Agent (Existing)
│   │   │   └── hello_world_agent.py         # Module 1: Simple hello world agent
│   │   └── advanced/                        # Module 4 - Tools: Multi-tool agents (New)
│   │       └── multi_tool_agent.py          # Module 4 (New): Multi-tool agent that calls multiple tools
│   ├── routers/
│   │   ├── basic_router.py                  # Module 3 (New): Endpoints for lifecycle and dynamic prompt agents
│   │   ├── streaming_router.py              # Module 3 (New): Combined endpoints for streaming agents
│   │   ├── story_router.py                  # Module 2: Endpoints for story agents
│   │   ├── hello_world.py                   # Module 1: Endpoints for hello world agent
│   │   └── tools_router.py                  # Module 4 (New): Endpoints for tool invocations
│   ├── tools/                               # Module 4 (New): Tool implementations
│   │   ├── __init__.py                      # Module 4: Empty __init__ file for the tools package
│   │   ├── base_tool.py                     # Module 4 (New): Base tool class definition
│   │   ├── echo_tools.py                    # Module 4 (New): Echo tool implementation
│   │   ├── math_tools.py                    # Module 4 (New): Math tool implementations (e.g., add, multiply)
│   │   ├── string_tools.py                  # Module 4 (New): String tool implementations (e.g., to_uppercase, concatenate)
│   │   ├── datetime_tools.py                # Module 4 (New): Date/time tool implementations (e.g., current_time, add_days)
│   │   ├── data_tools.py                    # Module 4 (New): Data tool implementations (e.g., fetch_mock_data, summarize_list)
│   │   ├── json_tools.py                    # Module 4 (New): JSON tool implementations (e.g., validate_json, transform_json)
│   │   ├── csv_tools.py                     # Module 4 (New): CSV tool implementations (e.g., parse_csv, generate_csv)
│   │   ├── database_tools.py                # Module 4 (New): Database tool implementations (e.g., store_data, retrieve_data)
│   │   ├── analysis_tools.py                # Module 4 (New): Analysis tool implementations (e.g., analyze_sentiment, extract_entities)
│   │   ├── api_tools.py                     # Module 4 (New): API tool implementations (e.g., make_request, cache_get)
│   │   └── visualization_tools.py           # Module 4 (New): Visualization tool implementations (e.g., create_bar_chart, create_line_chart)
│   ├── config.py                            # Module 3 (New): Configuration settings
│   └── dependencies.py                      # Module 3 (New): Shared dependencies (e.g., API key verification)
├── docs/                                    # Documentation, tutorials, and implementation notes
│   ├── implementation_plan.md               # Module 4 (New): Implementation plan for Tools
│   └── (other docs as needed)
└── tests/                                   # Tests for all modules
    ├── test_basic_agents.py                # Module 3: Tests for lifecycle & dynamic prompt agents
    ├── test_streaming_agents.py            # Module 3: Tests for streaming text & items agents
    ├── test_tools.py                       # Module 4 (New): Tests for tool implementations and multi-tool agent
    └── (other test files as needed from modules 1 and 2)
```

> **Legend:**  
> - Files marked **(New)** are introduced in Module 4 (Tools).  
> - Module 1 (Hello World), Module 2 (Story) remain unchanged.  
> - Module 3 (Basic & Streaming Agents) continue from previous modules.

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
# Update .env with your OPENAI_API_KEY
```

### Running the Server

Launch the FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

---

## API Endpoints

### Module 1 Endpoints (Existing)
- **Hello World Agent:**  
  - `/agent`

### Module 2 Endpoints (Existing)
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

### Module 4 Endpoints (New)
- **Tools Endpoints:** (Exposed via the Tools Router)
  - **Direct Tool Endpoints:**  
    - Example: `/tools/add`, `/tools/multiply`, `/tools/to_uppercase`, etc.
  - **Multi-Tool Agent Endpoint:**  
    - Example: `/tools/multi-tool` to run an agent that calls multiple tools.

> **Note:** Endpoints for tools allow you to invoke tool functionality directly via HTTP and also serve as examples for intra-module tool calls.

---

## Running Tests

Run all tests with:

```bash
python -m pytest tests/
```

> **Individual Test Files:**  
> - `python -m pytest tests/test_basic_agents.py`  
> - `python -m pytest tests/test_streaming_agents.py`  
> - `python -m pytest tests/test_tools.py`

---

## Documentation

Refer to the `/docs` directory for detailed guides and documentation:

- **Implementation Plan:** `implementation_plan.md` (Module 4)
- **Step-by-Step Process:** Additional documents outlining tool integration.
- **Tutorial:** Comprehensive instructions in `tutorial.md`

---

## Development Workflow

1. **Enhance Module 3:**  
   Build upon the existing basic and streaming agents.
2. **Implement Tools:**  
   Develop and integrate tool functionality in the `/tools` folder.
3. **Create Tools Endpoints:**  
   Expose each tool (and multi-tool agents) via a dedicated router.
4. **Test Thoroughly:**  
   Ensure that all tool endpoints and agent integrations work as expected.
5. **Iterate:**  
   Use feedback to refine the multi-tool agent and expand tool offerings.

---

## Contributing

1. Fork and clone the repository.
2. Create a feature branch.
3. Commit changes with clear messages.
4. Push your branch and open a Pull Request.

---

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.

---

By completing Module 4, you'll gain essential skills in integrating tools with AI agents and building endpoints to expose this functionality. For detailed instructions, refer to the documentation in `/docs`. Enjoy building your multi-tool agents!

Feel free to reach out if you have any questions or need further assistance!