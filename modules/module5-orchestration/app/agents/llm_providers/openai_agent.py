"""
OpenAI Agent implementation.

This module provides a class for interacting with OpenAI's API.
It supports multiple models and returns standardized responses.
"""

import os
import logging
import openai
from typing import Dict, Any, List


# Configure logging
logger = logging.getLogger(__name__)

class OpenAIAgent:
    """Agent for interacting with OpenAI models."""
    
    def __init__(self):
        """Initialize the OpenAI agent with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.default_model = "gpt-4o-mini"
        self.provider_name = "openai"  # Add provider_name attribute
        
        # Raise ValueError if API key is missing
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is missing in environment")
            
        logger.info(f"OpenAI agent initialized with default model: {self.default_model}")
    
    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt using OpenAI's API.
        
        Args:
            prompt_data: Dictionary containing:
                - prompt (str): The user's text prompt
                - system_message (str, optional): System message for the conversation
                - model (str, optional): Model name (default: gpt-4o-mini)
                - max_tokens (int, optional): Maximum tokens to generate
                - temperature (float, optional): Sampling temperature
            
        Returns:
            Dictionary with:
                - status (str): "success" or "error"
                - response (str): Response text (for success)
                - error (str): Error message (for error)
                - model (str): Model used for generation
                - usage (dict, optional): Token usage statistics
        """
        # Extract parameters from prompt_data
        prompt = prompt_data.get("prompt", "")
        system_message = prompt_data.get("system_message", None)
        model_name = prompt_data.get("model", self.default_model)
        max_tokens = prompt_data.get("max_tokens", 100)
        temperature = prompt_data.get("temperature", 0.7)
        
        logger.info(f"Processing prompt with model: {model_name}")
        
        try:
            # Create OpenAI client
            client = openai.OpenAI(api_key=self.api_key)
            
            # Prepare messages
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract completion text
            completion_text = response.choices[0].message.content
            
            # Extract usage statistics
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            logger.info(f"Successfully processed prompt with model: {model_name}")
            
            return {
                "status": "success",
                "response": completion_text,  # Change from "message" to "response"
                "model": model_name,
                "usage": usage
            }
            
        except Exception as e:
            error_message = str(e).lower()
            logger.error(f"Error processing prompt: {error_message}")
            
            # Categorize the error based on the error message
            if "authentication" in error_message or "api key" in error_message:
                error_type = "Authentication error"
            elif "rate limit" in error_message:
                error_type = "Rate limit exceeded"
            elif "invalid request" in error_message or "bad request" in error_message:
                error_type = "Invalid request"
            else:
                error_type = "API error"
            
            return {
                "status": "error",
                "error": f"{error_type}: {str(e)}",  # Change from "message" to "error"
                "model": model_name
            }