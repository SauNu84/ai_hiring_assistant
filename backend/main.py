"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.evaluate import router as evaluate_router

app = FastAPI(
    title="AI Hiring Assistant API",
    description="Candidate-facing CV vs JD evaluation engine powered by Claude",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(evaluate_router, prefix="/api")


@app.get("/api/health")
async def health():
    return {"status": "ok"}
