import requests
import json
from config.config import OLLAMA_HOST, OLLAMA_MODEL


def ask_llm(prompt: str, system: str = "", model: str = None) -> str:
    """
    Send a prompt to local Ollama and return the text response.
    Falls back gracefully if Ollama is not running.
    """
    model = model or OLLAMA_MODEL
    url   = f"{OLLAMA_HOST}/api/chat"

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model":    model,
        "messages": messages,
        "stream":   False,
        "options":  {
            "temperature": 0.8,
            "num_predict": 512,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()

    except requests.exceptions.ConnectionError:
        return "[LLM unavailable] Ollama is not running. Start it with: ollama serve"
    except Exception as e:
        return f"[LLM error] {e}"