from pydantic_ai.models.gemini import GeminiModel
import inspect
try:
    print(f"GeminiModel.__init__ Signature: {inspect.signature(GeminiModel.__init__)}")
except Exception as e:
    print(f"Error inspecting signature: {e}")
