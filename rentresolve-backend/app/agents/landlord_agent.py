import google.generativeai as genai
from app.agents.schemas import LandlordReply, LandlordReplyInput
from app.core.config import settings
import os
import json

# Ensure API Key is set
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

SYSTEM_PROMPT = (
    "You are a professional property management assistant in India. "
    "Your goal is to draft a professional, de-escalating reply to a tenant issue. "
    "Instructions: "
    "1. Be empathetic but firm. "
    "2. Address the specific points raised by the tenant. "
    "3. Offer a constructive next step or solution. "
    "4. Maintain a professional tone appropriate for a landlord/property manager. "
    "5. Use Indian English standards. "
    "6. Output must be a valid JSON object matching the following structure: "
    "{ 'reply_text': 'str', 'next_steps': ['str'], 'legal_protection_notes': ['str'] }"
)

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT,
    generation_config={"response_mime_type": "application/json"}
)

async def generate_landlord_reply(reply_input: LandlordReplyInput) -> LandlordReply:
    # Construct the user prompt context
    user_prompt = f"""
    Tenant Complaint Context:
    Description: {reply_input.issue_description}
    Tone Requested: {reply_input.tone}
    Landlord Name: {reply_input.landlord_name or "[Landlord Name]"}
    """
    
    try:
        # Run the agent (using SDK directly)
        response = model.generate_content(user_prompt)
        # Parse result into Pydantic model
        return LandlordReply.model_validate_json(response.text)
    except Exception as e:
        print(f"Error generating landlord reply with GenAI SDK: {e}")
        raise e
