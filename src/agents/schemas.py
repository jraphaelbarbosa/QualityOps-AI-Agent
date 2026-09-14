
from pydantic import BaseModel


class ComplianceResult(BaseModel):
    score: int
    security_violation: bool
    violations: list[str]
    coaching_feedback: str
    corrected_response: str
