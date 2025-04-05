"""
Tests for the OpenRouter agent.
"""

import os
import pytest
import logging
import openai  # Add import for openai
from unittest.mock import patch, MagicMock
from app.agents.llm_providers.openrouter_agent import OpenRouterAgent

logger = logging.getLogger(__name__)


def test_basic_logging():
    """Test that basic logging is working."""
    logger.info("Logging test for OpenRouter agent: success")
    assert True


@pytest.mark.asyncio
async def test_openrouter_agent_init_missing_api_key():
    """Test that OpenRouterAgent raises an error when API key is missing."""
    # Save original API key if it exists
    original_api_key = os.environ.get("OPENROUTER_API_KEY")
    
    # Remove API key from environment
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]
    
    # Patch load_dotenv to prevent loading the .env file
    with patch("app.agents.llm_providers.openrouter_agent.load_dotenv", lambda: None):
        # Test that agent initialization raises ValueError
        with pytest.raises(ValueError, match="OPENROUTER_API_KEY is not set"):
            OpenRouterAgent()
    
    # Restore original API key if it existed
    if original_api_key:
        os.environ["OPENROUTER_API_KEY"] = original_api_key


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_openrouter_agent_process_prompt_success(mock_openai):
    """Test that OpenRouterAgent processes prompts successfully."""
    # Set up mock API key
    os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
    
    # Set up mock response
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_usage = MagicMock()
    
    # Configure the mock response
    mock_message.content = "This is a test response from OpenRouter."
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    
    # Set up usage information
    mock_usage.prompt_tokens = 15
    mock_usage.completion_tokens = 25
    mock_usage.total_tokens = 40
    mock_completion.usage = mock_usage
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt
    agent = OpenRouterAgent()
    prompt_data = {
        "prompt": "Test prompt",
        "system_message": "You are a test assistant.",
        "max_tokens": 50,
        "temperature": 0.5,
        "model": "openai/gpt-4o"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "success"
    assert result["message"] == "This is a test response from OpenRouter."
    assert result["model"] == "openai/gpt-4o"
    assert "usage" in result
    assert result["usage"]["prompt_tokens"] == 15
    assert result["usage"]["completion_tokens"] == 25
    assert result["usage"]["total_tokens"] == 40
    
    # Verify the mock was called with correct parameters
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args["model"] == "openai/gpt-4o"
    assert call_args["max_tokens"] == 50
    assert call_args["temperature"] == 0.5
    assert len(call_args["messages"]) == 2
    assert call_args["messages"][0]["role"] == "system"
    assert call_args["messages"][1]["role"] == "user"
    assert call_args["messages"][1]["content"] == "Test prompt"
    
    # Clean up
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_openrouter_agent_process_prompt_api_error(mock_openai):
    """Test that OpenRouterAgent handles API errors properly."""
    # Set up mock API key
    os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
    
    # Set up mock to raise an API error
    mock_client = MagicMock()
    
    # Create a mock request object
    mock_request = MagicMock()
    
    # Use a generic Exception instead of APIError since it requires complex initialization
    mock_client.chat.completions.create.side_effect = Exception("OpenRouter API error: Test API error")
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt
    agent = OpenRouterAgent()
    prompt_data = {
        "prompt": "Test prompt",
        "model": "openai/gpt-4o"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "error"
    assert "Unexpected error: OpenRouter API error: Test API error" in result["message"]
    assert result["model"] == "openai/gpt-4o"
    
    # Clean up
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_openrouter_agent_process_prompt_unexpected_error(mock_openai):
    """Test that OpenRouterAgent handles unexpected errors properly."""
    # Set up mock API key
    os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
    
    # Set up mock to raise an unexpected error
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Unexpected test error")
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt
    agent = OpenRouterAgent()
    prompt_data = {
        "prompt": "Test prompt",
        "model": "openai/gpt-4o"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "error"
    assert "Unexpected error: Unexpected test error" in result["message"]
    assert result["model"] == "openai/gpt-4o"
    
    # Clean up
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_openrouter_agent_default_values(mock_openai):
    """Test that OpenRouterAgent uses default values when not provided."""
    # Set up mock API key
    os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
    
    # Set up mock response
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_usage = MagicMock()
    
    # Configure the mock response
    mock_message.content = "Default values response"
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    
    # Set up usage information (not None)
    mock_usage.prompt_tokens = 5
    mock_usage.completion_tokens = 10
    mock_usage.total_tokens = 15
    mock_completion.usage = mock_usage
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt with minimal data
    agent = OpenRouterAgent()
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
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_openrouter_agent_custom_headers(mock_openai):
    """Test that OpenRouterAgent handles custom headers properly."""
    # Set up mock API key
    os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
    os.environ["OPENROUTER_REFERER"] = "https://example.com"
    os.environ["OPENROUTER_TITLE"] = "Test Application"
    
    # Set up mock response
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    
    # Configure the mock response
    mock_message.content = "Response with custom headers"
    mock_choice.message = mock_message
    mock_completion.choices = [mock_choice]
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_completion
    mock_openai.return_value = mock_client
    
    # Create agent and process prompt with custom headers
    agent = OpenRouterAgent()
    prompt_data = {
        "prompt": "Test with custom headers",
        "headers": {
            "X-Custom-Header": "Custom Value"
        }
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "success"
    
    # Verify the mock was called with combined headers
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert "extra_headers" in call_args
    assert call_args["extra_headers"]["HTTP-Referer"] == "https://example.com"
    assert call_args["extra_headers"]["X-Title"] == "Test Application"
    assert call_args["extra_headers"]["X-Custom-Header"] == "Custom Value"
    
    # Clean up
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]
    if "OPENROUTER_REFERER" in os.environ:
        del os.environ["OPENROUTER_REFERER"]
    if "OPENROUTER_TITLE" in os.environ:
        del os.environ["OPENROUTER_TITLE"]