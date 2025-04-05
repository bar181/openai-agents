# refactor existing modules:
existing module 2 separated into 3 separate madules.

Basic Agents Module:

Contains only agents that handle simple prompt processing without invoking external tools.

Focuses solely on core agent lifecycle, dynamic prompt handling, and basic execution.

Tools Module:

Dedicated solely to the implementation and exposure of common tools (like math operations, string manipulation, etc.).

Exposes endpoints (if needed) and maintains a unified tool registry for consistency.

Advanced Agents Module:

Integrates the tools into agent logic.

Uses a tool registry or dependency injection to call tools as part of their processing workflow.

Incorporates complex behaviors like multi-step workflows, chaining tool calls, etc.

Guardrails/Handoffs Module:

Focuses on advanced functionalities such as guardrails, handoffs, dynamic instructions, and other higher-order features.