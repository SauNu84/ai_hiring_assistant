"""Pydantic request/response schemas for the API."""
from pydantic import BaseModel, HttpUrl
from typing import Optional


class EvaluateUrlRequest(BaseModel):
    """Evaluate using a public JD URL + CV text paste."""
    jd_url: HttpUrl
    cv_text: str


class EvaluationResult(BaseModel):
    """Top-level API response."""
    evaluation_id: str
    jd: dict
    cv: dict
    evaluation: dict
