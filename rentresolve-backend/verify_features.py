import asyncio
import os
from app.agents import tenant_agent
from app.agents.schemas import TenantIssueInput
from app.services import email_service
from app.core.config import settings

# Force load env if not loaded, though settings should handle it.
# Ensure we are in the right loop
async def main():
    print("--- STARTING FEATURE VERIFICATION ---")

    # 1. Verify AI Agent
    print("\n[1] Testing AI Agent (Gemini)...")
    try:
        input_data = TenantIssueInput(
            location="Bangalore",
            issue_type="Electrical",
            amount="2000",
            date="2023-10-27",
            description="Switch board sparking when turned on.",
            tone="Urgent",
            agreement_context=""
        )
        print("   Sending request to Gemini...")
        result = await tenant_agent.generate_complaint_kit(input_data)
        print("   [SUCCESS] AI Response Received:")
        print(f"   Subject: {result.email_subject}")
        print(f"   Body Preview: {result.email_body[:50]}...")
    except Exception as e:
        print(f"   [FAILED] AI Error: {e}")

    # 2. Verify Email
    print("\n[2] Testing Email Service (SMTP)...")
    target_email = "jukal0024@gmail.com"
    print(f"   Attempting to send email to {target_email} using {settings.SMTP_USER}...")
    
    # Mocking an issue ID for logging purposes, assuming db connection might be needed for logging?
    # Actually email_service tries to fetch issue. 
    # For this test, we might hit an error if DB isn't connected or issue doesn't exist.
    # Let's verify if we can send WITHOUT issue_id or if we need to mock DB.
    # The current implementation REQUIRES issue_id to log.
    # We will wrap it in try/except.
    
    # We need to initialize DB for email logging to work as coded?
    # The email sending part happens BEFORE logging in the 'try' block for 'sendmail'?
    # No, look at code: 'issue = await Issue.get(issue_id)' is at the TOP.
    # So we need a valid issue ID or it handles None?
    # Code: 'issue = await Issue.get(issue_id)' -> if issue_id is random, it returns None.
    # Then 'if issue: ...'
    # So it should be fine with a dummy ID.
    
    try:
        # DB Init needed for Beanie if we even call Issue.get
        from app.db.session import init_db
        await init_db()
        
        success = await email_service.send_email(
            to=target_email,
            subject="RentResolve Test Email",
            body="This is a test email to verify SMTP configuration.",
            issue_id="dummy_id_123" 
        )
        if success:
            print("   [SUCCESS] Email sent command executed successfully.")
        else:
            print("   [FAILED] Email service returned False.")
    except Exception as e:
        print(f"   [FAILED] Email Error: {e}")

    print("\n--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(main())
