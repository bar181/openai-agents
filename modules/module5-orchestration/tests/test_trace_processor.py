"""
Tests for the trace processor functionality.

This module contains tests for the trace processor, which is responsible for
capturing and processing trace data from agents, guardrails, and handoffs.
"""

import pytest
import asyncio
from app.agents.orchestration.trace_processor import trace_processor, format_trace_for_display
from app.agents.orchestration.handoff_agent import create_handoff_agent
from app.agents.orchestration.guardrail_agent import create_guardrail_agent
from agents.tracing import add_trace_processor, get_current_trace

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
async def test_handoff_agent_tracing():
    """Test that the handoff agent creates traces."""
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

@pytest.mark.asyncio
async def test_guardrail_agent_tracing():
    """Test that the guardrail agent creates traces."""
    # Create a guardrail agent
    agent = create_guardrail_agent()
    
    # Run the agent with a valid message
    message = "This is a valid message"
    try:
        response = await agent.run(message)
        
        # Verify that traces were captured
        traces = trace_processor.get_all_traces()
        assert len(traces) > 0, "No traces were captured"
        
        # Verify that spans were captured
        for trace in traces:
            assert len(trace["spans"]) > 0, "No spans were captured in trace"
            
            # Verify that guardrail spans were captured
            guardrail_spans = [span for span in trace["spans"] if "validate_" in span["name"]]
            assert len(guardrail_spans) > 0, "No guardrail spans were captured"
    except Exception as e:
        pytest.fail(f"Unexpected exception: {str(e)}")

@pytest.mark.asyncio
async def test_trace_formatting():
    """Test that traces can be formatted for display."""
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
    
    # Get the traces
    traces = trace_processor.get_all_traces()
    assert len(traces) > 0, "No traces were captured"
    
    # Format the first trace
    formatted_trace = format_trace_for_display(traces[0])
    
    # Verify that the formatted trace contains the expected information
    assert "Trace ID:" in formatted_trace, "Formatted trace does not contain Trace ID"
    assert "Duration:" in formatted_trace, "Formatted trace does not contain Duration"
    assert "determine_agent_type" in formatted_trace, "Formatted trace does not contain determine_agent_type span"
    assert "process_with_specialized_agent" in formatted_trace, "Formatted trace does not contain process_with_specialized_agent span"

@pytest.mark.asyncio
async def test_trace_processor_methods():
    """Test the methods of the trace processor."""
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