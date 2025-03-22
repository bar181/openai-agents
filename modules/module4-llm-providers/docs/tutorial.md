## Module 4: Custom LLM Providers - Tutorial

### Introduction

Welcome to Module 4 of this comprehensive course on building a multi-provider LLM system! In this module, we'll delve into the exciting world of custom LLM providers, focusing on OpenAI, Gemini, Requestry, and OpenRouter. We'll build upon the foundation laid in previous modules and equip you with the skills to integrate these diverse providers into your system.

### Learning Objectives

By the end of this module, you will be able to:

* Understand the capabilities and limitations of each custom LLM provider.
* Implement custom LLM agents for each provider, including API integration and error handling.
* Design and implement a model recommender to suggest the most suitable provider for a given task.
* Integrate custom LLM providers into your existing LLM system.
* Test and debug your implementation to ensure its functionality and robustness.

### Prerequisites

Before embarking on this module, it's essential to have a solid understanding of the following:

* Python programming language
* Basic knowledge of LLMs and their capabilities
* Familiarity with RESTful APIs and HTTP requests
* Experience with testing and debugging code

### Module Structure

This module is divided into five phases, each focusing on a specific aspect of custom LLM provider integration:

**Phase 1: Environment & Setup**

* Setting up the development environment
* Creating the necessary directory structure
* Initializing environment variables for API keys
* Implementing basic logging and testing infrastructure

**Phase 2: OpenAI Multi-Model Agent**

* Implementing an OpenAI agent that supports multiple models
* Handling API errors and providing standardized responses
* Creating comprehensive tests for the OpenAI agent
* Integrating the OpenAI agent into the LLM router

**Phase 3: Gemini, Requestry, OpenRouter Agents**

* Implementing agents for Gemini, Requestry, and OpenRouter
* Integrating these agents into the LLM router
* Handling API errors and providing standardized responses
* Creating comprehensive tests for each agent

**Phase 4: Model Recommender**

* Designing and implementing a model recommender
* Using task-specific information to suggest the most suitable provider
* Testing and validating the recommender's accuracy

**Phase 5: Documentation & Final Checks**

* Writing comprehensive documentation for each phase
* Running full test suite to ensure functionality
* Reviewing logs and code for potential issues
* Merging code into the main branch and preparing for release

### Resources

Throughout this module, you'll have access to various resources to support your learning:

* **Implementation Plan:** This document outlines the detailed steps for each phase, providing a roadmap for your development process.
* **Implementation Process:** This document tracks the progress of each phase, including completed tasks and outstanding items.
* **Phase-specific Tutorials:** Each phase will have its own dedicated tutorial, providing step-by-step instructions and explanations.
* **Code Examples:** You'll find code examples for each phase, demonstrating how to implement the required functionality.
* **Testing Guidelines:** This document provides guidelines for testing your code and ensuring its robustness.
* **Documentation Guidelines:** This document outlines the standards for writing clear and concise documentation.

### References

For further learning and exploration, we recommend the following resources:

* **OpenAI API Documentation:** https://beta.openai.com/docs/api-reference
* **Gemini API Documentation:** https://docs.gemini.ai/
* **Requestry API Documentation:** https://docs.requestry.com/
* **OpenRouter API Documentation:** https://openrouter.ai/docs/
* **OpenAI Agents SDK:** https://github.com/openai/openai-agents-sdk

### Conclusion

By completing this module, you'll gain the knowledge and skills to integrate custom LLM providers into your system, enhancing its capabilities and flexibility. Remember to leverage the provided resources and references to deepen your understanding and explore further. We encourage you to actively participate in discussions and seek clarification whenever needed. Let's embark on this exciting journey together!

### Phase 1: Environment & Setup

#### Setting Up the Development Environment

1. **Install Python:** Ensure you have Python 3.7 or higher installed on your system. You can verify this by running `python --version` in your terminal.
2. **Create a Virtual Environment:** It's recommended to create a virtual environment to isolate your project's dependencies. You can use tools like `venv` or `virtualenv` to create a virtual environment.
3. **Install Required Packages:** Install the necessary Python packages using `pip`. The `requirements.txt` file in the project directory lists the required packages.

#### Creating the Directory Structure

1. **Create a new directory:** Create a new directory for your project, for example, `llm-providers`.
2. **Copy or inherit files:** Copy or inherit all files from Module 3 into the `llm-providers` directory. This will provide you with a basic structure to build upon.
3. **Create new directories:** Create the following directories within the `app/agents` directory:
    * `llm_providers`: This directory will house the custom LLM provider agents.
    * `recommender`: This directory will contain the model recommender agent.
4. **Create a new file:** Create a new file named `llm_router.py` in the `app/routers` directory. This file will handle routing requests to the appropriate LLM provider.

#### Initializing Environment Variables

1. **Create a `.env` file:** Create a file named `.env` in the project's root directory. This file will store your API keys and other environment variables.
2. **Add API keys:** Add the following environment variables to the `.env` file, replacing the placeholders with your actual API keys:
    * `OPENAI_API_KEY`
    * `GEMINI_API_KEY`
    * `REQUESTRY_API_KEY`
    * `OPENROUTER_API_KEY`
3. **Load environment variables:** In your Python code, use the `dotenv` library to load the environment variables from the `.env` file.

#### Implementing Basic Logging and Testing Infrastructure

1. **Configure logging:** Set up basic logging using a library like `logging`. This will help you track the execution of your code and identify any errors.
2. **Create test files:** Create placeholder test files for each LLM provider agent and the model recommender. These files will serve as a starting point for writing comprehensive tests.

### Phase 2: OpenAI Multi-Model Agent

#### Implementing an OpenAI Agent

1. **Create the `openai_agent.py` file:** Create a new file named `openai_agent.py` in the `app/agents/llm_providers` directory.
2. **Implement the `OpenAIAgent` class:** Define a class named `OpenAIAgent` that will handle interactions with the OpenAI API.
3. **Support multiple models:** The `OpenAIAgent` class should support multiple OpenAI models, such as `gpt-4o` and `o3-mini`.
4. **Handle API errors:** Implement robust error handling to catch and handle various API errors, such as missing API keys, authentication errors, and rate limits.
5. **Provide standardized responses:** The agent should return a standardized response format, including the status, message, model used, and usage information.

#### Creating Comprehensive Tests

1. **Create the `test_openai_agent.py` file:** Create a new file named `test_openai_agent.py` in the `tests` directory.
2. **Write tests for valid model usage:** Write tests to ensure that the agent can successfully process prompts using different OpenAI models.
3. **Write tests for missing API key:** Write tests to verify that the agent handles missing API keys gracefully.
4. **Mock API calls:** Use mocking libraries to mock OpenAI API calls for testing purposes.
5. **Test error handling:** Write tests to ensure that the agent handles various API errors correctly.

#### Integrating the OpenAI Agent into the LLM Router

1. **Create an endpoint in `llm_router.py`:** Create an endpoint in the `llm_router.py` file to handle requests for the OpenAI agent.
2. **Use Pydantic models:** Use Pydantic models to validate request and response data, ensuring data integrity.
3. **Implement proper error handling:** Implement HTTP exceptions to handle errors gracefully and provide informative error messages.

### Phase 3: Gemini, Requestry, OpenRouter Agents

#### Implementing Agents for Gemini, Requestry, and OpenRouter

1. **Create agent files:** Create separate files for each provider agent: `gemini_agent.py`, `requestry_agent.py`, and `openrouter_agent.py`.
2. **Implement agent classes:** Define classes for each agent, similar to the `OpenAIAgent` class, handling interactions with their respective APIs.
3. **Handle API errors:** Implement robust error handling for each agent, specific to their APIs.
4. **Provide standardized responses:** Ensure that each agent returns a standardized response format, consistent with the OpenAI agent.

#### Integrating Agents into the LLM Router

1. **Create endpoints in `llm_router.py`:** Create endpoints for each provider agent in the `llm_router.py` file.
2. **Use Pydantic models:** Use Pydantic models for request and response validation for each agent.
3. **Implement proper error handling:** Implement HTTP exceptions for error handling, consistent with the OpenAI agent.

### Phase 4: Model Recommender

#### Designing and Implementing a Model Recommender

1. **Create the `recommender_agent.py` file:** Create a new file named `recommender_agent.py` in the `app/agents/recommender` directory.
2. **Define the recommender class:** Define a class named `RecommenderAgent` that will recommend the most suitable provider for a given task.
3. **Accept task-specific information:** The recommender should accept information about the task, such as the task type and prompt length.
4. **Return recommended provider and model:** The recommender should return the recommended provider and the most suitable model for the given task.
5. **Implement decision logic:** Implement logic to determine the best provider based on the task information. This could involve a simple lookup table or a more sophisticated approach using an LLM.

#### Testing and Validating the Recommender

1. **Create the `test_recommender_agent.py` file:** Create a new file named `test_recommender_agent.py` in the `tests` directory.
2. **Test various scenarios:** Write tests to validate the recommender's accuracy for different task types and prompt lengths.
3. **Validate response format:** Ensure that the recommender returns the expected response format, including the recommended provider and model.

### Phase 5: Documentation & Final Checks

#### Writing Comprehensive Documentation

1. **Document each phase:** Write detailed documentation for each phase, including the implementation details, rationale, and testing procedures.
2. **Update implementation process document:** Update the `implementation_process.md` document to reflect the completion of each phase.
3. **Write guidelines documents:** Write guidelines for testing, documentation, and code style.
4. **Update README.md:** Update the `README.md` file to provide an overview of the project, key references, and installation instructions.

#### Running Full Test Suite

1. **Run all tests:** Run the entire test suite to ensure that all components are functioning correctly.
2. **Review logs:** Review the logs for any potential issues or errors.
3. **Fix any issues:** Address any identified issues and re-run the tests.

#### Reviewing Code and Merging

1. **Review code for PEP 8 compliance:** Ensure that the code adheres to PEP 8 style guidelines.
2. **Merge code into main branch:** Merge the completed code into the main branch of your repository.
3. **Prepare for release:** Prepare the project for release, including creating a distribution package and updating documentation.

### Conclusion

By completing this module, you've gained the knowledge and skills to integrate custom LLM providers into your system, enhancing its capabilities and flexibility. Remember to leverage the provided resources and references to deepen your understanding and explore further. We encourage you to actively participate in discussions and seek clarification whenever needed. Let's embark on this exciting journey together!

### References

* **OpenAI API Documentation:** https://beta.openai.com/docs/api-reference
* **Gemini API Documentation:** https://docs.gemini.ai/
* **Requestry API Documentation:** https://docs.requestry.com/
* **OpenRouter API Documentation:** https://openrouter.ai/docs/
* **OpenAI Agents SDK:** https://github.com/openai/openai-agents-sdk

### Additional Notes

* This tutorial provides a high-level overview of the module. Each phase will have its own dedicated tutorial with more detailed instructions and explanations.
* The provided code examples are for illustrative purposes only. You may need to adapt them to your specific project requirements.
* Don't hesitate to ask questions or seek clarification if anything is unclear. We're here to support your learning journey!
