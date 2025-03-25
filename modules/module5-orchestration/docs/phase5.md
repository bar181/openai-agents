## Module 5 – Phase 5: Advanced Orchestration (Routing and Filtering)

In **Phase 5**, we focus on developing intelligent routing logic and filtering mechanisms to manage tasks across multiple specialized agents effectively. This phase enhances the system's ability to delegate tasks to the most appropriate agent based on the context and content of user inputs.

---

## Objectives

1. **Develop Intelligent Routing Logic:**
   - Implement a triage agent that assesses incoming requests and routes them to specialized agents.
   - Utilize the `handoffs.py` module from the OpenAI Agents SDK to facilitate seamless task delegation.

2. **Implement Message Filtering:**
   - Use `message_filter.py` and `message_filter_streaming.py` to manage and filter messages during the handoff process.
   - Ensure that only relevant information is passed to the receiving agent, maintaining efficiency and clarity.

---

## Implementation Steps

### Step 1: Define Specialized Agents

Create agents tailored to handle specific types of inquiries. Each agent should have clear instructions and capabilities relevant to its specialization.

**Example:**


```python
from agents import Agent

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

### Step 2: Implement the Triage Agent with Routing Logic

Develop a triage agent that evaluates incoming user inputs and determines the appropriate specialized agent for handling the request. Utilize the `handoffs.py` module to facilitate the delegation process.

**Pseudocode:**


```python
from agents import Agent, Runner

triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine the nature of the inquiry and handoff to the appropriate agent.",
    handoffs=[billing_agent, technical_support_agent]
)

# Example usage
result = Runner.run_sync(
    starting_agent=triage_agent,
    input="I have an issue with my latest invoice."
)
```


**Implementation Notes:**
- The triage agent's instructions should be designed to analyze the user's input and decide which specialized agent is best suited to handle the request.
- The `handoffs` parameter specifies the agents to which tasks can be delegated.

### Step 3: Utilize Message Filtering During Handoffs

Implement message filtering to ensure that only pertinent information is passed between agents during the handoff process. This can be achieved using the `message_filter.py` and `message_filter_streaming.py` modules.

**Pseudocode:**


```python
from agents import MessageFilter

# Define a message filter function
def filter_billing_messages(messages):
    # Implement logic to filter messages relevant to billing
    return [msg for msg in messages if "billing" in msg.content.lower()]

# Apply the message filter during handoff
billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle billing inquiries.",
    message_filter=MessageFilter(filter_billing_messages)
)
```


**Implementation Notes:**
- The `MessageFilter` class allows for custom filtering of messages based on defined criteria.
- Ensure that the filtering logic aligns with the specific needs of each specialized agent.

---

## Relevant SDK Files

- **`handoffs.py`**: Contains classes and functions to facilitate task delegation between agents.
- **`message_filter.py` and `message_filter_streaming.py`**: Provide utilities to filter and manage messages during the handoff process, ensuring that agents receive only pertinent information.

---

## Next Steps

With advanced orchestration implemented, proceed to **Phase 6: Final Documentation & Tests**. This phase will focus on documenting the full functionality with clear guidelines and tutorials, as well as creating final integration tests to ensure the orchestration works seamlessly with existing Module 4 features.

---

**Note:** Ensure that all routing and filtering mechanisms are thoroughly tested to maintain the system's reliability and efficiency. 