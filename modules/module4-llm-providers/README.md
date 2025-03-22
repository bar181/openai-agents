# Module 4: Custom LLM Providers

This module extends our agent capabilities by integrating multiple LLM providers (OpenAI, Gemini, Requestry, OpenRouter) and implementing a model recommender system to select the most appropriate provider and model for specific tasks.

## Features

### LLM Provider Agents
- **OpenAI Agent:** Support for multiple OpenAI models (gpt-3.5-turbo, gpt-4o, etc.)
- **Gemini Agent:** Integration with Google's Gemini models
- **Requestry Agent:** Support for Requestry's model routing capabilities
- **OpenRouter Agent:** Access to multiple models through OpenRouter's unified API

### Model Recommender
- **Task-Based Selection:** Recommends provider and model based on task type
- **Length-Aware Recommendations:** Considers prompt length for optimal selection
- **Intelligent Mapping:** Maps specific tasks to the most appropriate provider/model combination

### Common Features Across Providers
- **Standardized Interface:** Consistent API across all providers
- **Comprehensive Error Handling:** Robust error management for each provider
- **Usage Tracking:** Token usage statistics for all providers
- **Logging:** Detailed logging for debugging and monitoring

## Project Structure

```plaintext
module4-llm-providers/
├── app/
│   ├── agents/
│   │   └── llm_providers/
│   │       ├── openai_agent.py        # OpenAI integration
│   │       ├── gemini_agent.py        # Google Gemini integration
│   │       ├── requestry_agent.py     # Requestry integration
│   │       ├── openrouter_agent.py    # OpenRouter integration
│   │       └── recommender_agent.py   # Model recommender system
│   ├── routers/
│   │   └── llm_router.py              # Endpoints for all providers
│   └── tools/                         # Inherited tools from Module 3
├── docs/                              # Implementation guides
└── tests/                             # Comprehensive test suite
```

## Getting Started

1. **Environment Setup:**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd openai-agents/modules/module4-llm-providers

   # Create and activate virtual environment (optional)
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   # or
   .\venv\Scripts\activate  # Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configuration:**
   ```bash
   # Copy environment template
   cp .env.sample .env

   # Edit .env with your API keys
   # Required: OPENAI_API_KEY
   # Optional: GEMINI_API_KEY, REQUESTRY_API_KEY, OPENROUTER_API_KEY
   ```

3. **Run the FastAPI Server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

4. **Run Tests:**
   ```bash
   # Run all tests
   python -m pytest tests/

   # Run specific test suites
   python -m pytest tests/test_openai_agent.py
   python -m pytest tests/test_gemini_agent.py
   python -m pytest tests/test_requestry_agent.py
   python -m pytest tests/test_openrouter_agent.py
   python -m pytest tests/test_recommender_agent.py
   ```

5. **Run Health Check:**
   ```bash
   # Check connectivity with all providers
   python tests/health_check.py
   ```

## API Endpoints

### LLM Provider Endpoints
- `POST /agents/llm-providers/openai` - Process prompts with OpenAI models
- `POST /agents/llm-providers/gemini` - Process prompts with Gemini models
- `POST /agents/llm-providers/requestry` - Process prompts with Requestry models
- `POST /agents/llm-providers/openrouter` - Process prompts with OpenRouter models

### Model Recommender Endpoint
- `POST /agents/llm-providers/recommend-model` - Get provider/model recommendations based on task

## Supported Models

### OpenAI
- `gpt-3.5-turbo` - Default model, good balance of performance and cost
- `gpt-4o` - Latest model with advanced capabilities
- `gpt-4-turbo` - Powerful model with strong reasoning capabilities

### Gemini
- `gemini-2.0-pro-exp-02-05` - Default model, experimental version with advanced capabilities
- `gemini-1.5-pro` - Stable model with good performance
- `gemini-1.5-flash` - Faster, more efficient model for simpler tasks
- `gemini-1.0-pro` - Original model, still supported

### Requestry
- `cline/o3-mini` - Default model, efficient and cost-effective
- `cline/4o-mini` - More powerful model with advanced capabilities

### OpenRouter
- `openai/gpt-4o` - Default model, OpenAI's latest model through OpenRouter
- Many other models available through the OpenRouter platform

## Documentation

Detailed documentation is available in the `/docs` directory:
- `implementation_plan.md` - Project structure and implementation strategy
- `implementation_process.md` - Step-by-step implementation guide
- `phase1.md`, `phase2.md`, `phase3.md`, `phase4.md` - Detailed phase documentation
- `guidelines.md` - Coding standards and best practices
- `tutorial.md` - Comprehensive learning guide

## Development Workflow

1. Start with understanding the provider interfaces and standardized response format
2. Explore each provider's unique capabilities and limitations
3. Use the model recommender to optimize provider selection for specific tasks
4. Run health checks to verify connectivity with all providers
5. Consult documentation for detailed guidance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

This module provides a comprehensive framework for integrating multiple LLM providers into your applications, with a smart recommender system to optimize model selection based on task requirements. Through this implementation, you'll gain practical experience in working with diverse AI providers and building systems that can leverage the strengths of each.

For detailed guidance, refer to the tutorial in `/docs/tutorial.md`.