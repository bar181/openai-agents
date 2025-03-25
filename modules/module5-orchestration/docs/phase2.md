## Module 5 – Phase 2: Input & Output Guardrails

Welcome to **Phase 2** of Module 5. In this phase, we'll focus on implementing input and output guardrails using the OpenAI Agents SDK. Guardrails are essential for validating user inputs and agent outputs, ensuring they meet predefined safety and compliance standards. We'll also develop unit tests to verify the functionality of these guardrails.

---

## Overview

**Objective:** Enhance the robustness of our agents by:

1. **Implementing Input Guardrails:**
   - Validate user inputs before processing.
   - Utilize the `@input_guardrail()` decorator from the OpenAI Agents SDK.

2. **Implementing Output Guardrails:**
   - Validate agent outputs before they're returned to the user.
   - Ensure outputs adhere to safety and compliance rules.

3. **Writing Unit Tests:**
   - Develop tests in `tests/test_orchestration.py` to verify guardrail functionality.

**Relevant SDK Files:**
- `guardrail.py`
- `agent.py`
- `agent_output.py`

---

## Step-by-Step Implementation

### Step 1: Implement Input Guardrails

**Goal:** Ensure that all user inputs are validated before being processed by the agent.

**Implementation:**

1. **Define the Input Guardrail Function:**
   - Create a function that checks the validity of user inputs.
   - Use the `@input_guardrail()` decorator to designate it as an input guardrail.

   ```python
   from agents import input_guardrail, RunContextWrapper, Agent
   from agents.guardrail import GuardrailResult

   @input_guardrail()
   async def validate_user_input(context: RunContextWrapper, agent: Agent, user_input: str) -> GuardrailResult:
       # Implement validation logic here
       if not user_input or len(user_input.strip()) == 0:
           return GuardrailResult(tripwire_triggered=True, message="Input cannot be empty.")
       # Add additional validation as needed
       return GuardrailResult(tripwire_triggered=False)
   ```

   *Note:* The `input_guardrail()` decorator transforms the function into an `InputGuardrail`, which runs in parallel to the agent's execution to validate inputs. citeturn0search0

2. **Integrate the Input Guardrail with the Agent:**
   - When initializing the agent, include the input guardrail.

   ```python
   from agents import Agent

   agent = Agent(
       name="YourAgentName",
       instructions="Your agent instructions here.",
       input_guardrails=[validate_user_input],
       # Other agent configurations
   )
   ```

   *Note:* The `input_guardrails` parameter accepts a list of input guardrail functions to be applied to the agent.

---

### Step 2: Implement Output Guardrails

**Goal:** Ensure that all agent outputs are validated before being returned to the user.

**Implementation:**

1. **Define the Output Guardrail Function:**
   - Create a function that checks the validity of agent outputs.
   - Use the `@output_guardrail()` decorator to designate it as an output guardrail.

   ```python
   from agents import output_guardrail, RunContextWrapper, Agent
   from agents.guardrail import GuardrailResult

   @output_guardrail()
   async def validate_agent_output(context: RunContextWrapper, agent: Agent, agent_output: Any) -> GuardrailResult:
       # Implement validation logic here
       if "error" in agent_output:
           return GuardrailResult(tripwire_triggered=True, message="Agent output contains an error.")
       # Add additional validation as needed
       return GuardrailResult(tripwire_triggered=False)
   ```

   *Note:* The `output_guardrail()` decorator transforms the function into an `OutputGuardrail`, which runs on the final output of the agent to ensure it meets validation criteria. citeturn0search0

2. **Integrate the Output Guardrail with the Agent:**
   - When initializing the agent, include the output guardrail.

   ```python
   from agents import Agent

   agent = Agent(
       name="YourAgentName",
       instructions="Your agent instructions here.",
       output_guardrails=[validate_agent_output],
       # Other agent configurations
   )
   ```

   *Note:* The `output_guardrails` parameter accepts a list of output guardrail functions to be applied to the agent.

---

### Step 3: Write Unit Tests

**Goal:** Develop unit tests to verify the functionality of the input and output guardrails.

**Implementation:**

1. **Create the Test File:**
   - Ensure the test file `tests/test_orchestration.py` exists. If not, create it.

2. **Write Tests for Input Guardrails:**
   - Test scenarios where the input guardrail should trigger and where it should pass.

   ```python
   import pytest
   from agents import Agent
   from your_module import validate_user_input

   @pytest.mark.asyncio
   async def test_input_guardrail_empty_input():
       agent = Agent(
           name="TestAgent",
           instructions="Test instructions.",
           input_guardrails=[validate_user_input],
       )
       with pytest.raises(Exception) as exc_info:
           await agent.run("")
       assert "Input cannot be empty." in str(exc_info.value)

   @pytest.mark.asyncio
   async def test_input_guardrail_valid_input():
       agent = Agent(
           name="TestAgent",
           instructions="Test instructions.",
           input_guardrails=[validate_user_input],
       )
       result = await agent.run("Valid input")
       assert result is not None
   ```

3. **Write Tests for Output Guardrails:**
   - Test scenarios where the output guardrail should trigger and where it should pass.

   ```python
   import pytest
   from agents import Agent
   from your_module import validate_agent_output

   @pytest.mark.asyncio
   async def test_output_guardrail_error_in_output():
       agent = Agent(
           name="TestAgent",
           instructions="Test instructions.",
           output_guardrails=[validate_agent_output],
       )
       # Mock agent to return an output containing 'error'
       agent.run = AsyncMock(return_value={"error": "Some error"})
       with pytest.raises(Exception) as exc_info:
           await agent.run("Some input")
       assert "Agent output contains an error." in str(exc_info.value)

   @pytest.mark.asyncio
   async def test_output_guardrail_valid_output():
       agent = Agent(
           name="TestAgent",
           instructions="Test instructions.",
           output_guardrails=[validate_agent_output],
       )
       # Mock agent to return a valid output
       agent.run = AsyncMock(return_value={"result": "Valid output"})
       result = await agent.run("Some input")
       assert result == {"result": "Valid output"}
   ```

   *Note:* Replace `your_module` with the actual module name where `validate_user_input` and `validate_agent_output` are defined. Also, ensure that `AsyncMock` is imported from `unittest.mock` for mocking asynchronous functions.

---

## Notes and Comments

- **Understanding Guardrails:**
  - Input guardrails validate user inputs before the agent processes them, ensuring they meet certain criteria.
  - Output guardrails validate the agent's outputs before they're returned to the user, ensuring they adhere to safety and compliance standards 