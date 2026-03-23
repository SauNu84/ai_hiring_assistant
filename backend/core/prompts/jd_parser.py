"""Prompt template for JD parsing."""

JD_PARSER_SYSTEM = """You are a job description analyst. Extract structured requirements from job descriptions.
Output valid JSON only — no markdown, no explanation.
Follow the schema exactly. Use null for missing fields."""

JD_PARSER_USER = """Parse this job description and extract structured requirements.

Job Description:
{jd_text}

Return JSON matching this schema exactly:
{{
  "role_title": "string",
  "seniority_level": "junior|mid|senior|lead|principal|staff",
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "responsibilities": ["string"],
  "experience_years_min": number_or_null,
  "experience_years_max": number_or_null,
  "industry": "string_or_null",
  "keywords": ["string"]
}}"""
