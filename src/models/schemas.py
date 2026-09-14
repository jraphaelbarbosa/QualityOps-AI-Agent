"""
Data contracts and schema definitions for QualityOps AI audit pipelines.
Enforces validation and serialization using Pydantic v2.
"""

from typing import Literal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator


class PIIViolation(BaseModel):
    """Contract for sensitive data detection and leak auditing."""
    field_type: Literal["CPF", "CREDIT_CARD", "PHONE", "EMAIL", "API_KEY", "OTHER"]
    masked_value: str = Field(..., description="Masked value for audit log retention")
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = "HIGH"


class AuditRequest(BaseModel):
    """Input payload for customer conversation compliance validation."""
    conversation_text: str = Field(
        ...,
        min_length=10,
        description="Customer service chat or audio transcription text"
    )
    channel: str = Field(default="customer_support", description="Origin channel (chat, voice, ticket)")
    metadata: dict[str, str] = Field(default_factory=dict, description="Session or agent metadata")


class AuditReport(BaseModel):
    """Strict output schema for compliance audit reports."""
    score: int = Field(..., ge=0, le=100, description="Compliance score ranging from 0 to 100")
    security_violation: bool = Field(..., description="Flag indicating critical security or compliance breaches")
    pii_detected: list[PIIViolation] = Field(default_factory=list, description="List of detected and intercepted sensitive entities")
    violations: list[str] = Field(default_factory=list, description="Detailed descriptions of violated business or regulatory rules")
    coaching_feedback: str = Field(..., description="Actionable constructive guidance for the representative")
    corrected_response: str = Field(..., description="Recommended safe and compliant phrasing for the representative")
    eval_metric_pass: bool = Field(default=True, description="Quality gate evaluation pass/fail status")
    audited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC timestamp of audit execution")

    @field_validator("score")
    @classmethod
    def validate_score_range(cls, v: int) -> int:
        if not (0 <= v <= 100):
            raise ValueError("Audit score must be strictly between 0 and 100.")
        return v
