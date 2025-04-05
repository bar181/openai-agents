# Module 4: Custom LLM Providers

Welcome to Module 4, where you'll learn how to expand the capabilities of your AI agents by integrating multiple custom Large Language Model (LLM) providers—OpenAI, Gemini, Requestry, and OpenRouter—and implement an intelligent recommender system to select the most suitable provider and model for different tasks.

---

## What You'll Learn

By completing this module, you'll be able to:

- Integrate multiple popular LLM providers into your applications.
- Design and implement an intelligent recommender system to select the optimal provider based on specific tasks and prompt characteristics.
- Apply best practices in API integration, robust error handling, logging, and performance tracking.

---

## Key Features

### LLM Provider Agents

- **OpenAI Agent:** Supports various OpenAI models, such as `gpt-4o-mini` and `gpt-4-turbo`, for flexible, powerful text generation.
- **Gemini Agent:** Integrates Google's Gemini models, offering advanced and experimental AI capabilities.
- **Requestry Agent:** Leverages Requestry’s efficient routing for optimized model selection.
- **OpenRouter Agent:** Provides unified access to a wide array of models through OpenRouter’s API.

### Model Recommender System

- **Task-Based Recommendations:** Automatically selects the best provider and model based on the nature of the task.
- **Length-Aware Decisions:** Considers prompt length and complexity to improve performance and cost-efficiency.
- **Adaptive Logic:** Implements dynamic decision-making to maximize effectiveness across different scenarios.

### Common Integration Features

- **Unified Interface:** Consistent API structure across all LLM providers.
- **Error Handling:** Robust, standardized responses to errors from all providers.
- **Usage Tracking:** Detailed tracking and reporting of token usage.
- **Comprehensive Logging:** Enhanced debugging and operational monitoring.

---

## Project Structure

```plaintext
module4-llm-providers/
├── app/
│   ├── agents/
│   │   └── llm_providers/
│   │       ├── openai_agent.py        # Handles OpenAI integrations
│   │       ├── gemini_agent.py        # Handles Gemini integrations
│   │       ├── requestry_agent.py     # Handles Requestry integrations
│   │       ├── openrouter_agent.py    # Handles OpenRouter integrations
│   │       └── recommender_agent.py   # Intelligent model recommender
│   ├── routers/
│   │   └── llm_router.py              # API endpoints for providers
│   └── tools/                         # Shared utilities from Module 3
├── docs/                              # Implementation and tutorial guides
└── tests/                             # Test suites for validation
```

---

## Getting Started

Follow these steps to set up your development environment:

### 1. Environment Setup

```bash
git clone <repository-url>
cd openai-agents/modules/module4-llm-providers

python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
.\venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Configuration

```bash
cp .env.sample .env
# Update your API keys in the .env file
```

### 3. Run the Application

```bash
python -m uvicorn app.main:app --reload
```

### 4. Testing

```bash
python -m pytest tests/
```

### 5. Provider Health Check

```bash
python tests/health_check.py
```

---

## API Endpoints

### Provider-Specific Endpoints

- **OpenAI:** `POST /agents/llm-providers/openai`
- **Gemini:** `POST /agents/llm-providers/gemini`
- **Requestry:** `POST /agents/llm-providers/requestry`
- **OpenRouter:** `POST /agents/llm-providers/openrouter`

### Recommender Endpoint

- **Model Recommendation:** `POST /agents/llm-providers/recommend-model`

---

## Supported Models Overview

- **OpenAI:** `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`
- **Gemini:** `gemini-2.0-pro-exp-02-05`, `gemini-1.5-pro`, `gemini-1.5-flash`
- **Requestry:** `cline/o3-mini`, `cline/4o-mini`
- **OpenRouter:** `openai/gpt-4o` and many additional models

---

## Documentation

In-depth documentation is available in the `/docs` directory:

- **Implementation:** Step-by-step instructions (`implementation_process.md`)
- **Phase Details:** `phase1.md` to `phase5.md`
- **Testing Analysis:** Detailed test results (`test_work.md`)
- **Guidelines:** Coding best practices (`guidelines.md`)
- **Tutorial:** Comprehensive learning tutorial (`tutorial.md`)

---

## Development Workflow

- Familiarize yourself with provider documentation.
- Integrate providers individually, ensuring consistent response handling.
- Leverage the recommender system to optimize provider use.
- Continuously test integrations and recommender effectiveness.

---

## Contributing

1. Fork and clone the repository.
2. Create your feature branch.
3. Commit and push changes.
4. Submit a Pull Request for review.

---

## License

Licensed under MIT. See the LICENSE file for details.

---

By engaging with this module, you'll deepen your understanding of how to strategically integrate diverse AI capabilities into real-world applications, ensuring optimal performance tailored specifically to your project's needs.