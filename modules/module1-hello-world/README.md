# Module 1: Hello World Agent

Welcome to Module 1! In this initial module, you'll build a minimal yet fully functional "Hello World" AI agent using FastAPI and the OpenAI Python SDK. This module sets the foundational skills you'll need for more complex agent development in future modules.

You'll find the official OpenAI SDK documentation [here](https://github.com/openai/openai-python).

---

## Learning Objectives

By the end of this module, you'll be able to:

- Set up a structured FastAPI application for AI agents.
- Implement a simple AI agent responding with a basic greeting.
- Secure your endpoints using API key authentication.
- Run and interpret basic unit tests for your agents.

Your goal is to successfully run the provided tests:
```bash
python -m pytest tests/
```

---

## Project Structure

```plaintext
module1-hello-world/
├── app/
│   ├── __init__.py
│   ├── main.py                         # FastAPI entry point
│   ├── config.py                       # Configuration and environment management
│   ├── dependencies.py                 # API key validation and reusable dependencies
│   ├── agents/
│   │   ├── __init__.py
│   │   └── hello_world_agent.py        # Basic Hello World agent
│   └── routers/
│       ├── __init__.py
│       └── hello_world.py              # API router for Hello World agent
├── .env                                # Environment configuration
├── requirements.txt                    # Project dependencies
├── tests/
│   └── test_hello_world.py             # Unit tests for Hello World agent
├── tutorial.md                         # Detailed module tutorial
└── README.md                           # This file
```

---

## Setup & Installation

Follow these steps to prepare your local environment:

### Prerequisites
- Python 3.10+
- Virtual environment strongly recommended

### Installation

Clone the repository and set up the environment:
```bash
git clone <repository-url>
cd module1-hello-world

python -m venv env
source env/bin/activate  # Unix/macOS
# or
.\env\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Environment Configuration

Rename `.env.sample` to `.env` and add your credentials:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
API_KEY=your_custom_api_key_here
```

---

## Running the Application

Launch your FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

Visit the API documentation:

[http://localhost:8000/docs](http://localhost:8000/docs)

*Note: Use your custom `API_KEY` from the `.env` file to authorize requests.*

---

## API Endpoint

- **Hello World Agent**
  - **Endpoint:** `/agents/hello-world`
  - **Description:** Returns a simple greeting message.
  - **Authentication:** Requires `X-API-KEY` header.

---

## Running Tests

Validate your implementation using the provided tests:

```bash
python -m pytest tests/
```

Tests verify:
- Endpoint availability and HTTP status code (200).
- Correct greeting response.

---

## Documentation & Resources

For more information:
- **Official OpenAI Python SDK:** [OpenAI GitHub Repository](https://github.com/openai/openai-python)
- **FastAPI Documentation:** [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- **Module Tutorial:** Comprehensive guidance found in `tutorial.md`

---

## Quick Reference

```bash
# Navigate to the module directory
cd path/to/module1-hello-world

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
python -m uvicorn app.main:app --reload

# Access API documentation
http://localhost:8000/docs

# Run tests
python -m pytest tests/
```

---

Congratulations on beginning your AI agent development journey! Completing Module 1 will equip you with the essential skills for building more sophisticated and capable agents in upcoming modules.

Happy coding!

