# Guidance - Module 2: Coding Standards, Best Practices, and Project Organization

This document outlines the coding standards, best practices, and project organization guidelines for Module 2.  It ensures consistency, maintainability, and a clear structure for the project.

## Coding Standards and Conventions

*   **File Naming:** Use consistent and descriptive names for agent files:
    *   `deterministic_agent.py`
    *   `routing_agent.py` (or `handoff_agent.py`)
    *   `combined_agent.py`
*   **Function and Variable Names:** Use descriptive names that clearly indicate the purpose of functions and variables (e.g., `generate_outline`, `user_language`, `partial_results`).  Follow Python's snake_case convention.
*   **Docstrings:**  Write comprehensive docstrings for:
    *   All agent classes (explain their overall purpose and behavior).
    *   All key functions (explain their inputs, outputs, and any side effects).
    *   Use reStructuredText or Google style docstrings for compatibility with documentation generators.
*  **Comments**: Use comments to explain complex logic, non-obvious code, and any deviations.

## Project Organization

*   **Agent Logic:**  Place all agent-related code (classes, functions) within the `/app/agents` directory.
*   **Routers:** If you have separate router logic (e.g., for FastAPI endpoints), place it in the `/app/routers` directory.
*   **Unit Tests:** Store all unit tests in the `/tests` directory.  Name test files to correspond to the agent or feature they test (e.g., `tests/test_deterministic_agent.py`).
*   **In-Memory State:** Store in-memory state (partial results, conversation history) within local variables or class attributes.  Minimize coupling between modules by avoiding global variables where possible.  Pass data explicitly between functions or agent steps.

## Best Practices for Agent Development

*   **Single Responsibility Principle:**  Each agent and function should have a single, well-defined purpose.  Avoid creating overly complex agents or functions that do too many things.
*   **Modular Design:** For multi-step logic (deterministic agents), break down the task into separate functions or sub-agents.  This improves readability, testability, and maintainability.
*   **Clear Routing Criteria:**  For routing/triage logic (handoff agents), use simple, well-defined, and easily understandable criteria for delegating tasks to sub-agents.
*   **Code Reuse:**  Reuse code from Module 1 whenever possible (e.g., the `verify_api_key` function, utility functions).  This promotes consistency and demonstrates incremental development.
*   **Error Handling:** Implement robust error handling (using `try...except` blocks) to gracefully handle unexpected situations, especially in multi-step workflows and when interacting with external services or APIs.
* **Logging:** Use a logging library to help with debugging.

## Security & Safety Considerations

*   **Sensitive Data:**  **Never** store sensitive data (API keys, passwords, personal information) directly in the code or commit it to version control.
*   **Environment Variables:** Use environment variables to store API keys and other sensitive configuration settings.
*   **API Key Verification:** Continue to use the `verify_api_key` approach (or a similar secure method) from Module 1 to protect your API endpoints.
*   **Input Validation:**  Carefully validate all user inputs, especially when combining or chaining sub-agents.  This helps prevent injection attacks and ensures the agent behaves as expected.
* **Rate Limiting**: Consider implementing rate limits to prevent abuse.

## Testing & Validation

*   **Unit Tests:** Write thorough unit tests for each new agent (deterministic, routing, combined).  Focus on testing individual components and functions in isolation.
*   **Mocked Data:** Use mocked data or ephemeral in-memory storage (e.g., in-memory databases) to isolate tests from external dependencies and ensure they are repeatable.
*   **Integration Tests:** Create integration tests to verify that the different parts of your system (agents, routers, endpoints) work together correctly.
*   **FastAPI TestClient:** Use the `TestClient` from FastAPI to send requests to your API endpoints and assert that the responses are as expected.  Include tests for both success and error scenarios.
*   **Edge Cases:**  Test edge cases and boundary conditions to ensure your agents handle unexpected inputs or situations gracefully.