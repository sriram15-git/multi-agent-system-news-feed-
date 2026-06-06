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
DAILY_HOUR   = int(os.getenv("DAILY_HOUR", 10))
DAILY_MINUTE = int(os.getenv("DAILY_MINUTE", 0))

# --- News topics ---
TOPICS = [
    "Kollywood cinema",
    "Hollywood movies",
    "Tamil Nadu politics",
    "Indian cricket",
    "Tamil Nadu weather",
    "Tamil Nadu local news",
]

# --- Weather ---
CITY       = os.getenv("WEATHER_CITY") or "Vellore"

def _get_float_env(name, default):
    val = os.getenv(name)
    if not val or val.strip() == "":
        return default
    try:
        return float(val)
    except ValueError:
        return default

LATITUDE   = _get_float_env("WEATHER_LATITUDE", 12.9165)
LONGITUDE  = _get_float_env("WEATHER_LONGITUDE", 79.1325)

# --- Humor mode ---
HUMOR_MODE = os.getenv("HUMOR_MODE") or "sarcastic"   # options: sarcastic | funny | roast | gen-z | professional