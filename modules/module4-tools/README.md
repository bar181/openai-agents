
# Module 4: Tools

Welcome to **Module 4: Tools**! This module builds on the functionality from Module 3 by introducing a robust tool layer. In this module, you will learn to:

- Create endpoints to call tools both via HTTP and from within your application.
- Organize tool implementations in a dedicated `/tools` folder.
- Develop multi-tool agents that orchestrate multiple tools to accomplish complex, domain-specific tasks.
- Write comprehensive tests for all tool implementations and multi-tool agents.

> **Note:**  
> - **Module 1:** Contains the Hello World agent.  
> - **Module 2:** Contains the Story agents.  
> - **Module 3:** Introduces the Basic Agents (lifecycle, dynamic prompt) and Streaming Agents (text and items).  
> - **Module 4 (New):** Adds tool functionality – endpoints, tool implementations, and multi-tool agents such as:
>   - A basic multi-tool agent that calls multiple tools.
>   - A Financial Summary Agent that calculates financial metrics and processes messages.

---

## Features

### Tools Endpoints

- **Direct Tool Endpoints:**  
  Each tool is exposed via its own HTTP endpoint, allowing direct invocation. For example:
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
  - **Basic Multi-Tool Agent:** Exposed via `/tools/multi-tool`
  - **Financial Summary Agent:** Exposed via `/agents/financial-summary/financial_summary`

- **Intra-Module Tool Calls:**  
  Tools can also be invoked programmatically within your agents for more complex orchestration.

### Advanced Multi-Tool Agents

- **Financial Summary Agent:**  
  This advanced agent calculates simple interest and the total amount based on financial inputs, then processes a message.  
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

---

## Project Structure

Below is the comprehensive folder layout with annotations for each module. Files marked **(New)** are introduced in Module 4.

```plaintext
module4-tools/                          # Root for Module 4 (Tools)
├── app/
│   ├── agents/
│   │   ├── basic/                           # Module 3 - Basic Agents (Updated)
│   │   │   ├── lifecycle_agent.py           
│   │   │   ├── dynamic_prompt_agent.py      
│   │   │   ├── stream_text_agent.py         
│   │   │   └── stream_items_agent.py        
│   │   ├── story/                           # Module 2 - Story Agents (Existing)
│   │   │   ├── advanced_story_agent.py      
│   │   │   ├── baseline_story_agent.py      
│   │   │   └── custom_story_agent.py        
│   │   ├── hello_world/                     # Module 1 - Hello World Agent (Existing)
│   │   │   └── hello_world_agent.py         
│   │   └── advanced/                        # Module 4 - Tools: Advanced Agents (New)
│   │       ├── multi_tool_agent.py          # Module 4 (New): Basic multi-tool agent
│   │       └── financial_summary_agent.py   # Module 4 (New): Financial Summary Agent
│   ├── routers/
│   │   ├── basic_router.py                  # Module 3 (Updated): Basic agents
│   │   ├── streaming_router.py              # Module 3 (Updated): Streaming agents
│   │   ├── story_router.py                  # Module 2 (Existing): Story agents
│   │   ├── hello_world.py                   # Module 1 (Existing): Hello world agent
│   │   ├── math_router.py                   # Module 4 (New): Math tools endpoints
│   │   ├── string_router.py                 # Module 4 (New): String tools endpoints
│   │   ├── datetime_router.py               # Module 4 (New): Datetime tools endpoints
│   │   ├── echo_router.py                   # Module 4 (New): Echo tool endpoint
│   │   ├── multi_tool_router.py             # Module 4 (New): Basic multi-tool agent endpoint
│   │   ├── additional_tools_router.py       # Module 4 (New): Data, JSON, CSV, Analysis, API tools endpoints
│   │   ├── visualization_router.py          # Module 4 (New): Visualization tools endpoints
│   │   └── financial_summary_router.py      # Module 4 (New): Financial Summary Agent endpoint
│   ├── tools/                               # Module 4 (New): Tool implementations
│   │   ├── __init__.py                      # Empty __init__.py for tools package
│   │   ├── base_tool.py                     # Base tool class definition
│   │   ├── echo_tools.py                    # Echo tool implementation
│   │   ├── math_tools.py                    # Math tool implementations (e.g., add, multiply)
│   │   ├── string_tools.py                  # String tool implementations (e.g., to_uppercase, concatenate)
│   │   ├── datetime_tools.py                # Datetime tool implementations (e.g., current_time, add_days)
│   │   ├── data_tools.py                    # Data tool implementations (e.g., fetch_mock_data, summarize_list)
│   │   ├── json_tools.py                    # JSON tool implementations (e.g., validate_json, transform_json)
│   │   ├── csv_tools.py                     # CSV tool implementations (e.g., parse_csv, generate_csv)
│   │   ├── database_tools.py                # Database tool implementations (e.g., store_data, retrieve_data)
│   │   ├── analysis_tools.py                # Analysis tool implementations (e.g., analyze_sentiment, extract_entities)
│   │   ├── api_tools.py                     # API tool implementations (e.g., make_request, cache_get)
│   │   └── visualization_tools.py           # Visualization tool implementations (e.g., create_bar_chart, create_line_chart)
│   ├── config.py                            # Configuration settings
│   └── dependencies.py                      # Shared dependencies (e.g., API key verification)
├── docs/                                    # Documentation, tutorials, and implementation notes
│   ├── implementation_plan.md             # Detailed implementation plan for Module 4
│   └── (other docs as needed)
└── tests/                                   # Test suites for all modules
    ├── test_basic_agents.py                # Tests for basic agents
    ├── test_streaming_agents.py            # Tests for streaming agents
    ├── test_tools.py                       # Tests for tool implementations and multi-tool agents
    └── (other test files as needed)
```

---

## Getting Started

### Environment Setup

Clone the repository and set up your Python virtual environment:

```bash
git clone <repository-url>
cd openai-agents/modules/module4-tools
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Configuration

Copy the sample environment file and update it with your API keys:

```bash
cp .env.sample .env
# Update .env with your OPENAI_API_KEY and any other necessary keys
```

### Running the Server

Launch the FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

---

## API Endpoints

### Module 1 Endpoints (Existing)
- **Hello World Agent:** `/agent`

### Module 2 Endpoints (Existing)
- **Story Agents:** `/agents/story`

### Module 3 Endpoints (Updated)
- **Basic Agents:**  
  - Lifecycle: `/agents/basic/lifecycle/initialize`, `/agents/basic/lifecycle/execute`, `/agents/basic/lifecycle/terminate`
  - Dynamic Prompt: `/agents/basic/dynamic-prompt/update`, `/agents/basic/dynamic-prompt/execute`
- **Streaming Agents:**  
  - Text: `/agents/streaming/text/*`
  - Items: `/agents/streaming/items/*`

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


---

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


---

## Documentation

Refer to the `/docs` directory for detailed guides and documentation:
- **Implementation Plan:** `implementation_plan.md`
- **Tutorial:** `tutorial.md`
- **Testing Analysis:** `test_work.md`
- **Coding Guidelines:** `guidelines.md`

---

## Development Workflow

1. **Enhance Module 3:**  
   Build upon the existing basic and streaming agents.
2. **Implement Tools:**  
   Develop tool functionality in the `/tools` folder.
3. **Create Tools Endpoints:**  
   Expose endpoints via dedicated routers for each tool group.
4. **Test Thoroughly:**  
   Run unit and integration tests to validate all endpoints.
5. **Iterate:**  
   Refine agents and tools based on feedback and testing.
6. **Future Modules:**  
   - Module 5: LLM Provider Agents (using the OpenAI SDK)
   - Module 6: OpenAI SDK-based endpoints
   - Module 7: Custom orchestration agents integrating both OpenAI and custom agents

---

## Contributing

1. Fork and clone the repository.
2. Create a feature branch.
3. Commit changes with clear messages.
4. Push your branch and open a Pull Request for review.

---


---

By completing Module 4, you'll gain essential skills in integrating and orchestrating a variety of tools with your AI agents. This lays the foundation for more advanced integrations and orchestration in future modules. Enjoy building your multi-tool and LLM-powered agents!
```
