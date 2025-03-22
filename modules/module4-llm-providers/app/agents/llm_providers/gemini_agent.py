"""
Gemini Agent implementation.

This module provides a class for interacting with Google's Gemini API.
"""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiAgent:
    """
    Gemini Agent
    -------------
    Purpose: Interact with Google's Gemini API to generate text completions.

    Advanced Functionality:
    - Supports multiple models
    - Handles both simple and complex prompts
    - Provides usage statistics

    Usage (standalone - for testing):
        # In a Python shell:
        from app.agents.llm_providers.gemini_agent import GeminiAgent
        agent = GeminiAgent()
        result = agent.test_connection("Hello, how are you?")
        print(result)
    """

    def __init__(self):
        """Initialize the Gemini agent."""
        # Load environment variables
        load_dotenv()
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY environment variable is not set")
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        # Get model from environment or use default
        self.default_model = "gemini-1.0-pro"
        
        # List of supported models
        self.supported_models = [
            "gemini-1.0-pro",
            "gemini-1.0-pro-vision",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]
        
        # Initialize Gemini client
        genai.configure(api_key=self.api_key)
        logger.info(f"Gemini agent initialized with default model: {self.default_model}")

    def test_connection(self, input_text: str) -> Dict[str, Any]:
        """
        Test the connection to Gemini API with a simple text generation request.
        
        Args:
            input_text: The text to send to Gemini
            
        Returns:
            A dictionary containing the response and status
        """
        try:
            logger.info(f"Testing Gemini connection with model: {self.default_model}")
            model = genai.GenerativeModel(self.default_model)
            response = model.generate_content(input_text)
            
            logger.info("Gemini connection test successful")
            return {
                "status": "success",
                "message": response.text,
                "model": self.default_model
            }
        except Exception as e:
            logger.error(f"Gemini connection test failed: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "model": self.default_model
            }

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt with more options using Gemini's API.
        
        Args:
            prompt_data: A dictionary containing:
                - prompt: The text prompt to send to Gemini
                - system_message: (optional) System message to set context
                - max_tokens: (optional) Maximum tokens to generate
                - temperature: (optional) Sampling temperature
                - model: (optional) Model to use, defaults to the model in .env or gemini-1.0-pro
        
        Returns:
            A dictionary with the response data
        """
        try:
            # Extract parameters with defaults
            prompt = prompt_data.get("prompt", "")
            system_message = prompt_data.get("system_message", "You are a helpful assistant.")
            max_tokens = prompt_data.get("max_tokens", 100)
            temperature = prompt_data.get("temperature", 0.7)
            model_name = prompt_data.get("model", self.default_model)
            
            logger.info(f"Processing prompt with Gemini model: {model_name}")
            
            # Validate model - use default if invalid
            if not isinstance(model_name, str) or model_name not in self.supported_models:
                logger.warning(f"Invalid model '{model_name}', using default: {self.default_model}")
                model_name = self.default_model

            # Configure generation parameters
            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": temperature
            }
            
            # Initialize the model
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
            
            # For direct generation without chat
            if not system_message:
                response = model.generate_content(prompt)
                message_text = response.text
            else:
                # Create chat session with system message
                try:
                    # Try using the chat interface if available
                    chat = model.start_chat(history=[])
                    
                    # Add system message if provided
                    if system_message:
                        logger.debug(f"Adding system message: {system_message}")
                        chat.send_message(f"System: {system_message}")
                    
                    # Send user prompt and get response
                    logger.debug(f"Sending prompt: {prompt}")
                    response = chat.send_message(prompt)
                    message_text = response.text
                except Exception as chat_error:
                    # Fall back to direct generation if chat is not supported
                    logger.warning(f"Chat not supported for this model, falling back to direct generation: {str(chat_error)}")
                    full_prompt = f"System: {system_message}\n\nUser: {prompt}"
                    response = model.generate_content(full_prompt)
                    message_text = response.text
            
            # Estimate token usage (Gemini doesn't provide exact counts)
            prompt_chars = len(prompt) + len(system_message)
            response_chars = len(message_text)
            estimated_prompt_tokens = prompt_chars // 4  # Rough estimate
            estimated_completion_tokens = response_chars // 4  # Rough estimate
            
            usage = {
                "prompt_tokens": estimated_prompt_tokens,
                "completion_tokens": estimated_completion_tokens,
                "total_tokens": estimated_prompt_tokens + estimated_completion_tokens,
                "note": "Token counts are estimates as Gemini API doesn't provide exact usage"
            }
            
            logger.info(f"Gemini prompt processed successfully with model: {model_name}")
            return {
                "status": "success",
                "message": message_text,
                "model": model_name,
                "usage": usage
            }
        except Exception as e:
            logger.error(f"Error processing Gemini prompt: {str(e)}")
            return {
                "status": "error",
                "message": f"Error processing prompt: {str(e)}",
                "model": model_name if 'model_name' in locals() else self.default_model
            }