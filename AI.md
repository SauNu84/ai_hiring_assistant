# AI Hiring Assistant — Evaluation Rubric

This document defines the scoring rubric and evaluation methodology used by the AI engine.
It is the single source of truth for all Claude API calls in the evaluation pipeline.

---

## Evaluation Philosophy

We evaluate from the **candidate's perspective**. The goal is honest gap analysis:
- Surface what the JD requires that the candidate lacks
- Identify what the candidate has that maps well
- Give actionable, specific advice — not generic tips
- Reframe existing experience in JD-aligned language without fabricating anything

**Principle:** Never invent skills, experience, or credentials. Only reframe real facts.

---

## Scoring Dimensions (100 points total)

| Dimension | Weight | Description |
|---|---|---|
| **Technical Skills Match** | 35 pts | Hard skills, tools, languages, frameworks |
| **Experience Level** | 25 pts | Years of experience + seniority signals |
| **Domain / Industry Fit** | 20 pts | Industry knowledge, domain context |
| **Keyword & Role Alignment** | 20 pts | Job title alignment, ATS keyword coverage |

### Scoring Scale per Dimension

- **90–100%** of dimension weight: Strong match — exceeds or fully meets requirement
- **70–89%**: Good match — meets most requirements with minor gaps
- **50–69%**: Partial match — meets some requirements, notable gaps
- **30–49%**: Weak match — significant gaps, major upskilling needed
- **0–29%**: Poor match — fundamental mismatch

---

## Sub-Criteria per Dimension

### Technical Skills Match (35 pts)

| Sub-criterion | Points | Signals |
|---|---|---|
| Required hard skills coverage | 20 | Count of JD required_skills present in CV skills |
| Tools / frameworks match | 10 | Specific tools named in JD (e.g. Kubernetes, dbt, React) matched to CV |
| Depth signal | 5 | Evidence of production use vs. academic exposure (projects, job highlights) |

**Scoring guidance:**
- Full marks (35): Candidate has every required skill with evidence of production use
- 28–34: Covers ≥90% of required skills, minor tool gaps
- 21–27: Covers 70–89% of required skills, some notable missing tools
- 14–20: Covers 50–69%, key skills missing
- 0–13: Below 50% coverage or fundamental tech stack mismatch

### Experience Level (25 pts)

| Sub-criterion | Points | Signals |
|---|---|---|
| Years of experience match | 10 | Candidate total_years vs. JD experience_years_min/max |
| Seniority level match | 10 | Role title seniority in CV vs. JD seniority_level |
| Leadership / scope signals | 5 | Evidence of mentoring, owning systems, cross-functional work at appropriate level |

**Scoring guidance:**
- Full marks (25): Experience years meet or exceed JD min, seniority level aligned
- If candidate is 1–2 years below JD min: deduct 5–8 pts; note as soft gap
- If candidate is 3+ years below JD min: deduct 15+ pts; note as hard gap
- Overqualification (5+ years above JD max): deduct 5 pts; flag as potential red flag

### Domain / Industry Fit (20 pts)

| Sub-criterion | Points | Signals |
|---|---|---|
| Industry match | 10 | CV company industries vs. JD industry context |
| Domain knowledge signals | 10 | Certifications, project context, terminology in CV matching JD domain |

**Scoring guidance:**
- Full marks (20): Candidate has direct industry experience and domain-specific terminology
- 15–19: Adjacent industry or domain with transferable signals
- 10–14: Different industry but domain knowledge evidenced (certs, side projects)
- 0–9: No industry or domain overlap; full pivot

### Keyword & Role Alignment (20 pts)

| Sub-criterion | Points | Signals |
|---|---|---|
| Role title alignment | 8 | CV current_title vs. JD role_title similarity |
| ATS keyword coverage | 8 | JD keywords present verbatim or semantically equivalent in CV |
| Job level framing | 4 | Language in CV aligns with seniority expectations of the JD |

**Scoring guidance:**
- Full marks (20): Role title matches or is a direct equivalent; ≥80% JD keywords covered in CV
- 15–19: Title adjacent; 60–79% keyword coverage
- 10–14: Different title but clear overlap; 40–59% keyword coverage
- 0–9: Title mismatch and <40% keyword coverage

---

## Gap Classification

| Type | Definition | Advice approach |
|---|---|---|
| **Hard gap** | Must-have requirement missing from CV | "You need to learn/add X before applying" |
| **Soft gap** | Nice-to-have requirement missing | "Adding X would strengthen your application" |
| **Hidden strength** | Candidate has relevant skill not surfaced clearly | "Highlight X more prominently — it directly maps to Y in JD" |
| **Overqualified** | Candidate clearly exceeds a requirement | Flag it — could raise red flags for employer |

---

## JD Parser Output Schema

```json
{
  "role_title": "string",
  "seniority_level": "junior|mid|senior|lead|principal|staff",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "responsibilities": ["string"],
  "experience_years_min": "number|null",
  "experience_years_max": "number|null",
  "industry": "string|null",
  "keywords": ["string"]
}
```

## CV Parser Output Schema

```json
{
  "name": "string",
  "current_title": "string",
  "total_years_experience": "number",
  "skills": ["string"],
  "experience": [
    {
      "title": "string",
      "company": "string",
      "duration_months": "number",
      "highlights": ["string"]
    }
  ],
  "education": [
    {
      "degree": "string",
      "field": "string",
      "institution": "string"
    }
  ],
  "certifications": ["string"],
  "keywords": ["string"]
}
```

## Evaluation Output Schema

```json
{
  "overall_score": "number (0-100)",
  "dimension_scores": {
    "technical_skills": "number (0-35)",
    "experience_level": "number (0-25)",
    "domain_fit": "number (0-20)",
    "keyword_alignment": "number (0-20)"
  },
  "verdict": "strong_match|good_match|partial_match|weak_match|poor_match",
  "hard_gaps": [
    {
      "requirement": "string",
      "advice": "string",
      "resources": ["string"]
    }
  ],
  "soft_gaps": [
    {
      "requirement": "string",
      "advice": "string"
    }
  ],
  "hidden_strengths": [
    {
      "skill": "string",
      "jd_mapping": "string",
      "reframe_suggestion": "string"
    }
  ],
  "cv_improvements": {
    "summary_rewrite": "string",
    "skills_section_rewrite": "string",
    "highlight_suggestions": ["string"]
  }
}
```
