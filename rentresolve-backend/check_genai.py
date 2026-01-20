try:
    import google.generativeai as genai
    print("google-generativeai found!")
except ImportError:
    print("google-generativeai NOT found.")
