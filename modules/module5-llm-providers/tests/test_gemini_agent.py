"""
Tests for the Gemini agent.
"""

import os
import pytest
import logging
from unittest.mock import patch, MagicMock
from app.agents.llm_providers.gemini_agent import GeminiAgent

logger = logging.getLogger(__name__)


def test_basic_logging():
    """Test that basic logging is working."""
    logger.info("Logging test for Gemini agent: success")
    assert True


@pytest.mark.asyncio
async def test_gemini_agent_init_missing_api_key():
    """Test that GeminiAgent raises an error when API key is missing."""
    original_api_key = os.environ.get("GEMINI_API_KEY")
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]

    # Patch load_dotenv to prevent loading the .env file
    with patch("app.agents.llm_providers.gemini_agent.load_dotenv", lambda: None):
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is not set"):
            GeminiAgent()

    if original_api_key:
        os.environ["GEMINI_API_KEY"] = original_api_key


@pytest.mark.asyncio
@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
async def test_gemini_agent_process_prompt_success(mock_generative_model, mock_configure):
    """Test that GeminiAgent processes prompts successfully."""
    # Set up mock API key
    os.environ["GEMINI_API_KEY"] = "test-gemini-key"
    
    # Set up mock response
    mock_model_instance = MagicMock()
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a test response from Gemini."
    
    mock_chat.send_message.return_value = mock_response
    mock_model_instance.start_chat.return_value = mock_chat
    mock_generative_model.return_value = mock_model_instance
    
    # Create agent and process prompt
    agent = GeminiAgent()
    prompt_data = {
        "prompt": "Test prompt",
        "system_message": "You are a test assistant.",
        "max_tokens": 50,
        "temperature": 0.5,
        "model": "gemini-2.0-pro-exp-02-05"  # Updated to match the supported model
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "success"
    assert result["message"] == "This is a test response from Gemini."
    assert result["model"] == "gemini-2.0-pro-exp-02-05"  # Updated to match the supported model
    assert "usage" in result
    assert result["usage"]["note"] == "Token counts are estimates as Gemini API doesn't provide exact usage"
    
    # Verify the mock was called with correct parameters
    mock_generative_model.assert_called_once()
    mock_model_instance.start_chat.assert_called_once()
    
    # Clean up
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]


@pytest.mark.asyncio
@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
async def test_gemini_agent_process_prompt_error(mock_generative_model, mock_configure):
    """Test that GeminiAgent handles errors properly."""
    # Set up mock API key
    os.environ["GEMINI_API_KEY"] = "test-gemini-key"
    
    # Set up mock to raise an exception
    mock_model_instance = MagicMock()
    mock_model_instance.start_chat.side_effect = Exception("Test error")
    # Also make generate_content raise an exception to ensure error status
    mock_model_instance.generate_content.side_effect = Exception("Test error")
    mock_generative_model.return_value = mock_model_instance
    
    # Create agent and process prompt
    agent = GeminiAgent()
    prompt_data = {
        "prompt": "Test prompt",
        "model": "gemini-2.0-pro-exp-02-05"  # Updated to match the supported model
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "error"
    assert "Error processing prompt: Test error" in result["message"]
    assert result["model"] == "gemini-2.0-pro-exp-02-05"  # Updated to match the supported model
    
    # Clean up
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]


@pytest.mark.asyncio
@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
async def test_gemini_agent_default_values(mock_generative_model, mock_configure):
    """Test that GeminiAgent uses default values when not provided."""
    # Set up mock API key
    os.environ["GEMINI_API_KEY"] = "test-gemini-key"
    
    # Set up mock response
    mock_model_instance = MagicMock()
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Default values response"
    
    mock_chat.send_message.return_value = mock_response
    mock_model_instance.start_chat.return_value = mock_chat
    mock_generative_model.return_value = mock_model_instance
    
    # Create agent and process prompt with minimal data
    agent = GeminiAgent()
    prompt_data = {
        "prompt": "Test with defaults"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "success"
    assert result["model"] == agent.default_model
    
    # Verify the mock was called with default values
    mock_generative_model.assert_called_once()
    args, kwargs = mock_generative_model.call_args
    assert kwargs["model_name"] == agent.default_model
    assert kwargs["generation_config"]["max_output_tokens"] == 100
    assert kwargs["generation_config"]["temperature"] == 0.7
    
    # Clean up
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]


@pytest.mark.asyncio
@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
async def test_gemini_agent_invalid_model(mock_generative_model, mock_configure):
    """Test that GeminiAgent handles invalid model names properly."""
    # Set up mock API key
    os.environ["GEMINI_API_KEY"] = "test-gemini-key"
    
    # Set up mock response
    mock_model_instance = MagicMock()
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Response with default model"
    
    mock_chat.send_message.return_value = mock_response
    mock_model_instance.start_chat.return_value = mock_chat
    mock_generative_model.return_value = mock_model_instance
    
    # Create agent and process prompt with invalid model
    agent = GeminiAgent()
    prompt_data = {
        "prompt": "Test with invalid model",
        "model": "invalid-model-name"
    }
    
    result = agent.process_prompt(prompt_data)
    
    # Verify the result
    assert result["status"] == "success"
    assert result["model"] == agent.default_model  # Should fall back to default
    
    # Verify the mock was called with default model
    mock_generative_model.assert_called_once()
    args, kwargs = mock_generative_model.call_args
    assert kwargs["model_name"] == agent.default_model
    
    # Clean up
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]


@pytest.mark.asyncio
@patch('google.generativeai.configure')
@patch('google.generativeai.GenerativeModel')
async def test_gemini_agent_test_connection(mock_generative_model, mock_configure):
    """Test the test_connection method of GeminiAgent."""
    # Set up mock API key
    os.environ["GEMINI_API_KEY"] = "test-gemini-key"
    
    # Set up mock response
    mock_model_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Connection test response"
    
    mock_model_instance.generate_content.return_value = mock_response
    mock_generative_model.return_value = mock_model_instance
    
    # Create agent and test connection
    agent = GeminiAgent()
    result = agent.test_connection("Test connection")
    
    # Verify the result
    assert result["status"] == "success"
    assert result["message"] == "Connection test response"
    assert result["model"] == agent.default_model
    
    # Verify the mock was called correctly
    mock_generative_model.assert_called_once_with(agent.default_model)
    mock_model_instance.generate_content.assert_called_once_with("Test connection")
    
    # Clean up
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]