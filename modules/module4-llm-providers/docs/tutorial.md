## Module 4: Custom LLM Providers - Tutorial

### Introduction

Welcome to Module 4! So far, we've explored how Large Language Models (LLMs) like GPT-4 can help create powerful AI agents. Now, it's time to extend this knowledge to other providers such as OpenAI, Gemini, Requestry, and OpenRouter. Each of these platforms has unique strengths, pricing, performance, and API specifics. By the end of this module, you'll confidently integrate multiple custom LLM providers into your AI projects.

### Learning Objectives

In this module, you'll learn to:

- Compare the capabilities and limitations of OpenAI, Gemini, Requestry, and OpenRouter.
- Create custom LLM agents using APIs from multiple providers.
- Develop robust error-handling procedures for API interactions.
- Design a recommendation engine that selects the optimal provider based on specific tasks.
- Test, debug, and integrate custom LLM providers effectively.

### Prerequisites

Make sure you're comfortable with:

- Python programming
- Basic understanding of LLM concepts
- RESTful APIs and HTTP requests
- Writing and running Python tests

### Module Structure

This module unfolds in five clear phases, each building on the previous one:

1. **Environment & Setup**
2. **OpenAI Multi-Model Agent**
3. **Gemini, Requestry, and OpenRouter Agents**
4. **Model Recommender**
5. **Documentation & Final Checks**

Let's get started!

---

## Phase 1: Environment & Setup

Before coding, we'll prepare your workspace. Good preparation ensures smooth coding experiences.

### Step-by-Step Guide

1. **Install Python:**
   - Check your Python version (`python --version`). Ensure it's 3.7 or higher.

2. **Create a Virtual Environment:**
   - Virtual environments isolate dependencies for your project. Create one using:
   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install Dependencies:**
   - Install required packages using the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Project Directory Structure:**
   - Create a directory named `llm-providers`.
   - Inside this directory, copy all relevant files from Module 3 to reuse existing configurations.
   - Within `app/agents`, create:
     - `llm_providers`: To store our new LLM provider agent code.
     - `recommender`: For our recommendation engine.

5. **Set Up the LLM Router:**
   - Create a new file `llm_router.py` in `app/routers`. This file routes API requests to different providers.

6. **Environment Variables:**
   - Create a `.env` file at the root to safely store your API keys:
   ```env
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   REQUESTRY_API_KEY=your_requestry_key
   OPENROUTER_API_KEY=your_openrouter_key
   ```

7. **Logging and Testing:**
   - Implement basic logging using Python's built-in `logging` module.
   - Create placeholder test files for future test cases.

---

## Phase 2: OpenAI Multi-Model Agent

Now, let's create an agent that supports various OpenAI models.

### Implementation Steps

1. **OpenAI Agent Creation:**
   - In `app/agents/llm_providers`, create `openai_agent.py`.
   - Define an `OpenAIAgent` class to interface with OpenAI's API.
   - Support multiple models like `gpt-4o`, `gpt-4o-mini`, and `o3-mini`.

2. **Error Handling:**
   - Ensure your agent gracefully handles common API errors (e.g., rate limits, invalid API keys).
   - Provide clear, standardized responses indicating success or specific errors.

3. **Testing the Agent:**
   - Create comprehensive unit tests in `test_openai_agent.py` under the `tests` folder.
   - Use mock responses to simulate OpenAI's API.

4. **Integrating into Router:**
   - In `llm_router.py`, add endpoints that route API requests to the OpenAI agent.
   - Use Pydantic models for data validation.

---

## Phase 3: Gemini, Requestry, OpenRouter Agents

Repeat similar steps for Gemini, Requestry, and OpenRouter, ensuring each agent is robust and standardized.

### Key Points:

- Create separate agent files (`gemini_agent.py`, `requestry_agent.py`, `openrouter_agent.py`).
- Each agent class handles API-specific requirements.
- Implement consistent error handling.
- Write thorough unit tests for each provider.
- Add endpoints in `llm_router.py` to route requests appropriately.

---

## Phase 4: Model Recommender

This exciting phase will help your system select the most suitable provider based on the task.

### Implementing the Recommender:

- Create `recommender_agent.py` in `app/agents/recommender`.
- Develop logic (simple rules or AI-driven decision-making) that analyzes task requirements (e.g., speed, accuracy, complexity).
- Return recommended providers and models.

### Testing:

- Write tests in `test_recommender_agent.py`.
- Check multiple scenarios to validate recommendations.

---

## Phase 5: Documentation & Final Checks

Good documentation and thorough testing ensure reliability and maintainability.

### Documentation Steps:

- Clearly document every phase (`phase1.md` to `phase5.md`).
- Update your main `README.md`.
- Keep track of progress with an `implementation_process.md`.

### Final Testing:

- Run the complete test suite.
- Document results, categorizing and prioritizing issues clearly.
- Fix or recommend solutions based on severity and impact.

### Code Review:

- Check for PEP 8 compliance (clean, readable Python code).
- Securely handle API keys and sensitive data.
- Ensure documentation is accurate and user-friendly.

### Preparing for Release:

- Merge finalized code into your main branch.
- Perform final verification and release prep.


---

### Conclusion

Congratulations on completing Module 4! You've built practical knowledge to handle diverse LLM providers and developed critical skills for creating sophisticated, multi-provider AI agents. Continue exploring resources provided, and remember, we're here to support you every step of the way!