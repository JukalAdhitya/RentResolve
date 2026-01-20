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

print("--- Listing Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")

print("\n--- Testing Generation ---")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error generating: {e}")
