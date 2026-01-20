from openai import OpenAI
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

client = OpenAI(
    api_key=os.environ.get("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

models = ["gemini-1.5-flash-latest", "gemini-1.5-pro", "gemini-pro"]

for model_name in models:
    print(f"Testing model: {model_name}")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Hello"}],
        )
        print(f"SUCCESS: {model_name}")
        print(response.choices[0].message.content)
        break
    except Exception as e:
        print(f"FAILED: {model_name} - {e}")
