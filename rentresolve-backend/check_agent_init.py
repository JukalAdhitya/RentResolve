from pydantic_ai import Agent
import inspect
try:
    print(f"Agent Signature: {inspect.signature(Agent)}")
    print(f"Agent.__init__ Signature: {inspect.signature(Agent.__init__)}")
except Exception as e:
    print(f"Error inspecting signature: {e}")
