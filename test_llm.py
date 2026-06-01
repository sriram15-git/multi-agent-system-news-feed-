import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

sarcasm_prompt = """You are a brilliantly sarcastic Indian commentator. You love Tamil Nadu, cinema, sports and calling out absurdity.

Your style:
- Dry wit, no exclamation marks
- Use relatable comparisons (EB bill, auto fare, Chennai traffic, TASMAC)
- Never mean-spirited, always clever
- 2-4 short punchy lines max
- No emojis unless it's just one at the end

Example:
"The government announced another committee to study the committee's report on the previous committee. Democracy is thriving."

Now rewrite this weather report in your style (2-3 funny lines):

City: Vellore
Temperature: 35°C (feels like 40°C)
Condition: Clear sky ☀️
Humidity: 60%
Rain chance: 0%
Wind: 15 km/h
High / Low: 38°C / 28°C"""

# Test 1: No generationConfig
payload_no_config = {
    "contents": [{
        "parts": [{"text": sarcasm_prompt}]
    }]
}

# Test 2: generationConfig without maxOutputTokens
payload_no_limit = {
    "contents": [{
        "parts": [{"text": sarcasm_prompt}]
    }],
    "generationConfig": {
        "temperature": 0.8
    }
}

# Test 3: maxOutputTokens as max_output_tokens
payload_snake_case = {
    "contents": [{
        "parts": [{"text": sarcasm_prompt}]
    }],
    "generationConfig": {
        "temperature": 0.8,
        "max_output_tokens": 512
    }
}

for name, payload in [
    ("No Config", payload_no_config),
    ("No maxOutputTokens in Config", payload_no_limit),
    ("max_output_tokens (snake_case)", payload_snake_case)
]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    print(f"\n--- Testing: {name} ---")
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            res_json = response.json()
            text = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            print("Response:", text)
            print("Finish Reason:", res_json["candidates"][0].get("finishReason"))
        else:
            print("Error status:", response.status_code)
            print("Error text:", response.text)
    except Exception as e:
        print("Exception:", e)
