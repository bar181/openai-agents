"""
Tests for the OpenAI agent.
"""

import os
import pytest
from unittest.mock import MagicMock, patch
from app.agents.llm_providers.openai_agent import OpenAIAgent


@pytest.mark.asyncio
async def test_openai_agent_init():
    """Test that OpenAI agent can be initialized."""
    # Set a test API key
    os.environ["OPENAI_API_KEY"] = "test-key"
    
    agent = OpenAIAgent()
    assert agent is not None
    assert agent.provider_name == "openai"


@pytest.mark.asyncio
async def test_openai_agent_init_missing_api_key():
    """Test that OpenAI agent raises error when API key is missing."""
    # Remove the API key if it exists
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    with pytest.raises(ValueError):
        OpenAIAgent()


@pytest.mark.asyncio
async def test_openai_agent_process_prompt_success():
    """Test that OpenAI agent can process a prompt successfully."""
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
    mock_message.content = "This is a test response"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_usage.prompt_tokens = 5
    mock_usage.completion_tokens = 10
    mock_usage.total_tokens = 15
    mock_response.usage = mock_usage
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_response
    
    with patch('openai.OpenAI', return_value=mock_client):
        prompt_data = {
            "prompt": "Test prompt",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 100
        }
        result = agent.process_prompt(prompt_data)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["response"] == "This is a test response"
        assert result["usage"]["prompt_tokens"] == 5
        assert result["usage"]["completion_tokens"] == 10
        assert result["usage"]["total_tokens"] == 15
        
        # Verify the mock was called with the correct arguments
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == "gpt-4"
        assert call_args["temperature"] == 0.7
        assert call_args["max_tokens"] == 100
        assert len(call_args["messages"]) == 1
        assert call_args["messages"][0]["role"] == "user"
        assert call_args["messages"][0]["content"] == "Test prompt"


@pytest.mark.asyncio
async def test_openai_agent_process_prompt_api_error():
    """Test that OpenAI agent handles API errors correctly."""
    # Set a test API key
    os.environ["OPENAI_API_KEY"] = "test-key"
    
    agent = OpenAIAgent()
    
    # Create a mock client that raises an exception
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    
    with patch('openai.OpenAI', return_value=mock_client):
        prompt_data = {
            "prompt": "Test prompt",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 100
        }
        result = agent.process_prompt(prompt_data)
        
        # Verify the result indicates an error
        assert result["status"] == "error"
        assert "API Error" in result["error"]


@pytest.mark.asyncio
async def test_openai_agent_process_prompt_with_system_message():
    """Test that OpenAI agent can process a prompt with a system message."""
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
    mock_message.content = "Response with system message"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_usage.prompt_tokens = 10
    mock_usage.completion_tokens = 15
    mock_usage.total_tokens = 25
    mock_response.usage = mock_usage
    
    # Configure the mock client
    mock_client.chat.completions.create.return_value = mock_response
    
    with patch('openai.OpenAI', return_value=mock_client):
        prompt_data = {
            "prompt": "Test prompt",
            "system_message": "You are a helpful assistant",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 100
        }
        result = agent.process_prompt(prompt_data)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["response"] == "Response with system message"
        
        # Verify the mock was called with the correct arguments
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert len(call_args["messages"]) == 2
        assert call_args["messages"][0]["role"] == "system"
        assert call_args["messages"][0]["content"] == "You are a helpful assistant"
        assert call_args["messages"][1]["role"] == "user"
        assert call_args["messages"][1]["content"] == "Test prompt"


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
        assert call_args["model"] == "gpt-4o-mini"  # Updated to expect gpt-4o-mini
        assert call_args["temperature"] == 0.7
        assert call_args["max_tokens"] == 100  # Updated to match the actual default value