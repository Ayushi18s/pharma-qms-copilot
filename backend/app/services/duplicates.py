from sqlalchemy.orm import Session
from app.db.models import Complaint

def find_possible_duplicate(db: Session, complaint: dict):
    product = complaint.get("product_name", "")
    batch = complaint.get("batch_number", "")
    if product == "Not Provided" and batch == "Not Provided":
        return None
    candidates = db.query(Complaint).order_by(Complaint.created_at.desc()).limit(100).all()
    for c in candidates:
        same_batch = batch != "Not Provided" and c.batch_number == batch
        same_product = product != "Not Provided" and c.product_name and product.lower() in c.product_name.lower()
        if same_batch or same_product:
            return {"complaint_number": c.complaint_number, "reason": "Matching product or batch information", "confidence": 0.78 if same_batch else 0.62}
    return None
