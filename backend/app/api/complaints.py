from datetime import datetime, timezone
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Complaint
from app.schemas import AnalysisResponse, ComplaintCreate, ComplaintUpdate
from app.ai.graph import run_graph
from app.services.document import extract_pdf_text
from app.services.duplicates import find_possible_duplicate

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

def normalize(state):
    return {
        "complaint": state["complaint"],
        "risk": state["risk"],
        "completeness": state["completeness"],
        "ai_messages": state.get("messages", []),
    }

@router.post("/analyze", response_model=AnalysisResponse)
def analyze(payload: dict, db: Session = Depends(get_db)):
    text = (payload.get("text") or "").strip()
    if not text:
        raise HTTPException(400, "Complaint text is required")
    state = run_graph(text)
    result = normalize(state)
    result["possible_duplicate"] = find_possible_duplicate(db, result["complaint"])
    return result

@router.post("/analyze-file", response_model=AnalysisResponse)
async def analyze_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = await file.read()
    if file.filename and file.filename.lower().endswith(".pdf"):
        text = extract_pdf_text(data, file.filename)
    else:
        text = data.decode("utf-8", errors="ignore")
    if not text.strip():
        raise HTTPException(400, "Could not extract text from uploaded file")
    state = run_graph(text)
    result = normalize(state)
    result["possible_duplicate"] = find_possible_duplicate(db, result["complaint"])
    return result

@router.post("", response_model=dict)
def create(payload: ComplaintCreate, db: Session = Depends(get_db)):
    count = db.query(Complaint).count() + 1
    number = f"CC-2026-{count:04d}"
    c = Complaint(
        complaint_number=number,
        **payload.complaint.model_dump(),
        **payload.risk.model_dump(exclude={"confidence", "root_cause_recommendation", "capa_recommendation", "reasoning", "suggested_action"}),
        risk_reasoning=payload.risk.reasoning,
        suggested_action=payload.risk.suggested_action,
        capa_recommendation=payload.risk.capa_recommendation,
        completeness_score=payload.completeness.score,
        missing_information=payload.completeness.missing_information,
        source_text=payload.source_text,
        status="Logged",
    )
    db.add(c); db.commit(); db.refresh(c)
    return {"id": c.id, "complaint_number": number, "status": c.status}

@router.get("")
def list_complaints(db: Session = Depends(get_db)):
    rows = db.query(Complaint).order_by(Complaint.created_at.desc()).all()
    return [{"id": c.id, "complaint_number": c.complaint_number, "customer_name": c.customer_name, "product_name": c.product_name, "batch_number": c.batch_number, "risk_level": c.risk_level, "severity": c.severity, "status": c.status, "created_at": c.created_at} for c in rows]

@router.get("/{complaint_id}")
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    c = db.get(Complaint, complaint_id)
    if not c: raise HTTPException(404, "Complaint not found")
    return {k: getattr(c, k) for k in ["id","complaint_number","complaint_source","customer_name","product_name","product_strength","batch_number","affected_quantity","manufacturing_date","expiry_date","originating_site","impacted_materials","complaint_category","complaint_description","defect_summary","severity","risk_level","risk_score","risk_reasoning","suggested_action","capa_recommendation","completeness_score","missing_information","source_text","status"]}

@router.put("/{complaint_id}")
def update_complaint(complaint_id: int, payload: ComplaintUpdate, db: Session = Depends(get_db)):
    c = db.get(Complaint, complaint_id)
    if not c: raise HTTPException(404, "Complaint not found")
    for key, value in payload.complaint.model_dump().items(): setattr(c, key, value)
    for key, value in payload.risk.model_dump().items():
        if key in {"reasoning","suggested_action","capa_recommendation"}: continue
        setattr(c, key, value)
    c.risk_reasoning = payload.risk.reasoning
    c.suggested_action = payload.risk.suggested_action
    c.capa_recommendation = payload.risk.capa_recommendation
    c.completeness_score = payload.completeness.score
    c.missing_information = payload.completeness.missing_information
    if payload.source_text: c.source_text = payload.source_text
    c.updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": "updated", "id": c.id}
