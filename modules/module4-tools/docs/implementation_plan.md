
# Module 4: Tools

- **Expose Tool Endpoints:**  
  Create HTTP endpoints that allow you to call tools directly.
  
- **Organize Tool Implementations:**  
  Structure all tool functions and classes in a dedicated `/tools` folder.
  
- **Develop Multi-Tool Agents:**  
  Build agents that orchestrate multiple tool calls in sequence:
  - A basic multi-tool agent for fixed workflows.
  - An advanced Financial Summary Agent that performs domain-specific calculations and processes messages.

- **Comprehensive Testing:**  
  Write unit and integration tests covering each tool's functionality as well as the multi-tool agents.

> **Note:**  
> - **Module 1:** Contains the Hello World agent.  
> - **Module 2:** Contains the Story agents.  
> - **Module 3:** Introduces the Basic Agents (lifecycle, dynamic prompt) and Streaming Agents (text and items).  
> - **Module 4 (New):** Adds tool functionality – endpoints for various tool categories (Math, String, Datetime, Data, JSON, CSV, Analysis, API, Visualization) and multi-tool agents (basic multi-tool and Financial Summary Agent).

---

## 1. Overview

- **Objective:**  
  Enhance your existing agent framework by integrating a comprehensive set of tools. This module will provide endpoints to invoke these tools both directly (via HTTP) and internally (from within agents). It also demonstrates how to create multi-tool agents that combine multiple tools to achieve complex tasks.

- **Key Goals:**  
  - Update the main application to include new routers for tool endpoints.
  - Organize all tool implementations in a dedicated `/tools` folder.
  - Develop endpoints for each tool category as well as multi-tool agent endpoints.
  - Create multi-tool agents:
    - A **Basic Multi-Tool Agent** that demonstrates a fixed sequence of tool calls.
    - A **Financial Summary Agent** that computes financial metrics (simple interest and total amount) and processes messages.
  - Write comprehensive tests for both individual tool functionality and multi-tool agent orchestration.

---

## 2. Update the Main Application

- **Update Main File:**  
  In your module folder (`/modules/module4-tools`), update `app/main.py` to include:
  - Existing routers from Modules 1–3 (Hello World, Story, Basic, Streaming).
  - New routers for tools endpoints, organized into groups such as:
    - **Math Router:** for math tools endpoints.
    - **String Router:** for string tools endpoints.
    - **Datetime Router:** for datetime tools endpoints.
    - **Additional Tools Router:** for Data, JSON, CSV, Analysis, and API tools.
    - **Visualization Router:** for visualization tool endpoints.
    - **Advanced Agents Routers:** for multi-tool agent endpoints, including the Financial Summary Agent.
  
  This ensures that all endpoints are accessible and documented via Swagger.

---

## 3. New Tools Routers

- **Separate Routers for Modularity:**  
  To improve maintainability and readability, split the endpoints into several files:
  - **math_router.py:** Exposes endpoints such as `/tools/math/add` and `/tools/math/multiply`.
  - **string_router.py:** Exposes endpoints such as `/tools/string/to_uppercase` and `/tools/string/concatenate`.
  - **datetime_router.py:** Exposes endpoints such as `/tools/datetime/current_time` and `/tools/datetime/add_days`.
  - **echo_router.py:** Exposes the echo tool endpoint.
  - **additional_tools_router.py:** Exposes endpoints for Data, JSON, CSV, Analysis, and API tools.
  - **visualization_router.py:** Exposes endpoints for visualization tools.
  - **multi_tool_router.py:** Exposes a basic multi-tool agent endpoint.
  - **financial_summary_router.py:** Exposes an endpoint for the Financial Summary Agent.
  
- **Detailed Swagger Documentation:**  
  Each endpoint should include detailed descriptions that cover:
  - **Purpose:** What the endpoint does.
  - **Sample Input:** An example of the request payload.
  - **Sample Output:** An example of the response.

---

## 4. Organize the Tools Folder

- **Directory Structure:**  
  Place all tool implementations under `/app/tools/` with an empty `__init__.py`. For example:
  - `base_tool.py` – Defines the `BaseTool` class and `ToolResult` structure.
  - `math_tools.py` – Implements math tools (e.g., `add`, `multiply`).
  - `string_tools.py` – Implements string tools (e.g., `to_uppercase`, `concatenate`).
  - `datetime_tools.py` – Implements date/time tools (e.g., `current_time`, `add_days`).
  - `data_tools.py` – Implements data tools (e.g., `fetch_mock_data`, `summarize_list`).
  - `json_tools.py` – Implements JSON tools (e.g., `validate_json`, `transform_json`).
  - `csv_tools.py` – Implements CSV tools (e.g., `parse_csv`, `generate_csv`).
  - `database_tools.py` – Implements database tools (for future development).
  - `analysis_tools.py` – Implements analysis tools (e.g., `analyze_sentiment`, `extract_entities`).
  - `api_tools.py` – Implements API tools (e.g., `make_request`, `cache_get`).
  - `visualization_tools.py` – Implements visualization tools (e.g., `create_bar_chart`, `create_line_chart`).

---

## 5. Multi-Tool Agent

- **Develop Multi-Tool Agents:**  
  - **Basic Multi-Tool Agent:**  
    Demonstrates a fixed sequence of tool calls (e.g., calling math, string, and echo tools).  
  - **Financial Summary Agent:**  
    An advanced agent that calculates simple interest and total amount based on financial inputs, and processes a message.  
    - **Input Format:** `"principal,rate,time;message"`  
    - **Example:** `"1000,0.05,2;thank you"`  
    - **Output:**  
      ```json
      {
        "interest": 100.0,
        "total": 1100.0,
        "message": "Echo: THANK YOU"
      }
      ```

- **Configuration and Hooks:**  
  Each advanced multi-tool agent should be configurable, dynamically build its instructions (listing available tools), and maintain context and state (using components like ContextManager and StateMachine).

---

## 6. Endpoints and Intra-Module Calls

- **Direct Tool Endpoints:**  
  Each tool is accessible via its dedicated HTTP endpoint, which validates input using Pydantic models and returns JSON responses.
  
- **Multi-Tool Agent Endpoints:**  
  Separate endpoints are provided for the multi-tool agents. For example:
  - **Basic Multi-Tool Agent:** `/tools/multi-tool`
  - **Financial Summary Agent:** `/agents/financial-summary/financial_summary`
  
- **Intra-Module Usage:**  
  Tools can be called internally by agents to orchestrate more complex workflows.

---

## 7. Testing

- **Tool Unit Tests:**  
  Create a test file (e.g., `tests/test_tools.py`) with unit tests for each tool. Validate both expected outputs and error handling.
  
- **Multi-Tool Agent Tests:**  
  Write tests for the basic multi-tool agent and Financial Summary Agent to ensure they aggregate tool outputs correctly.
  
- **Endpoint Tests:**  
  Develop integration tests for all tool endpoints (e.g., in `tests/test_tools_router.py`) to verify HTTP status codes and response formats.

---

## 8. Folder Layout for Module 4

Below is an updated folder structure including all Module 4 components:

```plaintext
modules/
└── module4-tools/                           # Root for Module 4 (Tools)
    ├── app/
    │   ├── agents/
    │   │   ├── basic/                       # Module 3 - Basic Agents (unchanged)
    │   │   │   ├── lifecycle_agent.py       
    │   │   │   ├── dynamic_prompt_agent.py  
    │   │   │   ├── stream_text_agent.py     
    │   │   │   └── stream_items_agent.py    
    │   │   ├── story/                       # Module 2 - Story Agents (unchanged)
    │   │   │   ├── advanced_story_agent.py  
    │   │   │   ├── baseline_story_agent.py  
    │   │   │   └── custom_story_agent.py    
    │   │   ├── hello_world/                 # Module 1 - Hello World Agent (unchanged)
    │   │   │   └── hello_world_agent.py     
    │   │   └── advanced/                    # Module 4 - Tools: Advanced Agents (New)
    │   │       ├── multi_tool_agent.py      # Basic multi-tool agent implementation
    │   │       └── financial_summary_agent.py   # Financial Summary Agent implementation
    │   ├── routers/
    │   │   ├── basic_router.py              # Module 3 (unchanged)
    │   │   ├── streaming_router.py          # Module 3 (unchanged)
    │   │   ├── story_router.py              # Module 2 (unchanged)
    │   │   ├── hello_world.py               # Module 1 (unchanged)
    │   │   ├── math_router.py               # Module 4 (New): Math tools endpoints
    │   │   ├── string_router.py             # Module 4 (New): String tools endpoints
    │   │   ├── datetime_router.py           # Module 4 (New): Datetime tools endpoints
    │   │   ├── echo_router.py               # Module 4 (New): Echo tool endpoint
    │   │   ├── multi_tool_router.py         # Module 4 (New): Basic multi-tool agent endpoint
    │   │   ├── additional_tools_router.py   # Module 4 (New): Data, JSON, CSV, Analysis, API tools endpoints
    │   │   ├── visualization_router.py      # Module 4 (New): Visualization tools endpoints
    │   │   └── financial_summary_router.py  # Module 4 (New): Financial Summary Agent endpoint
    │   ├── tools/                           # Module 4 (New): Tool implementations
    │   │   ├── __init__.py                  # Empty __init__.py for tools package
    │   │   ├── base_tool.py                 # Base tool class definition
    │   │   ├── echo_tools.py                # Echo tool implementation
    │   │   ├── math_tools.py                # Math tool implementations (e.g., add, multiply)
    │   │   ├── string_tools.py              # String tool implementations (e.g., to_uppercase, concatenate)
    │   │   ├── datetime_tools.py            # Datetime tool implementations (e.g., current_time, add_days)
    │   │   ├── data_tools.py                # Data tool implementations (e.g., fetch_mock_data, summarize_list)
    │   │   ├── json_tools.py                # JSON tool implementations (e.g., validate_json, transform_json)
    │   │   ├── csv_tools.py                 # CSV tool implementations (e.g., parse_csv, generate_csv)
    │   │   ├── database_tools.py            # Database tool implementations (to be implemented)
    │   │   ├── analysis_tools.py            # Analysis tool implementations (e.g., analyze_sentiment, extract_entities)
    │   │   ├── api_tools.py                 # API tool implementations (e.g., make_request, cache_get)
    │   │   └── visualization_tools.py       # Visualization tool implementations (e.g., create_bar_chart, create_line_chart)
    │   ├── config.py                        # Configuration settings
    │   └── dependencies.py                  # Shared dependencies (e.g., API key verification)
    ├── docs/                                # Documentation, tutorials, and implementation notes
    │   ├── implementation_plan.md         # Detailed implementation plan for Module 4
    │   └── (other docs as needed)
    └── tests/                               # Test suites for all modules
        ├── test_basic_agents.py            # Tests for basic agents
        ├── test_streaming_agents.py        # Tests for streaming agents
        └── test_tools.py                   # Tests for tool implementations and multi-tool agents
```

---

## API Endpoints


### Module 4 Endpoints (New)
- **Tools Endpoints:**  
  - **Math Tools:** `/tools/math/add`, `/tools/math/multiply`
  - **String Tools:** `/tools/string/to_uppercase`, `/tools/string/concatenate`
  - **Datetime Tools:** `/tools/datetime/current_time`, `/tools/datetime/add_days`
  - **Data Tools:** `/tools/additional/get_item`, `/tools/additional/summarize_list`, `/tools/additional/fetch_mock_data`
  - **JSON Tools:** `/tools/additional/validate_json`, `/tools/additional/transform_json`
  - **CSV Tools:** `/tools/additional/parse_csv`, `/tools/additional/generate_csv`
  - **Analysis Tools:** `/tools/additional/analyze_sentiment`, `/tools/additional/extract_entities`, `/tools/additional/extract_keywords`, `/tools/additional/calculate_basic_stats`, `/tools/additional/perform_correlation`, `/tools/additional/find_patterns`, `/tools/additional/apply_regex`
  - **API Tools:** `/tools/additional/make_request`, `/tools/additional/cache_set`, `/tools/additional/cache_get`, `/tools/additional/check_rate_limit`
  - **Visualization Tools:** `/tools/visualization/bar_chart`, `/tools/visualization/line_chart`, `/tools/visualization/pie_chart`, `/tools/visualization/scatter_plot`
- **Multi-Tool Agents:**  
  - Basic Multi-Tool Agent: `/tools/multi-tool`
  - Financial Summary Agent: `/agents/financial-summary/financial_summary`


## Running Tests

Run all tests with:

```bash
python -m pytest tests/
```

> **Individual Test Files:**  
> - `python -m pytest tests/test_tools_router.py`  
> - `python -m pytest tests/test_visualization_tools.py`  
> - `python -m pytest tests/test_initial_tools.py`
> - `python -m pytest tests/test_phase2_tools.py`
> - `python -m pytest tests/test_multi_tool_agent.py`
