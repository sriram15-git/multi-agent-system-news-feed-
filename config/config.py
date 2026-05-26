import os
from dotenv import load_dotenv

load_dotenv()

# --- Gmail ---
GMAIL_ADDRESS      = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
RECIPIENTS         = os.getenv("RECIPIENTS", "").split(",")

# --- Ollama ---
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
OLLAMA_HOST  = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# --- Scheduler ---
DAILY_HOUR   = int(os.getenv("DAILY_HOUR", 7))
DAILY_MINUTE = int(os.getenv("DAILY_MINUTE", 0))

# --- News topics ---
TOPICS = [
    "Kollywood cinema",
    "Hollywood movies",
    "Tamil Nadu politics",
    "Indian cricket",
    "ipl",
    "Tamil Nadu weather",
    "Tamil Nadu local news",
]

# --- Weather ---
CITY       = "Vellore"
LATITUDE   = 12.9165
LONGITUDE  = 79.1325

# --- Humor mode ---
HUMOR_MODE = "sarcastic"   # options: sarcastic | funny | roast | gen-z | professional