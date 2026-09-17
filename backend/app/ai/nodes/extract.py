import re
from app.ai.llm import ask_json
from app.config import settings


def mock_extract(text: str) -> dict:
    def grab(pattern, default="Not Provided"):
        m = re.search(pattern, text, re.I)
        return m.group(1).strip() if m else default
    product = grab(r"(?:product|in|for)\s*[:\-]?\s*([A-Za-z][A-Za-z ]+(?:Capsules|Tablets|API|FDF))")
    batch = grab(r"batch(?: number)?\s*[:#\-]?\s*([A-Z0-9\-]+)")
    qty = grab(r"affected quantity\s*(?:is|:)\s*([\w ()]+)")
    customer = grab(r"(?:customer|pharmacy)\s*[:\-]?\s*([A-Za-z][A-Za-z .&]+)")
    return {
        "complaint_source": "Pharmacy" if "pharmacy" in text.lower() else "Email",
        "customer_name": customer,
        "product_name": product,
        "product_strength": grab(r"(\d+\s*(?:mg|g|mcg|%)\b)", "Not Provided"),
        "batch_number": batch,
        "affected_quantity": qty,
        "manufacturing_date": grab(r"manufacturing date\s*[:\-]?\s*([A-Za-z0-9 ,]+)", "Not Provided"),
        "expiry_date": grab(r"expiry date\s*[:\-]?\s*([A-Za-z0-9 ,]+)", "Not Provided"),
        "originating_site": "Manufacturing",
        "impacted_materials": "Primary Packaging (Bottle)" if "seal" in text.lower() or "bottle" in text.lower() else "Not Provided",
        "complaint_category": "Product Quality Complaint",
        "complaint_description": text.strip(),
        "defect_summary": text.strip()[:500],
    }


def extract_node(state):
    text = state["source_text"]
    if settings.ai_mock_mode:
        data = mock_extract(text)
    else:
        data = ask_json(f"Extract a pharmaceutical customer complaint into exactly these fields:\n{list(mock_extract('').keys())}\n\nComplaint:\n{text}")
    return {"complaint": data, "messages": ["Complaint parsed successfully. Product, batch and complaint details were extracted."]}
