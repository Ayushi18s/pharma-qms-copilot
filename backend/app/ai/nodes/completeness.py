from app.ai.llm import ask_json
from app.config import settings

REQUIRED = ["customer_name", "product_name", "batch_number", "complaint_description"]

def completeness_node(state):
    c = state["complaint"]
    missing = [f.replace("_", " ").title() for f in REQUIRED if not c.get(f) or c.get(f) == "Not Provided"]
    score = round((len(REQUIRED)-len(missing))/len(REQUIRED)*100, 1)
    if not settings.ai_mock_mode:
        try:
            result = ask_json(f"Assess completeness of this pharmaceutical complaint. Required fields: {REQUIRED}. Return score 0-100 and missing_information list. Complaint JSON: {c}")
            score = float(result.get("score", score))
            missing = result.get("missing_information", missing)
        except Exception:
            pass
    return {"completeness": {"score": score, "missing_information": missing}, "messages": [f"Completeness check: {score:.0f}%."]}
