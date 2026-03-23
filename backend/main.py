"""FastAPI application entry point."""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.logging_config import configure_logging, get_logger
from api.routes.evaluate import router as evaluate_router

configure_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="AI Hiring Assistant API",
    description="Candidate-facing CV vs JD evaluation engine powered by Claude",
    version="0.1.0",
)

_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(
        "HTTP error",
        extra={"status_code": exc.status_code, "detail": exc.detail,
               "path": str(request.url)},
    )
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "Validation error",
        extra={"detail": str(exc), "path": str(request.url)},
    )
    return JSONResponse(status_code=422, content={"error": str(exc)})


app.include_router(evaluate_router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
