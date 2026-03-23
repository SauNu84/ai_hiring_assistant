"""Evaluation API endpoints."""
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from ...core.parsers.file_parser import extract_text
from ...core.parsers.url_scraper import scrape_jd_from_url
from ...core.evaluator.pipeline import run_evaluation

router = APIRouter(prefix="/evaluate", tags=["evaluate"])


@router.post("/upload")
async def evaluate_by_upload(
    jd_file: UploadFile = File(..., description="JD as PDF or DOCX"),
    cv_file: UploadFile = File(..., description="CV as PDF or DOCX"),
):
    """Evaluate CV against JD — both uploaded as files."""
    try:
        jd_text = extract_text(await jd_file.read(), jd_file.filename)
        cv_text = extract_text(await cv_file.read(), cv_file.filename)
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
    try:
        jd_text = await scrape_jd_from_url(jd_url)
        cv_text = extract_text(await cv_file.read(), cv_file.filename)
    except (ValueError, RuntimeError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await run_evaluation(jd_text, cv_text)
    return {"evaluation_id": str(uuid.uuid4()), **result}
