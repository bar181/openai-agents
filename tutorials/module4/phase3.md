```markdown
# Module 4 – Phase 3: Gemini, Requestry, and OpenRouter Agents

**Objective:**  
Implement three additional LLM provider agents—Gemini, Requestry, and OpenRouter—by creating their respective agent files, writing tests, and exposing endpoints in the FastAPI router.

This phase follows the same iterative workflow:
1. Write tests.
2. Implement the agent code.
3. Run tests and refactor.
4. Update the implementation process documentation.

---

## Part 1: Gemini Agent

### 1.1 Create `gemini_agent.py`

- **Requirements:**
  - Load the `GEMINI_API_KEY` from the environment.
  - Use the Gemini client from `google.generativeai` to generate completions.
  - Support multiple models (e.g., `gemini-2.0`, `gemini-pro`, `gemini-ultra`).

### 1.2 Reference Code Snippet

Below is the reference code provided for Gemini:

```python
# agents/gemini_agent.py
import os
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

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
        from agents import gemini_agent
        agent = gemini_agent.GeminiAgent()
        result = agent.test_connection("Hello, how are you?")
        print(result)
    """

    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        # Get model from environment or use default
        self.default_model = os.getenv("GEMINI_MODEL", "gemini-2.0")
        
        # List of supported models
        self.supported_models = [
            "gemini-2.0",
            "gemini-pro",
            "gemini-pro-vision",
            "gemini-ultra"
        ]
        
        # Initialize Gemini client
        genai.configure(api_key=self.api_key)

    def test_connection(self, input_text: str) -> Dict[str, Any]:
        """
        Test the connection to Gemini API with a simple text generation request.
        
        Args:
            input_text: The text to send to Gemini
            
        Returns:
            A dictionary containing the response and status
        """
        try:
            model = genai.GenerativeModel(self.default_model)
            response = model.generate_content(input_text)
            
            return {
                "status": "success",
                "message": response.text,
                "model": self.default_model
            }
        except Exception as e:
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
                - model: (optional) Model to use, defaults to the model in .env or gemini-2.0
        
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
            
            # Validate model - use default if invalid
            if not isinstance(model_name, str) or model_name not in self.supported_models:
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
            
            # Create chat session with system message
            chat = model.start_chat(history=[])
            
            # Add system message if provided
            if system_message:
                chat.send_message(f"System: {system_message}")
            
            # Send user prompt and get response
            response = chat.send_message(prompt)
            
            # Estimate token usage (Gemini doesn't provide exact counts)
            prompt_chars = len(prompt) + len(system_message)
            response_chars = len(response.text)
            estimated_prompt_tokens = prompt_chars // 4  # Rough estimate
            estimated_completion_tokens = response_chars // 4  # Rough estimate
            
            usage = {
                "prompt_tokens": estimated_prompt_tokens,
                "completion_tokens": estimated_completion_tokens,
                "total_tokens": estimated_prompt_tokens + estimated_completion_tokens,
                "note": "Token counts are estimates as Gemini API doesn't provide exact usage"
            }
            
            return {
                "status": "success",
                "message": response.text,
                "model": model_name,
                "usage": usage
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing prompt: {str(e)}",
                "model": model_name if 'model_name' in locals() else self.default_model
            }
```

### 1.3 Testing Gemini Agent

Create `tests/test_gemini_agent.py` with tests that:
- Verify that a valid prompt returns a success response.
- Handle exceptions and report error statuses.

*Example placeholder test:*
```python
# tests/test_gemini_agent.py
import os
import pytest
from app.agents.llm_providers.gemini_agent import GeminiAgent

@pytest.mark.asyncio
async def test_gemini_agent_connection():
    # Ensure GEMINI_API_KEY is set for testing
    os.environ["GEMINI_API_KEY"] = "test-gemini-key"
    agent = GeminiAgent()
    result = agent.test_connection("Test prompt")
    assert "status" in result
```

---

## Part 2: Requestry Agent

### 2.1 Create `requestry_agent.py`

- **Requirements:**
  - Load `REQUESTRY_API_KEY` from the environment.
  - Support model selection such as `"cline/o3-mini"` and `"cline/4o-mini"`.
  - Wrap the provided Requestry code snippet.

### 2.2 Reference Code Snippet

Below is the provided Requestry example:

```python
import openai

ROUTER_API_KEY = "your-api-key"

# Initialize the client
client = openai.OpenAI(
    api_key=ROUTER_API_KEY,
    base_url="https://router.requesty.ai/v1"
)

try:
    # Make your API call
    response = client.chat.completions.create(
        model="cline/o3-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello! How can you help me today?"
            }
        ]
    )

    # Print the assistant's response
    print("Assistant:", response.choices[0].message.content)

except openai.APIError as e:
    print(f"OpenAI API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 2.3 Implementation in `requestry_agent.py`

Adapt the snippet to a class structure with a method `process_prompt`:

```python
# app/agents/llm_providers/requestry_agent.py
import os
import openai
from typing import Any, Dict

class RequestryAgent:
    """
    Requestry Agent for handling prompts via Requesty.
    Supports models like "cline/o3-mini" and "cline/4o-mini".
    """

    def __init__(self):
        self.api_key = os.getenv("REQUESTRY_API_KEY", "")
        if not self.api_key:
            raise ValueError("REQUESTRY_API_KEY is not set")
        self.base_url = "https://router.requesty.ai/v1"
        self.default_model = "cline/o3-mini"
        # Initialize the OpenAI client with Requesty base URL
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt using Requestry's API.
        
        Args:
            prompt_data: Dictionary containing:
                - prompt: User prompt text.
                - model: Optional model name; defaults to default_model.
        
        Returns:
            Dictionary with status, message, model, and (if available) usage.
        """
        model_name = prompt_data.get("model", self.default_model)
        prompt = prompt_data.get("prompt", "")
        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return {
                "status": "success",
                "message": response.choices[0].message.content,
                "model": model_name,
                "usage": response.get("usage", {})
            }
        except openai.APIError as e:
            return {
                "status": "error",
                "message": f"OpenAI API error: {e}",
                "model": model_name
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {e}",
                "model": model_name
            }
```

### 2.4 Testing Requestry Agent

Create `tests/test_requestry_agent.py` with tests similar to the OpenAI agent tests.  
For example, check that:
- A valid prompt returns a success.
- The agent properly handles missing or invalid API keys.
- The returned model is as expected.

---

## Part 3: OpenRouter Agent

### 3.1 Create `openrouter_agent.py`

- **Requirements:**
  - Load `OPENROUTER_API_KEY` from the environment.
  - Use base URL `https://openrouter.ai/api/v1`.
  - Allow optional headers such as `"HTTP-Referer"` and `"X-Title"` for ranking.
  
### 3.2 Implementation Example

```python
# app/agents/llm_providers/openrouter_agent.py
import os
import openai
from typing import Any, Dict

class OpenRouterAgent:
    """
    OpenRouter Agent for interfacing with the OpenRouter API.
    Supports optional headers for ranking and access to models like "openai/gpt-4o".
    """

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = "openai/gpt-4o"
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        # Optional headers can be defined here if needed
        self.optional_headers = {
            "HTTP-Referer": os.getenv("OPENROUTER_REFERER", ""),
            "X-Title": os.getenv("OPENROUTER_TITLE", "")
        }

    def process_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a prompt using OpenRouter's API.
        
        Args:
            prompt_data: Dictionary containing:
                - prompt: The text prompt.
                - model: Optional model name; defaults to default_model.
        
        Returns:
            Dictionary with response details.
        """
        model_name = prompt_data.get("model", self.default_model)
        prompt = prompt_data.get("prompt", "")
        try:
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                extra_headers=self.optional_headers
            )
            return {
                "status": "success",
                "message": response.choices[0].message.content,
                "model": model_name,
                "usage": response.get("usage", {})
            }
        except openai.APIError as e:
            return {
                "status": "error",
                "message": f"OpenAI API error: {e}",
                "model": model_name
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {e}",
                "model": model_name
            }
```

### 3.3 Testing OpenRouter Agent

Create `tests/test_openrouter_agent.py`:
- Write tests to ensure valid responses are returned.
- Simulate a call with optional headers and check that errors are handled.

---

## Part 4: Update FastAPI Endpoints in `llm_router.py`

Update or add endpoints to expose the new agents:

```python
# app/routers/llm_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.llm_providers.gemini_agent import GeminiAgent
from app.agents.llm_providers.requestry_agent import RequestryAgent
from app.agents.llm_providers.openrouter_agent import OpenRouterAgent

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    model: str = ""
    max_tokens: int = 100
    temperature: float = 0.7

@router.post("/gemini")
async def gemini_endpoint(request_data: PromptRequest):
    agent = GeminiAgent()
    result = agent.process_prompt(request_data.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.post("/requestry")
async def requestry_endpoint(request_data: PromptRequest):
    agent = RequestryAgent()
    result = agent.process_prompt(request_data.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.post("/openrouter")
async def openrouter_endpoint(request_data: PromptRequest):
    agent = OpenRouterAgent()
    result = agent.process_prompt(request_data.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result
```

---

## Part 5: Refactoring and Documentation Updates

- **Refactor:** Ensure that all agent classes implement a consistent interface (for example, a common `process_prompt` method).
- **Documentation:**  
  - Update `docs/guidelines.md` to reflect any new conventions.
  - Add notes in `docs/implementation_process.md` detailing the progress for Phase 3.
  - Refer to `/common/provider_references.md` as needed to ensure all details match the providers’ requirements.

---

## Final Checklist for Phase 3

- [ ] **Gemini Agent:**
  - Implemented `gemini_agent.py` with proper API key handling and model selection.
  - Tests in `tests/test_gemini_agent.py` are passing.
- [ ] **Requestry Agent:**
  - Implemented `requestry_agent.py` with support for models like `"cline/o3-mini"` and `"cline/4o-mini"`.
  - Tests in `tests/test_requestry_agent.py` are passing.
- [ ] **OpenRouter Agent:**
  - Implemented `openrouter_agent.py` with optional headers support.
  - Tests in `tests/test_openrouter_agent.py` are passing.
- [ ] **Endpoints:**  
  - Added endpoints in `llm_router.py` for `/gemini`, `/requestry`, and `/openrouter`.
- [ ] **Refactor & Documentation:**
  - Code refactored for consistency.
  - Documentation and `docs/implementation_process.md` updated with Phase 3 progress.

---

**Next Steps:**  
Once all tests pass and endpoints function correctly, proceed to Phase 4 (Model Recommender) following a similar pattern.
```