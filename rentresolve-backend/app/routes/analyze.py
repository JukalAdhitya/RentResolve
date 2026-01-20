from fastapi import APIRouter, HTTPException, Depends
from app.agents import tenant_agent, landlord_agent, schemas
from fastapi import UploadFile, File
from app.utils.document_parser import parse_document
from app.core import security
from app.db.models import User

router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.post("/tenant", response_model=schemas.ComplaintKit)
async def analyze_tenant_issue(input_data: schemas.TenantIssueInput, current_user: User = Depends(security.get_current_user)):
    try:
        # Inject user details if available
        if not input_data.tenant_name and current_user.full_name:
            input_data.tenant_name = current_user.full_name
        if not input_data.tenant_phone and current_user.phone_number:
            input_data.tenant_phone = current_user.phone_number
            
        result = await tenant_agent.generate_complaint_kit(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation failed: {str(e)}")

@router.post("/landlord", response_model=schemas.LandlordReply)
async def analyze_landlord_reply(input_data: schemas.LandlordReplyInput, current_user: User = Depends(security.get_current_user)):
    if current_user.role != "landlord":
        raise HTTPException(status_code=403, detail="Only landlords can use this feature")
        
    try:
        # Inject landlord details if available
        if not input_data.landlord_name and current_user.full_name:
            input_data.landlord_name = current_user.full_name
        if not input_data.landlord_phone and current_user.phone_number:
            input_data.landlord_phone = current_user.phone_number

        result = await landlord_agent.generate_landlord_reply(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation failed: {str(e)}")

@router.post("/agreement")
async def analyze_agreement(file: UploadFile = File(...), current_user: User = Depends(security.get_current_user)):
    """
    Parses a lease agreement (PDF/Docx) and extracts text.
    In a real scenario, this would also feed into an AI agent to extract key terms.
    """
    try:
        text = await parse_document(file)
        # TODO: Pass 'text' to an AI agent to summarize or extract data
        return {"filename": file.filename, "extracted_text": text[:5000]} # Limit return size for now
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document analysis failed: {str(e)}")
