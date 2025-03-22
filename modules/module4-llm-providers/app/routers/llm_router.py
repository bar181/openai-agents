"""
LLM Providers Router.

This module provides FastAPI endpoints for interacting with various LLM providers.
"""

import logging
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from app.agents.llm_providers.openai_agent import OpenAIAgent
from app.agents.llm_providers.gemini_agent import GeminiAgent
from app.agents.llm_providers.requestry_agent import RequestryAgent
from app.agents.llm_providers.openrouter_agent import OpenRouterAgent
from app.agents.llm_providers.recommender_agent import RecommenderAgent

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

router = APIRouter()


class OpenAIRequest(BaseModel):
    """Request model for OpenAI endpoint."""
    prompt: str = Field(..., description="The text prompt to send to the model")
    model: str = Field("gpt-3.5-turbo", description="The model to use for generation")
    max_tokens: Optional[int] = Field(100, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")


class GeminiRequest(BaseModel):
    """Request model for Gemini endpoint."""
    prompt: str = Field(..., description="The text prompt to send to the model")
    model: str = Field(os.getenv("GEMINI_MODEL", "gemini-2.0-pro-exp-02-05"), description="The model to use for generation")
    max_tokens: Optional[int] = Field(100, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")


class RequestryRequest(BaseModel):
    """Request model for Requestry endpoint."""
    prompt: str = Field(..., description="The text prompt to send to the model")
    model: str = Field("cline/o3-mini", description="The model to use for generation")
    max_tokens: Optional[int] = Field(100, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")


class OpenRouterRequest(BaseModel):
    """Request model for OpenRouter endpoint."""
    prompt: str = Field(..., description="The text prompt to send to the model")
    model: str = Field("openai/gpt-4o", description="The model to use for generation")
    max_tokens: Optional[int] = Field(100, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    system_message: Optional[str] = Field("You are a helpful assistant.", description="System message to set context")
    headers: Optional[Dict[str, str]] = Field(None, description="Optional headers for the request")


class RecommenderRequest(BaseModel):
    """Request model for Model Recommender endpoint."""
    task_type: str = Field(..., description="Type of task (reasoning, conversation, creative, code)")
    prompt_length: int = Field(..., description="Length of the prompt in characters")


class LLMResponse(BaseModel):
    """Response model for LLM endpoints."""
    status: str = Field(..., description="Status of the request (success or error)")
    message: str = Field(..., description="Response text or error message")
    model: str = Field(..., description="Model used for generation")
    usage: Optional[Dict[str, Any]] = Field(None, description="Token usage statistics")


class RecommenderResponse(BaseModel):
    """Response model for Model Recommender endpoint."""
    status: str = Field(..., description="Status of the request (success or error)")
    recommended_provider: str = Field(..., description="Recommended LLM provider")
    model: str = Field(..., description="Recommended model")
    message: Optional[str] = Field(None, description="Additional information or error message")


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


@router.post("/gemini", response_model=LLMResponse)
async def gemini_endpoint(request_data: GeminiRequest):
    """
    Endpoint for Gemini LLM provider.
    
    Processes a prompt using Google's Gemini API and returns the generated text.
    """
    logger.info(f"Received request for Gemini endpoint with model: {request_data.model}")
    
    try:
        agent = GeminiAgent()
        result = agent.process_prompt(request_data.dict())
        
        if result["status"] == "error":
            logger.error(f"Error processing Gemini request: {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
        
        logger.info(f"Successfully processed Gemini request with model: {result['model']}")
        return result
    except ValueError as e:
        logger.error(f"Gemini configuration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in Gemini endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/requestry", response_model=LLMResponse)
async def requestry_endpoint(request_data: RequestryRequest):
    """
    Endpoint for Requestry LLM provider.
    
    Processes a prompt using Requestry's API and returns the generated text.
    """
    logger.info(f"Received request for Requestry endpoint with model: {request_data.model}")
    
    try:
        agent = RequestryAgent()
        result = agent.process_prompt(request_data.dict())
        
        if result["status"] == "error":
            logger.error(f"Error processing Requestry request: {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
        
        logger.info(f"Successfully processed Requestry request with model: {result['model']}")
        return result
    except ValueError as e:
        logger.error(f"Requestry configuration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in Requestry endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/openrouter", response_model=LLMResponse)
async def openrouter_endpoint(request_data: OpenRouterRequest):
    """
    Endpoint for OpenRouter LLM provider.
    
    Processes a prompt using OpenRouter's API and returns the generated text.
    """
    logger.info(f"Received request for OpenRouter endpoint with model: {request_data.model}")
    
    try:
        agent = OpenRouterAgent()
        result = agent.process_prompt(request_data.dict())
        
        if result["status"] == "error":
            logger.error(f"Error processing OpenRouter request: {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
        
        logger.info(f"Successfully processed OpenRouter request with model: {result['model']}")
        return result
    except ValueError as e:
        logger.error(f"OpenRouter configuration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in OpenRouter endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/recommend-model", response_model=RecommenderResponse)
async def recommend_model_endpoint(request_data: RecommenderRequest):
    """
    Endpoint for model recommendation.
    
    Accepts task type and prompt length, and returns a recommended provider and model.
    
    Example request:
    ```json
    {
      "task_type": "reasoning",
      "prompt_length": 200
    }
    ```
    
    Example response:
    ```json
    {
      "status": "success",
      "recommended_provider": "openai",
      "model": "gpt-4o",
      "message": "Based on reasoning task and 200 characters (short length)"
    }
    ```
    """
    logger.info(f"Received request for model recommendation with task_type: {request_data.task_type}, prompt_length: {request_data.prompt_length}")
    
    try:
        agent = RecommenderAgent()
        result = agent.process_prompt(request_data.dict())
        
        if result["status"] == "error":
            logger.error(f"Error processing recommendation request: {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
        
        logger.info(f"Successfully processed recommendation request: {result['recommended_provider']}/{result['model']}")
        return result
    except Exception as e:
        logger.error(f"Unexpected error in recommendation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")