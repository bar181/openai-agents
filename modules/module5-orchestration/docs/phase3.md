# Module 5 – Phase 3: Implement Agent Handoffs

In **Phase 3** of Module 5, we focus on implementing agent handoffs to enable seamless task delegation between agents using the OpenAI Agents SDK. This phase ensures that tasks are handled by the most appropriate agent based on the context, enhancing the system's efficiency and responsiveness.

---

## Overview

**Objective:** Enable agents to delegate tasks to other specialized agents through handoff mechanisms, ensuring seamless task delegation and efficient handling of user requests.

**Key Components:**

1. **Define Handoff Mechanisms:**
   - Utilize the `handoff()` function from `handoffs.py` to create handoff instances.
   - Specify the target agent and the conditions under which the handoff should occur.

2. **Implement Handoffs in Agents:**
   - Integrate handoff logic within agent definitions to delegate tasks when necessary.
   - Ensure that the handoff process maintains the context and history of the conversation.

3. **Utilize Message Filtering:**
   - Leverage `message_filter.py` and `message_filter_streaming.py` to manage and filter messages during the handoff process.
   - Ensure that only relevant information is passed to the receiving agent, maintaining efficiency and clarity.

---

## Step-by-Step Implementation

### Step 1: Define Specialized Agents

**Goal:** Create agents specialized in handling specific tasks.

**Implementation:**


```python
from agents import Agent

# Define specialized agents
billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle billing inquiries."
)

technical_support_agent = Agent(
    name="Technical Support Agent",
    instructions="You handle technical support issues."
)
```


**Notes:**

- Each agent is defined with a unique name and specific instructions outlining its responsibilities.

---

### Step 2: Define Triage Agent with Handoff Capabilities

**Goal:** Create a triage agent that delegates tasks to specialized agents based on the nature of the inquiry.

**Implementation:**


```python
from agents import Agent, handoff

# Define triage agent with handoff capabilities
triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine the nature of the inquiry and handoff to the appropriate agent.",
    handoffs=[billing_agent, technical_support_agent]
)
```


**Notes:**

- The `handoffs` parameter specifies the agents to which tasks can be delegated.
- The triage agent assesses the user's input and delegates the task to the appropriate specialized agent based on the inquiry's nature.

---

### Step 3: Implement Message Filtering During Handoffs

**Goal:** Ensure that only relevant information is passed to the receiving agent during a handoff.

**Implementation:**


```python
from agents import message_filter

# Define a message filter function
def filter_relevant_messages(messages):
    # Implement logic to filter messages
    return filtered_messages

# Apply message filter during handoff
handoff_agent = handoff(
    agent=technical_support_agent,
    input_filter=filter_relevant_messages
)
```


**Notes:**

- The `input_filter` parameter in the `handoff()` function allows specifying a function to filter messages during the handoff process.
- This ensures that the receiving agent gets only the pertinent information needed to handle the task.

---

### Step 4: Integrate Handoff Logic in Agent Workflow

**Goal:** Incorporate handoff logic within the agent's workflow to delegate tasks appropriately.

**Implementation:**


```python
from agents import Runner
import asyncio

async def main():
    user_input = "I have a question about my latest invoice."
    result = await Runner.run(triage_agent, input=user_input)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```


**Notes:**

- The `Runner.run()` function executes the agent's workflow, processing the user input and handling any necessary handoffs.
- The triage agent evaluates the input and delegates the task to the appropriate specialized agent.

---

## Relevant SDK Files

- **`handoffs.py`**: Contains the `handoff()` function and related classes to facilitate task delegation between agents.
- **`message_filter.py` and `message_filter_streaming.py`**: Provide utilities to filter and manage messages during the handoff process, ensuring that agents receive only pertinent information.

---

## Completion & Next Steps

**Phase 3** completes when:

- Specialized agents are defined with clear responsibilities.
- The triage agent is capable of delegating tasks to specialized agents based on the inquiry's nature.
- Message filtering is implemented to ensure efficient and relevant communication between agents during handoffs.

Next up: **Phase 4** – Implementing comprehensive tracing for guardrails and handoffs to enhance monitoring and debugging capabilities.

---

**Congratulations on completing Phase 3!** 