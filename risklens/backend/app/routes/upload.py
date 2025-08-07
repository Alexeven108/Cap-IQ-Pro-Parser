# upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from pathlib import Path

# Optional: Your parsing function from another module
# from .parser import parse_excel_file

router = APIRouter()

# Set where to temporarily save uploaded Excel files
UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/")
async def upload_excel_file(file: UploadFile = File(...)):
    """
    Accepts an Excel file from the frontend and saves it for processing.
    """
    # ✅ Step 1: Validate file type
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")

    try:
        # ✅ Step 2: Save the uploaded file to a local directory (however if truly local, then potentially S3 buckets)
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ Step 3 (Optional): Parse the file
        # parsed_data = parse_excel_file(file_path)

        return {
            "filename": file.filename,
            "status": "Upload successful",
            # "preview_data": parsed_data[:5]  # Return a snippet if needed
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

