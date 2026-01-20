from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TenantIssueInput(BaseModel):
    location: str
    issue_type: str
    amount: Optional[str] = None
    date: str
    description: str
    tone: str
    agreement_context: Optional[str] = None # Text extracted from lease
    tenant_name: Optional[str] = None
    tenant_phone: Optional[str] = None

class ComplaintKit(BaseModel):
    whatsapp_message: str
    email_subject: str
    email_body: str
    evidence_checklist: List[str]
    escalation_timeline: List[str]
    complaint_strength_score: Optional[int] = 0  # 0-100 score (Non-legal guidance)

class LandlordReplyInput(BaseModel):
    issue_details: str
    landlord_stance: str
    tone: str
    landlord_name: Optional[str] = None
    landlord_phone: Optional[str] = None

class LandlordReply(BaseModel):
    whatsapp_reply: str
    email_reply_subject: str
    email_reply_body: str
    next_steps: List[str]
