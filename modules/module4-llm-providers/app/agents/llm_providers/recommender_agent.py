"""
Model Recommender Agent implementation.

This module provides a class for recommending the appropriate LLM provider and model
based on the task type and prompt length.
"""

import logging
from typing import Any, Dict

# Configure logging
logger = logging.getLogger(__name__)

class RecommenderAgent:
    """
    Recommender Agent
    -----------------
    Purpose:
    - Accepts a task specification and prompt length.
    - Returns a recommended provider and model.
    
    Expected Input:
    {
      "task_type": "reasoning",
      "prompt_length": 200
    }
    
    Expected Output:
    {
      "status": "success",
      "recommended_provider": "openai",
      "model": "gpt-4o-mini"
    }
    """

    def __init__(self):
        """Initialize the recommender agent with model mappings."""
        # Define provider-specific models for different task types
        self.provider_models = {
            "openai": {
                "reasoning": "gpt-4o",
                "conversation": "gpt-4o-mini",
                "creative": "gpt-4o",
                "code": "gpt-4o",
                "default": "gpt-4o-mini"
            },
            "gemini": {
                "reasoning": "gemini-2.0-pro-exp-02-05",
                "conversation": "gemini-1.5-pro",
                "creative": "gemini-2.0-pro-exp-02-05",
                "code": "gemini-1.5-pro",
                "default": "gemini-1.5-pro"
            },
            "requestry": {
                "reasoning": "cline/4o-mini",
                "conversation": "cline/o3-mini",
                "creative": "cline/4o-mini",
                "code": "cline/4o-mini",
                "default": "cline/o3-mini"
            },
            "openrouter": {
                "reasoning": "openai/gpt-4o",
                "conversation": "openai/gpt-4o-mini",
                "creative": "openai/gpt-4o",
                "code": "openai/gpt-4o",
                "default": "openai/gpt-4o-mini"
            }
        }
        
        # Define provider selection based on task type and prompt length
        self.task_provider_mapping = {
            "reasoning": {
                "short": "openai",  # < 500 tokens
                "medium": "openai",  # 500-2000 tokens
                "long": "openrouter"  # > 2000 tokens
            },
            "conversation": {
                "short": "openai",
                "medium": "gemini",
                "long": "gemini"
            },
            "creative": {
                "short": "openai",
                "medium": "openai",
                "long": "gemini"
            },
            "code": {
                "short": "openai",
                "medium": "openai",
                "long": "openrouter"
            },
            "default": {
                "short": "openai",
                "medium": "openai",
                "long": "openai"
            }
        }
        
        logger.info("RecommenderAgent initialized with provider and model mappings")

    def _get_length_category(self, prompt_length: int) -> str:
        """
        Determine the length category based on prompt length.
        
        Args:
            prompt_length: The length of the prompt in characters
            
        Returns:
            A string representing the length category: "short", "medium", or "long"
        """
        # Rough estimate: 1 token ≈ 4 characters
        estimated_tokens = prompt_length // 4
        
        if estimated_tokens < 500:
            return "short"
        elif estimated_tokens < 2000:
            return "medium"
        else:
            return "long"

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and recommend a provider and model.
        
        Args:
            prompt_data: Dictionary containing:
                - task_type (str): The type of task (reasoning, conversation, creative, code)
                - prompt_length (int): The length of the prompt in characters
                
        Returns:
            Dictionary with:
                - status (str): "success" or "error"
                - recommended_provider (str): The recommended provider
                - model (str): The recommended model
                - message (str, optional): Additional information or error message
        """
        try:
            # Extract values with defaults
            task_type = prompt_data.get("task_type", "").lower()
            prompt_length = prompt_data.get("prompt_length", 100)
            
            logger.info(f"Processing recommendation for task_type: {task_type}, prompt_length: {prompt_length}")
            
            # Determine length category
            length_category = self._get_length_category(prompt_length)
            
            # Get task type mapping or default if not found
            task_mapping = self.task_provider_mapping.get(task_type, self.task_provider_mapping["default"])
            
            # Get provider based on task type and length
            recommended_provider = task_mapping.get(length_category, task_mapping["short"])
            
            # Get provider's model mapping
            provider_model_mapping = self.provider_models.get(recommended_provider, self.provider_models["openai"])
            
            # Get model based on task type or default if not found
            model = provider_model_mapping.get(task_type, provider_model_mapping["default"])
            
            logger.info(f"Recommended provider: {recommended_provider}, model: {model}")
            
            return {
                "status": "success",
                "recommended_provider": recommended_provider,
                "model": model,
                "message": f"Based on {task_type} task and {prompt_length} characters ({length_category} length)"
            }
            
        except Exception as e:
            logger.error(f"Error in recommender agent: {str(e)}")
            return {
                "status": "error",
                "message": f"Error processing recommendation: {str(e)}",
                "recommended_provider": "openai",  # Fallback to a safe default
                "model": "gpt-3.5-turbo"
            }