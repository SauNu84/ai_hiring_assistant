"""Prompt template for CV/resume parsing."""

CV_PARSER_SYSTEM = """You are a resume analyst. Extract structured profile data from resumes.
Output valid JSON only — no markdown, no explanation.
Follow the schema exactly. Infer total_years_experience from work history if not stated."""

CV_PARSER_USER = """Parse this resume and extract structured profile data.

Resume:
{cv_text}

Return JSON matching this schema exactly:
{{
  "name": "string",
  "current_title": "string",
  "total_years_experience": number,
  "skills": ["string"],
  "experience": [
    {{
      "title": "string",
      "company": "string",
      "duration_months": number,
      "highlights": ["string"]
    }}
  ],
  "education": [
    {{
      "degree": "string",
      "field": "string",
      "institution": "string"
    }}
  ],
  "certifications": ["string"],
  "keywords": ["string"]
}}"""
