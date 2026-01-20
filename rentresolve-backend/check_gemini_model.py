try:
    from pydantic_ai.models.gemini import GeminiModel
    print("GeminiModel found!")
except ImportError:
    print("GeminiModel NOT found.")
    try:
        from pydantic_ai.models.google import GoogleModel
        print("GoogleModel found!")
    except ImportError:
        print("GoogleModel NOT found.")
