"""Main evaluation pipeline — orchestrates all Claude API calls."""
import json
from anthropic import AsyncAnthropic

from ..prompts.jd_parser import JD_PARSER_SYSTEM, JD_PARSER_USER
from ..prompts.cv_parser import CV_PARSER_SYSTEM, CV_PARSER_USER
from ..prompts.evaluator import EVALUATOR_SYSTEM, EVALUATOR_USER

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096


async def _call_claude(client: AsyncAnthropic, system: str, user: str) -> dict:
    """Single structured Claude API call — returns parsed JSON."""
    message = await client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    raw = message.content[0].text
    return json.loads(raw)


async def run_evaluation(jd_text: str, cv_text: str) -> dict:
    """
    Full evaluation pipeline:
    1. Parse JD → structured requirements
    2. Parse CV → structured profile
    3. Evaluate → scores, gaps, advice, CV rewrite suggestions
    """
    client = AsyncAnthropic()

    # Step 1: Parse JD
    jd_data = await _call_claude(
        client,
        JD_PARSER_SYSTEM,
        JD_PARSER_USER.format(jd_text=jd_text),
    )

    # Step 2: Parse CV
    cv_data = await _call_claude(
        client,
        CV_PARSER_SYSTEM,
        CV_PARSER_USER.format(cv_text=cv_text),
    )

    # Step 3: Evaluate
    evaluation = await _call_claude(
        client,
        EVALUATOR_SYSTEM,
        EVALUATOR_USER.format(
            jd_json=json.dumps(jd_data, indent=2),
            cv_json=json.dumps(cv_data, indent=2),
        ),
    )

    return {
        "jd": jd_data,
        "cv": cv_data,
        "evaluation": evaluation,
    }
