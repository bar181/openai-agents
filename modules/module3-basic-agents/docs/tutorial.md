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
- Develop streaming agents for real-time content delivery
- Organize agents by complexity level (basic vs. advanced)
- Design clear API endpoints using FastAPI
- Write comprehensive tests for agent validation

---

## Module Structure Overview

We've organized this module into two main categories:
### 1. Basic Agents
- **Lifecycle Agent:** Learn fundamental agent state management
- **Dynamic Prompt Agent:** Explore runtime prompt modifications
- **Streaming Text Agent:** Implement real-time text streaming
- **Streaming Items Agent:** Create structured item sequence streaming

### 2. Advanced Agents
- **Generic Lifecycle Agent:** Implement sophisticated agents with tool integration
- **Multi-Tool Agent:** Create advanced agents with multiple tool capabilities and context management

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

#### Multi-Tool Agent with Advanced Capabilities
```python
# Example: Multi-Tool Agent Configuration
multi_tool_config = MultiToolAgentConfig(
    name="MultiToolAgent",
    instructions="Process complex tasks using multiple tools",
    tools=[
        # Basic tools
        echo, add, multiply, to_uppercase, current_time, fetch_mock_data,
        # Advanced tools
        json_tool, csv_tool, database_tool, text_analysis_tool,
        statistics_tool, pattern_tool, api_tool, visualization_tool
    ],
    debug_mode=True
)
```

**Key Learning Points:**
- Integrating diverse tool categories (data processing, analysis, integration)
- Managing context between operations
- Implementing state machines for execution phases
- Handling errors and recovery
- Processing multi-step workflows

### Phase 3: RESTful API Design

#### API Endpoints
```python
# Basic Agent Endpoints
@router.post("/lifecycle/initialize")
@router.post("/lifecycle/execute")
@router.post("/lifecycle/terminate")
@router.post("/dynamic-prompt/update")
@router.post("/dynamic-prompt/execute")

# Advanced Agent Endpoints
@router.post("/generic-lifecycle")
@router.post("/multi-tool")

# Streaming Endpoints
@router.post("/stream-text")
@router.post("/stream-items")
```

**Key Learning Points:**
- Designing clean, RESTful API endpoints
- Organizing endpoints by agent type and functionality
- Implementing proper request/response models
- Adding comprehensive API documentation
- Ensuring proper error handling and validation

### Phase 4: Streaming Agents Development

#### Streaming Text Agent
```python
# Example: Streaming Text Agent
class StreamTextAgent:
    async def initialize(self):
        """Initialize streaming agent"""
        return {"status": "initialized"}
    
    async def execute(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream text response incrementally"""
        async for chunk in self.stream_response(prompt):
            yield chunk
    
    async def terminate(self):
        """Clean up resources"""
        return {"status": "terminated"}
```

**Key Learning Points:**
- Implementing asynchronous generators for streaming
- Managing real-time content delivery
- Handling streaming response protocols
- Enhancing user experience with incremental content

#### Streaming Items Agent
```python
# Example: Streaming Items Agent
class StreamItemsAgent:
    async def execute(self, category: str, count: Optional[int] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream structured items incrementally"""
        # Status event
        yield {"type": "status", "message": f"Generating {category} items..."}
        
        # Count event
        count = count or await self._determine_count(category)
        yield {"type": "count", "count": count}
        
        # Item events
        for i in range(count):
            item = await self._generate_item(category, i)
            yield {"type": "item", "index": i + 1, "content": item}
            
        # Complete event
        yield {"type": "complete", "message": f"Generated {count} {category} items."}
```

**Key Learning Points:**
- Structuring streaming events for client processing
- Implementing multi-stage streaming workflows
- Managing state during streaming operations
- Creating dynamic content generation pipelines

#### Streaming API Endpoints
```python
# Streaming Endpoints
@router.post("/stream-text")
async def stream_text_endpoint(request: TextStreamRequest):
    """Stream a text response from the agent."""
    return StreamingResponse(generate(), media_type="text/plain")

@router.post("/stream-items")
async def stream_items_endpoint(request: ItemStreamRequest):
    """Stream a sequence of items from the agent."""
    return StreamingResponse(generate(), media_type="application/x-ndjson")
```

**Key Learning Points:**
- Implementing FastAPI streaming responses
- Managing different content types for streaming
- Handling client connections during streaming
- Implementing proper error handling for streams

---

## Working with the Code

### Basic Agents Directory (`app/agents/basic/`)
```plaintext
basic/
├── lifecycle_agent.py      # Basic lifecycle management
├── dynamic_prompt_agent.py # Dynamic prompt handling
├── stream_text_agent.py    # Streaming text responses
└── stream_items_agent.py   # Streaming structured items
```

### Advanced Agents Directory (`app/agents/advanced/`)
```plaintext
advanced/
├── generic_lifecycle_agent.py # Enhanced agent with tools
└── multi_tool_agent.py        # Advanced agent with multiple tool capabilities
```

### Tools Directory (`app/tools/`)
```plaintext
tools/
├── base_tool.py         # Abstract base class for all tools
│   ├── BaseTool         # Base class for all tools
│   └── ToolResult       # Standardized result structure
│
├── math_tools.py        # Mathematical operations
│   ├── add              # Add two numbers
│   └── multiply         # Multiply two numbers
│
├── string_tools.py      # String manipulation
│   ├── concatenate      # Join strings together
│   └── to_uppercase     # Convert string to uppercase
│
├── datetime_tools.py    # Time utilities
│   ├── current_time     # Get current date and time
│   └── add_days         # Add days to a date
│
├── data_tools.py        # Data handling
│   ├── get_item         # Get item from a list by index
│   ├── summarize_list   # Generate summary statistics for a list
│   └── fetch_mock_data  # Retrieve sample data for testing
│
├── echo_tools.py        # Echo functionality
│   └── echo             # Return input as output
│
├── json_tools.py        # JSON validation and transformation
│   ├── JsonTool         # JSON processing tool class
│   ├── validate_json    # Validate JSON against schema
│   └── transform_json   # Apply transformations to JSON
│
├── csv_tools.py         # CSV parsing and generation
│   ├── CsvTool          # CSV processing tool class
│   ├── parse_csv        # Convert CSV to structured data
│   └── generate_csv     # Create CSV from structured data
│
├── database_tools.py    # Mock database operations
│   ├── DatabaseTool     # Database interaction tool class
│   ├── store_data       # Save data to database
│   ├── retrieve_data    # Get data from database
│   ├── list_keys        # List available keys
│   ├── delete_data      # Remove data by key
│   └── clear_database   # Reset database
│
├── analysis_tools.py    # Text and data analysis
│   ├── TextAnalysisTool # Text analysis tool class
│   ├── analyze_sentiment # Determine text sentiment
│   ├── extract_entities # Identify entities in text
│   ├── extract_keywords # Extract important keywords
│   ├── StatisticsTool   # Statistical analysis tool class
│   ├── calculate_basic_stats # Calculate mean, median, mode, etc.
│   ├── perform_correlation # Measure relationship between variables
│   ├── PatternTool      # Pattern recognition tool class
│   ├── find_patterns    # Identify patterns in data
│   └── apply_regex      # Apply regular expressions
│
├── api_tools.py         # API integration utilities
│   ├── ApiTool          # API interaction tool class
│   ├── make_request     # Send HTTP requests
│   ├── CacheTool        # Caching tool class
│   ├── cache_get        # Retrieve cached data
│   ├── cache_set        # Store data in cache
│   ├── RateLimiterTool  # Rate limiting tool class
│   └── check_rate_limit # Verify request limits
│
└── visualization_tools.py # Data visualization
    ├── VisualizationTool # Visualization tool class
    ├── create_bar_chart  # Generate bar charts
    ├── create_line_chart # Generate line charts
    ├── create_pie_chart  # Generate pie charts
    └── create_scatter_plot # Generate scatter plots
```

---

## Testing Your Implementation

We've provided comprehensive tests for both basic and advanced agents:

```bash
# Test basic agents
python -m pytest tests/test_basic_agents.py

# Test advanced agents
python -m pytest tests/test_advanced_agents.py

# Test streaming agents
python -m pytest tests/test_stream_text.py tests/test_stream_items.py
```

Key test scenarios include:
- Lifecycle management validation
- Dynamic prompt updates
- Tool integration verification
- Error handling checks
- Multi-tool agent capabilities:
  - JSON processing
  - Text analysis
  - Data visualization
  - Multi-step workflows
  - Context preservation
- Streaming agent capabilities:
  - Real-time text streaming
  - Structured items streaming
  - Custom instructions handling
  - Error handling and validation

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
   - Enhance the streaming text agent with progress indicators
   - Add new item types to the streaming items agent

2. **Advanced Agent Exercise:**
   - Add a new tool to the generic lifecycle agent
   - Implement custom lifecycle hooks for logging
   - Extend the multi-tool agent with a new tool category
   - Implement context preservation between tool executions

3. **Streaming Agent Exercise:**
   - Implement a streaming agent that combines text and items
   - Add filtering capabilities to the streaming items agent
   - Create a streaming visualization agent for real-time charts
   - Implement pause/resume functionality for streaming responses

4. **Integration Exercise:**
   - Create a new endpoint combining multiple agent capabilities
   - Implement error handling and validation
   - Build a frontend demo that consumes streaming endpoints

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
