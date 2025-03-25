import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# API Keys for different providers
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
REQUESTRY_API_KEY = os.getenv("REQUESTRY_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
API_KEY = os.getenv("API_KEY", "")  # Keep for backward compatibility

# Orchestration-specific configs
TRACE_LOG_LEVEL = os.getenv("TRACE_LOG_LEVEL", "INFO")
ORCHESTRATION_MODE = os.getenv("ORCHESTRATION_MODE", "DEVELOPMENT")

# Log warnings for missing keys (but don't raise errors yet)
# We'll handle missing keys in each provider's implementation
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY is missing. OpenAI provider will not work.")
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY is missing. Gemini provider will not work.")
if not REQUESTRY_API_KEY:
    logger.warning("REQUESTRY_API_KEY is missing. Requestry provider will not work.")
if not OPENROUTER_API_KEY:
    logger.warning("OPENROUTER_API_KEY is missing. OpenRouter provider will not work.")
if not API_KEY:
    logger.warning("API_KEY is missing. Some functionality may be limited.")

# Log orchestration configuration
logger.info(f"Orchestration mode: {ORCHESTRATION_MODE}")
logger.info(f"Trace log level: {TRACE_LOG_LEVEL}")
