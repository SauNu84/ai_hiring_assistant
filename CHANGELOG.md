# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Standardized logging system (`backend/core/logging_config.py`) with:
  - Structured JSON output by default (production-ready)
  - Human-readable text format for local development (`LOG_FORMAT=text`)
  - Log-level control via `LOG_LEVEL` env var (default `INFO`)
  - `get_logger(name)` helper for per-module named loggers
  - Noise suppression for `httpx`, `httpcore`, `anthropic`, and `uvicorn.access`
- Logging instrumentation across all backend modules:
  - `main.py` — HTTP error and validation warning logs
  - `api/routes/evaluate.py` — request received, evaluation completed, parse failures
  - `core/evaluator/pipeline.py` — pipeline start/finish and per-Claude-call debug traces
  - `core/parsers/file_parser.py` — file dispatch and unsupported-type warnings
  - `core/parsers/url_scraper.py` — scrape start, empty-response warnings, success

---

## [0.5.0] - 2026-03-23

### Added
- Vercel deployment configuration (`vercel.json`) for Next.js frontend (SAU-93)
- Railway deployment configuration (`backend/railway.toml`) for FastAPI backend (SAU-93)
- Minimal server-side usage analytics with append-only JSONL event log (`backend/core/analytics.py`) — no PII stored (SAU-94)
  - Events: `evaluation_started`, `evaluation_completed`
  - Session hash derived from IP + User-Agent (SHA-256, first 16 hex chars)
  - Configurable log path via `ANALYTICS_LOG_PATH` env var
- Analytics query script (`backend/scripts/query_analytics.py`) for weekly volume and 7-day return-rate reporting

### Fixed
- Enforce 5 MB file size limit on `/api/evaluate/upload` and `/api/evaluate/url` endpoints (SAU-92)

---

## [0.4.0] - 2026-03-22

### Added
- Comprehensive README with setup instructions, API reference, and project structure (SAU-91)
- App screenshots in `docs/screenshots/` (SAU-91)

---

## [0.3.0] - 2026-03-21

### Added
- Frontend `Dockerfile` for Docker Compose (SAU-89)
- `docker-compose.yml` for local full-stack development with hot-reload

### Fixed
- Next.js API URL now configured via `NEXT_PUBLIC_API_URL` environment variable instead of being hard-coded (SAU-90)

---

## [0.2.0] - 2026-03-20

### Added
- Next.js evaluation form (`frontend/app/`) — file upload + URL input, dual-mode (SAU-84)
- Score & gap analysis results page with visual score breakdown (SAU-85)

---

## [0.1.0] - 2026-03-18

### Added
- FastAPI backend with CORS, structured error responses, and `/api/health` endpoint
- File upload endpoints: `POST /api/evaluate/upload` (PDF/DOCX for JD and CV)
- URL-based JD ingestion: `POST /api/evaluate/url` (Jina.ai reader)
- Three-step Claude evaluation pipeline (JD parse → CV parse → evaluate)
- PDF text extraction via PyMuPDF; DOCX extraction via python-docx
- Smoke tests (`backend/tests/test_smoke.py`)
- Initial `docker-compose.yml` scaffold
