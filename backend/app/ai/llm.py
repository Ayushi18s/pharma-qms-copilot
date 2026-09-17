import json
from groq import Groq
from app.config import settings

SYSTEM_PROMPT = """You are an AI assistant inside a pharmaceutical Quality Management System (QMS).
Your job is to structure customer complaint information for QA review.
Never invent facts. If a value is absent, use 'Not Provided'.
Risk assessments are preliminary recommendations, not final QA decisions.
Return valid JSON only when JSON is requested.
"""

def _client():
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")
    return Groq(api_key=settings.groq_api_key)

def ask_json(instruction: str) -> dict:
    client = _client()
    models = [settings.groq_model]
    if settings.groq_fallback_model and settings.groq_fallback_model not in models:
        models.append(settings.groq_fallback_model)
    last_error = None
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0.1,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": instruction},
                ],
            )
            raw = response.choices[0].message.content or "{}"
            return json.loads(raw)
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Groq request failed: {last_error}")
