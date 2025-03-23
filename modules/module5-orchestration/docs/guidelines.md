# Guidelines for Module 5 — Orchestration (Guardrails, Handoffs, Tracing)

This document outlines coding and design standards for Module 5, which covers advanced orchestration techniques including guardrails, agent handoffs, and tracing.

---

## 1. Naming and Project Structure

- Place orchestration-related agents and components under:
  ```
  app/agents/orchestration/
  ```
  Example filenames:
  ```
  input_guardrail_agent.py
  output_guardrail_agent.py
  triage_agent.py
  specialized_agents.py
  ```

- FastAPI routers should be organized within:
  ```
  app/routers/orchestration_router.py
  ```

- Define consistent guardrail and handoff interfaces:
  ```python
  class BaseGuardrail:
      async def run_guardrail(self, context, agent_input):
          raise NotImplementedError("Implement guardrail logic.")

  class BaseHandoff:
      async def invoke_handoff(self, context, agent_input):
          raise NotImplementedError("Implement handoff logic.")
  ```

---

## 2. Endpoint Conventions

Define clear endpoints in `orchestration_router.py`:

1. **POST** `/agents/orchestration/triage`
2. **POST** `/agents/orchestration/handoff`
3. **POST** `/agents/orchestration/input-guardrail`
4. **POST** `/agents/orchestration/output-guardrail`

Maintain a consistent request/response schema structure:

- Request Example:
```json
{
  "message": "User input message to the agent.",
  "context": {"session_id": "abc123"}
}
```

- Response Example:
```json
{
  "status": "success",
  "response": "Agent response message.",
  "guardrail_triggered": false,
  "handoff_agent": "MathTutorAgent",
  "trace_id": "trace-xyz-789"
}
```

---

## 3. Testing Conventions

Create comprehensive tests for orchestration functionality in the `tests/` directory:
- `test_input_guardrail.py`
- `test_output_guardrail.py`
- `test_handoff.py`
- `test_tracing.py`

Write tests **prior to implementation**:
1. Define clear scenarios and expected outcomes.
2. Mock external API calls or complex agent interactions.
3. Ensure coverage for guardrail triggers, successful handoffs, and tracing logs.

---

## 4. Logging and Error Handling

- Utilize Python’s built-in logging consistently:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Running guardrail check...")
```

- Standardize API error responses:
```json
{
  "status": "error",
  "message": "Guardrail validation failed.",
  "details": "Input not related to homework."
}
```

- Catch specific exceptions for guardrails and handoffs:
  - `InputGuardrailTripwireTriggered`
  - `OutputGuardrailTripwireTriggered`
  - `HandoffError`

---

## 5. Implementation Flow

Follow a structured implementation approach:

1. **Draft tests** for guardrails, handoffs, and tracing.
2. **Implement guardrail agents**:
   - Input guardrail (validate incoming requests).
   - Output guardrail (validate outgoing responses).
3. **Implement triage and handoff agents**.
4. **Add tracing functionality** to log agent execution flow.
5. **Refine documentation** and continuously update:
   - `docs/implementation_process.md`
   - `README.md`

---

## 6. Style Checks

- Adhere strictly to PEP 8 formatting (use tools like `black` or `flake8`).
- Annotate all functions and methods with type hints.
- Use consistent docstring format:
  ```python
  """
  Args:
      input_message (str): The user's input message.
  Returns:
      GuardrailFunctionOutput: The result of the guardrail check.
  Raises:
      ValueError: If input_message is invalid.
  """
  ```

- Minimize the use of "the" and "its" in user-facing documentation and responses.

---

## 7. Tracing and Debugging

- Implement tracing with the OpenAI SDK tracing system:
```python
from agents import trace

with trace("Orchestration Trace"):
    result = await Runner.run(agent, input_message)
```

- Define custom trace processors if needed for advanced logging or external monitoring.

---

## 8. Future Expansions

- Additional specialized guardrails and handoffs.
- Enhanced tracing processors for integration with monitoring systems.
- Expanded tests for complex multi-agent orchestration scenarios.