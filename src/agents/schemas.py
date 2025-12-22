from pydantic import BaseModel
from typing import List

class ComplianceResult(BaseModel):
    score: int
    security_violation: bool
    violations: List[str]
    coaching_feedback: str
    corrected_response: str
