```markdown
# Phase1a-Hello-World Tutorial

Welcome to Phase1a-Hello-World of our OpenAI Agents tutorial series! In this lesson, we will build a simple "Hello World" agent using FastAPI and the OpenAI Agents SDK. This project is structured as a mono repo where each phase is in its own folder. In this phase, everything is contained within the `phase1a-hello-world` folder.

This tutorial is designed in a teaching-assistant style to guide you through every step. Later phases will follow a similar pattern as we build more sophisticated agents.

---

## 1. Introduction

In this tutorial, you'll learn:
- How to set up your Python environment and install required packages.
- The project structure for our agent system.
- The role of each file in building our "Hello World" agent.
- How to test your agent using unit tests.

We'll explain the conceptual steps first, then provide detailed code snippets and pseudocode for each file.

---

## 2. Prerequisites

Before starting, ensure that you have:
- **Python 3.10+** installed.
- A basic understanding of Python and asynchronous programming.
- An OpenAI API key, which you will set as an environment variable (instructions below).

This tutorial is designed for beginners and uses a friendly TA style to explain every step.

---

## 3. Installation

### Step 3.1: Create a Virtual Environment

Creating a virtual environment sets up your personal workspace and keeps your project dependencies isolated.

Run this command:
```bash
python -m venv env
```
Then activate it:
```bash
source env/bin/activate  # For Linux/macOS
# or on Windows:
env\Scripts\activate
```

### Step 3.2: Install Dependencies

Install the necessary packages. These include FastAPI, Uvicorn, and the OpenAI Agents SDK, along with testing libraries.
```bash
pip install fastapi uvicorn python-dotenv openai pydantic openai-agents pytest pytest-asyncio
```

### Step 3.3: Create the `.env` File

This file will securely hold your sensitive keys. Create a file named `.env` in the root of your project with the following contents:
```dotenv
OPENAI_API_KEY=sk-YourOpenAIKeyHere
API_KEY=mysecretkey
```

---

## 4. Project Structure Overview

For Phase1a-Hello-World, the folder structure is as follows:

```
phase1a-hello-world/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization
│   ├── config.py              # Loads environment variables
│   ├── dependencies.py        # Handles API key authentication
│   ├── agents/
│   │   ├── __init__.py
│   │   └── hello_world_agent.py  # Contains our "Hello World" agent logic
│   └── routers/
│       ├── __init__.py
│       └── hello_world.py     # Exposes the agent via an API endpoint
├── .env                       # Environment variables file
├── requirements.txt           # Lists all project dependencies
├── tests/
│   └── test_hello_world.py    # Unit tests for our agent
├── tutorial.md                # This detailed tutorial (you are reading it now)
└── README.md                  # Project overview and usage instructions
```

**File Roles:**
- **config.py:** Reads environment variables.
- **dependencies.py:** Sets up API key authentication to secure endpoints.
- **hello_world_agent.py:** Implements our "Hello World" agent using the OpenAI Agents SDK.
- **hello_world.py (router):** Connects our agent logic to a FastAPI endpoint.
- **main.py:** Initializes the FastAPI application and includes the routers.
- **tests/test_hello_world.py:** Contains tests to verify our endpoint works as expected.
- **README.md:** Provides an overview of the project and basic usage instructions.

---

## 5. Detailed File Explanations and Code

Below are the complete code snippets (with pseudocode where appropriate) for each file.

### 5.1. `.env`

This file holds your secret keys. **Do not commit this file to public repositories.**
```dotenv
OPENAI_API_KEY=sk-YourOpenAIKeyHere
API_KEY=mysecretkey
```

### 5.2. `requirements.txt`

This file lists all the packages required for the project.
```plaintext
fastapi
uvicorn
python-dotenv
openai
pydantic
openai-agents
pytest
pytest-asyncio
```

### 5.3. `app/config.py`

This file loads environment variables using the `python-dotenv` package.
```python
from dotenv import load_dotenv
load_dotenv()

import os

# Load your API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
API_KEY = os.getenv("API_KEY", "mysecretkey")
```

### 5.4. `app/dependencies.py`

Sets up API key authentication.
```python
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from app.config import API_KEY

# Define the header for API key authentication
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key is None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
```

### 5.5. `app/agents/hello_world_agent.py`

Contains the logic for the "Hello World" agent. We use the `@function_tool` decorator to designate a simple function as a tool.
```python
from agents import Agent, Runner, function_tool

@function_tool
def hello_world_tool() -> str:
    # This tool returns a greeting.
    return "Hello, world!"

# Create the agent by combining instructions and the tool.
hello_agent = Agent(
    name="HelloAgent",
    instructions="You are a friendly agent that greets the user.",
    tools=[hello_world_tool],
)

async def run_hello_agent(user_message: str) -> str:
    """
    Run the HelloAgent with the provided message and return its response.
    """
    try:
        result = await Runner.run(hello_agent, user_message)
        return result.final_output if result else "Error: No response from agent."
    except Exception as e:
        return f"Error: {str(e)}"
```

### 5.6. `app/routers/hello_world.py`

Creates a FastAPI router that exposes our agent through an HTTP POST endpoint.
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
    Endpoint that triggers the Hello World agent.
    """
    agent_response = await run_hello_agent(request.message)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)
    return {"response": agent_response}
```

### 5.7. `app/main.py`

Initializes the FastAPI application and includes the hello_world router.
```python
from fastapi import FastAPI
from app.routers import hello_world

app = FastAPI(title="FastAPI Agent System", version="1.0.0")

# Mount the hello_world router at the /agent path.
app.include_router(hello_world.router, prefix="/agent")

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
```

### 5.8. `tests/test_hello_world.py`

Unit test to verify that the endpoint works correctly. Notice that we include the API key retrieved from our configuration.
```python
from fastapi.testclient import TestClient
from app.main import app
from app.config import API_KEY

client = TestClient(app)

def test_hello_world():
    # Test the hello endpoint with the API key from the .env file.
    response = client.post(
        "/agent/hello",
        json={"message": "Hi from Bradley"},
        headers={"X-API-KEY": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Bradley" in data["response"]
```

---

## 6. Running the Application and Tests

### To Start the Server:
1. Open a terminal and navigate to the `phase1a-hello-world` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server with Uvicorn:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
4. Open your browser and visit [http://localhost:8000/docs](http://localhost:8000/docs) to interact with the API via Swagger UI.

### To Run the Tests:
Run the following command in your terminal:
```bash
python -m pytest tests/
```

---

## 7. Final Remarks

This tutorial has guided you through setting up a mono repo for Phase1a-Hello-World. We covered:
- Environment setup and dependency installation.
- The project structure and role of each file.
- Detailed code for each component.
- How to run and test your application.

This foundation will be used in later phases to create more advanced agents following a similar pattern.

Happy coding, and see you in the next phase!
```

---
