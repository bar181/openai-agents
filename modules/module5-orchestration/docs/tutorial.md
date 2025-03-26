## Module 5: Orchestration - Tutorial

### Introduction

Welcome to Module 5! In previous modules, we've explored creating AI agents with various LLM providers. Now, we'll take a significant step forward by implementing advanced orchestration patterns that enable multiple specialized agents to work together seamlessly. This module focuses on implementing guardrails, agent-to-agent handoffs, comprehensive tracing, and intelligent message routing to create robust, safe, and efficient multi-agent systems.

### Learning Objectives

In this module, you'll learn to:

- Implement input and output guardrails to ensure safe and appropriate agent interactions
- Create agent-to-agent handoff mechanisms for specialized task delegation
- Develop message filtering for contextual information passing between agents
- Implement comprehensive tracing for monitoring and debugging agent interactions
- Design advanced orchestration patterns for intelligent task routing

### Prerequisites

Make sure you're comfortable with:

- Python programming
- Asynchronous programming with Python
- Basic understanding of AI agent concepts
- FastAPI for building API endpoints
- Writing and running Python tests

### Module Structure

This module unfolds in six clear phases, each building on the previous one:

1. **Environment & Setup**
2. **Input & Output Guardrails**
3. **Agent Handoffs**
4. **Comprehensive Tracing**
5. **Advanced Orchestration**
6. **Documentation & Final Checks**

Let's get started!

---

## Phase 1: Environment & Setup

Before diving into code, we'll prepare your workspace to ensure a smooth development experience.

### Step-by-Step Guide

1. **Project Directory Structure:**
   - Create a directory structure that supports orchestration components
   - Set up folders for guardrails, handoffs, and tracing

2. **Configuration Setup:**
   - Configure environment variables for orchestration settings
   - Set up logging levels for tracing and debugging

3. **Placeholder Files:**
   - Create placeholder files for guardrails, handoffs, and tracing
   - Set up basic router structure for orchestration endpoints

4. **Testing Framework:**
   - Prepare test files for each orchestration component
   - Set up mock objects for testing agent interactions

---

## Phase 2: Input & Output Guardrails

Guardrails are essential for ensuring that agent interactions remain safe, appropriate, and within defined boundaries.

### Implementation Steps

1. **Input Guardrails:**
   - Create `input_guardrails.py` to validate user inputs before processing
   - Implement guardrails for:
     - Empty input validation
     - Input length validation
     - Harmful content detection
     - Inappropriate language detection
   - Use the `@input_guardrail()` decorator from the OpenAI Agents SDK

2. **Output Guardrails:**
   - Create `output_guardrails.py` to validate agent outputs before returning to users
   - Implement guardrails for:
     - Empty output validation
     - Output length validation
     - Error detection in outputs
     - Output format validation
   - Use the `@output_guardrail()` decorator from the OpenAI Agents SDK

3. **Guardrail Agent:**
   - Create a `GuardrailAgent` class that combines input and output guardrails
   - Implement a factory function for easy agent creation with configurable guardrails
   - Ensure proper error handling for guardrail tripwires

4. **Router Integration:**
   - Add endpoints for testing input and output guardrails
   - Implement error handling for guardrail violations
   - Create test endpoints for individual guardrail testing

---

## Phase 3: Agent Handoffs

Agent handoffs enable specialized agents to handle specific types of tasks, improving efficiency and response quality.

### Key Components

1. **Specialized Agents:**
   - **Billing Agent:** Handles billing inquiries, payment issues, and invoice questions
   - **Technical Support Agent:** Resolves technical issues, troubleshooting, and system problems
   - **Customer Service Agent:** Manages general inquiries and non-technical assistance
   - Each agent is specialized with specific instructions and capabilities

2. **Handoff Mechanism:**
   - Create `handoff_agent.py` to implement agent-to-agent handoffs
   - Implement the `HandoffAgent` class that can delegate tasks to specialized agents
   - Use the OpenAI Agents SDK's `handoff()` function to create handoff instances
   - Create a factory function for easy handoff agent creation

3. **Message Filtering:**
   - Implement message filters for each specialized agent type:
     - `filter_billing_messages` for billing-related content
     - `filter_technical_messages` for technical support-related content
     - `filter_customer_service_messages` for customer service-related content
   - Ensure only relevant information is passed during handoffs
   - Add appropriate context for specialized agents

4. **Agent Type Determination:**
   - Implement keyword-based routing to determine the appropriate agent type
   - Create logic to analyze user messages and route to the correct specialized agent
   - Ensure seamless delegation based on message content

5. **Router Integration:**
   - Add `/handoffs` endpoint for processing requests with specialized agents
   - Add `/handoffs/triage` endpoint for determining which agent should handle a request
   - Implement error handling for handoff failures

---

## Phase 4: Comprehensive Tracing

Tracing provides visibility into agent interactions, making debugging and monitoring easier.

### Implementation Steps

1. **Trace Processor:**
   - Create `trace_processor.py` to capture and process trace information
   - Implement the `OrchestrationTraceProcessor` class to store and manage traces
   - Register the trace processor with the agents library using `add_trace_processor()`
   - Implement methods to retrieve, format, and clear traces
   - Add a `shutdown` method for proper cleanup during application shutdown

2. **Trace Integration:**
   - Enhance input guardrails with tracing:
     - Add spans for each validation step
     - Record input details and validation results
     - Capture tripwire triggers and reasons
   - Enhance output guardrails with tracing:
     - Add spans for each validation step
     - Record output details and validation results
     - Capture error conditions and format issues
   - Enhance handoff agent with tracing:
     - Add spans for agent type determination
     - Add spans for specialized agent processing
     - Record message filtering operations
     - Capture handoff decisions and results

3. **Trace Visualization:**
   - Implement `format_trace_for_display` function to format traces in a hierarchical format
   - Create helper functions to format spans and their attributes
   - Ensure proper indentation for nested spans
   - Add detailed timing information for performance analysis

4. **Router Integration:**
   - Add `/traces` endpoint to retrieve all traces
   - Add `/traces/{trace_id}` endpoint to retrieve a specific trace
   - Add `/traces/{trace_id}/formatted` endpoint to get a formatted trace
   - Add `/traces/clear` endpoint to clear all traces
   - Enhance `/trace-status` endpoint to provide trace summary information

5. **Testing:**
   - Create mock trace and span classes for testing
   - Use patching to inject mock traces during tests
   - Manually process traces in test scenarios
   - Verify trace capture, formatting, and retrieval

### Example: Adding Tracing to a Guardrail

```python
@input_guardrail()
async def validate_empty_input(context: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailFunctionOutput:
    """Validate that the user input is not empty."""
    logger.info(f"Validating input is not empty: {user_input[:50]}...")
    
    # Get the current trace
    trace = get_current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_empty_input") as span:
        span.set_attribute("input_length", len(user_input))
        
        if not user_input or len(user_input.strip()) == 0:
            logger.warning("Input is empty")
            span.set_attribute("tripwire_triggered", True)
            span.set_attribute("reason", "Input cannot be empty")
            
            return GuardrailFunctionOutput(
                output_info="Input cannot be empty.",
                tripwire_triggered=True
            )
        
        span.set_attribute("tripwire_triggered", False)
        return GuardrailFunctionOutput(
            output_info=None,
            tripwire_triggered=False
        )
```

### Example: Retrieving and Formatting Traces

```python
# Get all traces
traces = trace_processor.get_all_traces()

# Get a specific trace
trace = trace_processor.get_trace(trace_id)

# Format a trace for display
formatted_trace = format_trace_for_display(trace)
print(formatted_trace)
```

---

## Phase 5: Advanced Orchestration

Advanced orchestration patterns enable more sophisticated agent interactions and routing.

### Key Components

1. **Message Routing:**
   - Implement intelligent message routing based on content analysis
   - Create routing rules for different types of requests
   - Enable dynamic routing based on agent availability and specialization

2. **State Management:**
   - Implement in-memory state management for agent interactions
   - Maintain context across multiple interactions
   - Enable stateful conversations with multiple agents

3. **Router Integration:**
   - Add endpoints for advanced orchestration patterns
   - Implement state management endpoints
   - Create configuration endpoints for routing rules

---

## Phase 6: Documentation & Final Checks

Comprehensive documentation and thorough testing ensure reliability and maintainability.

### Documentation Steps

- Document each phase in detail
- Create clear usage examples for each orchestration pattern
- Update the main README with orchestration capabilities

### Final Testing

- Run the complete test suite
- Verify all orchestration patterns work as expected
- Ensure proper error handling throughout the system

### Code Review

- Check for clean, readable code
- Ensure proper separation of concerns
- Verify that all components work together seamlessly

---

### Conclusion

Congratulations on completing Module 5! You've built a sophisticated orchestration system that enables multiple specialized agents to work together seamlessly. The guardrails, handoffs, tracing, and advanced orchestration patterns you've implemented provide a robust foundation for creating complex, safe, and efficient multi-agent systems.

Continue exploring the capabilities of agent orchestration, and remember that these patterns can be extended and customized for a wide range of applications. The skills you've developed in this module are essential for creating enterprise-grade AI agent systems that can handle complex tasks while maintaining safety and efficiency.