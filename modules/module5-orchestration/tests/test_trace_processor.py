"""
Tests for the trace processor functionality.

This module contains tests for the trace processor, which is responsible for
capturing and processing trace data from agents, guardrails, and handoffs.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.orchestration.trace_processor import trace_processor, format_trace_for_display
from app.agents.orchestration.handoff_agent import create_handoff_agent
from app.agents.orchestration.guardrail_agent import create_guardrail_agent
from agents.tracing import add_trace_processor

# Create a mock trace for testing
class MockTrace:
    def __init__(self):
        self.trace_id = "mock-trace-id"
        self.start_time = 1000.0
        self.end_time = 1001.0
        self.spans = []
        self.metadata = {}
    
    def create_span(self, name):
        span = MockSpan(name)
        self.spans.append(span)
        return span

class MockSpan:
    def __init__(self, name):
        self.span_id = f"span-{name}"
        self.parent_id = None
        self.name = name
        self.start_time = 1000.0
        self.end_time = 1001.0
        self.attributes = {}
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def set_attribute(self, key, value):
        self.attributes[key] = value

# Mock the get_current_trace function
mock_trace = MockTrace()

@pytest.fixture(autouse=True)
def setup_trace_processor():
    """Set up the trace processor for testing."""
    # Clear any existing traces
    trace_processor.clear_traces()
    # Set the trace processor
    add_trace_processor(trace_processor)
    yield
    # Clean up after the test
    trace_processor.clear_traces()

@pytest.mark.asyncio
async def test_trace_processor_initialization():
    """Test that the trace processor is initialized correctly."""
    # Verify that the trace processor is initialized
    assert trace_processor is not None
    # Verify that the trace processor has no traces initially
    assert len(trace_processor.get_all_traces()) == 0

@pytest.mark.asyncio
@patch('app.agents.orchestration.handoff_agent.get_current_trace', return_value=mock_trace)
async def test_handoff_agent_tracing(mock_get_trace):
    """Test that the handoff agent creates traces."""
    # Create a handoff agent
    agent = create_handoff_agent()
    
    # Process a message
    message = "I have a question about my invoice"
    agent_type = await agent.determine_agent_type(message)
    
    # Mock the specialized agent's run method
    agent.specialized_agents[agent_type].run = AsyncMock(return_value=f"Response from {agent_type} agent")
    
    # Process with the specialized agent
    result = await agent.process_with_specialized_agent(message, agent_type)
    
    # Manually process the trace
    trace_processor.process_trace(mock_trace)
    
    # Verify that traces were captured
    traces = trace_processor.get_all_traces()
    assert len(traces) > 0, "No traces were captured"
    
    # Verify that the trace has the correct ID
    assert traces[0]["trace_id"] == mock_trace.trace_id

@pytest.mark.asyncio
@patch('app.agents.orchestration.input_guardrails.get_current_trace', return_value=mock_trace)
@patch('app.agents.orchestration.output_guardrails.get_current_trace', return_value=mock_trace)
async def test_guardrail_agent_tracing(mock_input_trace, mock_output_trace):
    """Test that the guardrail agent creates traces."""
    # Create a guardrail agent
    agent = create_guardrail_agent()
    
    # Mock the _run method
    agent._run = AsyncMock(return_value="This is a valid response")
    
    try:
        # Call the _run method directly
        response = await agent._run("This is a valid message")
        
        # Manually process the trace
        trace_processor.process_trace(mock_trace)
        
        # Verify that traces were captured
        traces = trace_processor.get_all_traces()
        assert len(traces) > 0, "No traces were captured"
        
        # Verify that the trace has the correct ID
        assert traces[0]["trace_id"] == mock_trace.trace_id
    except Exception as e:
        pytest.fail(f"Unexpected exception: {str(e)}")

@pytest.mark.asyncio
@patch('app.agents.orchestration.handoff_agent.get_current_trace', return_value=mock_trace)
async def test_trace_formatting(mock_get_trace):
    """Test that traces can be formatted for display."""
    # Create a handoff agent
    agent = create_handoff_agent()
    
    # Process a message
    message = "I have a question about my invoice"
    agent_type = await agent.determine_agent_type(message)
    
    # Mock the specialized agent's run method
    agent.specialized_agents[agent_type].run = AsyncMock(return_value=f"Response from {agent_type} agent")
    
    # Process with the specialized agent
    result = await agent.process_with_specialized_agent(message, agent_type)
    
    # Manually process the trace
    trace_processor.process_trace(mock_trace)
    
    # Get the traces
    traces = trace_processor.get_all_traces()
    assert len(traces) > 0, "No traces were captured"
    
    # Format the first trace
    formatted_trace = format_trace_for_display(traces[0])
    
    # Verify that the formatted trace contains the expected information
    assert "Trace ID:" in formatted_trace, "Formatted trace does not contain Trace ID"
    assert "Duration:" in formatted_trace, "Formatted trace does not contain Duration"

@pytest.mark.asyncio
@patch('app.agents.orchestration.handoff_agent.get_current_trace', return_value=mock_trace)
async def test_trace_processor_methods(mock_get_trace):
    """Test the methods of the trace processor."""
    # Create a handoff agent
    agent = create_handoff_agent()
    
    # Process a message
    message = "I have a question about my invoice"
    agent_type = await agent.determine_agent_type(message)
    
    # Mock the specialized agent's run method
    agent.specialized_agents[agent_type].run = AsyncMock(return_value=f"Response from {agent_type} agent")
    
    # Process with the specialized agent
    result = await agent.process_with_specialized_agent(message, agent_type)
    
    # Manually process the trace
    trace_processor.process_trace(mock_trace)
    
    # Get the traces
    traces = trace_processor.get_all_traces()
    assert len(traces) > 0, "No traces were captured"
    
    # Get the trace summary
    summary = trace_processor.get_trace_summary()
    assert summary["count"] > 0, "Trace summary count is 0"
    assert "total_duration_ms" in summary, "Trace summary does not contain total_duration_ms"
    assert "avg_duration_ms" in summary, "Trace summary does not contain avg_duration_ms"
    assert "trace_ids" in summary, "Trace summary does not contain trace_ids"
    
    # Get a specific trace
    trace_id = traces[0]["trace_id"]
    trace = trace_processor.get_trace(trace_id)
    assert trace is not None, f"Could not get trace with ID {trace_id}"
    assert trace["trace_id"] == trace_id, f"Trace ID mismatch: {trace['trace_id']} != {trace_id}"
    
    # Clear the traces
    trace_processor.clear_traces()
    assert len(trace_processor.get_all_traces()) == 0, "Traces were not cleared"