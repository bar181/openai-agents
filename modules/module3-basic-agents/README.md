# Module 3: Basic and Advanced OpenAI Agents

This module introduces a comprehensive exploration of agent development, from basic lifecycle management to advanced tool integration. Through a structured learning path, you'll master both fundamental and sophisticated agent concepts.


## Features

### Basic Agents
- **Lifecycle Management:** Initialize, execute, and terminate agents
- **Dynamic System Prompts:** Update agent behavior at runtime
- **Streaming Text Agent:** Generate and stream text responses in real-time
- **Streaming Items Agent:** Stream sequences of structured items incrementally

### Advanced Agents
- **Generic Lifecycle Agent:** Enhanced agent with comprehensive tool integration
- **Multi-Tool Agent:** Advanced agent with multiple tool capabilities and context management
- **Integrated Tools Suite:**
  - **Basic Tools:**
    - Mathematical operations (add, multiply)
    - String manipulation (concatenate, to_uppercase)
    - Data operations (get_item, summarize_list, fetch_mock_data)
    - Time utilities (current_time, add_days)
    - Echo functionality
  - **Advanced Tools:**
    - JSON processing (validate_json, transform_json)
    - CSV handling (parse_csv, generate_csv)
    - Database operations (store_data, retrieve_data, list_keys, delete_data, clear_database)
    - Text analysis (analyze_sentiment, extract_entities, extract_keywords)
    - Statistics (calculate_basic_stats, perform_correlation)
    - Pattern matching (find_patterns, apply_regex)
    - API integration (make_request, cache_get, cache_set, check_rate_limit)
    - Visualization (create_bar_chart, create_line_chart, create_pie_chart, create_scatter_plot)

## Project Structure

```plaintext
module3-basic-agents/
├── app/
│   ├── agents/
│   │   ├── basic/
│   │   │   ├── lifecycle_agent.py        # Basic lifecycle management
│   │   │   ├── dynamic_prompt_agent.py   # Dynamic system prompt usage
│   │   │   ├── stream_text_agent.py      # Streaming text responses
│   │   │   └── stream_items_agent.py     # Streaming structured items
│   │   └── advanced/
│   │       ├── generic_lifecycle_agent.py # Enhanced generic lifecycle agent
│   │       └── multi_tool_agent.py        # Advanced agent with multiple tool capabilities
│   ├── routers/
│   │   ├── basic_router.py               # Basic agents endpoints
│   │   └── advanced_router.py            # Advanced agents endpoints
│   └── tools/                            # Comprehensive tool implementations
│       ├── base_tool.py                  # Base tool class and result handling
│       ├── math_tools.py                 # Mathematical operations (add, multiply)
│       ├── string_tools.py               # String manipulation (concatenate, to_uppercase)
│       ├── data_tools.py                 # Data handling (get_item, summarize_list, fetch_mock_data)
│       ├── datetime_tools.py             # Time utilities (current_time, add_days)
│       ├── echo_tools.py                 # Echo functionality
│       ├── json_tools.py                 # JSON processing (validate_json, transform_json)
│       ├── csv_tools.py                  # CSV handling (parse_csv, generate_csv)
│       ├── database_tools.py             # Database operations (store_data, retrieve_data, etc.)
│       ├── analysis_tools.py             # Text and data analysis (sentiment, entities, keywords)
│       ├── api_tools.py                  # API integration (requests, caching, rate limiting)
│       └── visualization_tools.py        # Data visualization (charts, plots)
├── docs/                                 # Implementation guides
└── tests/                                # Comprehensive test suite
```

## Getting Started

1. **Environment Setup:**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd openai-agents/modules/module3-basic-agents

   # Create and activate virtual environment (optional)
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   # or
   .\venv\Scripts\activate  # Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configuration:**
   ```bash
   # Copy environment template
   cp .env.sample .env

   # Edit .env with your settings
   # Required: OPENAI_API_KEY
   ```

3. **Run the FastAPI Server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

4. **Run Tests:**
   ```bash
   # Run all tests
   python -m pytest tests/

   # Run specific test suites
   python -m pytest tests/test_basic_agents.py
   python -m pytest tests/test_advanced_agents.py
   python -m pytest tests/test_stream_text.py
   python -m pytest tests/test_stream_items.py
   ```

## API Endpoints

### Basic Agent Endpoints
- `POST /agents/basic/lifecycle/initialize` - Initialize lifecycle agent
- `POST /agents/basic/lifecycle/execute` - Execute lifecycle agent
- `POST /agents/basic/lifecycle/terminate` - Terminate lifecycle agent
- `POST /agents/basic/dynamic-prompt/update` - Update dynamic prompt
- `POST /agents/basic/dynamic-prompt/execute` - Execute with current prompt
- `POST /agents/basic/stream-text` - Stream text responses incrementally
- `POST /agents/basic/stream-items` - Stream sequences of structured items

### Advanced Agent Endpoints
- `POST /agents/advanced/generic-lifecycle` - Execute generic lifecycle agent with tools
- `POST /agents/advanced/multi-tool` - Execute multi-tool agent with advanced capabilities

## Documentation

Detailed documentation is available in the `/docs` directory:
- `implementation_plan.md` - Project structure and implementation strategy
- `implementation_process.md` - Step-by-step implementation guide
- `phase1.md`, `phase2.md`, `phase3.md`, `phase4.md` - Detailed phase documentation
- `tutorial.md` - Comprehensive learning guide

## Development Workflow

1. Start with basic agents to understand core concepts
2. Explore streaming agents for real-time content delivery
3. Progress to advanced agents with tool integration
4. Run tests frequently to verify functionality
5. Consult documentation for detailed guidance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

This module provides a structured learning path from basic to advanced agent development, including real-time streaming capabilities and comprehensive tool integration. Through hands-on implementation of various agent types and features, you'll gain practical experience in building sophisticated AI agent systems with both synchronous and streaming interactions, leveraging a wide range of tools for enhanced functionality.

For detailed guidance, refer to the tutorial in `/docs/tutorial.md`.