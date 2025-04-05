"""
OpenAI Agent implementation.

This module provides a class for interacting with OpenAI's API.
It supports multiple models and returns standardized responses.
"""

import os
import logging
import openai
from typing import Dict, Any


# Configure logging
logger = logging.getLogger(__name__)

class OpenAIAgent:
    """Agent for interacting with OpenAI models."""
    
    def __init__(self):
        """Initialize the OpenAI agent with API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.default_model = "gpt-4o-mini"
        logger.info(f"OpenAI agent initialized with default model: {self.default_model}")
    
    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt using OpenAI's API.
        
        Args:
            prompt_data: Dictionary containing:
                - prompt (str): The user's text prompt
                - model (str, optional): Model name (default: gpt-4o-mini)
                - max_tokens (int, optional): Maximum tokens to generate
                - temperature (float, optional): Sampling temperature
            
        Returns:
            Dictionary with:
                - status (str): "success" or "error"
                - message (str): Response text or error message
                - model (str): Model used for generation
                - usage (dict, optional): Token usage statistics
        """
        # Check for API key
        if not self.api_key:
            logger.error("OPENAI_API_KEY is missing in environment")
            return {
                "status": "error",
                "message": "OPENAI_API_KEY missing in environment.",
                "model": "unknown"
            }
        
        # Extract parameters from prompt_data
        prompt = prompt_data.get("prompt", "")
        model_name = prompt_data.get("model", self.default_model)
        max_tokens = prompt_data.get("max_tokens", 100)
        temperature = prompt_data.get("temperature", 0.7)
        
        logger.info(f"Processing prompt with model: {model_name}")
        
        try:
            # Create OpenAI client
            client = openai.OpenAI(api_key=self.api_key)
            
            # Call OpenAI API
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
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
                "message": completion_text,
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
                "message": f"{error_type}: {str(e)}",
                "model": model_name
            }