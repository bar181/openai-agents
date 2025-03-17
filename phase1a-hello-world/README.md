### README.md

# Phase1a-Hello-World

This is Phase1a of our multi-phase project to build OpenAI agents using FastAPI and the OpenAI Agents SDK. In this phase, we implement a minimal "Hello World" agent that responds with a greeting.

## Project Structure

```
phase1a-hello-world/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── hello_world_agent.py
│   └── routers/
│       ├── __init__.py
│       └── hello_world.py
├── .env
├── requirements.txt
├── tests/
│   └── test_hello_world.py
├── tutorial.md
└── README.md
```

## Getting Started

1. **Clone the repository** and navigate to the `phase1a-hello-world` folder.
2. **Create a virtual environment** and activate it.
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the `.env` file** with your API keys.
5. **Run the server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
6. **Access the API documentation** at [http://localhost:8000/docs](http://localhost:8000/docs).

## Running Tests

To run unit tests, use:
```bash
python -m pytest tests
```

## Overview

This phase demonstrates how to build a simple agent that:
- Uses the OpenAI Agents SDK to define a function tool.
- Is exposed via a FastAPI endpoint.
- Is secured using API key authentication.
- Includes unit tests to verify functionality.

Happy coding!
```

---

## QUICK GUIDE

### Create your .env file
Rename the `.env.sample` file to `.env` and add your OpenAI API key (visit openai.com for details) along with a custom `API_KEY` for authorization.

### In the terminal:

```bash
cd phase1a-hello-world

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Start the FastAPI server with Uvicorn
python -m uvicorn app.main:app --reload

# View FastAPI API documentation (requires you to authorize using the API_KEY in your .env file)
http://localhost:8000/docs

# Run tests
python -m pytest tests/
```
