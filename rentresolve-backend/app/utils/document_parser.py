import io
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
import docx

async def parse_document(file: UploadFile) -> str:
    """
    Extract text from PDF or DOCX file.
    """
    content = await file.read()
    file_type = file.filename.split('.')[-1].lower()
    
    text = ""
    
    try:
        if file_type == "pdf":
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        elif file_type in ["docx", "doc"]:
            doc = docx.Document(io.BytesIO(content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or DOCX.")
            
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from document.")
            
        return text
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing document: {str(e)}")
    finally:
        await file.seek(0) # Reset cursor just in case
