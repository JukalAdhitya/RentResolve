from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from app.services import email_service
from app.core import security
from app.db.models import User

router = APIRouter(prefix="/email", tags=["Email"])

class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    issue_id: str

@router.post("/send")
async def send_email_endpoint(
    email_req: EmailRequest, 
    background_tasks: BackgroundTasks,
    current_user: User = Depends(security.get_current_user)
):
    # Enqueue email sending to background
    background_tasks.add_task(
        email_service.send_email, 
        email_req.to, 
        email_req.subject, 
        email_req.body, 
        email_req.issue_id
    )
    return {"message": "Email queued for sending"}
