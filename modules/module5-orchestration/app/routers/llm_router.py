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

router = APIRouter(tags=["LLM Providers"])

class OpenAIRequest(BaseModel):
    """Request model for OpenAI endpoint."""
    prompt: str = Field(..., description="The text prompt to send to the model")
    model: str = Field("gpt-4o-mini", description="The model to use for generation")
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


@router.post(
    "/openai",
    response_model=LLMResponse,
    summary="Process prompt with OpenAI LLM provider",
    description="""
**Endpoint Overview:**
This endpoint processes a prompt using OpenAI's LLM via the OpenRouterAgent. It accepts a JSON payload conforming to the OpenAIRequest schema and returns a response that includes the generated text, the model used, and token usage metrics.

**Processing Steps:**
1. **Request Validation and Logging:**  
   - Validates the incoming JSON request against the OpenAIRequest schema.  
   - Logs the received model information from the request.

2. **Prompt Processing:**  
   - Instantiates an OpenRouterAgent to interface with the OpenRouter API.  
   - Constructs a message sequence including an optional system message and the user prompt.  
   - Merges default headers with any custom headers provided for ranking and identification.

3. **Response Handling:**  
   - On successful processing, returns a JSON response containing:
     - **message:** The generated text.
     - **model:** The LLM model used for processing.
     - **usage:** Token usage details (prompt_tokens, completion_tokens, total_tokens) if available.
   - In case of an error, logs the error and raises an HTTPException with a 400 status code.

**Response Model Details:**
- **status:** Indicates success or error.
- **message:** Contains the generated text or error description.
- **model:** The model identifier used.
- **usage:** An object detailing token usage metrics.

**Usage Considerations:**  
- Ensure the required environment variables (e.g., API keys) are properly set.
- This endpoint is intended for integration scenarios where OpenAI-based text generation is required.
"""
)
async def openai_endpoint(request_data: OpenAIRequest):
    logger.info(f"Received request for OpenAI endpoint with model: {request_data.model}")

    agent = OpenAIAgent()
    result = agent.process_prompt(request_data.dict())

    if result["status"] == "error":
        logger.error(f"Error processing OpenAI request: {result['message']}")
        raise HTTPException(status_code=400, detail=result["message"])

    logger.info(f"Successfully processed OpenAI request with model: {result['model']}")
    return result



@router.post(
    "/gemini",
    response_model=LLMResponse,
    summary="Process prompt using Gemini LLM provider",
    description="""
Triggers Gemini LLM generation using Google's Gemini API.

**Overview:**
- Accepts JSON payload matching GeminiRequest schema.
- Returns generated text, model identifier, and estimated token usage.

**Workflow:**
1. **Request Verification & Logging:**  
   - Validates incoming JSON payload.
   - Logs received model identifier.

2. **Prompt Processing:**  
   - Instantiates GeminiAgent for API interaction.
   - Extracts parameters with defaults: prompt, system message, maximum tokens, sampling temperature, model selection.
   - Validates provided model; reverts to default if invalid.
   - Initiates chat session if supported; falls back to direct generation when necessary.

3. **Response Formation:**  
   - On success, returns JSON containing:
     - **message:** Generated text.
     - **model:** Model used for generation.
     - **usage:** Estimated token usage (prompt, completion, total).

4. **Error Management:**  
   - Logs issues encountered during prompt processing.
   - Raises appropriate HTTPException for configuration issues or unexpected errors.

**Usage Considerations:**  
- Confirm required environment variables (e.g., GEMINI_API_KEY, GEMINI_ENDPOINT) are set.
- Endpoint is designed for integration in applications requiring Gemini text generation.
"""
)
async def gemini_endpoint(request_data: GeminiRequest):
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

@router.post(
    "/requestry",
    response_model=LLMResponse,
    summary="Generate text using Requestry LLM provider",
    description="""
Initiates text generation via Requestry API.

**Overview:**
- Accepts JSON payload conforming to RequestryRequest.
- Returns generated text, chosen model, and token usage estimates.

**Processing Steps:**
1. **Request Handling:**
   - Validates JSON input against RequestryRequest schema.
   - Logs incoming model identifier.

2. **Prompt Execution:**
   - Instantiates RequestryAgent to interface with Requestry API.
   - Extracts parameters: prompt, system message (default: "You are a helpful assistant."), maximum tokens, sampling temperature, and optional model.
   - Constructs a message sequence comprising a system message and user prompt.
   - Dispatches API call using provided parameters.

3. **Response Formation:**
   - On success, returns a JSON response with:
     - **message:** Generated text.
     - **model:** Model used for generation.
     - **usage:** Estimated token counts (prompt, completion, total).
   - Logs errors and raises appropriate HTTP exceptions (400 or 500) on failures.

**Usage Considerations:**
- Confirm required environment variable (REQUESTRY_API_KEY) is set.
- For configuration errors or API issues, endpoint responds with relevant HTTP status codes.
"""
)
async def requestry_endpoint(request_data: RequestryRequest):
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


@router.post(
    "/openrouter",
    response_model=LLMResponse,
    summary="Process prompt using OpenRouter API",
    description="""
Uses OpenRouter API for text generation. Accepts JSON payload matching OpenRouterRequest schema and returns generated text, model identifier, and token usage details.

**Overview:**
- Accepts JSON input conforming to OpenRouterRequest.
- Utilizes OpenRouterAgent to interact with OpenRouter API.
- Returns generated text, chosen model, and token usage metrics.

**Processing Steps:**
1. **Request Handling:**
   - Validates incoming JSON payload.
   - Logs received model identifier.

2. **Prompt Execution:**
   - Instantiates OpenRouterAgent for API communication.
   - Extracts parameters: prompt, optional system message (defaults to "You are a helpful assistant."), maximum tokens, sampling temperature, and extra headers.
   - Combines default headers with any custom headers provided.
   - Prepares a message sequence starting with system message followed by user prompt.
   - Sends request to OpenRouter API.

3. **Response Formation:**
   - On success, returns JSON with:
     - **message:** Generated text.
     - **model:** Model used for generation.
     - **usage:** Token usage details (prompt tokens, completion tokens, total tokens) if available.
   - On error, logs issue and raises HTTPException with status code 400 or 500.

**Usage Considerations:**
- Ensure required environment variables (e.g., OPENROUTER_API_KEY) are set.
- Endpoint supports custom headers for ranking or identification.
"""
)
async def openrouter_endpoint(request_data: OpenRouterRequest):
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
    
    **Overview:**
    - **Input:** JSON payload containing:
    - **task_type:** Type of task (e.g., reasoning, conversation, creative, code).
    - **prompt_length:** Number of characters in prompt.
    - **Output:** JSON response including:
    - **status:** Indicates success or error.
    - **recommended_provider:** Provider identifier.
    - **model:** Model identifier.
    - **message:** Additional details regarding recommendation.

    **Processing Steps:**
    1. Validates incoming request using RecommenderRequest schema.
    2. Uses RecommenderAgent to:
        - Determine length category (short, medium, long) from prompt_length.
        - Map task type and length category to a recommended provider.
        - Choose a model from provider-specific configuration.
    3. Returns JSON response with recommendation details.

    
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
      "model": "gpt-4o-mini",
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