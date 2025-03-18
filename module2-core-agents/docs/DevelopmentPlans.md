# Development Plans - Module 2: Core Research Agents & Advanced Patterns

**Project Title:** Core Research Agents & Advanced Patterns (Module 2)

**Description:**

This module builds upon the foundational "Hello World" agent from Module 1.  It introduces three core research agent patterns: deterministic, handoff (routing), and a combination of both.  The primary goal is to demonstrate how to create agents that can handle complex tasks by breaking them down into smaller steps, delegating to specialized sub-agents, or combining these approaches.

**Plans:**

| Plan                | Description                                                                                                                                                                                                                               |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Deterministic Agent | Breaks a complex task into a sequence of well-defined steps (e.g., generate an outline, then write a story based on the outline, then create an ending).  The agent executes these steps in a predetermined order.                       |
| Handoff Agent       | Employs a triage or routing approach.  This agent analyzes the user's request and delegates the task to a specialized sub-agent based on specific criteria (e.g., the user's requested language, the type of task).                      |
| Combined Agent      | Integrates both deterministic and handoff patterns within a single agent.  This allows for both sequential execution of steps and dynamic delegation to sub-agents, providing a more flexible and powerful agent design.                   |

**Key Objectives:**

*   **Multi-Step Logic:**  Provide a clear demonstration of how to implement agents that perform tasks requiring multiple steps.
*   **Dynamic Delegation:**  Show how to create agents that can intelligently route tasks to specialized sub-agents.
*   **In-Memory State:**  Demonstrate how to maintain state (e.g., partial results, conversation history) within a single agent run to track progress and pass information between steps.
*   **Pattern Combination:**  Illustrate how different agent patterns can be combined to create more versatile and capable agents.
*   **Incremental Development:** Build upon the concepts and code from Module 1, demonstrating a clear progression.