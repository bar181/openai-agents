# Module 3: Basic and Advanced OpenAI Agents

This module introduces a comprehensive exploration of agent development, from basic lifecycle management to advanced tool integration. Through a structured learning path, you'll master both fundamental and sophisticated agent concepts.

## Features

### Basic Agents
- **Lifecycle Management:** Initialize, execute, and terminate agents
- **Dynamic System Prompts:** Update agent behavior at runtime

### Advanced Agents
- **Generic Lifecycle Agent:** Enhanced agent with comprehensive tool integration
- **Integrated Tools Suite:**
  - Mathematical operations (add, multiply)
  - String manipulation (to_uppercase)
  - Data operations (fetch_mock_data)
  - Time utilities (current_time)
  - Echo functionality

## Project Structure

```plaintext
module3-basic-agents/
├── app/
│   ├── agents/
│   │   ├── basic/
│   │   │   ├── lifecycle_agent.py        # Basic lifecycle management
│   │   │   └── dynamic_prompt_agent.py   # Dynamic system prompt usage
│   │   └── advanced/
│   │       └── generic_lifecycle_agent.py # Enhanced generic lifecycle agent
│   ├── routers/
│   │   ├── basic_router.py               # Basic agents endpoints
│   │   └── advanced_router.py            # Advanced agents endpoints
│   └── tools/                            # Shared tool implementations
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
   ```

## API Endpoints

### Basic Agent Endpoints
- `POST /agents/basic/lifecycle/initialize` - Initialize lifecycle agent
- `POST /agents/basic/lifecycle/execute` - Execute lifecycle agent
- `POST /agents/basic/lifecycle/terminate` - Terminate lifecycle agent
- `POST /agents/basic/dynamic-prompt/update` - Update dynamic prompt
- `POST /agents/basic/dynamic-prompt/execute` - Execute with current prompt

### Advanced Agent Endpoints
- `POST /agents/advanced/generic-lifecycle/execute` - Execute generic lifecycle agent with tools

## Documentation

Detailed documentation is available in the `/docs` directory:
- `implementation_plan.md` - Project structure and implementation strategy
- `implementation_process.md` - Step-by-step implementation guide
- `phase1.md`, `phase2.md`, `phase3.md` - Detailed phase documentation
- `tutorial.md` - Comprehensive learning guide

## Development Workflow

1. Start with basic agents to understand core concepts
2. Progress to advanced agents with tool integration
3. Run tests frequently to verify functionality
4. Consult documentation for detailed guidance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

This module provides a structured learning path from basic to advanced agent development. Through hands-on implementation of various agent types and features, you'll gain practical experience in building sophisticated AI agent systems.

For detailed guidance, refer to the tutorial in `/docs/tutorial.md`.