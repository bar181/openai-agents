"""
Tests for the OpenAI agent.

These tests verify the functionality of the OpenAI agent implementation.
"""

import os
import pytest
import openai
import logging
from unittest.mock import patch, MagicMock
from app.agents.llm_providers.openai_agent import OpenAIAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_basic_logging():
    """Test that basic logging is working."""
    logger = logging.getLogger(__name__)
    logger.info("Logging test for OpenAI agent: success")
    assert True


@pytest.mark.asyncio
async def test_openai_agent_valid_prompt():
    """Test OpenAI agent with a valid prompt and mocked API response."""
    # Set a test API key in the environment
    os.environ["OPENAI_API_KEY"] = "test-key"
    
    agent = OpenAIAgent()
    
    # Create a mock for the OpenAI client
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_usage = MagicMock()
    
    # Configure the mock response
    mock_message.content = "Test response from mock model."
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_usage.prompt_tokens = 10
    mock_usage.completion_tokens = 20
    mock_usage.total_tokens = 30
    mock_response.usage = mock_usage
    
    # Configure the mock client to return our mock response
    mock_client.chat.completions.create.return_value = mock_response
    
    # Patch the OpenAI client creation
    with patch('openai.OpenAI', return_value=mock_client):
        # Test data
        prompt_data = {
            "prompt": "Hello from tests.",
            "model": "gpt-o3-mini",
            "max_tokens": 50,
            "temperature": 0.5
        }
        
        # Call the agent
        result = agent.process_prompt(prompt_data)
        
        # Verify the result
        assert result["status"] == "success"
        assert "Test response from mock model." in result["message"]
        assert result["model"] == "gpt-o3-mini"
        assert result["usage"]["prompt_tokens"] == 10
        assert result["usage"]["completion_tokens"] == 20
        assert result["usage"]["total_tokens"] == 30
        
        # Verify the mock was called with the correct arguments
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == "gpt-o3-mini"
        assert call_args["max_tokens"] == 50
        assert call_args["temperature"] == 0.5
        assert call_args["messages"][0]["content"] == "Hello from tests."


@pytest.mark.asyncio
async def test_openai_agent_missing_api_key():
    """Test OpenAI agent behavior when API key is missing."""
    # Clear the API key from the environment
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    agent = OpenAIAgent()
    prompt_data = {"prompt": "No API key here", "model": "gpt-o3-mini"}
    
    # Call the agent
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "error"
    assert "missing" in result["message"].lower()
    assert "unknown" in result["model"].lower()


@pytest.mark.asyncio
async def test_openai_agent_authentication_error():
    """Test OpenAI agent behavior when authentication fails."""
    # Set an invalid API key
    os.environ["OPENAI_API_KEY"] = "invalid-key"
    
    agent = OpenAIAgent()
    
    # Create a mock response for the error
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Invalid API key"
    
    # Create a mock client that raises an exception
    mock_client = MagicMock()
    # Use a generic Exception for simplicity in testing
    mock_client.chat.completions.create.side_effect = Exception("Authentication error: Invalid API key")
    
    with patch('openai.OpenAI', return_value=mock_client):
        prompt_data = {"prompt": "This will fail", "model": "gpt-o3-mini"}
        result = agent.process_prompt(prompt_data)
        
        # Verify the result
        assert result["status"] == "error"
        assert "authentication" in result["message"].lower()
        assert result["model"] == "gpt-o3-mini"


@pytest.mark.asyncio
async def test_openai_agent_rate_limit_error():
    """Test OpenAI agent behavior when rate limit is exceeded."""
    # Set a test API key
    os.environ["OPENAI_API_KEY"] = "test-key"
    
    agent = OpenAIAgent()
    
    # Create a mock response for the error
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.text = "Rate limit exceeded"
    
    # Create a mock client that raises an exception
    mock_client = MagicMock()
    # Use a generic Exception for simplicity in testing
    mock_client.chat.completions.create.side_effect = Exception("Rate limit exceeded. Please try again later.")
    
    with patch('openai.OpenAI', return_value=mock_client):
        prompt_data = {"prompt": "This will hit rate limit", "model": "gpt-o3-mini"}
        result = agent.process_prompt(prompt_data)
        
        # Verify the result
        assert result["status"] == "error"
        assert "rate limit" in result["message"].lower()
        assert result["model"] == "gpt-o3-mini"


@pytest.mark.asyncio
async def test_openai_agent_default_values():
    """Test that OpenAI agent uses default values when not provided."""
    # Set a test API key
    os.environ["OPENAI_API_KEY"] = "test-key"
    
    agent = OpenAIAgent()
    
    # Create mock objects
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_usage = MagicMock()
    
    # Configure the mock response
    mock_message.content = "Default response"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_usage.prompt_tokens = 5
    mock_usage.completion_tokens = 10
    mock_usage.total_tokens = 15
    mock_response.usage = mock_usage
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_response
    
    with patch('openai.OpenAI', return_value=mock_client):
        # Only provide the prompt, let other values use defaults
        prompt_data = {"prompt": "Use defaults"}
        result = agent.process_prompt(prompt_data)
        
        # Verify the mock was called with default values
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == "gpt-3.5-turbo"  # Default model
        assert call_args["max_tokens"] == 100  # Default max_tokens
        assert call_args["temperature"] == 0.7  # Default temperature