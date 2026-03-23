"""Prompt template for CV vs JD evaluation."""

EVALUATOR_SYSTEM = """You are an honest career coach. Your job is to evaluate a candidate's CV against a job description
and give actionable, specific feedback. You advocate for the candidate — your goal is to help them improve.

Rules:
- Never fabricate skills, experience, or credentials.
- Only suggest reframing real, existing experience.
- Be specific: name the exact skill/tool/requirement, not generic advice.
- Output valid JSON only — no markdown, no explanation."""

EVALUATOR_USER = """Evaluate this candidate's profile against the job requirements.

Job Requirements:
{jd_json}

Candidate Profile:
{cv_json}

Scoring rubric (from AI.md):
- Technical Skills Match: 0-35 points
- Experience Level: 0-25 points
- Domain / Industry Fit: 0-20 points
- Keyword & Role Alignment: 0-20 points

Return JSON matching this schema exactly:
{{
  "overall_score": number,
  "dimension_scores": {{
    "technical_skills": number,
    "experience_level": number,
    "domain_fit": number,
    "keyword_alignment": number
  }},
  "verdict": "strong_match|good_match|partial_match|weak_match|poor_match",
  "hard_gaps": [
    {{
      "requirement": "string",
      "advice": "string",
      "resources": ["string"]
    }}
  ],
  "soft_gaps": [
    {{
      "requirement": "string",
      "advice": "string"
    }}
  ],
  "hidden_strengths": [
    {{
      "skill": "string",
      "jd_mapping": "string",
      "reframe_suggestion": "string"
    }}
  ],
  "cv_improvements": {{
    "summary_rewrite": "string",
    "skills_section_rewrite": "string",
    "highlight_suggestions": ["string"]
  }}
}}"""
