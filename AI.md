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
