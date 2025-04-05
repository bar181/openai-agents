# Module 3: Basic and Advanced OpenAI Agents

Welcome to Module 3! This module introduces you to essential concepts in AI agent development, covering everything from basic lifecycle management to advanced tool integration. You'll progressively enhance your skills, starting from simple agents and moving towards building sophisticated agents capable of real-time streaming and complex tool interactions.

---

## Features

### Basic Agents

- **Lifecycle Management:** Initialize, execute, and terminate agents effectively.
- **Dynamic System Prompts:** Modify agent behaviors dynamically during runtime.
- **Streaming Text Agent:** Real-time incremental streaming of text-based responses.
- **Streaming Items Agent:** Stream structured items sequentially in real-time.

### Advanced Agents

- **Generic Lifecycle Agent:** Sophisticated agent integrating multiple tools seamlessly.
- **Multi-Tool Agent:** Advanced agent with multi-tool integration and context awareness.

### Integrated Tools Suite

- **Basic Tools:**
  - Math operations: Add, multiply.
  - String manipulation: Concatenate, uppercase conversion.
  - Data utilities: Fetch mock data, summarize lists.
  - Date/time utilities: Current time retrieval, date calculations.
  - Echo functionality.

- **Advanced Tools:**
  - JSON and CSV processing.
  - Database operations.
  - Text analysis and statistics.
  - Pattern matching and regex operations.
  - API integration and management.
  - Data visualization (charts and plots).

---

## Project Structure

```plaintext
module3-basic-agents/
├── app/
│   ├── agents/
│   │   ├── basic/
│   │   │   ├── lifecycle_agent.py
│   │   │   ├── dynamic_prompt_agent.py
│   │   │   ├── stream_text_agent.py
│   │   │   └── stream_items_agent.py
│   │   └── advanced/
│   │       ├── generic_lifecycle_agent.py
│   │       └── multi_tool_agent.py
│   ├── routers/
│   │   ├── basic_router.py
│   │   └── advanced_router.py
│   └── tools/
│       ├── base_tool.py
│       ├── math_tools.py
│       ├── string_tools.py
│       ├── data_tools.py
│       ├── datetime_tools.py
│       ├── echo_tools.py
│       ├── json_tools.py
│       ├── csv_tools.py
│       ├── database_tools.py
│       ├── analysis_tools.py
│       ├── api_tools.py
│       └── visualization_tools.py
├── docs/
└── tests/
```

---

## Getting Started

### Environment Setup

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

```bash
cp .env.sample .env
# Update .env file with your OPENAI_API_KEY
```

### Run the FastAPI Server

```bash
python -m uvicorn app.main:app --reload
```

### Running Tests

```bash
python -m pytest tests/

# Individual tests
python -m pytest tests/test_basic_agents.py
python -m pytest tests/test_advanced_agents.py
python -m pytest tests/test_stream_text.py
python -m pytest tests/test_stream_items.py
```

---

## API Endpoints

### Basic Agents

- `/agents/basic/lifecycle/initialize`
- `/agents/basic/lifecycle/execute`
- `/agents/basic/lifecycle/terminate`
- `/agents/basic/dynamic-prompt/update`
- `/agents/basic/dynamic-prompt/execute`
- `/agents/basic/stream-text`
- `/agents/basic/stream-items`

### Advanced Agents

- `/agents/advanced/generic-lifecycle`
- `/agents/advanced/multi-tool`

---

## Documentation

Detailed guides are located in the `/docs` directory:

- `implementation_plan.md`
- `implementation_process.md`
- Phase-specific documents (`phase1.md`, etc.)
- Comprehensive `tutorial.md`

---

## Development Workflow

- Begin with basic agent implementations.
- Explore real-time streaming capabilities.
- Progress to advanced agent and tool integrations.
- Frequently test and validate functionality.

---

## Contributing

1. Fork and clone the repository.
2. Create and switch to a new feature branch.
3. Commit your changes clearly and concisely.
4. Push your branch and create a Pull Request.

---

## License

This project is licensed under the MIT License – see `LICENSE` for details.

---

By completing Module 3, you'll acquire the essential skills needed for creating advanced, interactive AI agents capable of sophisticated behaviors and real-time interactions. For detailed instructions, refer to the comprehensive tutorial located in `/docs/tutorial.md`.

