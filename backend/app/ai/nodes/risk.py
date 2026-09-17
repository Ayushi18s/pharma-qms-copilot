from app.ai.llm import ask_json
from app.config import settings

def risk_node(state):
    c = state["complaint"]
    text = state["source_text"].lower()
    if settings.ai_mock_mode:
        high_terms = ["contamination", "foreign matter", "adverse", "patient", "wrong strength", "sterility"]
        level = "HIGH" if any(t in text for t in high_terms) else "MEDIUM"
        severity = "Critical" if level == "HIGH" and any(t in text for t in ["patient", "sterility", "contamination"]) else "Major"
        score = 82 if level == "HIGH" else 58
        reasoning = "Potential product quality impact identified; QA investigation should confirm scope and patient impact." if level == "HIGH" else "A product quality defect is described; preliminary QA review is recommended."
        action = "Route to QA Investigation; quarantine/hold affected batch if warranted by site SOPs." if level == "HIGH" else "Route to QA Investigation and review batch/retain samples."
        root = "Review batch manufacturing records, packaging records, deviations and retain samples; verify whether the defect mechanism is recurring."
        capa = "If root cause is confirmed, define corrective action and preventive controls through the site's CAPA process."
        return {"risk": {"severity": severity, "risk_level": level, "risk_score": score, "confidence": 0.82, "reasoning": reasoning, "suggested_action": action, "root_cause_recommendation": root, "capa_recommendation": capa}, "messages": [f"Initial AI risk assessment generated: {level}."]}
    result = ask_json(f"Assess this pharmaceutical complaint. Return severity, risk_level (LOW/MEDIUM/HIGH/CRITICAL), risk_score 0-100, confidence 0-1, reasoning, suggested_action, root_cause_recommendation, capa_recommendation. Do not invent facts. Complaint: {c}. Source: {state['source_text']}")
    return {"risk": result, "messages": [f"Initial AI risk assessment generated: {result.get('risk_level', 'MEDIUM')}."]}
