from pydantic_ai import Agent
import inspect
try:
    print(f"Agent Signature: {inspect.signature(Agent)}")
except Exception as e:
    print(f"Error inspecting signature: {e}")
