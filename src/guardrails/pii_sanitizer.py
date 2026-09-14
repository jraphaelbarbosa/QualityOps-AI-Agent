"""
Deterministic PII guardrails and sanitization utilities.
Intercepts and redacts sensitive data (CPF, Credit Card, Email, Phone) prior to external LLM calls.
"""

import re

from src.models.schemas import PIIViolation

# High-precision regex patterns for sensitive data
CPF_PATTERN = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\d{4}[-\s]?\d{4}|\d{4}[-\s]?\d{4})\b")


def sanitize_text_and_extract_violations(raw_text: str) -> tuple[str, list[PIIViolation]]:
    """
    Deterministic safety guardrail:
    Intercepts personally identifiable information (PII) before transmission to external language models.

    Args:
        raw_text: Raw conversation string to inspect.

    Returns:
        tuple[str, list[PIIViolation]]: Sanitized text and list of recorded violations.
    """
    violations: list[PIIViolation] = []
    sanitized = raw_text

    # 1. Detect and mask Credit Card numbers
    for match in CREDIT_CARD_PATTERN.finditer(sanitized):
        val = match.group(0)
        masked = f"****-****-****-{val[-4:]}" if len(val) >= 4 else "****"
        violations.append(
            PIIViolation(
                field_type="CREDIT_CARD",
                masked_value=masked,
                severity="CRITICAL"
            )
        )
    sanitized = CREDIT_CARD_PATTERN.sub("[REDACTED_CREDIT_CARD]", sanitized)

    # 2. Detect and mask Brazilian CPF numbers
    for match in CPF_PATTERN.finditer(sanitized):
        val = match.group(0)
        masked = f"{val[:3]}.***.***-**"
        violations.append(
            PIIViolation(
                field_type="CPF",
                masked_value=masked,
                severity="HIGH"
            )
        )
    sanitized = CPF_PATTERN.sub("[REDACTED_CPF]", sanitized)

    # 3. Detect and mask Email addresses
    for match in EMAIL_PATTERN.finditer(sanitized):
        val = match.group(0)
        parts = val.split("@")
        masked = f"{parts[0][:2]}***@{parts[1]}" if len(parts) == 2 else "***@***"
        violations.append(
            PIIViolation(
                field_type="EMAIL",
                masked_value=masked,
                severity="MEDIUM"
            )
        )
    sanitized = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", sanitized)

    # 4. Detect and mask Phone numbers
    for match in PHONE_PATTERN.finditer(sanitized):
        val = match.group(0)
        masked = f"{val[:4]}****{val[-2:]}" if len(val) >= 6 else "****"
        violations.append(
            PIIViolation(
                field_type="PHONE",
                masked_value=masked,
                severity="MEDIUM"
            )
        )
    sanitized = PHONE_PATTERN.sub("[REDACTED_PHONE]", sanitized)

    return sanitized, violations
