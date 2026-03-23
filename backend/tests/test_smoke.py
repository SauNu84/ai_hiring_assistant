"""Smoke tests for the AI Hiring Assistant API."""
import io
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app

client = TestClient(app)

MOCK_EVAL_RESULT = {
    "jd": {
        "role_title": "Software Engineer",
        "seniority_level": "mid",
        "required_skills": ["Python", "FastAPI"],
        "preferred_skills": ["Docker"],
        "responsibilities": ["Build APIs"],
        "experience_years_min": 2,
        "experience_years_max": 5,
        "industry": "Tech",
        "keywords": ["Python", "API"],
    },
    "cv": {
        "name": "Jane Doe",
        "current_title": "Software Engineer",
        "total_years_experience": 3,
        "skills": ["Python", "FastAPI", "Docker"],
        "experience": [
            {
                "title": "SWE",
                "company": "Acme",
                "duration_months": 36,
                "highlights": ["Built REST APIs"],
            }
        ],
        "education": [{"degree": "BSc", "field": "CS", "institution": "MIT"}],
        "certifications": [],
        "keywords": ["Python", "FastAPI"],
    },
    "evaluation": {
        "overall_score": 80,
        "dimension_scores": {
            "technical_skills": 30,
            "experience_level": 20,
            "domain_fit": 15,
            "keyword_alignment": 15,
        },
        "verdict": "strong_match",
        "hard_gaps": [],
        "soft_gaps": [],
        "hidden_strengths": [],
        "cv_improvements": {
            "summary_rewrite": "Experienced engineer.",
            "skills_section_rewrite": "Python, FastAPI, Docker",
            "highlight_suggestions": [],
        },
    },
}


def _make_pdf_bytes() -> bytes:
    """Minimal valid PDF bytes for testing."""
    return (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\n"
        b"xref\n0 4\n0000000000 65535 f\n"
        b"trailer<</Size 4/Root 1 0 R>>\nstartxref\n%%EOF\n"
    )


def test_health():
    """Health endpoint returns 200 with correct payload."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


def test_invalid_file_type_returns_400_error_json():
    """Uploading a .txt file returns 400 with {\"error\": ...} body."""
    txt_bytes = b"This is plain text"
    response = client.post(
        "/api/evaluate/upload",
        files={
            "jd_file": ("jd.txt", io.BytesIO(txt_bytes), "text/plain"),
            "cv_file": ("cv.txt", io.BytesIO(txt_bytes), "text/plain"),
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "txt" in data["error"].lower() or "unsupported" in data["error"].lower()


def test_file_too_large_returns_400():
    """Uploading a file exceeding 10 MB returns 400 with {\"error\": ...}."""
    oversized = b"x" * (10 * 1024 * 1024 + 1)
    response = client.post(
        "/api/evaluate/upload",
        files={
            "jd_file": ("jd.pdf", io.BytesIO(oversized), "application/pdf"),
            "cv_file": ("cv.pdf", io.BytesIO(b"%PDF-1.4"), "application/pdf"),
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "10 mb" in data["error"].lower() or "limit" in data["error"].lower()


@patch("api.routes.evaluate.run_evaluation", new_callable=AsyncMock)
@patch("api.routes.evaluate.extract_text", return_value="Sample text")
def test_evaluate_upload_end_to_end(mock_extract, mock_run):
    """Full upload flow returns evaluation JSON with all required fields."""
    mock_run.return_value = MOCK_EVAL_RESULT

    pdf_bytes = _make_pdf_bytes()
    response = client.post(
        "/api/evaluate/upload",
        files={
            "jd_file": ("jd.pdf", io.BytesIO(pdf_bytes), "application/pdf"),
            "cv_file": ("cv.pdf", io.BytesIO(pdf_bytes), "application/pdf"),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "evaluation_id" in data
    assert "jd" in data
    assert "cv" in data
    assert "evaluation" in data
    assert data["evaluation"]["overall_score"] == 80
    assert data["evaluation"]["verdict"] == "strong_match"
