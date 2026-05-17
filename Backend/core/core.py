# All settings realated must come here


import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
GOOGLE_MAP = os.getenv("GOOGLE_MAP")

if not OLLAMA_BASE_URL:
    raise ValueError("OLLAMA_BASE_URL is not set in .env")
if not OLLAMA_MODEL:
    raise ValueError("OLLAMA_MODEL is not set in .env")
if not GOOGLE_MAP:
    raise ValueError("GOOGLE_MAP is not set in .env")