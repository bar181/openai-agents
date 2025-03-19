Below is a sample `guidance.md` file that outlines the best practices and details on how to structure your monorepo, with extra emphasis on routers, agents, dependencies, and configuration.

---

```markdown
# Guidance for Structuring the FastAPI Agent Monorepo

This document outlines the recommended structure and best practices for organizing your monorepo as a self-paced course. The goal is to keep each module self-contained while sharing common resources and guidance across modules.

---

## 1. Monorepo Structure

Organize your repository into distinct top-level directories:

- **modules/**: Contains each module as a separate folder. Each module holds its own application code, tests, and module-specific documentation.
- **tutorials/**: Contains detailed, step-by-step tutorials for each module.
- **common/**: Stores shared resources like guidance documents and code snippets that are used across modules.
- **plans/**: Contains implementation plans and phase documents for each module.

### Example Directory Layout

```
monorepo/
├── modules/
│   ├── module1/
│   │   ├── app/
│   │   │   ├── agents/
│   │   │   │   └── hello_world_agent.py
│   │   │   ├── routers/
│   │   │   │   └── hello_world_router.py
│   │   │   ├── config.py
│   │   │   ├── dependencies.py
│   │   │   ├── main.py
│   │   │   └── models.py
│   │   ├── docs/
│   │   │   ├── guidance.md   # Module-specific guidance (optional)
│   │   │   ├── tutorial.md
│   │   │   └── code_snippets/
│   │   ├── tests/
│   │   │   └── test_hello_world.py
│   │   └── requirements.txt
│   ├── module2/
│   │   └── ... (similar structure as module1)
│   └── ...
├── tutorials/
│   ├── module1/
│   │   └── tutorial.md
│   ├── module2/
│   │   └── tutorial.md
│   └── ...
├── common/
│   ├── guidance.md         # Global guidance and best practices
│   └── code_snippets/
│       ├── snippet1.py
│       └── snippet2.py
└── plans/
    ├── module1/
    │   ├── phase1.md
    │   ├── phase2.md
    │   └── ...
    ├── module2/
    │   └── ...
    └── ...
```

---

## 2. Application Code Structure

### Agents (app/agents/)

- **Purpose**: Each agent encapsulates its own logic and is self-contained.  
- **Best Practice**: One agent per file.
- **Example: `hello_world_agent.py`**

  ```python
  from agents import Agent, Runner, function_tool

  @function_tool
  def hello_world_tool() -> str:
      """Returns a 'Hello, world!' string."""
      return "Hello, world!"

  # Create the agent using the function_tool-decorated function.
  hello_agent = Agent(
      name="HelloAgent",
      instructions="You are a friendly agent that greets the user.",
      tools=[hello_world_tool],
  )

  async def run_hello_agent(user_message: str) -> str:
      """
      Runs the hello_agent with the provided user message using an async runner.
      Returns the final output from the agent.
      """
      try:
          result = await Runner.run(hello_agent, user_message)
          return result.final_output if result else "Error: No response from agent."
      except Exception as e:
          return f"Error: {str(e)}"
  ```

### Routers (app/routers/)

- **Purpose**: Expose agent functionality via API endpoints.
- **Best Practice**: One router per agent, grouping endpoints logically (e.g., `/agents/simple/`).
- **Example: `hello_world_router.py`**

  ```python
  from fastapi import APIRouter, Depends, HTTPException
  from pydantic import BaseModel, Field
  from app.dependencies import verify_api_key
  from app.agents.hello_world_agent import run_hello_agent

  router = APIRouter()

  class HelloRequest(BaseModel):
      message: str = Field(..., description="The user's message to the agent.")

  class HelloResponse(BaseModel):
      response: str = Field(..., description="The agent's response.")

  @router.post("/hello", response_model=HelloResponse, dependencies=[Depends(verify_api_key)])
  async def hello_endpoint(request: HelloRequest):
      """
      A simple endpoint that greets the user using the Hello World agent.
      """
      agent_response = await run_hello_agent(request.message)
      if agent_response.startswith("Error"):
          raise HTTPException(status_code=500, detail=agent_response)
      return {"response": agent_response}
  ```

### Main Application (app/main.py)

- **Purpose**: Bootstraps the FastAPI application and includes all routers.
- **Example:**

  ```python
  from fastapi import FastAPI
  from app.routers import hello_world_router  # Import additional routers as needed

  app = FastAPI(title="FastAPI Agent System", version="1.0.0")

  # Group endpoints under logical prefixes.
  app.include_router(hello_world_router.router, prefix="/agents/simple")

  @app.get("/")
  async def root():
      return {"message": "FastAPI Agent System Running"}
  ```

---

## 3. Dependencies and Configuration

### Dependencies (app/dependencies.py)

- **Purpose**: Defines reusable dependencies (e.g., authentication).
- **Example:**

  ```python
  from fastapi import HTTPException, Security
  from fastapi.security import APIKeyHeader
  from app.config import API_KEY

  api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

  def verify_api_key(api_key: str = Security(api_key_header)):
      if api_key is None or api_key != API_KEY:
          raise HTTPException(status_code=401, detail="Unauthorized")
      return True
  ```

### Configuration (app/config.py)

- **Purpose**: Manages environment variables and configuration settings.
- **Example:**

  ```python
  import os
  from dotenv import load_dotenv

  load_dotenv()

  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
  API_KEY = os.getenv("API_KEY")

  if not OPENAI_API_KEY:
      raise ValueError("Error: OPENAI_API_KEY is missing. Please set it in .env.")
  if not API_KEY:
      raise ValueError("Error: API_KEY is missing. Please set it in .env.")
  ```

---

## 4. Best Practices

- **Modularity**: Keep each agent self-contained. Expose only necessary methods to the routers.
- **Minimal Imports**: Limit dependencies to what is strictly necessary. Ensure that `requirements.txt` includes only essential packages.
- **Clear Documentation**: Include comprehensive docstrings and comments in each file. Provide both in-code documentation and external guidance via markdown files.
- **Logical Grouping**: Use API route prefixes to group related endpoints (e.g., `/agents/simple` for simple agents and `/agents/complex` for more advanced workflows).
- **Testing**: Write unit tests for agents and routers to ensure reliable functionality.
- **Shared Resources**: Maintain common guidance and code snippets in the root-level `/common` directory to avoid duplication.

---

## 5. Conclusion

By following this guidance, you'll create a maintainable and scalable monorepo that supports a self-paced course on building FastAPI agents. Each module is self-contained yet benefits from centralized documentation and shared best practices, ensuring consistency across the course.

Happy coding!
```

---

This `guidance.md` file should be placed in your root-level `common/` directory. It serves as a central reference for developers and learners, ensuring that every module adheres to the same high standards in structure, documentation, and best practices.