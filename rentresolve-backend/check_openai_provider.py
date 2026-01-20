try:
    from pydantic_ai.providers.openai import OpenAIProvider
    import inspect
    print(f"OpenAIProvider Signature: {inspect.signature(OpenAIProvider)}")
    print(f"OpenAIProvider.__init__ Signature: {inspect.signature(OpenAIProvider.__init__)}")
except ImportError:
    print("OpenAIProvider NOT found.")
except Exception as e:
    print(f"Error: {e}")
