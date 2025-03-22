# Module 4 Tutorial: Custom LLM Providers

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Master's Student at Harvard University, CS50 Teaching Fellow/Course Assistant. Instructor and course designer for Pair Programming with AI - A documentation 1st approach to AI assisted code wiring*

---

## Welcome to Module 4!

Hello again! In this module, we'll explore how to integrate multiple LLM providers into your agent system. You'll learn how to work with OpenAI, Gemini, Requestry, and OpenRouter APIs, and build a model recommender that suggests the best model for different tasks. This module builds on the agent patterns from previous modules while adding the flexibility to use different LLM providers.

---

## Learning Goals

By completing this module, you will:

- Implement agents that work with multiple LLM providers (OpenAI, Gemini, Requestry, OpenRouter)
- Create a consistent interface for different LLM APIs
- Build a model recommender system that suggests appropriate models for different tasks
- Handle provider-specific authentication and error scenarios
- Design a unified API for accessing different LLM providers

---

## Module Structure Overview

We've organized this module into five phases:

### 1. Environment & Setup
Setting up the project structure and environment variables for multiple LLM providers.

### 2. OpenAI Multi-Model Agent
Implementing an agent that works with various OpenAI models.

### 3. Gemini, Requestry, and OpenRouter Agents
Creating agents for additional LLM providers with consistent interfaces.

### 4. Model Recommender
Building a system that recommends the best model for different task types.

### 5. Documentation & Final Checks
Finalizing documentation and ensuring all components work together.

---

## Step-by-Step Learning Path

### Phase 1: Environment & Setup
**Key Learning Points:**
- Setting up environment variables for multiple API keys
- Creating a consistent directory structure
- Preparing test files for each provider

### Phase 2: OpenAI Multi-Model Agent
**Key Learning Points:**
- Working with multiple OpenAI models
- Implementing a consistent interface for model interaction
- Handling API errors and edge cases

### Phase 3: Additional LLM Providers
**Key Learning Points:**
- Integrating with Gemini API
- Working with Requestry for model access
- Using OpenRouter for additional model options
- Creating a consistent response format across providers

### Phase 4: Model Recommender
**Key Learning Points:**
- Building a system to recommend models based on task requirements
- Implementing decision logic for model selection
- Creating an API endpoint for model recommendations

### Phase 5: Documentation & Testing
**Key Learning Points:**
- Comprehensive testing across providers
- Finalizing documentation
- Ensuring code quality and standards

---

## RESTful API Design

### API Endpoints
```python
# LLM Provider Endpoints

# POST /agents/llm-providers/openai
# Process prompts using OpenAI models (gpt-4o, o3-mini, etc.)
# Request: {"prompt": "text", "model": "gpt-o3-mini", "max_tokens": 100, "temperature": 0.7}
# Response: {"status": "success", "message": "...", "model": "gpt-o3-mini", "usage": {...}}

# POST /agents/llm-providers/gemini
# Process prompts using Google's Gemini models
# Request: {"prompt": "text", "model": "gemini-2.0", "max_tokens": 100, "temperature": 0.7}
# Response: {"status": "success", "message": "...", "model": "gemini-2.0", "usage": {...}}

# POST /agents/llm-providers/requestry
# Process prompts using Requestry's model routing
# Request: {"prompt": "text", "model": "cline/o3-mini", "max_tokens": 100, "temperature": 0.7}
# Response: {"status": "success", "message": "...", "model": "cline/o3-mini", "usage": {...}}

# POST /agents/llm-providers/openrouter
# Process prompts using OpenRouter's model marketplace
# Request: {"prompt": "text", "model": "openai/gpt-4o", "max_tokens": 100, "temperature": 0.7}
# Response: {"status": "success", "message": "...", "model": "openai/gpt-4o", "usage": {...}}

# POST /agents/llm-providers/recommend-model
# Get model recommendations based on task requirements
# Request: {"task_type": "reasoning", "prompt_length": 200}
# Response: {"provider": "openai", "model": "gpt-4o", "reasoning": "..."}
```

---

## Working with the Code

### LLM Providers Directory (`app/agents/llm_providers/`)
```plaintext
llm_providers/
├── __init__.py
├── base_llm_agent.py       # Base class for all LLM providers
├── openai_agent.py         # OpenAI implementation
├── gemini_agent.py         # Google Gemini implementation
├── requestry_agent.py      # Requestry implementation
├── openrouter_agent.py     # OpenRouter implementation
└── recommender_agent.py    # Model recommendation system
```

### Router Implementation (`app/routers/llm_router.py`)
```plaintext
llm_router.py
├── router                  # FastAPI router
├── openai_endpoint         # OpenAI provider endpoint
├── gemini_endpoint         # Gemini provider endpoint
├── requestry_endpoint      # Requestry provider endpoint
├── openrouter_endpoint     # OpenRouter provider endpoint
└── recommend_model         # Model recommendation endpoint
```

### Tools Directory (`app/tools/`)
The tools directory from previous modules is maintained for reference and potential use in provider implementations.

---

## Testing Your Implementation

We've provided comprehensive tests for all LLM providers:

```bash
# Test OpenAI agent
python -m pytest tests/test_openai_agent.py

# Test Gemini agent
python -m pytest tests/test_gemini_agent.py

# Test Requestry agent
python -m pytest tests/test_requestry_agent.py

# Test OpenRouter agent
python -m pytest tests/test_openrouter_agent.py

# Test model recommender
python -m pytest tests/test_recommender_agent.py

# Run all tests
python -m pytest tests/
```

Key test scenarios include:
- API key validation
- Model availability checking
- Error handling for rate limits and invalid requests
- Response format consistency across providers
- Model recommendation accuracy

---

## Tips for Success

1. **API Key Management:**
   - Store API keys in environment variables
   - Never hardcode keys in your code
   - Implement proper error handling for missing keys

2. **Provider Consistency:**
   - Create a consistent interface across providers
   - Standardize response formats
   - Handle provider-specific errors gracefully

3. **Common Pitfalls to Avoid:**
   - Assuming all providers have the same features
   - Forgetting to handle rate limits
   - Not validating model names before requests
   - Ignoring provider-specific response formats

---

## Practical Exercises

1. **Basic Provider Exercise:**
   - Add support for additional OpenAI models
   - Implement streaming responses for compatible providers
   - Create a unified error handling system

2. **Advanced Provider Exercise:**
   - Add a new LLM provider (e.g., Anthropic, Cohere)
   - Implement provider-specific features while maintaining the common interface
   - Create a fallback system that tries alternative providers when one fails

3. **Model Recommender Exercise:**
   - Enhance the recommender to consider cost factors
   - Add support for specialized task types (e.g., code generation, creative writing)
   - Implement a learning system that improves recommendations based on feedback

4. **Integration Exercise:**
   - Create a unified chat interface that can switch between providers
   - Implement a system that distributes requests across providers for load balancing
   - Build a dashboard that compares responses from different providers for the same prompt

---

## Next Steps

After completing this module, you'll have a flexible system that can work with multiple LLM providers. This foundation will allow you to:

- Choose the best model for different tasks
- Reduce dependency on a single provider
- Optimize for cost, performance, or specialized capabilities
- Easily integrate new providers as they become available

Remember:
- Review the provider documentation for updates
- Test with different model parameters
- Monitor usage and costs across providers
- Keep your API keys secure

---

*Keep building and exploring! The multi-provider approach you're learning here gives you flexibility and resilience in your AI systems.*

*- Bradley Ross*
