# Module 3 Tutorial: Basic and Advanced Agent Development

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Master's Student at Harvard University, CS50 Teaching Fellow*

---

## Welcome to Module 3!

Hello again! In this module, we're taking a significant step forward in agent development by exploring both basic and advanced agent concepts. You'll learn how to manage agent lifecycles, implement dynamic system prompts, and create sophisticated agents with integrated tools. This module is structured to progressively build your understanding from fundamental concepts to advanced implementations.

---

## Learning Goals

By completing this module, you will:

- Master agent lifecycle management (initialization, execution, termination)
- Implement dynamic system prompts for flexible agent behavior
- Create advanced agents with integrated tool suites
- Organize agents by complexity level (basic vs. advanced)
- Design clear API endpoints using FastAPI
- Write comprehensive tests for agent validation

---

## Module Structure Overview

We've organized this module into two main categories:

### 1. Basic Agents
- **Lifecycle Agent:** Learn fundamental agent state management
- **Dynamic Prompt Agent:** Explore runtime prompt modifications

### 2. Advanced Agents
- **Generic Lifecycle Agent:** Implement sophisticated agents with tool integration

This structure helps you progressively build your understanding while keeping code organized and maintainable.

---

## Step-by-Step Learning Path

### Phase 1: Basic Agent Development

#### Lifecycle Management
```python
# Example: Basic Lifecycle Agent
async def initialize_agent():
    """Initialize agent state"""
    return {"status": "initialized"}

async def execute_agent(input_data):
    """Process user input"""
    return {"result": process_input(input_data)}

async def terminate_agent():
    """Clean up resources"""
    return {"status": "terminated"}
```

**Key Learning Points:**
- Understanding agent state management
- Handling initialization and cleanup
- Processing user inputs systematically

#### Dynamic System Prompts
```python
# Example: Dynamic Prompt Agent
async def update_system_prompt(new_prompt: str):
    """Update agent's behavior instructions"""
    return {"updated_prompt": new_prompt}

async def execute_with_prompt(input_data: str):
    """Execute with current prompt context"""
    return {"response": generate_response(input_data)}
```

**Key Learning Points:**
- Modifying agent behavior at runtime
- Managing prompt context
- Adapting agent responses dynamically

### Phase 2: Advanced Agent Development

#### Generic Lifecycle Agent with Tools
```python
# Example: Advanced Agent Configuration
config = GenericAgentConfig(
    name="AdvancedAgent",
    instructions="Process inputs using available tools",
    tools=[
        echo,           # Basic echo functionality
        add,           # Mathematical operations
        to_uppercase,  # String manipulation
        current_time,  # Time utilities
        fetch_mock_data # Data operations
    ]
)
```

**Key Learning Points:**
- Integrating multiple tools into agents
- Configuring agent behavior
- Implementing lifecycle hooks for monitoring
- Managing complex agent states

---

## Working with the Code

### Basic Agents Directory (`app/agents/basic/`)
```plaintext
basic/
├── lifecycle_agent.py     # Basic lifecycle management
└── dynamic_prompt_agent.py # Dynamic prompt handling
```

### Advanced Agents Directory (`app/agents/advanced/`)
```plaintext
advanced/
└── generic_lifecycle_agent.py # Enhanced agent with tools
```

### Tools Directory (`app/tools/`)
```plaintext
tools/
├── math_tools.py      # Mathematical operations
├── string_tools.py    # String manipulation
├── datetime_tools.py  # Time utilities
├── data_tools.py      # Data handling
└── echo_tools.py      # Echo functionality
```

---

## Testing Your Implementation

We've provided comprehensive tests for both basic and advanced agents:

```bash
# Test basic agents
python -m pytest tests/test_basic_agents.py

# Test advanced agents
python -m pytest tests/test_advanced_agents.py
```

Key test scenarios include:
- Lifecycle management validation
- Dynamic prompt updates
- Tool integration verification
- Error handling checks

---

## Tips for Success

1. **Progressive Learning:**
   - Start with basic agents to understand core concepts
   - Move to advanced agents once comfortable with basics
   - Take time to understand each tool's purpose

2. **Testing Strategy:**
   - Write tests before implementing features
   - Verify each agent function independently
   - Test tool integrations thoroughly

3. **Common Pitfalls to Avoid:**
   - Don't skip basic concepts to jump to advanced features
   - Always handle agent cleanup properly
   - Verify tool availability before usage

---

## Practical Exercises

1. **Basic Agent Exercise:**
   - Modify the lifecycle agent to include custom state tracking
   - Add new prompt templates to the dynamic prompt agent

2. **Advanced Agent Exercise:**
   - Add a new tool to the generic lifecycle agent
   - Implement custom lifecycle hooks for logging

3. **Integration Exercise:**
   - Create a new endpoint combining multiple agent capabilities
   - Implement error handling and validation

---

## Next Steps

After completing this module, you'll have a solid foundation in both basic and advanced agent development. The next module will build upon these concepts to create even more sophisticated agent systems.

Remember:
- Review the documentation in `/docs`
- Test your implementations thoroughly
- Experiment with different tool combinations
- Practice error handling and validation

---

*Keep building and exploring! The skills you're learning here are fundamental to creating sophisticated AI agent systems.*

*- Bradley Ross*
