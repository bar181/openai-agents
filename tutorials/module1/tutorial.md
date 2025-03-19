
<!-- File: root/tutorials/module1/tutorial.md -->

# Module 1 Tutorial: Hello World Agent

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Master's Student at Harvard University, CS50 Teaching Fellow*

---

## Welcome!

Welcome to Module 1 of our self-paced AI Agents course! I'm Bradley Ross, your instructor for this course. This module introduces you to building your very first AI agent—a simple "Hello World" agent using FastAPI and the OpenAI Agents SDK. 

This module sets the foundation for all future modules. Once you've mastered this initial setup, you'll reuse and expand upon these concepts throughout the course.

Let's get started!

---

## Learning Objectives

By completing this module, you will:

- Set up your Python development environment.
- Understand the recommended structure for AI agent projects.
- Learn the role of each key file in your project.
- Build a simple but fully functional AI agent.
- Test your agent's functionality using FastAPI and Pytest.

---

## Prerequisites

Before starting this module, ensure you have:

- **Python 3.10+** installed on your machine.
- Basic familiarity with Python and asynchronous programming concepts.
- An OpenAI API key (sign up at [OpenAI](https://platform.openai.com/signup)).

---

## Recommended Approach

For the best learning experience, follow this process:

1. **Create a copy** of the module template (`module1-hello-world`).
2. Rename the folder as needed for experimentation.
3. Follow the step-by-step explanations below.
4. Refer to the actual code files within the folder as you read the explanations.

For advanced learners:  
Feel free to use AI coding tools (e.g., GitHub Copilot) by pointing them toward these module files to help customize your agents.

---

## Step-by-Step Guide

### Step 1: Setting Up Your Environment

First, you'll create an isolated workspace (a virtual environment) to avoid dependency conflicts. This is crucial for professional and consistent coding practice.

- **Create a virtual environment** named `env`.
- **Activate it** to begin using the environment.
- **Install dependencies** listed in `requirements.txt` (e.g., FastAPI, Uvicorn, OpenAI SDK).

> **Tip:** Refer to the `requirements.txt` file to see exactly which packages you'll need.

---

### Step 2: Securely Managing API Keys (`.env` File)

Your API keys are private. You'll store them securely in a `.env` file.

- Create a file named `.env` in the project root.
- Add your OpenAI API key and your own API key for authentication.

> **Important:** Never commit your `.env` file to a public repository! 

---

### Step 3: Understanding the Project Structure

Your module should look like this:

```
module1-hello-world/
├── app/
│   ├── agents/              # Holds your agent code
│   │   └── hello_world_agent.py
│   ├── routers/             # API endpoints
│   │   └── hello_world.py
│   ├── config.py            # Environment variable management
│   ├── dependencies.py      # API authentication setup
│   └── main.py              # Main FastAPI application
├── .env                     # Secret keys
├── requirements.txt         # Project dependencies
├── tests/                   # Tests for your agent
│   └── test_hello_world.py
├── tutorial.md              # (You're reading this now!)
└── README.md                # Quick overview
```

Each file has a specific role. We'll explain these in the next section.

---

### Step 4: Key Files and Their Roles

#### 4.1 **Environment Configuration (`config.py`)**

- Loads environment variables from your `.env` file.
- Ensures that sensitive information (like your API keys) is handled safely.

*Pseudocode:*
```
Load environment variables:
    OPENAI_API_KEY
    API_KEY
```

#### 4.2 **Authentication (`dependencies.py`)**

- Defines how the API key authentication works.
- Prevents unauthorized access to your agent.

*Pseudocode:*
```
Create an API key header ("X-API-KEY"):
Check received API key:
    If incorrect or missing, deny access
    If correct, allow access
```

#### 4.3 **Agent Logic (`hello_world_agent.py`)**

- Implements the simple "Hello World" agent using OpenAI's SDK.
- Demonstrates how an agent is structured with tools and instructions.

*Pseudocode:*
```
Define a tool "hello_world_tool" that returns "Hello, world!"
Create an agent with instructions: "You are a friendly agent that greets the user."
Run the agent asynchronously with provided user input
```

#### 4.4 **API Endpoint (`routers/hello_world.py`)**

- Exposes your agent through an API endpoint using FastAPI.
- Receives user input and returns the agent’s response.

*Pseudocode:*
```
Create a POST endpoint "/agent/hello":
    Accept user message
    Call hello_world_agent with the message
    Return agent's response
```

#### 4.5 **Application Entry (`main.py`)**

- Initializes your FastAPI application.
- Includes routers to expose endpoints.

*Pseudocode:*
```
Initialize FastAPI app
Include router for hello_world agent at path "/agent"
Add root endpoint for checking if app is running
```

#### 4.6 **Testing Your Agent (`tests/test_hello_world.py`)**

- Validates the functionality of your agent's endpoint.
- Ensures that the response includes the user's input.

*Pseudocode:*
```
Send POST request to "/agent/hello" with message "Hi from Bradley"
Check response status is 200 (OK)
Ensure response contains "Bradley"
```

---

## Step 5: Running Your Application and Tests

**Starting your application:**
- Activate your virtual environment.
- Navigate to your project folder.
- Run the FastAPI server using Uvicorn:
  ```bash
  python -m uvicorn app.main:app --reload
  ```
- Visit `http://localhost:8000/docs` to test your API.

**Running tests:**
- Ensure your server isn't running to avoid conflicts.
- Execute:
  ```bash
  python -m pytest tests/
  ```
- Confirm all tests pass successfully.

---

## Final Thoughts & Next Steps

Congratulations! You've successfully built and tested your first AI agent. You've learned the foundations of setting up an AI project, integrating FastAPI, and writing structured, maintainable code.

In Module 2, you'll expand this foundation by creating a more complex Story Telling Agent, exploring advanced agent workflows, and improving your project structure.

Keep exploring, experimenting, and enhancing your agent-building skills.

Happy coding, and see you in the next module!

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, CS50 Teaching Fellow*
