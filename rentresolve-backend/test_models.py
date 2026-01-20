import google.generativeai as genai
import os

# Manual .env loading
try:
    with open(".env", "r") as f:
        for line in f:
            if "GOOGLE_API_KEY" in line:
                key = line.strip().split("=", 1)[1]
                os.environ["GOOGLE_API_KEY"] = key
                break
except Exception:
    pass

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

candidates = [
    "models/deep-research-pro-preview-12-2025",
    "gemini-1.5-flash",
    "models/gemini-1.5-flash",
    "gemini-2.0-flash-exp",
    "gemini-pro",
    "models/gemini-pro"
]

print(f"API Key: {os.environ.get('GOOGLE_API_KEY')[:5]}...")

for model_name in candidates:
    print(f"\nTesting: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"SUCCESS: {model_name}")
        break  # Found one!
    except Exception as e:
        print(f"FAILED: {model_name} - {e}")
