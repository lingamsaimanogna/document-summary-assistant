from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from extraction import (
    extract_text_from_pdf,
    extract_text_from_image
)


from summarizer import generate_summary

app = FastAPI(
    title="Document Summary Assistant",
    description="API for extracting and summarizing documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Document Summary Assistant API is running"
    }


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):

    allowed_types = {
        "application/pdf",
        "image/png",
        "image/jpeg"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF, PNG, JPG or JPEG file."
        )

    contents = await file.read()

    file_extension = ".pdf"

    if file.content_type == "image/png":
        file_extension = ".png"
    elif file.content_type == "image/jpeg":
        file_extension = ".jpg"

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:

        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(temp_path)

        else:
            text = extract_text_from_image(temp_path)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this document."
            )

        return {
            "filename": file.filename,
            "text": text
        }

    finally:
        os.remove(temp_path)


@app.post("/summarize")
async def summarize_document(
    file: UploadFile = File(...),
    summary_length: str = "medium"
):

    allowed_types = {
        "application/pdf",
        "image/png",
        "image/jpeg"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF, PNG, JPG or JPEG file."
        )

    if summary_length not in {"short", "medium", "long"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid summary length."
        )

    contents = await file.read()

    file_extension = ".pdf"

    if file.content_type == "image/png":
        file_extension = ".png"
    elif file.content_type == "image/jpeg":
        file_extension = ".jpg"

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:

        if file.content_type == "application/pdf":
            text = extract_text_from_pdf(temp_path)
        else:
            text = extract_text_from_image(temp_path)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this document."
            )

        result = generate_summary(
            text,
            summary_length
        )

        return {
            "filename": file.filename,
            "result": result
        }

    finally:
        os.remove(temp_path)