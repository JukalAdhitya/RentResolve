from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ComplaintKit(BaseModel):
    whatsapp_message: str
    email_subject: str
    email_body: str
    evidence_checklist: List[str]
    escalation_timeline: List[str]

class UserRole(str, Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"

class IssueStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

class User(Document):
    email: str = Field(unique=True)
    password_hash: str
    role: UserRole
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"

class Message(BaseModel):
    sender_id: str # User ID
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

class EmailLog(BaseModel):
    recipient: str
    subject: str
    status: str # sent, failed
    timestamp: datetime = Field(default_factory=datetime.now)

class Issue(Document):
    tenant_id: str # Link/ID to User
    title: str
    description: str
    status: IssueStatus = IssueStatus.PENDING
    location: str
    issue_type: str
    amount: Optional[float] = None
    date_incident: Optional[str] = None
    
    # Phase 2: Privacy & Documents
    landlord_email: Optional[str] = None
    agreement_content: Optional[str] = None 
    
    # Phase 3: High-Impact Add-ons
    timeline_events: List[dict] = [] # e.g. [{ "date": "...", "title": "Created", "description": "..." }]
    evidence_files: List[dict] = [] # e.g. [{ "filename": "...", "url": "...", "type": "image/png" }]

    created_at: datetime = Field(default_factory=datetime.now)
    
    messages: List[Message] = []
    emails: List[EmailLog] = []
    complaint_kit: Optional[ComplaintKit] = None

    class Settings:
        name = "issues"
