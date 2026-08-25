from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from extraction import extract_text_from_pdf
from summarizer import generate_summary


app = FastAPI(
    title="Document Summary Assistant",
    description="API for extracting and summarizing documents",
    version="1.0.0"
)


# Allow the frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        text = extract_text_from_pdf(temp_path)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF."
            )

        return {
            "filename": file.filename,
            "text": text
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/summarize")
async def summarize_document(
    file: UploadFile = File(...),
    summary_length: str = "medium"
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    if summary_length not in {"short", "medium", "long"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid summary length. Choose short, medium or long."
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        text = extract_text_from_pdf(temp_path)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in this PDF."
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
        if os.path.exists(temp_path):
            os.remove(temp_path)