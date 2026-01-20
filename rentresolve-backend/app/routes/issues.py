from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from app.agents import tenant_agent, schemas as agent_schemas
from app.db.models import Issue, User, IssueStatus
from app.core import security
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/issues", tags=["Issues"])

class IssueCreate(BaseModel):
    title: str
    description: str
    location: str
    issue_type: str
    amount: Optional[float] = None
    amount: Optional[float] = None
    date_incident: Optional[str] = None
    landlord_email: Optional[str] = None
    tone: Optional[str] = "Professional"
    agreement_context: Optional[str] = None

class IssueUpdate(BaseModel):
    status: Optional[IssueStatus] = None

@router.post("/", response_model=Issue)
async def create_issue(issue_in: IssueCreate, current_user: User = Depends(security.get_current_user)):
    if current_user.role != "tenant":
        raise HTTPException(status_code=403, detail="Only tenants can create issues")
    
    try:
        # Prepare input for AI agent
        ai_input = agent_schemas.TenantIssueInput(
            location=issue_in.location,
            issue_type=issue_in.issue_type,
            amount=str(issue_in.amount) if issue_in.amount else None,
            date=issue_in.date_incident or datetime.now().strftime("%Y-%m-%d"),
            description=issue_in.description,
            tone=issue_in.tone or "Professional",
            agreement_context=issue_in.agreement_context,
            tenant_name=current_user.full_name,
            tenant_phone=current_user.phone_number
        )
        
        # Generate Complaint Kit
        complaint_kit = await tenant_agent.generate_complaint_kit(ai_input)
    except Exception as e:
        print(f"AI Generation failed (non-blocking): {e}")
        complaint_kit = None

    new_issue = Issue(
        tenant_id=str(current_user.id),
        **issue_in.dict(exclude={"tone", "agreement_context"}), # Exclude fields not in Issue model
        agreement_content=issue_in.agreement_context, # Map explicitly if needed, or rely on dict() if model updated
        complaint_kit=complaint_kit,
        timeline_events=[{
            "date": datetime.now().isoformat(), 
            "title": "Issue Created", 
            "description": f"Issue reported by {current_user.full_name or 'Tenant'}"
        }]
    )
    await new_issue.insert()
    return new_issue

@router.get("/", response_model=List[Issue])
async def get_issues(current_user: User = Depends(security.get_current_user)):
    if current_user.role == "tenant":
        issues = await Issue.find(Issue.tenant_id == str(current_user.id)).sort("-created_at").to_list()
    else:
        # Landlord sees only issues assigned to their email
        issues = await Issue.find(Issue.landlord_email == current_user.email).sort("-created_at").to_list()
    return issues

@router.get("/{issue_id}", response_model=Issue)
async def get_issue(issue_id: str, current_user: User = Depends(security.get_current_user)):
    issue = await Issue.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Access control: only owner tenant or landlord
    if current_user.role == "tenant" and issue.tenant_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this issue")
        
    return issue

@router.patch("/{issue_id}", response_model=Issue)
async def update_issue_status(issue_id: str, update: IssueUpdate, current_user: User = Depends(security.get_current_user)):
    issue = await Issue.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
        
    if current_user.role != "landlord":
        raise HTTPException(status_code=403, detail="Only landlords can update status")
    
    
    if update.status:
        old_status = issue.status
        issue.status = update.status
        
        # Add timeline event
        issue.timeline_events.append({
            "date": datetime.now().isoformat(),
            "title": "Status Updated",
            "description": f"Status changed from {old_status} to {update.status} by Landlord"
        })
        
        await issue.save()
        
    return issue

from fastapi import File, UploadFile
import shutil
import os

@router.post("/{issue_id}/evidence", response_model=Issue)
async def upload_evidence(
    issue_id: str, 
    file: UploadFile = File(...), 
    current_user: User = Depends(security.get_current_user)
):
    issue = await Issue.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
        
    if current_user.role == "tenant" and issue.tenant_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # Save file locally
    file_location = f"static/uploads/{issue_id}_{file.filename}"
    with open(file_location, "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Update Issue
    evidence_data = {
        "filename": file.filename,
        "url": f"http://localhost:8000/{file_location}",
        "type": file.content_type,
        "uploaded_at": datetime.now().isoformat()
    }
    
    issue.evidence_files.append(evidence_data)
    
    # Add timeline event
    issue.timeline_events.append({
        "date": datetime.now().isoformat(),
        "title": "Evidence Uploaded",
        "description": f"File uploaded: {file.filename}"
    })
    
    await issue.save()
    return issue

from fastapi.responses import StreamingResponse
from app.services.pdf_service import PDFService

@router.get("/{issue_id}/export")
async def export_issue_pdf(issue_id: str, current_user: User = Depends(security.get_current_user)):
    issue = await Issue.get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
        
    if current_user.role == "tenant" and issue.tenant_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get user details for the report
    user = await User.get(issue.tenant_id)
    user_data = user.dict() if user else {}
    
    pdf_buffer = PDFService.generate_complaint_pack(
        issue.dict(), 
        issue.complaint_kit.dict() if issue.complaint_kit else {}, 
        user_data
    )
    
    headers = {
        'Content-Disposition': f'attachment; filename="RentResolve_Case_{issue_id}.pdf"'
    }
    
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)
