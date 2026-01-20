from pydantic_ai.models.openai import OpenAIModel
import inspect
try:
    print(f"OpenAIModel.__init__ Signature: {inspect.signature(OpenAIModel.__init__)}")
except Exception as e:
    print(f"Error inspecting signature: {e}")
