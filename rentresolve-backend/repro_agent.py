from pydantic_ai import Agent
from pydantic import BaseModel

class MyResult(BaseModel):
    foo: str

print("--- TEST 1: Init with result_type ---")
try:
    agent = Agent('test-model', result_type=MyResult)
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")

print("\n--- TEST 2: Generic instantiation ---")
try:
    # Note: Runtime generic subscription might require creating a type alias or direct usage
    # This syntax Agent[None, MyResult] works if Agent implements __class_getitem__
    agent = Agent[None, MyResult]('test-model')
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")

print("\n--- TEST 3: Init without result_type ---")
try:
    agent = Agent('test-model')
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
