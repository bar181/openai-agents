# Module 1 - Phase 3: API Router and Endpoint Creation

In Phase 3, you'll create the FastAPI router and define an endpoint to expose your "Hello World" agent functionality via an API. This document will guide you step-by-step through setting up the router and securing it with API key authentication.

---

## Step 1: Creating the Router File

Navigate to `app/routers/` and create a file named `hello_world.py`.

Begin by importing necessary modules:

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.dependencies import verify_api_key
from app.agents.hello_world_agent import run_hello_agent
```

---

## Step 2: Defining Data Models

Define the request and response schemas using Pydantic to validate and document API interactions clearly:

```python
class HelloRequest(BaseModel):
    message: str = Field(..., description="The user's message to the agent.")

class HelloResponse(BaseModel):
    response: str = Field(..., description="The agent's response.")
```

- **Explanation:**
  - Clearly defined request and response structures improve API clarity and data validation.

---

## Step 3: Creating the API Endpoint

Create a router instance and define the endpoint that utilizes your agent:

```python
router = APIRouter()

@router.post("/hello", response_model=HelloResponse, dependencies=[Depends(verify_api_key)])
async def hello_endpoint(request: HelloRequest):
    """
    Endpoint to greet the user via the Hello World agent.
    """
    agent_response = await run_hello_agent(request.message)
    if agent_response.startswith("Error"):
        raise HTTPException(status_code=500, detail=agent_response)

    return {"response": agent_response}
```

- **Explanation:**
  - `POST` method used for secure and structured API interactions.
  - Endpoint secured by verifying the API key with `verify_api_key` dependency.

---

## Step 4: Integrating the Router into the Main Application

In `app/main.py`, include your newly created router:

```python
from fastapi import FastAPI
from app.routers import hello_world

app = FastAPI()

app.include_router(hello_world.router, prefix="/agent")

@app.get("/")
async def root():
    return {"message": "FastAPI Agent System Running"}
```

- **Explanation:**
  - The router is included at a specific prefix (`/agent`) for organized URL structuring.

---

## Step 5: Testing Your Endpoint

Start your FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs):
- Click **Authorize** at the top right corner.
- Enter your API key (`API_KEY` from `.env`) and click **Authorize**.
- Expand the `/agent/hello` endpoint.
- Test the endpoint by submitting a valid message.

You should receive a successful response:

```json
{
  "response": "Hello, world!"
}
```

---

## Completion of Phase 3

Upon completion, you will have:

- Defined and secured a FastAPI endpoint.
- Integrated your agent with a RESTful API.
- Verified proper endpoint functionality using Swagger UI.

You're now ready to proceed to **Phase 4: Integration and Testing**.