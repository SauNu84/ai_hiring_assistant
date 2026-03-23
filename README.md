# AI Hiring Assistant

A candidate-facing evaluation tool that scores CV-to-JD fit and gives actionable gap advice — powered by the Claude API.

## What It Does

- **Upload or URL-fetch a Job Description** (PDF, DOCX, or paste a public URL)
- **Upload your CV** (PDF or DOCX)
- Click **Evaluate** — a 3-stage Claude pipeline parses the JD, parses the CV, then scores the match
- See an **overall fit score** (0–100), **4-dimension breakdown**, **gap analysis**, and **CV improvement suggestions** — all in one page, no login required

### Scoring Dimensions

| Dimension | Weight |
|---|---|
| Technical Skills Match | 35 pts |
| Experience Level | 25 pts |
| Domain / Industry Fit | 20 pts |
| Keyword & Role Alignment | 20 pts |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router), React 18, Tailwind CSS, TypeScript |
| Backend | FastAPI 0.115, Python 3.12 |
| AI | Anthropic Claude (via `anthropic` SDK) |
| File parsing | PyMuPDF (PDF), python-docx (DOCX) |
| URL scraping | Jina.ai reader API |
| Containerisation | Docker + Docker Compose |

---

## Prerequisites

- **Docker & Docker Compose** — for the recommended one-command start
- **Anthropic API key** — obtain from [console.anthropic.com](https://console.anthropic.com)

For local development without Docker:
- Python 3.12+
- Node.js 20+

---

## Quick Start (Docker Compose)

```bash
# 1. Clone the repository
git clone https://github.com/SauNu84/ai_hiring_assistant.git
cd ai_hiring_assistant

# 2. Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Start the full stack
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs

---

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
# NEXT_PUBLIC_API_URL defaults to http://localhost:8000 when not set
npm run dev
```

Then open http://localhost:3000.

---

## API Reference

All routes are prefixed with `/api`.

### `GET /api/health`
Returns `{ "status": "ok", "version": "0.1.0" }`.

### `POST /api/evaluate/upload`
Evaluate CV against a JD — both as uploaded files.

| Field | Type | Description |
|---|---|---|
| `jd_file` | File | Job description — PDF or DOCX, max 10 MB |
| `cv_file` | File | Candidate CV — PDF or DOCX, max 10 MB |

### `POST /api/evaluate/url`
Evaluate CV against a JD fetched from a public URL.

| Field | Type | Description |
|---|---|---|
| `jd_url` | Form string | Public URL to a job posting |
| `cv_file` | File | Candidate CV — PDF or DOCX, max 10 MB |

Both endpoints return an [evaluation result object](#evaluation-result-schema).

### Evaluation Result Schema

```json
{
  "evaluation_id": "uuid",
  "overall_score": 74,
  "dimension_scores": {
    "technical_skills": 28,
    "experience_level": 20,
    "domain_fit": 14,
    "keyword_alignment": 12
  },
  "verdict": "good_match",
  "hard_gaps": [
    {
      "requirement": "Kubernetes",
      "advice": "Add a Kubernetes project to your GitHub and highlight it",
      "resources": ["https://kubernetes.io/docs/tutorials/"]
    }
  ],
  "soft_gaps": [...],
  "hidden_strengths": [...],
  "cv_improvements": {
    "summary_rewrite": "...",
    "skills_section_rewrite": "...",
    "highlight_suggestions": [...]
  }
}
```

Verdict labels: `strong_match` | `good_match` | `partial_match` | `weak_match` | `poor_match`

---

## Project Structure

```
ai_hiring_assistant/
├── backend/
│   ├── api/
│   │   ├── models/schemas.py          # Pydantic request/response models
│   │   └── routes/evaluate.py         # POST /evaluate/upload, /evaluate/url
│   ├── core/
│   │   ├── evaluator/pipeline.py      # 3-stage Claude evaluation pipeline
│   │   ├── parsers/
│   │   │   ├── file_parser.py         # PDF + DOCX text extraction
│   │   │   └── url_scraper.py         # Jina.ai JD URL scraper
│   │   └── prompts/
│   │       ├── jd_parser.py           # JD parsing prompt
│   │       ├── cv_parser.py           # CV parsing prompt
│   │       └── evaluator.py           # Evaluation + gap analysis prompt
│   ├── tests/test_smoke.py
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx                   # Landing / home
│   │   ├── evaluate/page.tsx          # Evaluation form
│   │   └── results/page.tsx           # Score + gap analysis results
│   ├── components/                    # Shared React components
│   ├── lib/                           # API client helpers
│   ├── Dockerfile
│   ├── next.config.mjs
│   └── package.json
├── docker-compose.yml
├── AI.md                              # Rubric schema (single source of truth)
└── PRODUCT.md                         # Product spec and user stories
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | — | Anthropic API key for Claude |
| `NEXT_PUBLIC_API_URL` | No | `http://localhost:8000` | Backend URL (used by Next.js rewrite proxy) |

---

## Running Tests

```bash
cd backend
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
pytest tests/test_smoke.py -v
```

---

## Design Decisions

- **No authentication** — MVP is session-less. No data is persisted after the request completes.
- **3-stage pipeline** — JD and CV are parsed separately before evaluation so each Claude call has a focused, bounded task. This improves accuracy and makes errors easier to attribute.
- **Next.js API rewrite proxy** — The frontend proxies `/api/*` to the backend, so no CORS issues in the browser and no API URL leaks to the client.
- **Jina.ai for URL scraping** — Handles JS-rendered pages (LinkedIn, Indeed) without a headless browser.
- **No fabrication rule** — CV improvement suggestions only reframe existing experience; they never invent skills or credentials. This is enforced at the prompt level and surfaced to the user with a disclaimer.
