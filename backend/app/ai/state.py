from typing import TypedDict, Any

class ComplaintState(TypedDict, total=False):
    source_text: str
    complaint: dict[str, Any]
    risk: dict[str, Any]
    completeness: dict[str, Any]
    messages: list[str]
