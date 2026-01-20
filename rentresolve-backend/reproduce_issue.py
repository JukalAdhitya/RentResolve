import asyncio
import os
import sys
# Add project root to sys.path
sys.path.append(os.getcwd())

from app.agents import tenant_agent
from app.agents.schemas import TenantIssueInput
from app.core.config import settings

async def main():
    print("--- STARTING REPRODUCTION ---")
    try:
        # Mocking the input from the frontend request
        input_data = TenantIssueInput(
            location="New York", # Using example data
            issue_type="Plumbing",
            amount="100.50",
            date="2024-01-20",
            description="Leaking pipe in the kitchen.",
            tone="Professional",
            agreement_context=""
        )
        print("1. Sending Request to Gemini...")
        result = await tenant_agent.generate_complaint_kit(input_data)
        print("2. Success!")
        print(result)
    except Exception as e:
        print(f"3. FAILED with Error: {type(e).__name__}: {e}")
        import traceback
        with open("error.txt", "w") as f:
            f.write(traceback.format_exc())
            f.write(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())
