# AI Hiring Assistant — Product Specification

## MVP Scope

**Version:** 1.0
**Goal:** Deliver a working candidate-facing evaluation tool that scores CV-to-JD fit and gives actionable gap advice.

### In Scope (MVP)

| Feature | Description |
|---|---|
| JD ingestion — URL | Paste a public job posting URL; system extracts JD content via Jina.ai |
| JD ingestion — File | Upload PDF or DOCX JD; system extracts text |
| CV upload | Upload PDF or DOCX resume; system extracts structured profile |
| AI evaluation | 3-stage Claude pipeline: JD parse → CV parse → evaluate |
| Fit score display | Overall score (0–100) + 4-dimension breakdown |
| Gap report | Hard gaps, soft gaps, hidden strengths with per-item advice |
| CV improvement suggestions | Rewritten summary + skills section aligned to JD (no fabrication) |
| Results page | Single-page results view with score, report, and suggestions |

### Out of Scope (MVP — V2 and beyond)

- User accounts / auth (no login required for MVP)
- Saving or persisting evaluations
- JD inventory / multi-JD comparison
- LinkedIn CV import
- Progress tracking (score improvement over time)
- Learning path / course recommendations
- Interview question preview
- Mobile-optimized UI (responsive is enough)
- Bulk / batch evaluation

---

## User Personas

| Persona | Description | Primary Motivation |
|---|---|---|
| **Active Job Seeker** | Applying to multiple roles, getting low response rates | Understand why CVs are rejected; know what to fix |
| **Career Switcher** | Moving domains (e.g. QA → Dev, Finance → PM) | Know which skills to prioritize learning first |
| **Student / New Grad** | First job search, no recruiter feedback loop | Get honest benchmark vs. real job requirements |

**Primary target for MVP:** Active Job Seeker — highest pain, most immediate value.

---

## User Stories

### Epic 1 — JD Ingestion

**US-01 — Paste JD URL**
As an active job seeker, I want to paste a URL from LinkedIn, Indeed, or a company careers page so that I don't have to manually copy the job description.

*Acceptance criteria:*
- [ ] User can paste any public URL into an input field
- [ ] System fetches and extracts JD text (via Jina.ai or fallback)
- [ ] Extracted JD content is displayed for user confirmation before evaluation
- [ ] If URL scraping fails, user sees a clear error and is prompted to upload a file instead
- [ ] Loading state shown while fetching

**US-02 — Upload JD File**
As an active job seeker, I want to upload a PDF or DOCX job description so that I can evaluate roles from company portals that block scrapers.

*Acceptance criteria:*
- [ ] Accepts PDF and DOCX files up to 5 MB
- [ ] Rejects unsupported file types with a clear error message
- [ ] Extracted text displayed for confirmation before evaluation
- [ ] File upload shows progress indicator

---

### Epic 2 — CV Upload

**US-03 — Upload CV**
As an active job seeker, I want to upload my CV as a PDF or DOCX so that the system can analyze my experience against the JD.

*Acceptance criteria:*
- [ ] Accepts PDF and DOCX files up to 5 MB
- [ ] Rejects unsupported file types with clear error
- [ ] System extracts structured data (skills, experience, education)
- [ ] Parsed CV summary shown briefly before evaluation starts

**US-04 — Paste CV text (fallback)**
As an active job seeker, I want to paste my CV as plain text if my PDF parses poorly, so that I still get accurate results even with complex PDF layouts.

*Acceptance criteria:*
- [ ] Text area fallback available on CV upload screen
- [ ] Plain text input processed identically to parsed PDF output
- [ ] Option clearly labelled as "My PDF isn't parsing well — paste text instead"

---

### Epic 3 — Evaluation & Results

**US-05 — View overall fit score**
As an active job seeker, I want to see an overall fit score (0–100) so that I can quickly understand how well my CV matches this role.

*Acceptance criteria:*
- [ ] Score displayed prominently (large number, color-coded: green ≥70, amber 50–69, red <50)
- [ ] Verdict label shown ("Strong Match", "Good Match", "Partial Match", "Weak Match", "Poor Match")
- [ ] Score explained in one sentence (e.g. "You meet most technical requirements but lack seniority signals")

**US-06 — View dimension breakdown**
As an active job seeker, I want to see how I scored in each dimension so that I know which areas drag down my overall score.

*Acceptance criteria:*
- [ ] Four dimensions shown: Technical Skills, Experience Level, Domain Fit, Keyword Alignment
- [ ] Each dimension shows score (e.g. 28/35) and a short label (Strong / Good / Partial / Weak / Poor)
- [ ] Visual representation (progress bar or similar) for each dimension

**US-07 — View gap analysis**
As an active job seeker, I want to see exactly which JD requirements I'm missing so that I know what to add to my CV or learn.

*Acceptance criteria:*
- [ ] Hard gaps listed with specific advice per gap ("Add a Python project to GitHub" not just "Learn Python")
- [ ] Soft gaps listed separately with strengthening advice
- [ ] Hidden strengths listed with specific reframe suggestions ("Rename 'data analysis' to 'product analytics'")
- [ ] Each hard gap links to at least one specific resource (course, certification, or documentation)

**US-08 — View CV improvement suggestions**
As an active job seeker, I want to see a rewritten CV summary and skills section so that I can update my CV to better fit this specific role.

*Acceptance criteria:*
- [ ] Rewritten professional summary shown (3–5 sentences, aligned to JD language)
- [ ] Rewritten skills section shown (keywords from JD that the candidate legitimately has)
- [ ] Diff-style presentation: original vs. suggested (or clear "before/after" labels)
- [ ] Disclaimer shown: "This rewrites how your experience is presented — it does not add skills you don't have"
- [ ] Copy-to-clipboard button on each section

**US-09 — Run evaluation**
As an active job seeker, I want to submit my JD and CV for evaluation and see results within 30 seconds so that I get fast feedback.

*Acceptance criteria:*
- [ ] "Evaluate" button active only when both JD and CV are provided
- [ ] Loading state with progress indication during AI processing
- [ ] Results displayed within 30 seconds for standard JD+CV pairs
- [ ] If evaluation fails, user sees a clear error message with retry option

---

### Epic 4 — UX / Accessibility

**US-10 — Mobile-responsive layout**
As an active job seeker on mobile, I want to access the tool from my phone so that I can evaluate while job hunting on the go.

*Acceptance criteria:*
- [ ] All screens usable on 375px+ viewport width
- [ ] File upload works on iOS Safari and Android Chrome
- [ ] Results page readable without horizontal scroll

**US-11 — Clear error states**
As a user, I want clear error messages when something goes wrong so that I know what action to take.

*Acceptance criteria:*
- [ ] File type error: "Only PDF and DOCX files are supported"
- [ ] URL fetch error: "Could not fetch this URL. Please upload the JD as a file instead."
- [ ] Evaluation timeout: "Evaluation is taking longer than expected. Please try again."
- [ ] All errors have an actionable next step

---

## Rubric Schema (Extended)

See `AI.md` for the canonical rubric schema used by the AI engine.

The rubric is intentionally owned by `AI.md` (single source of truth). This section captures the **product rationale** behind each dimension's weight.

| Dimension | Weight | Rationale |
|---|---|---|
| Technical Skills Match | 35 pts | Most job rejections are skills mismatches — this is the highest-signal dimension |
| Experience Level | 25 pts | Seniority misjudgment (applying senior roles with junior experience) is the #2 rejection driver |
| Domain / Industry Fit | 20 pts | Domain knowledge is hard to fake in interviews; candidates should know their domain gap |
| Keyword & Role Alignment | 20 pts | ATS filters are real; keyword coverage affects whether humans even see the CV |

**Scoring design principle:** Dimensions are scored independently. A candidate with 10 years of Python experience in fintech applying to a blockchain role can score high on Technical Skills and Experience Level but low on Domain Fit. The per-dimension view is as important as the total.

---

## MVP Acceptance Criteria (End-to-End)

The MVP is shippable when a user can:

1. Paste a LinkedIn job URL **or** upload a PDF JD
2. Upload a PDF CV
3. Click "Evaluate"
4. See an overall score, 4-dimension breakdown, gap analysis, and CV suggestions
5. All within a single page session, no login required, under 30 seconds

---

## Definition of Done (Engineering)

- [ ] E2E test: URL JD + PDF CV → evaluation result rendered
- [ ] E2E test: PDF JD + PDF CV → evaluation result rendered
- [ ] Error test: unsupported file type → clear error message
- [ ] Error test: bad URL → fallback prompt shown
- [ ] Load test: 3 concurrent evaluations complete within 60 seconds
- [ ] All CV improvement text includes "This rewrites presentation, not facts" disclaimer
- [ ] No hardcoded API keys
- [ ] `docker compose up` starts full stack cleanly
