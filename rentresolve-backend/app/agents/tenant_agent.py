import google.generativeai as genai
from app.agents.schemas import ComplaintKit, TenantIssueInput
from app.core.config import settings
import os
import json

# Ensure API Key is set
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

SYSTEM_PROMPT = (
    "You are an expert legal assistant for Indian tenants. "
    "Your goal is to generate a comprehensive complaint kit based on the tenant's issue. "
    "Instructions: "
    "1. Be professional, clear, and action-oriented. "
    "2. Use Indian English and reference generic Indian rental laws (like the Rent Control Act) if applicable. "
    "3. Use Rupees (₹) for all monetary amounts. "
    "4. Do NOT use markdown formatting in email_body or whatsapp_message. "
    "5. Sign off the email and whatsapp message with the provided Tenant Name and Phone Number. "
    "6. Output must be a valid JSON object matching the following structure: "
    "{ 'formal_complaint_letter': 'str', 'email_body': 'str', 'whatsapp_message': 'str', 'action_plan': ['str'], 'legal_references': ['str'] }"
)

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT,
    generation_config={"response_mime_type": "application/json"}
)

async def generate_complaint_kit(issue_input: TenantIssueInput) -> ComplaintKit:
    # Construct the user prompt context
    user_prompt = f"""
    Issue Details:
    Location: {issue_input.location}
    Issue Type: {issue_input.issue_type}
    Amount: {issue_input.amount} (in INR)
    Date: {issue_input.date}
    Description: {issue_input.description}
    Tone: {issue_input.tone}
    
    Lease Agreement Context:
    {issue_input.agreement_context or "No agreement provided."}
    
    Tenant Details:
    Name: {issue_input.tenant_name or "[Tenant Name]"}
    Phone: {issue_input.tenant_phone or "[Contact Number]"}
    """
    
    try:
        # Run the agent (using SDK directly)
        response = model.generate_content(user_prompt)
        # Parse result into Pydantic model
        return ComplaintKit.model_validate_json(response.text)
    except Exception as e:
        print(f"Error generating complaint kit with GenAI SDK: {e}")
        # Improve error logging to see raw response if needed
        raise e
