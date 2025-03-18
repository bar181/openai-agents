# Tests - Module 2: Complete Testing Strategy

**Overview:**

Module 2 introduces three new agent patterns: deterministic, routing (handoff), and combined.  This document outlines a comprehensive testing strategy to ensure that each agent functions correctly, including multi-step logic, sub-agent delegation, and in-memory state management.

## Deterministic Agent Tests

*   **Step Execution Order:**  Validate that each step in the deterministic workflow is executed in the *correct* order.  This is crucial for ensuring the agent produces the expected results. *Note:* As mentioned in the `PackagesDetailsForOpenAIAgents.md`, relying solely on the order of tools in the `tools` list is insufficient. Tests must verify the actual execution order based on the agent's behavior.
*   **Partial Result Propagation:** Check that partial results (outputs from each step) are correctly passed as inputs to subsequent steps.
*   **Error Handling:** Test edge cases where a sub-step might:
    *   Return an error.
    *   Return an empty response.
    *   Take an unexpectedly long time to complete (consider timeouts).
*   **Input Validation:** Test with various valid and invalid inputs to check input validation.

## Handoff Agent Tests

*   **Triage Logic:** Confirm that the triage (routing) logic correctly identifies the user's request criteria (e.g., language, task type).
*   **Sub-Agent Delegation:** Ensure that the correct sub-agent receives the appropriate portion of the user's request.
*   **Fallback Behavior:** Verify that fallback or default behaviors are triggered if no sub-agent matches the request criteria.  This prevents the agent from failing completely.
*   **Error Handling:** Test error conditions, such as an invalid sub-agent or a failure in the handoff process.

## Combined Agent Tests

*   **Integration:** Ensure that the combined agent successfully integrates both deterministic and handoff patterns.
*   **Deterministic Sub-Steps:** Validate that sub-steps within the deterministic part of the workflow execute in the correct order.
*   **Delegation:**  Confirm that specific tasks are correctly delegated to specialized sub-agents.
*   **Concurrency/Error Handling:**  If parts of the combined workflow can run concurrently (not explicitly covered in Module 2, but good to consider), test how the agent handles partial failures or errors in one branch of the workflow.
*   **Complex Scenarios:** Test complex scenarios that involve both deterministic steps and handoffs to ensure the agent behaves as expected in more realistic situations.

## In-Memory State Tests

*   **Persistence:** Confirm that in-memory data structures (e.g., dictionaries used for context) correctly persist information across multiple steps within a single agent run.
*   **Reset/Clearance:** Validate that partial results or conversation history are reset or cleared appropriately between test runs (and between different agent invocations) to avoid unintended state leakage.
* **Data Integrity**: Test that the state is not corrupted.

## Integration & Endpoint Tests

*   **FastAPI Endpoints:** Each agent should have a corresponding FastAPI endpoint.
*   **TestClient:**  Use the `TestClient` from FastAPI to send requests to these endpoints.
*   **Response Validation:**  Confirm that the responses from the endpoints match the expected results, including:
    *   Success scenarios (correct outputs).
    *   Error scenarios (appropriate error messages and status codes).
*   **Input Validation (Endpoint Level):**  Test the endpoint's input validation to ensure it rejects invalid requests.

## General Testing Practices

*   **Test-Driven Development (TDD):** Consider writing tests *before* implementing the agent logic.  This helps clarify requirements and ensures testability.
*   **Code Coverage:**  Use code coverage tools to measure the percentage of your code that is covered by tests.  Aim for high code coverage.
*   **Continuous Integration (CI):**  Integrate your tests into a CI/CD pipeline to automatically run tests whenever you make changes to the code.