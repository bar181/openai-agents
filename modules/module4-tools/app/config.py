import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv("API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is missing. Please set it in .env.")
if not API_KEY:
    raise ValueError("Error: API_KEY is missing. Please set it in .env.")
