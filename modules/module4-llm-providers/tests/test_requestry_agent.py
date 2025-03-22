"""
Tests for the Requestry agent.
"""

import os
import pytest
import logging
from unittest.mock import patch, MagicMock
from app.agents.llm_providers.requestry_agent import RequestryAgent

logger = logging.getLogger(__name__)


def test_basic_logging():
    """Test that basic logging is working."""
    logger.info("Logging test for Requestry agent: success")
    assert True


@pytest.mark.asyncio
async def test_requestry_agent_init_missing_api_key():
    """Test that RequestryAgent raises an error when API key is missing."""
    # Save original API key if it exists
    original_api_key = os.environ.get("REQUESTRY_API_KEY")
    
    # Remove API key from environment
    if "REQUESTRY_API_KEY" in os.environ:
        del os.environ["REQUESTRY_API_KEY"]
    
    # Test that agent initialization raises ValueError
    with pytest.raises(ValueError, match="REQUESTRY_API_KEY is not set"):
        RequestryAgent()
    
    # Restore original API key if it existed
    if original_api_key:
        os.environ["REQUESTRY_API_KEY"] = original_api_key


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_requestry_agent_process_prompt_success(mock_openai):
    """Test that RequestryAgent processes prompts successfully."""
    # Set up mock API key
    os.environ["REQUESTRY_API_KEY"] = "test-requestry-key"
    
    # Set up mock response
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_usage = MagicMock()
    
    # Configure the mock response
    mock_message.content = "This is a test response from Requestry."
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    
    # Set up usage information
    mock_usage.prompt_tokens = 10
    mock_usage.completion_tokens = 20
    mock_usage.total_tokens = 30
    mock_completion.usage = mock_usage
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt
    agent = RequestryAgent()
    prompt_data = {
        "prompt": "Test prompt",
        "system_message": "You are a test assistant.",
        "max_tokens": 50,
        "temperature": 0.5,
        "model": "cline/o3-mini"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "success"
    assert result["message"] == "This is a test response from Requestry."
    assert result["model"] == "cline/o3-mini"
    assert "usage" in result
    assert result["usage"]["prompt_tokens"] == 10
    assert result["usage"]["completion_tokens"] == 20
    assert result["usage"]["total_tokens"] == 30
    
    # Verify the mock was called with correct parameters
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["model"] == "cline/o3-mini"
    assert call_args["max_tokens"] == 50
    assert call_args["temperature"] == 0.5
    assert len(call_args["messages"]) == 2
    assert call_args["messages"][0]["role"] == "system"
    assert call_args["messages"][1]["role"] == "user"
    assert call_args["messages"][1]["content"] == "Test prompt"
    
    # Clean up
    if "REQUESTRY_API_KEY" in os.environ:
        del os.environ["REQUESTRY_API_KEY"]


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_requestry_agent_process_prompt_api_error(mock_openai):
    """Test that RequestryAgent handles API errors properly."""
    # Set up mock API key
    os.environ["REQUESTRY_API_KEY"] = "test-requestry-key"
    
    # Set up mock to raise an API error
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = openai.APIError("Test API error")
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt
    agent = RequestryAgent()
    prompt_data = {
        "prompt": "Test prompt",
        "model": "cline/o3-mini"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "error"
    assert "Requestry API error: Test API error" in result["message"]
    assert result["model"] == "cline/o3-mini"
    
    # Clean up
    if "REQUESTRY_API_KEY" in os.environ:
        del os.environ["REQUESTRY_API_KEY"]


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_requestry_agent_process_prompt_unexpected_error(mock_openai):
    """Test that RequestryAgent handles unexpected errors properly."""
    # Set up mock API key
    os.environ["REQUESTRY_API_KEY"] = "test-requestry-key"
    
    # Set up mock to raise an unexpected error
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Unexpected test error")
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt
    agent = RequestryAgent()
    prompt_data = {
        "prompt": "Test prompt",
        "model": "cline/o3-mini"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "error"
    assert "Unexpected error: Unexpected test error" in result["message"]
    assert result["model"] == "cline/o3-mini"
    
    # Clean up
    if "REQUESTRY_API_KEY" in os.environ:
        del os.environ["REQUESTRY_API_KEY"]


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_requestry_agent_default_values(mock_openai):
    """Test that RequestryAgent uses default values when not provided."""
    # Set up mock API key
    os.environ["REQUESTRY_API_KEY"] = "test-requestry-key"
    
    # Set up mock response
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    
    # Configure the mock response
    mock_message.content = "Default values response"
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    mock_completion.usage = None  # No usage info
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt with minimal data
    agent = RequestryAgent()
    prompt_data = {
        "prompt": "Test with defaults"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "success"
    assert result["model"] == agent.default_model
    
    # Verify the mock was called with default values
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["model"] == agent.default_model
    assert call_args["max_tokens"] == 100
    assert call_args["temperature"] == 0.7
    
    # Clean up
    if "REQUESTRY_API_KEY" in os.environ:
        del os.environ["REQUESTRY_API_KEY"]


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_requestry_agent_invalid_model(mock_openai):
    """Test that RequestryAgent handles invalid model names properly."""
    # Set up mock API key
    os.environ["REQUESTRY_API_KEY"] = "test-requestry-key"
    
    # Set up mock response
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    
    # Configure the mock response
    mock_message.content = "Response with default model"
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt with invalid model
    agent = RequestryAgent()
    prompt_data = {
        "prompt": "Test with invalid model",
        "model": "invalid-model-name"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "success"
    assert result["model"] == "invalid-model-name"  # Requestry agent doesn't validate models
    
    # Verify the mock was called with the provided model (even if invalid)
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["model"] == "invalid-model-name"
    
    # Clean up
    if "REQUESTRY_API_KEY" in os.environ:
        del os.environ["REQUESTRY_API_KEY"]