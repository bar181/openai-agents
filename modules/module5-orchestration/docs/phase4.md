## Module 5 – Phase 4: Comprehensive Tracing Implementation

In **Phase 4**, we will implement comprehensive tracing for guardrails and handoffs within our agent orchestration system. Tracing is vital for monitoring, debugging, and optimizing agent workflows, providing visibility into each step of the agent's execution.

---

## Objectives

1. **Integrate Tracing Mechanisms:**
   - Implement tracing to monitor agent interactions, guardrail validations, and handoff processes.
   - Utilize the OpenAI Agents SDK's built-in tracing capabilities to capture detailed execution flows.

2. **Configure Tracing Processors:**
   - Set up tracing processors to handle and export trace data to observability platforms.
   - Ensure that tracing data is structured and accessible for analysis.

3. **Monitor and Debug Agent Workflows:**
   - Use tracing data to identify bottlenecks, errors, and inefficiencies in agent operations.
   - Leverage insights from tracing to optimize agent performance and reliability.

---

## Implementation Steps

### Step 1: Create a Trace Processor

First, we'll create a custom trace processor that captures and processes trace data from our agents, guardrails, and handoffs.

```python
# app/agents/orchestration/trace_processor.py

import logging
import json
import time
from typing import Dict, Any, List, Optional
from agents.tracing import TraceProcessor, Trace, Span
from app import config

logger = logging.getLogger(__name__)

class OrchestrationTraceProcessor(TraceProcessor):
    """
    Custom trace processor for orchestration operations.
    
    This processor captures and processes trace data from agents, guardrails, and handoffs.
    """
    
    def __init__(self, log_level: str = config.TRACE_LOG_LEVEL):
        """Initialize the trace processor with the specified log level."""
        self.log_level = log_level
        self.traces: Dict[str, Dict[str, Any]] = {}
        
    def process_trace(self, trace: Trace) -> None:
        """
        Process a trace from an agent operation.
        
        Args:
            trace: The trace to process.
        """
        trace_id = trace.trace_id
        
        # Store the trace
        self.traces[trace_id] = {
            "trace_id": trace_id,
            "start_time": trace.start_time,
            "end_time": trace.end_time,
            "duration_ms": (trace.end_time - trace.start_time) * 1000,
            "spans": [self._process_span(span) for span in trace.spans],
            "metadata": trace.metadata
        }
        
        # Log the trace
        logger.log(
            getattr(logging, self.log_level),
            f"Trace {trace_id}: {json.dumps(self.traces[trace_id], indent=2)}"
        )
    
    def _process_span(self, span: Span) -> Dict[str, Any]:
        """
        Process a span from a trace.
        
        Args:
            span: The span to process.
            
        Returns:
            A dictionary representation of the span.
        """
        return {
            "span_id": span.span_id,
            "parent_id": span.parent_id,
            "name": span.name,
            "start_time": span.start_time,
            "end_time": span.end_time,
            "duration_ms": (span.end_time - span.start_time) * 1000,
            "attributes": span.attributes
        }
    
    def get_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a trace by its ID.
        
        Args:
            trace_id: The ID of the trace to get.
            
        Returns:
            The trace, or None if not found.
        """
        return self.traces.get(trace_id)
    
    def get_all_traces(self) -> List[Dict[str, Any]]:
        """
        Get all traces.
        
        Returns:
            A list of all traces.
        """
        return list(self.traces.values())
    
    def clear_traces(self) -> None:
        """Clear all traces."""
        self.traces.clear()
```

### Step 2: Configure Tracing in the Application

Next, we'll configure the application to use our custom trace processor and enable tracing for all agent operations.

```python
# app/main.py (additions)

from agents import set_trace_processors
from app.agents.orchestration.trace_processor import OrchestrationTraceProcessor

# Initialize the trace processor
trace_processor = OrchestrationTraceProcessor()

# Set the trace processor for the application
set_trace_processors([trace_processor])

# The rest of the application setup...
```

### Step 3: Implement Tracing for Guardrails

Now, let's enhance our guardrail implementations to include detailed tracing information.

```python
# app/agents/orchestration/input_guardrails.py (modifications)

from agents import input_guardrail, RunContextWrapper, Agent
from agents.guardrail import GuardrailResult
from agents.tracing import current_trace

@input_guardrail()
async def validate_empty_input(context: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailResult:
    """Validate that the input is not empty."""
    # Get the current trace
    trace = current_trace()
    
    # Add a span for this guardrail
    with trace.create_span("validate_empty_input") as span:
        span.set_attribute("input_length", len(user_input))
        
        if not user_input or len(user_input.strip()) == 0:
            span.set_attribute("tripwire_triggered", True)
            span.set_attribute("reason", "Input cannot be empty")
            return GuardrailResult(tripwire_triggered=True, message="Input cannot be empty")
        
        span.set_attribute("tripwire_triggered", False)
        return GuardrailResult(tripwire_triggered=False)
```

### Step 4: Implement Tracing for Handoffs

Let's enhance our handoff agent to include detailed tracing information.

```python
# app/agents/orchestration/handoff_agent.py (modifications)

from agents import Agent, handoff, RunContextWrapper
from agents.tracing import current_trace

class HandoffAgent(Agent):
    # ... existing code ...
    
    async def determine_agent_type(self, message: str) -> str:
        """Determine which type of agent should handle the message."""
        # Get the current trace
        trace = current_trace()
        
        # Add a span for agent type determination
        with trace.create_span("determine_agent_type") as span:
            span.set_attribute("message", message)
            
            # Simple keyword-based routing for demonstration
            message_lower = message.lower()
            
            if any(word in message_lower for word in ["bill", "payment", "invoice", "charge", "subscription", "refund", "price"]):
                agent_type = "billing"
            elif any(word in message_lower for word in ["error", "bug", "crash", "not working", "broken", "fix", "problem", "technical"]):
                agent_type = "technical"
            else:
                agent_type = "customer_service"
            
            span.set_attribute("determined_agent_type", agent_type)
            return agent_type
    
    async def process_with_specialized_agent(self, message: str, agent_type: str) -> Dict[str, Any]:
        """Process a message with a specialized agent."""
        # Get the current trace
        trace = current_trace()
        
        # Add a span for processing with specialized agent
        with trace.create_span("process_with_specialized_agent") as span:
            span.set_attribute("message", message)
            span.set_attribute("agent_type", agent_type)
            
            try:
                agent = self.specialized_agents.get(agent_type)
                if not agent:
                    span.set_attribute("error", f"Unknown agent type: {agent_type}")
                    return {
                        "status": "error",
                        "message": f"Unknown agent type: {agent_type}",
                        "agent_type": "unknown"
                    }
                
                # Process with the specialized agent
                with trace.create_span(f"specialized_agent_{agent_type}") as agent_span:
                    response = await agent.run(message)
                    agent_span.set_attribute("response", response)
                
                span.set_attribute("status", "success")
                return {
                    "status": "success",
                    "message": response,
                    "agent_type": agent_type
                }
            except Exception as e:
                error_message = f"Error processing with specialized agent: {str(e)}"
                span.set_attribute("error", error_message)
                logger.error(error_message)
                return {
                    "status": "error",
                    "message": error_message,
                    "agent_type": agent_type
                }
```

### Step 5: Add Tracing Endpoints to the Router

Now, let's add endpoints to our router for retrieving and managing trace data.

```python
# app/routers/orchestration_router.py (additions)

from app.agents.orchestration.trace_processor import OrchestrationTraceProcessor

# Get the trace processor instance
trace_processor = OrchestrationTraceProcessor()

@router.get("/traces")
async def get_all_traces():
    """
    Get all traces.
    
    Returns:
        A list of all traces.
    """
    return trace_processor.get_all_traces()

@router.get("/traces/{trace_id}")
async def get_trace(trace_id: str):
    """
    Get a trace by its ID.
    
    Args:
        trace_id: The ID of the trace to get.
        
    Returns:
        The trace, or a 404 error if not found.
    """
    trace = trace_processor.get_trace(trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail=f"Trace {trace_id} not found")
    return trace

@router.delete("/traces")
async def clear_traces():
    """
    Clear all traces.
    
    Returns:
        A success message.
    """
    trace_processor.clear_traces()
    return {"status": "success", "message": "All traces cleared"}
```

### Step 6: Visualize Trace Data

Finally, let's create a simple utility function to visualize trace data in a hierarchical format.

```python
# app/utils/trace_visualizer.py

import json
from typing import Dict, Any, List

def format_trace_for_display(trace: Dict[str, Any]) -> str:
    """
    Format a trace for display in a hierarchical format.
    
    Args:
        trace: The trace to format.
        
    Returns:
        A formatted string representation of the trace.
    """
    output = []
    
    # Add trace header
    output.append(f"Trace ID: {trace['trace_id']}")
    output.append(f"Duration: {trace['duration_ms']:.2f} ms")
    output.append(f"Start Time: {trace['start_time']}")
    output.append(f"End Time: {trace['end_time']}")
    output.append("")
    
    # Add spans in a hierarchical format
    spans_by_id = {span["span_id"]: span for span in trace["spans"]}
    root_spans = [span for span in trace["spans"] if not span["parent_id"]]
    
    for root_span in root_spans:
        _format_span(root_span, spans_by_id, output, indent=0)
    
    return "\n".join(output)

def _format_span(span: Dict[str, Any], spans_by_id: Dict[str, Dict[str, Any]], output: List[str], indent: int) -> None:
    """
    Format a span and its children recursively.
    
    Args:
        span: The span to format.
        spans_by_id: A dictionary mapping span IDs to spans.
        output: The output list to append to.
        indent: The current indentation level.
    """
    # Add span header
    output.append(f"{' ' * indent}|- {span['name']} ({span['duration_ms']:.2f} ms)")
    
    # Add span attributes
    for key, value in span["attributes"].items():
        output.append(f"{' ' * (indent + 3)}|- {key}: {value}")
    
    # Add child spans
    child_spans = [s for s in spans_by_id.values() if s["parent_id"] == span["span_id"]]
    for child_span in child_spans:
        _format_span(child_span, spans_by_id, output, indent + 3)
```

---

## Testing Tracing Implementation

To test our tracing implementation, we'll create a test file that verifies the trace processor captures and processes trace data correctly.

```python
# tests/test_trace_processor.py

import pytest
import asyncio
from app.agents.orchestration.trace_processor import OrchestrationTraceProcessor
from app.agents.orchestration.handoff_agent import create_handoff_agent
from agents.tracing import set_trace_processors

@pytest.mark.asyncio
async def test_trace_processor():
    """Test that the trace processor captures and processes trace data correctly."""
    # Create a trace processor
    trace_processor = OrchestrationTraceProcessor()
    
    # Set the trace processor
    set_trace_processors([trace_processor])
    
    # Create a handoff agent
    agent = create_handoff_agent()
    
    # Process a message
    message = "I have a question about my invoice"
    agent_type = await agent.determine_agent_type(message)
    
    # Mock the specialized agent's run method
    agent.specialized_agents[agent_type].run = asyncio.coroutine(
        lambda msg, **kwargs: f"Response from {agent_type} agent"
    )
    
    # Process with the specialized agent
    result = await agent.process_with_specialized_agent(message, agent_type)
    
    # Verify that traces were captured
    traces = trace_processor.get_all_traces()
    assert len(traces) > 0, "No traces were captured"
    
    # Verify that spans were captured
    for trace in traces:
        assert len(trace["spans"]) > 0, "No spans were captured in trace"
        
        # Verify that the determine_agent_type span was captured
        determine_spans = [span for span in trace["spans"] if span["name"] == "determine_agent_type"]
        assert len(determine_spans) > 0, "determine_agent_type span was not captured"
        
        # Verify that the process_with_specialized_agent span was captured
        process_spans = [span for span in trace["spans"] if span["name"] == "process_with_specialized_agent"]
        assert len(process_spans) > 0, "process_with_specialized_agent span was not captured"
```

---

## Relevant SDK Files

- **`tracing.py`**: Contains classes and functions for implementing tracing within the OpenAI Agents SDK.
- **`agent.py`**: Defines the `Agent` class, which can be instrumented for tracing.
- **`guardrail.py`**: Includes guardrail implementations that can be traced for input and output validations.
- **`handoffs.py`**: Manages handoff mechanisms between agents, with tracing to monitor delegation processes.

---

## Next Steps

With comprehensive tracing implemented, proceed to **Phase 5: Advanced Orchestration (Routing and Filtering)**. This phase will focus on developing intelligent routing logic and filtering mechanisms to manage tasks across multiple specialized agents effectively.

---

**Note:** Ensure that all tracing configurations comply with your organization's data privacy and security policies. Trace data may contain sensitive information, so implement appropriate access controls and data retention policies.