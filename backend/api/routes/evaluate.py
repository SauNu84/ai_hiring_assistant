"""Evaluation API endpoints."""
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from core.parsers.file_parser import extract_text
from core.parsers.url_scraper import scrape_jd_from_url
from core.evaluator.pipeline import run_evaluation

router = APIRouter(prefix="/evaluate", tags=["evaluate"])

UPLOAD_DIR = Path("/tmp/uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def _save_upload(file_bytes: bytes, filename: str) -> Path:
    """Persist uploaded file to /tmp/uploads/ and return the path."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    dest = UPLOAD_DIR / f"{uuid.uuid4()}_{filename}"
    dest.write_bytes(file_bytes)
    return dest


def _validate_and_read(file_bytes: bytes, filename: str) -> bytes:
    """Raise 400 if file exceeds size limit."""
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File '{filename}' exceeds the 10 MB limit.",
        )
    return file_bytes


@router.post("/upload")
async def evaluate_by_upload(
    jd_file: UploadFile = File(..., description="JD as PDF or DOCX"),
    cv_file: UploadFile = File(..., description="CV as PDF or DOCX"),
):
    """Evaluate CV against JD — both uploaded as files."""
    jd_bytes = _validate_and_read(await jd_file.read(), jd_file.filename)
    cv_bytes = _validate_and_read(await cv_file.read(), cv_file.filename)

    _save_upload(jd_bytes, jd_file.filename)
    _save_upload(cv_bytes, cv_file.filename)

    try:
        jd_text = extract_text(jd_bytes, jd_file.filename)
        cv_text = extract_text(cv_bytes, cv_file.filename)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await run_evaluation(jd_text, cv_text)
    return {"evaluation_id": str(uuid.uuid4()), **result}


@router.post("/url")
async def evaluate_by_url(
    jd_url: str = Form(..., description="Public URL to job posting"),
    cv_file: UploadFile = File(..., description="CV as PDF or DOCX"),
):
    """Evaluate CV against JD fetched from a public URL."""
    cv_bytes = _validate_and_read(await cv_file.read(), cv_file.filename)
    _save_upload(cv_bytes, cv_file.filename)

    try:
        jd_text = await scrape_jd_from_url(jd_url)
        cv_text = extract_text(cv_bytes, cv_file.filename)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await run_evaluation(jd_text, cv_text)
    return {"evaluation_id": str(uuid.uuid4()), **result}
