import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

sarcasm_prompt_template = """You are a brilliantly sarcastic Indian commentator. You love Tamil Nadu, cinema, sports and calling out absurdity.

Your style:
- Dry wit, no exclamation marks
- Use relatable comparisons (EB bill, auto fare, Chennai traffic, TASMAC)
- Never mean-spirited, always clever
- 2-4 short punchy lines max
- No emojis unless it's just one at the end

Example:
"The government announced another committee to study the committee's report on the previous committee. Democracy is thriving."

Now rewrite this news item in your style (3-4 punchy lines):

Title: {title}
Context: {context}"""

title = '"With Heavy Heart, Sadness": Another Key Tamil Nadu BJP Leader Quits'
context = 'Another key BJP leader has decided to leave the Tamil Nadu unit.'

prompt = sarcasm_prompt_template.format(title=title, context=context)
completeness_instruction = "\\n\\nCRITICAL: Ensure your output is a fully complete thought, ends with a proper punctuation mark (period, exclamation, or question mark), and is NEVER truncated or cut off mid-sentence."
raw_prompt = f"{prompt}{completeness_instruction}"

configs = [
    ("No maxOutputTokens", {
        "temperature": 0.7
    }),
    ("maxOutputTokens = 2048", {
        "temperature": 0.7,
        "maxOutputTokens": 2048
    }),
    ("maxOutputTokens = 4096", {
        "temperature": 0.7,
        "maxOutputTokens": 4096
    }),
    ("No generationConfig at all", None)
]

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"

for name, gen_config in configs:
    payload = {
        "contents": [{
            "parts": [{"text": raw_prompt}]
        }],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    if gen_config is not None:
        payload["generationConfig"] = gen_config
        
    print(f"\n--- Testing: {name} ---")
    response = requests.post(url, json=payload, timeout=60)
    if response.status_code == 200:
        res_json = response.json()
        candidate = res_json["candidates"][0]
        text = candidate["content"]["parts"][0]["text"].strip()
        print("Response:", text)
        print("Finish Reason:", candidate.get("finishReason"))
    else:
        print("Error status:", response.status_code)
        print("Error text:", response.text)
