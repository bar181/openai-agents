# Module 1 - Phase 1: Environment Setup and Project Initialization

This document provides step-by-step instructions for setting up your Python development environment and initializing the project structure for the "Hello World" AI agent.

---

## Step 1: Python and Virtual Environment Setup

### 1.1 Verify Python Installation

Ensure Python 3.10 or higher is installed:

```bash
python --version
```

You should see a response like:
```
Python 3.10.5
```

### 1.2 Create a Virtual Environment

Navigate to your project directory and create a virtual environment:

```bash
python -m venv env
```

Activate the virtual environment:

- **Windows:**
  ```bash
  .\env\Scripts\activate
  ```

- **macOS/Linux:**
  ```bash
  source env/bin/activate
  ```

---

## Step 2: Install Dependencies

With your virtual environment activated, install required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Your dependencies (`requirements.txt`) include:
- fastapi
- uvicorn
- openai
- python-dotenv
- pydantic
- pytest
- pytest-asyncio

---

## Step 3: Environment Variables Configuration

Create a `.env` file in your project root directory and securely store your API keys:

```dotenv
OPENAI_API_KEY=your_openai_api_key
API_KEY=your_custom_api_key
```

Replace `your_openai_api_key` and `your_custom_api_key` with your actual API keys.

**Important:** Do not commit `.env` to version control. Always add `.env` to your `.gitignore` file.

---

## Step 4: Project Directory Structure

Verify your directory matches the following structure:

```plaintext
module1-hello-world/
├── app/
│   ├── agents/
│   │   └── hello_world_agent.py
│   ├── routers/
│   │   └── hello_world.py
│   ├── config.py
│   ├── dependencies.py
│   └── main.py
├── .env
├── requirements.txt
├── tests/
│   └── test_hello_world.py
├── tutorial.md
└── README.md
```

Ensure all directories and placeholder files are properly created.

---

## Step 5: Validate Environment Setup

Check that environment variables load correctly:

Create or verify `app/config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("API_KEY")

if not OPENAI_API_KEY or not API_KEY:
    raise ValueError("Missing required API keys. Ensure they are set in your .env file.")
```

Run a quick check:

```bash
python -c "from app.config import OPENAI_API_KEY, API_KEY; print('Keys loaded successfully.')"
```

You should see:
```
Keys loaded successfully.
```

---

## Completion of Phase 1

Upon completion of this phase, you will have:

- A working virtual environment
- Installed dependencies
- Configured environment variables
- A correctly structured project

You're now ready to proceed to **Phase 2: Agent Implementation**.