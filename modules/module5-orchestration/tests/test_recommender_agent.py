"""
Tests for the Model Recommender agent.
"""

import pytest
import logging
from app.agents.llm_providers.recommender_agent import RecommenderAgent

logger = logging.getLogger(__name__)


def test_basic_logging():
    """Test that basic logging is working."""
    logger.info("Logging test for Recommender agent: success")
    assert True


@pytest.mark.asyncio
async def test_recommender_reasoning_short():
    """Test recommender for short reasoning task."""
    agent = RecommenderAgent()
    input_data = {
        "task_type": "reasoning",
        "prompt_length": 200
    }
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    assert result["recommended_provider"] == "openai"
    assert result["model"] == "gpt-4o"


@pytest.mark.asyncio
async def test_recommender_reasoning_long():
    """Test recommender for long reasoning task."""
    agent = RecommenderAgent()
    input_data = {
        "task_type": "reasoning",
        "prompt_length": 10000
    }
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    assert result["recommended_provider"] == "openrouter"
    assert result["model"] == "openai/gpt-4o"


@pytest.mark.asyncio
async def test_recommender_conversation():
    """Test recommender for conversation task."""
    agent = RecommenderAgent()
    input_data = {
        "task_type": "conversation",
        "prompt_length": 50
    }
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    assert result["recommended_provider"] == "openai"
    assert result["model"] == "gpt-4o-mini"  # Updated to expect gpt-4o-mini instead of gpt-3.5-turbo


@pytest.mark.asyncio
async def test_recommender_creative():
    """Test recommender for creative task."""
    agent = RecommenderAgent()
    input_data = {
        "task_type": "creative",
        "prompt_length": 500
    }
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    assert result["recommended_provider"] == "openai"
    assert result["model"] == "gpt-4o"


@pytest.mark.asyncio
async def test_recommender_code():
    """Test recommender for code task."""
    agent = RecommenderAgent()
    input_data = {
        "task_type": "code",
        "prompt_length": 1000
    }
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    assert result["recommended_provider"] == "openai"
    assert result["model"] == "gpt-4o"


@pytest.mark.asyncio
async def test_recommender_default():
    """Test recommender with no task type provided."""
    agent = RecommenderAgent()
    input_data = {}  # No task_type provided
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    # Default fallback as defined in the agent logic
    assert result["recommended_provider"] == "openai"
    assert "model" in result


@pytest.mark.asyncio
async def test_recommender_unknown_task():
    """Test recommender with unknown task type."""
    agent = RecommenderAgent()
    input_data = {
        "task_type": "unknown_task_type",
        "prompt_length": 100
    }
    result = agent.process_prompt(input_data)
    assert result["status"] == "success"
    # Should fall back to default mapping
    assert result["recommended_provider"] == "openai"
    assert "model" in result


@pytest.mark.asyncio
async def test_recommender_message_field():
    """Test that the recommender includes a message field."""
    agent = RecommenderAgent()
    input_data = {
        "task_type": "reasoning",
        "prompt_length": 200
    }
    result = agent.process_prompt(input_data)
    assert "message" in result
    assert "Based on reasoning task" in result["message"]