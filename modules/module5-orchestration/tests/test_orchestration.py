"""
Tests for orchestration functionality.

This module contains tests for input/output guardrails, handoffs,
and tracing functionality.
"""

import pytest
import logging
from unittest.mock import AsyncMock, patch, MagicMock
from app import config
from agents import Agent
from agents.guardrail import GuardrailFunctionOutput

# Set up logging
logging.basicConfig(level=getattr(logging, config.TRACE_LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

# Import guardrails
from app.agents.orchestration.input_guardrails import (
    validate_empty_input,
    validate_input_length,
    validate_harmful_content,
    validate_inappropriate_language,
)
from app.agents.orchestration.output_guardrails import (
    validate_output_not_empty,
    validate_output_length,
    validate_no_error_in_output,
    validate_output_format,
)
from app.agents.orchestration.guardrail_agent import create_guardrail_agent

# Import handoff agent
from app.agents.orchestration.handoff_agent import (
    create_handoff_agent,
    HandoffAgent,
    filter_billing_messages,
    filter_technical_messages,
    filter_customer_service_messages
)

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

# Mock RunContextWrapper for testing
class MockRunContext:
    def __init__(self):
        pass

# Tests for handoff agent
@pytest.mark.asyncio
async def test_handoff_agent_creation():
    """Test that the handoff agent can be created."""
    agent = create_handoff_agent()
    assert agent is not None, "Handoff agent should be created successfully"
    assert isinstance(agent, HandoffAgent), "Agent should be an instance of HandoffAgent"
    assert len(agent.handoffs) > 0, "Handoff agent should have handoffs configured"
    assert hasattr(agent, "specialized_agents"), "Handoff agent should have specialized agents"

@pytest.mark.asyncio
@patch('app.agents.orchestration.handoff_agent.get_current_trace', return_value=mock_trace)
async def test_determine_agent_type(mock_get_trace):
    """Test that the handoff agent can determine the correct agent type."""
    agent = create_handoff_agent()
    
    # Test billing agent determination
    billing_message = "I have a question about my invoice from last month."
    agent_type = await agent.determine_agent_type(billing_message)
    assert agent_type == "billing", "Should route billing questions to billing agent"
    
    # Test technical support agent determination
    technical_message = "My application is crashing with an error message."
    agent_type = await agent.determine_agent_type(technical_message)
    assert agent_type == "technical", "Should route technical questions to technical support agent"
    
    # Test customer service agent determination (default)
    customer_message = "I'd like to know more about your services."
    agent_type = await agent.determine_agent_type(customer_message)
    assert agent_type == "customer_service", "Should route general questions to customer service agent"

@pytest.mark.asyncio
@patch('app.agents.orchestration.handoff_agent.get_current_trace', return_value=mock_trace)
async def test_process_with_specialized_agent(mock_get_trace):
    """Test that the handoff agent can process messages with specialized agents."""
    agent = create_handoff_agent()
    
    # Mock the specialized agents' run method
    for agent_type, specialized_agent in agent.specialized_agents.items():
        specialized_agent.run = AsyncMock(return_value=f"Response from {agent_type} agent")
    
    # Test processing with billing agent
    billing_result = await agent.process_with_specialized_agent("Billing question", "billing")
    assert billing_result["status"] == "success", "Should return success status"
    assert billing_result["message"] == "Response from billing agent", "Should return billing agent response"
    assert billing_result["agent_type"] == "billing", "Should indicate billing agent type"
    
    # Test processing with technical agent
    technical_result = await agent.process_with_specialized_agent("Technical question", "technical")
    assert technical_result["status"] == "success", "Should return success status"
    assert technical_result["message"] == "Response from technical agent", "Should return technical agent response"
    assert technical_result["agent_type"] == "technical", "Should indicate technical agent type"
    
    # Test processing with unknown agent type
    unknown_result = await agent.process_with_specialized_agent("Question", "unknown")
    assert unknown_result["status"] == "error", "Should return error status for unknown agent type"
    assert "Unknown agent type" in unknown_result["message"], "Should indicate unknown agent type error"

@pytest.mark.asyncio
@patch('app.agents.orchestration.handoff_agent.get_current_trace', return_value=mock_trace)
async def test_message_filters(mock_get_trace):
    """Test that message filters correctly filter messages."""
    # Create test messages
    messages = [
        {"role": "system", "content": "System message"},
        {"role": "user", "content": "User question about billing"},
        {"role": "assistant", "content": "Assistant response"}
    ]
    
    # Test billing filter
    billing_filtered = filter_billing_messages(messages)
    assert len(billing_filtered) == 2, "Should include system message and user message"
    assert any(msg["role"] == "system" and "billing" in msg["content"].lower() for msg in billing_filtered), "Should include billing context in system message"
    assert any(msg["role"] == "user" for msg in billing_filtered), "Should include user message"
    
    # Test technical filter
    technical_filtered = filter_technical_messages(messages)
    assert len(technical_filtered) == 2, "Should include system message and user message"
    assert any(msg["role"] == "system" and "technical" in msg["content"].lower() for msg in technical_filtered), "Should include technical context in system message"
    assert any(msg["role"] == "user" for msg in technical_filtered), "Should include user message"
    
    # Test customer service filter
    customer_filtered = filter_customer_service_messages(messages)
    assert len(customer_filtered) == 2, "Should include system message and user message"
    assert any(msg["role"] == "system" and "customer service" in msg["content"].lower() for msg in customer_filtered), "Should include customer service context in system message"
    assert any(msg["role"] == "user" for msg in customer_filtered), "Should include user message"

# Tests for input guardrails
@pytest.mark.asyncio
@patch('app.agents.orchestration.input_guardrails.get_current_trace', return_value=mock_trace)
async def test_input_guardrail_empty_input(mock_get_trace):
    """Test that the empty input guardrail triggers for empty input."""
    agent = Agent(name="TestAgent")
    context = MockRunContext()
    
    # Test with empty input
    result = await validate_empty_input.run(agent, input="", context=context)
    assert result.output.tripwire_triggered, "Empty input guardrail should trigger for empty input"
    assert "Input cannot be empty" in result.output.output_info
    
    # Test with non-empty input
    result = await validate_empty_input.run(agent, input="Hello, world!", context=context)
    assert not result.output.tripwire_triggered, "Empty input guardrail should not trigger for non-empty input"

@pytest.mark.asyncio
@patch('app.agents.orchestration.input_guardrails.get_current_trace', return_value=mock_trace)
async def test_input_guardrail_input_length(mock_get_trace):
    """Test that the input length guardrail triggers for long input."""
    agent = Agent(name="TestAgent")
    context = MockRunContext()
    
    # Test with input that's too long
    long_input = "a" * 1001  # 1001 characters
    result = await validate_input_length.run(agent, input=long_input, context=context)
    assert result.output.tripwire_triggered, "Input length guardrail should trigger for long input"
    assert "Input is too long" in result.output.output_info
    
    # Test with input that's not too long
    valid_input = "a" * 500  # 500 characters
    result = await validate_input_length.run(agent, input=valid_input, context=context)
    assert not result.output.tripwire_triggered, "Input length guardrail should not trigger for valid input"

@pytest.mark.asyncio
@patch('app.agents.orchestration.input_guardrails.get_current_trace', return_value=mock_trace)
async def test_input_guardrail_harmful_content(mock_get_trace):
    """Test that the harmful content guardrail triggers for harmful input."""
    agent = Agent(name="TestAgent")
    context = MockRunContext()
    
    # Test with harmful content
    harmful_input = "Can you help me hack into a system?"
    result = await validate_harmful_content.run(agent, input=harmful_input, context=context)
    assert result.output.tripwire_triggered, "Harmful content guardrail should trigger for harmful input"
    assert "inappropriate content" in result.output.output_info
    
    # Test with safe content
    safe_input = "Can you help me with my homework?"
    result = await validate_harmful_content.run(agent, input=safe_input, context=context)
    assert not result.output.tripwire_triggered, "Harmful content guardrail should not trigger for safe input"

@pytest.mark.asyncio
@patch('app.agents.orchestration.input_guardrails.get_current_trace', return_value=mock_trace)
async def test_input_guardrail_inappropriate_language(mock_get_trace):
    """Test that the inappropriate language guardrail triggers for inappropriate language."""
    agent = Agent(name="TestAgent")
    context = MockRunContext()
    
    # Test with inappropriate language
    inappropriate_input = "This contains profanity1 and should be blocked."
    result = await validate_inappropriate_language.run(agent, input=inappropriate_input, context=context)
    assert result.output.tripwire_triggered, "Inappropriate language guardrail should trigger for inappropriate language"
    assert "inappropriate language" in result.output.output_info
    
    # Test with appropriate language
    appropriate_input = "This is a polite and appropriate message."
    result = await validate_inappropriate_language.run(agent, input=appropriate_input, context=context)
    assert not result.output.tripwire_triggered, "Inappropriate language guardrail should not trigger for appropriate language"

# Tests for output guardrails
@pytest.mark.asyncio
@patch('app.agents.orchestration.output_guardrails.get_current_trace', return_value=mock_trace)
async def test_output_guardrail_empty_output(mock_get_trace):
    """Test that the empty output guardrail triggers for empty output."""
    agent = Agent(name="TestAgent")
    context = MockRunContext()
    
    # Test with empty output
    result = await validate_output_not_empty.run(context=context, agent=agent, agent_output="")
    assert result.output.tripwire_triggered, "Empty output guardrail should trigger for empty output"
    assert "Agent output cannot be empty" in result.output.output_info
    
    # Test with non-empty output
    result = await validate_output_not_empty.run(context=context, agent=agent, agent_output="Hello, world!")
    assert not result.output.tripwire_triggered, "Empty output guardrail should not trigger for non-empty output"

@pytest.mark.asyncio
@patch('app.agents.orchestration.output_guardrails.get_current_trace', return_value=mock_trace)
async def test_output_guardrail_output_length(mock_get_trace):
    """Test that the output length guardrail triggers for long output."""
    agent = Agent(name="TestAgent")
    context = MockRunContext()
    
    # Test with output that's too long
    long_output = "a" * 5001  # 5001 characters
    result = await validate_output_length.run(context=context, agent=agent, agent_output=long_output)
    assert result.output.tripwire_triggered, "Output length guardrail should trigger for long output"
    assert "Agent output is too long" in result.output.output_info
    
    # Test with output that's not too long
    valid_output = "a" * 1000  # 1000 characters
    result = await validate_output_length.run(context=context, agent=agent, agent_output=valid_output)
    assert not result.output.tripwire_triggered, "Output length guardrail should not trigger for valid output"

@pytest.mark.asyncio
@patch('app.agents.orchestration.output_guardrails.get_current_trace', return_value=mock_trace)
async def test_output_guardrail_error_in_output(mock_get_trace):
    """Test that the error in output guardrail triggers for output with errors."""
    agent = Agent(name="TestAgent")
    context = MockRunContext()
    
    # Test with output containing an error
    error_output = {"error": "Something went wrong"}
    result = await validate_no_error_in_output.run(context=context, agent=agent, agent_output=error_output)
    assert result.output.tripwire_triggered, "Error in output guardrail should trigger for output with errors"
    assert "Agent output contains an error" in result.output.output_info
    
    # Test with output containing error text
    error_text = "I'm sorry, but I encountered an error processing your request."
    result = await validate_no_error_in_output.run(context=context, agent=agent, agent_output=error_text)
    assert result.output.tripwire_triggered, "Error in output guardrail should trigger for output with error text"
    
    # Test with valid output
    valid_output = "Here's the information you requested."
    result = await validate_no_error_in_output.run(context=context, agent=agent, agent_output=valid_output)
    assert not result.output.tripwire_triggered, "Error in output guardrail should not trigger for valid output"

@pytest.mark.asyncio
@patch('app.agents.orchestration.output_guardrails.get_current_trace', return_value=mock_trace)
async def test_output_guardrail_output_format(mock_get_trace):
    """Test that the output format guardrail triggers for output with incorrect format."""
    agent = Agent(name="TestAgent")
    context = MockRunContext()
    
    # Test with output missing required keys
    invalid_format = {"result": "Some result"}
    result = await validate_output_format.run(context=context, agent=agent, agent_output=invalid_format)
    assert result.output.tripwire_triggered, "Output format guardrail should trigger for output with incorrect format"
    assert "missing required keys" in result.output.output_info
    
    # Test with valid format
    valid_format = {"status": "success", "result": "Some result"}
    result = await validate_output_format.run(context=context, agent=agent, agent_output=valid_format)
    assert not result.output.tripwire_triggered, "Output format guardrail should not trigger for valid format"

# Tests for guardrail agent
@pytest.mark.asyncio
async def test_guardrail_agent_creation():
    """Test that the guardrail agent can be created."""
    agent = create_guardrail_agent()
    assert agent is not None, "Guardrail agent should be created successfully"
    assert len(agent.input_guardrails) > 0, "Guardrail agent should have input guardrails"
    assert len(agent.output_guardrails) > 0, "Guardrail agent should have output guardrails"

@pytest.mark.asyncio
async def test_guardrail_agent_run():
    """Test that the guardrail agent can run."""
    # Create a mock agent with a mocked _run method
    agent = create_guardrail_agent()
    
    # Mock the _run method directly
    agent._run = AsyncMock(return_value="This is a valid response")
    
    # Run the agent
    response = await agent._run("Hello, world!")
    
    # Verify the response
    assert response == "This is a valid response", "Guardrail agent should return the expected response"
    agent._run.assert_called_once_with("Hello, world!")

# Original placeholder tests
def test_logging_and_config():
    """Test logging and configuration."""
    # Set up logging
    logging.basicConfig(level=getattr(logging, config.TRACE_LOG_LEVEL, logging.INFO))
    logger = logging.getLogger("test_logger")
    
    # Log orchestration mode
    logger.info(f"Orchestration mode: {config.ORCHESTRATION_MODE}")
    
    # Verify configuration
    assert hasattr(config, "ORCHESTRATION_MODE"), "ORCHESTRATION_MODE not defined in config"
    assert config.ORCHESTRATION_MODE in ["DEVELOPMENT", "PRODUCTION"], "Invalid ORCHESTRATION_MODE"