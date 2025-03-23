<!-- File: root/tutorials/module1/tutorial.md -->

# Module 1 Tutorial: Hello World Agent

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Director @ Agentics Foundation, Programmer and Data Scientist with over 20 years of experience, Master's Student at Harvard University, CS50 Teaching Fellow/Course Assistant, Instructor and Course Designer*

---

## Welcome!

Welcome to the very first module of our AI Agents course! I'm Bradley Ross, and I'll guide you step-by-step through building your first AI-powered "Hello World" agent. This foundational module will introduce you to essential concepts and tools that you'll use throughout this course.

Let's dive in and get started!

---

## Learning Objectives

By the end of Module 1, you'll:

- Set up your Python environment properly.
- Understand how to securely manage API keys using environment variables.
- Learn the recommended project structure for building AI agents.
- Build and test a simple AI agent using FastAPI and the OpenAI SDK.

---

## Step-by-Step Guide

### Step 1: Setting Up Your Python Environment

Creating a dedicated workspace ensures your project remains isolated and organized.

1. **Install Python:**
   - Ensure Python 3.10 or newer is installed ([Download Python](https://www.python.org/downloads/)).

2. **Create and Activate a Virtual Environment:**

```bash
# Navigate to your module folder (replace with your actual path)
cd path/to/module1-hello-world

# Create virtual environment named 'env'
python -m venv env

# Activate virtual environment:
source env/bin/activate       # macOS/Linux
.\env\Scripts\activate       # Windows
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

Your environment is now set up and ready!

---

### Step 2: Setting Up Environment Variables (`.env` file)

Environment variables help you securely store sensitive information like API keys.

1. **Create a `.env` file** in your project root (same directory as `requirements.txt`).

2. **Add Your API Keys:**

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
API_KEY=your_custom_api_key_here
```

Replace `your_openai_api_key_here` with the key obtained from [OpenAI](https://platform.openai.com/signup), and choose your own unique key for `API_KEY` (e.g., `API_KEY=my_custom_key123`).

**Important:** Keep `.env` private—never share or upload it to public repositories!

---

### Step 3: Project Structure Overview

Here's your project's layout and what each part does:

```
module1-hello-world/
├── app/
│   ├── agents/               # Contains AI agent code
│   │   └── hello_world_agent.py
│   ├── routers/              # API endpoints
│   │   └── hello_world.py
│   ├── config.py             # Manages environment variables
│   ├── dependencies.py       # Handles API key authentication
│   └── main.py               # Main FastAPI application
├── .env                      # Your secret API keys
├── requirements.txt          # List of required packages
├── tests/                    # Tests for your application
│   └── test_hello_world.py
├── tutorial.md               # This detailed guide
└── README.md                 # Project overview
```

---

### Step 4: Understanding Key Files

#### `config.py`
- Loads and manages your environment variables.

#### `dependencies.py`
- Defines API key authentication to secure endpoints.

#### `hello_world_agent.py`
- Implements your first basic AI agent.

#### `hello_world.py` (inside `routers`)
- Creates an API endpoint to interact with your agent.

#### `main.py`
- Starts your FastAPI application and includes your endpoints.

#### `test_hello_world.py`
- Contains tests to verify your agent and API work correctly.

---

### Step 5: Running Your Application

1. **Start the FastAPI server:**

```bash
python -m uvicorn app.main:app --reload
```

2. **Access Swagger Documentation:**

- Visit [http://localhost:8000/docs](http://localhost:8000/docs).
- Click on the **Authorize** button (top right).
- Enter your `API_KEY` from `.env` (e.g., `my_custom_key123`).
- Click **Authorize**, then **Close**.

Now you're authenticated and ready to interact with your API!

---

### Step 6: Testing Your Agent

Testing ensures your code works as expected.

1. **Stop your server** if it's running (Ctrl+C).

2. **Run the test suite:**

```bash
python -m pytest tests/
```

Make sure all tests pass successfully.

---

## Frequently Asked Questions (FAQs)

### What is a `.env` file?
A `.env` file stores sensitive information like API keys securely outside your codebase. It prevents accidental exposure of sensitive data.

### How do I get an OpenAI API Key?
Sign up and create an account at [OpenAI](https://platform.openai.com/signup). Follow instructions there to generate your unique API key.

### What is Swagger and how do I authorize requests?
Swagger provides interactive API documentation. After opening the docs (`http://localhost:8000/docs`), click "Authorize" and enter your `API_KEY` from your `.env` file to securely access your endpoints.

---

## Next Steps

Congratulations! You've successfully built, deployed, and tested your first AI agent. You've learned essential foundations that you'll use throughout this course.

In Module 2, you'll expand these concepts further by building storytelling agents that produce rich, narrative-driven outputs.

Keep exploring and building great things!

---

Happy coding!

*Instructor: Bradley Ross – Agentics Engineer and Technical Lead, Director @ Agentics Foundation*

