from pydantic import BaseModel, Field
from typing import Any

class ComplaintData(BaseModel):
    complaint_source: str = "Unknown"
    customer_name: str = "Not Provided"
    product_name: str = "Not Provided"
    product_strength: str = "Not Provided"
    batch_number: str = "Not Provided"
    affected_quantity: str = "Not Provided"
    manufacturing_date: str = "Not Provided"
    expiry_date: str = "Not Provided"
    originating_site: str = "Manufacturing"
    impacted_materials: str = "Not Provided"
    complaint_category: str = "Product Quality Complaint"
    complaint_description: str = "Not Provided"
    defect_summary: str = "Not Provided"

class RiskAssessment(BaseModel):
    severity: str = "Major"
    risk_level: str = "MEDIUM"
    risk_score: float = Field(default=50, ge=0, le=100)
    confidence: float = Field(default=0.75, ge=0, le=1)
    reasoning: str = "Initial QA review recommended."
    suggested_action: str = "Route to QA investigation."
    root_cause_recommendation: str = "Review batch, packaging and manufacturing records."
    capa_recommendation: str = "Evaluate corrective and preventive actions after investigation."

class Completeness(BaseModel):
    score: float = Field(default=50, ge=0, le=100)
    missing_information: list[str] = []

class AnalysisResponse(BaseModel):
    complaint: ComplaintData
    risk: RiskAssessment
    completeness: Completeness
    possible_duplicate: dict[str, Any] | None = None
    ai_messages: list[str] = []

class ComplaintCreate(BaseModel):
    complaint: ComplaintData
    risk: RiskAssessment
    completeness: Completeness
    source_text: str

class ComplaintUpdate(BaseModel):
    complaint: ComplaintData
    risk: RiskAssessment
    completeness: Completeness
    source_text: str | None = None
