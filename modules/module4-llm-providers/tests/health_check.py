"""
Health check script for LLM providers.

This script tests the connection to each LLM provider to ensure they're working correctly.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.llm_providers.openai_agent import OpenAIAgent
from app.agents.llm_providers.gemini_agent import GeminiAgent
from app.agents.llm_providers.requestry_agent import RequestryAgent
from app.agents.llm_providers.openrouter_agent import OpenRouterAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_openai():
    """Test the OpenAI agent."""
    logger.info("Testing OpenAI agent...")
    try:
        agent = OpenAIAgent()
        result = agent.process_prompt({
            "prompt": "Hello, can you give me a short health check response?",
            "max_tokens": 50
        })
        
        if result["status"] == "success":
            logger.info(f"OpenAI test successful! Response: {result['message']}")
            logger.info(f"Model used: {result['model']}")
            if "usage" in result:
                logger.info(f"Token usage: {result['usage']}")
            return True
        else:
            logger.error(f"OpenAI test failed: {result['message']}")
            return False
    except Exception as e:
        logger.error(f"Error testing OpenAI: {str(e)}")
        return False

def test_gemini():
    """Test the Gemini agent."""
    logger.info("Testing Gemini agent...")
    try:
        agent = GeminiAgent()
        result = agent.process_prompt({
            "prompt": "Hello, can you give me a short health check response?",
            "max_tokens": 50
        })
        
        if result["status"] == "success":
            logger.info(f"Gemini test successful! Response: {result['message']}")
            logger.info(f"Model used: {result['model']}")
            if "usage" in result:
                logger.info(f"Token usage: {result['usage']}")
            return True
        else:
            logger.error(f"Gemini test failed: {result['message']}")
            return False
    except Exception as e:
        logger.error(f"Error testing Gemini: {str(e)}")
        return False

def test_requestry():
    """Test the Requestry agent."""
    logger.info("Testing Requestry agent...")
    try:
        agent = RequestryAgent()
        result = agent.process_prompt({
            "prompt": "Hello, can you give me a short health check response?",
            "max_tokens": 50
        })
        
        if result["status"] == "success":
            logger.info(f"Requestry test successful! Response: {result['message']}")
            logger.info(f"Model used: {result['model']}")
            if "usage" in result:
                logger.info(f"Token usage: {result['usage']}")
            return True
        else:
            logger.error(f"Requestry test failed: {result['message']}")
            return False
    except Exception as e:
        logger.error(f"Error testing Requestry: {str(e)}")
        return False

def test_openrouter():
    """Test the OpenRouter agent."""
    logger.info("Testing OpenRouter agent...")
    try:
        agent = OpenRouterAgent()
        result = agent.process_prompt({
            "prompt": "Hello, can you give me a short health check response?",
            "max_tokens": 50
        })
        
        if result["status"] == "success":
            logger.info(f"OpenRouter test successful! Response: {result['message']}")
            logger.info(f"Model used: {result['model']}")
            if "usage" in result:
                logger.info(f"Token usage: {result['usage']}")
            return True
        else:
            logger.error(f"OpenRouter test failed: {result['message']}")
            return False
    except Exception as e:
        logger.error(f"Error testing OpenRouter: {str(e)}")
        return False

def main():
    """Run health checks for all providers."""
    # Load environment variables
    load_dotenv()
    
    logger.info("Starting LLM provider health checks...")
    
    results = {
        "OpenAI": test_openai(),
        "Gemini": test_gemini(),
        "Requestry": test_requestry(),
        "OpenRouter": test_openrouter()
    }
    
    # Print summary
    logger.info("\n--- Health Check Summary ---")
    for provider, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        logger.info(f"{provider}: {status}")
    
    # Return overall success (all providers working)
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)