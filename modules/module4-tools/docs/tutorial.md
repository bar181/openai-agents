# Module 3 Tutorial: Basic and Advanced Agent Development

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Director @ Agentics Foundation, Programmers and Data Scientist with over 20 years experience, Master's Student at Harvard University, CS50 Teaching Fellow/Course Assistant,  Instructor and Course Designer* 

---

## Welcome to Module 3!

Welcome back! In Module 3, you'll dive deeper into the fascinating world of AI agent development, starting from foundational concepts and progressing toward more advanced implementations. You’ll learn essential techniques for managing agent lifecycles, dynamically updating agent behaviors, and creating advanced agents that can handle real-time tasks and sophisticated tool integrations. Let’s get started!

---

## What You’ll Learn

By the end of Module 3, you will confidently:

- Manage complete agent lifecycles, from initialization to execution and termination.
- Implement dynamic system prompts, enabling flexible agent behaviors.
- Build advanced agents equipped with multiple integrated tools.
- Develop streaming agents capable of real-time content delivery.
- Structure your agents clearly by complexity (basic vs. advanced).
- Create clean and robust API endpoints using FastAPI.
- Write effective tests to validate agent functionality and stability.

---

## Module Structure

We’ve designed Module 3 to smoothly guide you through two essential levels:

### 1. Basic Agents
- **Lifecycle Agent:** Master fundamental state management.
- **Dynamic Prompt Agent:** Learn to adapt agent behavior in real-time.
- **Streaming Text Agent:** Implement real-time text streaming.
- **Streaming Items Agent:** Stream structured data incrementally.

### 2. Advanced Agents
- **Generic Lifecycle Agent:** Create versatile agents with integrated tools.
- **Multi-Tool Agent:** Develop highly capable agents with multiple tools and context management.

This structured approach ensures steady progress and easy-to-maintain code.

---

## Step-by-Step Guide

### Phase 1: Basic Agent Development

#### Agent Lifecycle Management
Understand the core aspects of an agent's lifecycle:
```python
async def initialize_agent():
    return {"status": "initialized"}

async def execute_agent(input_data):
    return {"result": process_input(input_data)}

async def terminate_agent():
    return {"status": "terminated"}
```

#### Dynamic Prompts
Update your agents dynamically:
```python
async def update_system_prompt(new_prompt: str):
    return {"updated_prompt": new_prompt}

async def execute_with_prompt(input_data: str):
    return {"response": generate_response(input_data)}
```

### Phase 2: Advanced Agent Development

#### Tool Integration
Create agents capable of using multiple tools:
```python
config = GenericAgentConfig(
    name="AdvancedAgent",
    instructions="Use provided tools effectively",
    tools=[echo, add, to_uppercase, current_time, fetch_mock_data]
)
```

#### Multi-Tool Advanced Agents
Develop powerful, multi-capability agents:
```python
multi_tool_config = MultiToolAgentConfig(
    name="MultiToolAgent",
    instructions="Solve complex tasks efficiently",
    tools=[echo, add, multiply, json_tool, csv_tool, database_tool, text_analysis_tool, api_tool, visualization_tool],
    debug_mode=True
)
```

### Phase 3: RESTful API Design

#### Designing Clear API Endpoints
Organize endpoints logically and clearly:
```python
@router.post("/lifecycle/initialize")
@router.post("/lifecycle/execute")
@router.post("/lifecycle/terminate")
@router.post("/dynamic-prompt/update")
@router.post("/dynamic-prompt/execute")

# Advanced endpoints
@router.post("/generic-lifecycle")
@router.post("/multi-tool")

# Streaming endpoints
@router.post("/stream-text")
@router.post("/stream-items")
```

### Phase 4: Streaming Agents

#### Real-Time Streaming Agents
Implement responsive agents delivering content incrementally:
```python
class StreamTextAgent:
    async def execute(self, prompt: str) -> AsyncGenerator[str, None]:
        async for chunk in self.stream_response(prompt):
            yield chunk
```

---

## Project Structure Overview

### Basic Agents (`app/agents/basic/`)
- Lifecycle management
- Dynamic prompts
- Text and structured item streaming

### Advanced Agents (`app/agents/advanced/`)
- Enhanced lifecycle with tool integration
- Multi-tool capabilities

### Tool Suite (`app/tools/`)
- Math, string, datetime utilities
- Data management and analysis
- JSON and CSV processing
- API integration and visualization

---

## Testing Your Agents

Run provided tests to ensure your agents function correctly:
```bash
# Basic agent tests
python -m pytest tests/test_basic_agents.py

# Advanced agent tests
python -m pytest tests/test_advanced_agents.py

# Streaming agent tests
python -m pytest tests/test_stream_text.py tests/test_stream_items.py
```

Key testing scenarios:
- Lifecycle validations
- Dynamic behavior updates
- Tool integrations and error handling
- Multi-step workflows
- Real-time streaming capabilities

---

## Tips for Success

- Start simple and gradually move to complex implementations.
- Always thoroughly test each function and agent separately.
- Practice integrating multiple tools early on.
- Avoid skipping foundational concepts.

---

## Practical Exercises

Strengthen your skills with these hands-on tasks:

- **Basic Agent:** Add custom state tracking and enhanced prompts.
- **Advanced Agent:** Integrate new tools and improve lifecycle hooks.
- **Streaming Agent:** Combine multiple streams and add advanced controls.
- **Integration Task:** Build an API endpoint that combines agent capabilities.

---

## Next Steps

With Module 3 complete, you’re well-prepared for more sophisticated agent architectures. Module 4 awaits, where you'll integrate diverse LLM providers to further empower your AI systems!

Keep exploring and building—the skills you're acquiring are central to creating advanced AI agents.

*- Bradley Ross*

