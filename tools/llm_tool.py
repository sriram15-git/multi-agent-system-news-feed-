import requests
import json
from config.config import OLLAMA_HOST, OLLAMA_MODEL


import os

def ask_llm(prompt: str, system: str = "", model: str = None) -> str:
    """
    Send a prompt to an LLM.
    If GEMINI_API_KEY is set in environment, uses Google Gemini API (cloud-compatible).
    Otherwise, defaults to local Ollama.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key:
        # Use Google Gemini API (no extra packages needed, uses requests)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        
        # Combine system instruction and prompt for Gemini structure
        full_prompt = f"System Instruction: {system}\n\nUser Prompt: {prompt}" if system else prompt
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 512
            }
        }
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            return f"[Gemini API error] {e}"

    # Default to local Ollama
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