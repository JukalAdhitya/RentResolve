from pydantic_ai import Agent
import inspect
try:
    print(f"Agent.run Signature: {inspect.signature(Agent.run)}")
except Exception as e:
    print(f"Error inspecting signature: {e}")
