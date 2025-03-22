"""
LLM Providers Router.

This module provides FastAPI endpoints for interacting with various LLM providers.
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from app.agents.llm_providers.openai_agent import OpenAIAgent

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()


class OpenAIRequest(BaseModel):
    """Request model for OpenAI endpoint."""
    prompt: str = Field(..., description="The text prompt to send to the model")
    model: str = Field("gpt-o3-mini", description="The model to use for generation")
    max_tokens: Optional[int] = Field(100, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")


class LLMResponse(BaseModel):
    """Response model for LLM endpoints."""
    status: str = Field(..., description="Status of the request (success or error)")
    message: str = Field(..., description="Response text or error message")
    model: str = Field(..., description="Model used for generation")
    usage: Optional[Dict[str, int]] = Field(None, description="Token usage statistics")


@router.post("/openai", response_model=LLMResponse)
async def openai_endpoint(request_data: OpenAIRequest):
    """
    Endpoint for OpenAI LLM provider.
    
    Processes a prompt using OpenAI's API and returns the generated text.
    """
    logger.info(f"Received request for OpenAI endpoint with model: {request_data.model}")
    
    agent = OpenAIAgent()
    result = agent.process_prompt(request_data.dict())
    
    if result["status"] == "error":
        logger.error(f"Error processing OpenAI request: {result['message']}")
        raise HTTPException(status_code=400, detail=result["message"])
    
    logger.info(f"Successfully processed OpenAI request with model: {result['model']}")
    return result


@router.post("/gemini")
async def gemini_endpoint():
    """
    Endpoint for Gemini LLM provider.
    Will be implemented in Phase 3.
    """
    return {"status": "placeholder"}


@router.post("/requestry")
async def requestry_endpoint():
    """
    Endpoint for Requestry LLM provider.
    Will be implemented in Phase 3.
    """
    return {"status": "placeholder"}


@router.post("/openrouter")
async def openrouter_endpoint():
    """
    Endpoint for OpenRouter LLM provider.
    Will be implemented in Phase 3.
    """
    return {"status": "placeholder"}


@router.post("/recommend-model")
async def recommend_model_endpoint():
    """
    Endpoint for model recommendation.
    Will be implemented in Phase 4.
    """
    return {"status": "placeholder"}