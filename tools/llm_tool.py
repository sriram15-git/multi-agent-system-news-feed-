import requests
import json
import time
import os
from config.config import OLLAMA_HOST, OLLAMA_MODEL


def ask_llm(prompt: str, system: str = "", model: str = None) -> str:
    """
    Send a prompt to an LLM.
    If GEMINI_API_KEY is set in environment, uses Google Gemini API (cloud-compatible).
    Otherwise, defaults to local Ollama.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key:
    # Targeted gemini-2.5-flash as the active model to resolve 404 errors
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        
        # 1. CRITICAL: Inject a strict completeness instruction to guarantee all sentences end naturally
        completeness_instruction = "\n\nCRITICAL: Ensure your output is a fully complete thought, ends with a proper punctuation mark (period, exclamation, or question mark), and is NEVER truncated or cut off mid-sentence."
        
        raw_prompt = f"{prompt}{completeness_instruction}"
        full_prompt = f"System Instruction: {system}\n\nUser Prompt: {raw_prompt}" if system else raw_prompt
        
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,  # 2. Lowered slightly to make generation more structured and complete
                "maxOutputTokens": 1024
            },
            # Explicitly set safety thresholds to BLOCK_NONE to prevent the 
            # safety guardrails from cutting off sarcastic/roast content mid-sentence.
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
        }
        
        max_retries = 5
        backoff_seconds = 3.0
        
        for attempt in range(max_retries):
            try:
                # Add a tiny base delay to stagger consecutive calls slightly
                time.sleep(20.0)
                
                response = requests.post(url, json=payload, timeout=60)
                
                # Check specifically for rate limiting (429)
                if response.status_code == 429:
                    print(f"  [LLM Tool] 429 Rate Limit hit. Retrying in {backoff_seconds}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2.0  # Exponential backoff
                    continue
                    
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
                
            except Exception as e:
                # If we hit an error other than 429, or we've run out of retries
                if attempt == max_retries - 1:
                    return f"[Gemini API error] {e}"
                time.sleep(backoff_seconds)
                backoff_seconds *= 2.0

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