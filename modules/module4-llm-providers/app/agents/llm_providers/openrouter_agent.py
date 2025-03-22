"""
OpenRouter Agent implementation.

This module provides a class for interacting with OpenRouter's API.
"""

import os
import logging
import openai
from typing import Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class OpenRouterAgent:
    """
    OpenRouter Agent for interfacing with the OpenRouter API.
    Supports optional headers for ranking and access to models like "openai/gpt-4o".
    """

    def __init__(self):
        """Initialize the OpenRouter agent."""
        # Load environment variables
        load_dotenv()
        
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            logger.error("OPENROUTER_API_KEY environment variable is not set")
            raise ValueError("OPENROUTER_API_KEY is not set")
            
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = "openai/gpt-4o"
        
        # List of supported models (this is a subset, OpenRouter supports many more)
        self.supported_models = [
            "openai/gpt-4o",
            "openai/gpt-4-turbo",
            "anthropic/claude-3-opus",
            "anthropic/claude-3-sonnet",
            "google/gemini-pro",
            "meta/llama-3-70b-instruct"
        ]
        
        # Optional headers for ranking and identification
        self.optional_headers = {
            "HTTP-Referer": os.getenv("OPENROUTER_REFERER", ""),
            "X-Title": os.getenv("OPENROUTER_TITLE", "OpenAI Agents Module 4")
        }
        
        # Filter out empty headers
        self.optional_headers = {k: v for k, v in self.optional_headers.items() if v}
        
        # Initialize the OpenAI client with OpenRouter base URL
        try:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info(f"OpenRouter agent initialized with default model: {self.default_model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter client: {str(e)}")
            raise

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt using OpenRouter's API.
        
        Args:
            prompt_data: Dictionary containing:
                - prompt: The text prompt.
                - model: Optional model name; defaults to default_model.
                - max_tokens: Optional maximum tokens to generate.
                - temperature: Optional sampling temperature.
                - system_message: Optional system message to set context.
                - headers: Optional additional headers to include.
        
        Returns:
            Dictionary with status, message, model, and (if available) usage.
        """
        # Extract parameters with defaults
        prompt = prompt_data.get("prompt", "")
        model_name = prompt_data.get("model", self.default_model)
        max_tokens = prompt_data.get("max_tokens", 100)
        temperature = prompt_data.get("temperature", 0.7)
        system_message = prompt_data.get("system_message", "You are a helpful assistant.")
        custom_headers = prompt_data.get("headers", {})
        
        logger.info(f"Processing prompt with OpenRouter model: {model_name}")
        
        # Combine default headers with any custom headers
        headers = {**self.optional_headers, **custom_headers}
        
        try:
            # Prepare messages
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            logger.debug(f"Sending request to OpenRouter with model: {model_name}")
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                extra_headers=headers if headers else None
            )
            
            # Extract usage information if available
            usage = {}
            if hasattr(response, 'usage') and response.usage is not None:
                try:
                    usage = {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                except AttributeError as e:
                    logger.warning(f"Could not extract usage information: {str(e)}")
                    # Provide default usage values
                    usage = {
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0,
                        "note": "Token usage information not available"
                    }
            else:
                # Provide default usage values when usage is not available
                usage = {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "note": "Token usage information not available"
                }
            
            logger.info(f"OpenRouter prompt processed successfully with model: {model_name}")
            return {
                "status": "success",
                "message": response.choices[0].message.content,
                "model": model_name,
                "usage": usage
            }
        except openai.APIError as e:
            logger.error(f"OpenRouter API error: {str(e)}")
            return {
                "status": "error",
                "message": f"OpenRouter API error: {str(e)}",
                "model": model_name
            }
        except Exception as e:
            logger.error(f"Unexpected error with OpenRouter: {str(e)}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "model": model_name
            }