Below is an implementation plan for **Module 4: Tools**. This module will be located in a new folder `/modules/module4-tools` and will include all files from Module 3 (and earlier) plus the new tool functionality. The plan outlines the steps to integrate tools into the existing system, expose them via endpoints, and create a multi-tool agent to demonstrate their combined use.

---

## 1. Overview

- **Objective:**  
  Enhance your existing agents (from Module 3) by integrating a tools layer. This module will provide endpoints to call tools directly and also include a multi-tool agent that can orchestrate multiple tools.

- **Key Goals:**  
  - Update the main application to include the new tools router.
  - Create a new router for tools endpoints.
  - Organize all tool implementations under the `/tools` folder.
  - Develop endpoints for each tool and for a multi-tool agent.
  - Provide a mechanism to call these tools both via HTTP and internally within agents.
  - Write comprehensive tests for each tool and for the multi-tool agent.

---

## 2. Update the Main Application

- **Update Main File:**  
  - In the new module folder (`/modules/module4-tools`), update `app/main.py` to include:
    - Existing routers from Module 3 (basic, streaming, story, hello_world).
    - **New Tools Router:** Mount the new tools endpoints under a prefix such as `/tools`.

---

## 3. New Tools Router

- **Create a New Router:**  
  - File: `app/routers/tools_router.py`
  - Responsibilities:
    - Expose endpoints for direct tool usage (e.g., `/tools/add`, `/tools/to_uppercase`).
    - Expose an endpoint for the multi-tool agent (e.g., `/tools/multi-tool`) that demonstrates calling multiple tools in sequence.
  - **Input/Output:**  
    - Use request models (with Pydantic) for each tool endpoint to validate incoming parameters.
    - Return JSON responses indicating success and tool outputs.

---

## 4. Organize the Tools Folder

- **Directory Structure:**  
  - Create or update the `/app/tools/` folder with an empty `__init__.py`.
  - Add individual files for each group of tools:
    - `base_tool.py` (defines the `BaseTool` class and `ToolResult` structure).
    - `math_tools.py` (e.g., `add`, `multiply`).
    - `string_tools.py` (e.g., `to_uppercase`, `concatenate`).
    - `datetime_tools.py` (e.g., `current_time`, `add_days`).
    - `data_tools.py` (e.g., `fetch_mock_data`, `summarize_list`).
    - Other tool files as needed (e.g., `json_tools.py`, `csv_tools.py`, `database_tools.py`, `analysis_tools.py`, `api_tools.py`, `visualization_tools.py`).

---

## 5. Multi-Tool Agent

- **Develop a Multi-Tool Agent:**  
  - Create a new file in an appropriate folder (e.g., `/app/agents/advanced/multi_tool_agent.py`).
  - This agent should:
    - Accept a configuration specifying which tools are available.
    - Build its instructions dynamically by listing available tools.
    - Execute a task by calling multiple tools in sequence, aggregating the results.
  - **Simplified Approach:**  
    - Instead of one massive agent, prefer multiple smaller multi-tool agents focusing on different tasks if needed.

---

## 6. Endpoints and Intra-Module Calls

- **Direct Tool Endpoints:**  
  - Each tool should have its own endpoint (e.g., `/tools/add` accepts two numbers and returns their sum).
  - Design endpoints so they can be called via HTTP and also easily invoked internally by the multi-tool agent.

- **Multi-Tool Agent Endpoint:**  
  - Create an endpoint (e.g., `/tools/multi-tool`) that runs the multi-tool agent.
  - This endpoint should accept input parameters and return aggregated results from all tool calls.

---

## 7. Testing

- **Tool Unit Tests:**  
  - Create a new test file: `tests/test_tools.py`.
  - Write tests for each individual tool, verifying both expected outputs and error cases.

- **Multi-Tool Agent Tests:**  
  - Include tests that simulate multi-step tasks using the multi-tool agent.
  - Verify that the agent correctly calls the tools in sequence and aggregates results as expected.

- **Endpoint Tests:**  
  - Update or create tests to cover the new tools endpoints in `tests/test_tools.py`.
  - Ensure that HTTP requests to `/tools/*` return the correct status codes and outputs.

---

## 8. Folder Layout for Module 4

Below is an updated folder structure including Module 4 components:

```plaintext
modules/
└── module4-tools/                           # Root for Module 4 (Tools)
    ├── app/
    │   ├── agents/
    │   │   ├── basic/                       # Module 3 - Basic Agents (unchanged from previous modules)
    │   │   │   ├── lifecycle_agent.py       # Module 3
    │   │   │   ├── dynamic_prompt_agent.py  # Module 3
    │   │   │   ├── stream_text_agent.py     # Module 3
    │   │   │   └── stream_items_agent.py    # Module 3
    │   │   ├── story/                       # Module 2 - Story Agents (unchanged)
    │   │   │   ├── advanced_story_agent.py  # Module 2
    │   │   │   ├── baseline_story_agent.py  # Module 2
    │   │   │   └── custom_story_agent.py    # Module 2
    │   │   ├── hello_world/                 # Module 1 - Hello World Agent (unchanged)
    │   │   │   └── hello_world_agent.py     # Module 1
    │   │   └── advanced/                    # Module 4 - Tools: Multi-Tool Agents (New)
    │   │       └── multi_tool_agent.py      # Module 4 (New): Multi-tool agent implementation
    │   ├── routers/
    │   │   ├── basic_router.py              # Module 3 (unchanged)
    │   │   ├── streaming_router.py          # Module 3 (unchanged)
    │   │   ├── story_router.py              # Module 2 (unchanged)
    │   │   ├── hello_world.py               # Module 1 (unchanged)
    │   │   └── tools_router.py              # Module 4 (New): Endpoints for tools and multi-tool agent
    │   ├── tools/                           # Module 4 (New): Tool implementations
    │   │   ├── __init__.py                  # Module 4: Empty __init__ file for tools package
    │   │   ├── base_tool.py                 # Module 4 (New): Base tool definition
    │   │   ├── echo_tools.py                # Module 4 (New)
    │   │   ├── math_tools.py                # Module 4 (New)
    │   │   ├── string_tools.py              # Module 4 (New)
    │   │   ├── datetime_tools.py            # Module 4 (New)
    │   │   ├── data_tools.py                # Module 4 (New)
    │   │   ├── json_tools.py                # Module 4 (New)
    │   │   ├── csv_tools.py                 # Module 4 (New)
    │   │   ├── database_tools.py            # Module 4 (New)
    │   │   ├── analysis_tools.py            # Module 4 (New)
    │   │   ├── api_tools.py                 # Module 4 (New)
    │   │   └── visualization_tools.py       # Module 4 (New)
    │   ├── config.py                        # Module 3 (unchanged)
    │   └── dependencies.py                  # Module 3 (unchanged)
    ├── docs/                                # Documentation, tutorials, and implementation notes
    │   ├── implementation_plan.md         # Module 4 (New): This implementation plan and further documentation
    │   └── (other docs as needed)
    └── tests/                               # Tests for all modules (including new tool tests)
        ├── test_basic_agents.py            # Module 3 (unchanged)
        ├── test_streaming_agents.py        # Module 3 (unchanged)
        └── test_tools.py                   # Module 4 (New): Tests for all tool implementations and multi-tool agent
```

---

## 9. Next Steps

1. **Develop Each Component:**  
   - Implement individual tool functions in the `/tools` folder.
   - Create the multi-tool agent in `/agents/advanced/multi_tool_agent.py` to orchestrate tool calls.
   - Build the new `tools_router.py` with endpoints for each tool and for the multi-tool agent.

2. **Integrate with Existing Code:**  
   - Update `app/main.py` to include the new tools router.
   - Ensure that all previous Module 3 functionality remains intact.

3. **Write and Run Tests:**  
   - Develop tests in `tests/test_tools.py` covering each tool’s functionality.
   - Test the multi-tool agent and all new endpoints.

4. **Document and Iterate:**  
   - Update documentation in `/docs/implementation_plan.md` and other guides.
   - Refine and extend tool functionality based on testing and feedback.

---

This plan sets a clear path for integrating tools into your existing agent framework while maintaining modularity and a tutorial-style progression. Feel free to ask if you need further details or adjustments!