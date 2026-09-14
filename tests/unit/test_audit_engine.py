"""
Unit tests for audit engine orchestration and Pydantic data contracts.
"""

from unittest.mock import patch

import pytest
from src.langchain_backend import execute_compliance_audit
from src.models.schemas import AuditReport


def test_audit_report_schema_validation():
    """Validate Pydantic v2 schema integrity."""
    report = AuditReport(
        score=85,
        security_violation=False,
        violations=[],
        coaching_feedback="Constructive coaching notes.",
        corrected_response="Maintain compliant protocols.",
        eval_metric_pass=True
    )
    assert report.score == 85
    assert not report.security_violation
    assert report.eval_metric_pass


def test_audit_report_invalid_score_raises_error():
    """Verify that out-of-range audit scores raise validation errors."""
    with pytest.raises(ValueError):
        AuditReport(
            score=150,  # Invalid
            security_violation=False,
            violations=[],
            coaching_feedback="Error",
            corrected_response="Error",
            eval_metric_pass=False
        )


def test_execute_audit_missing_env_key(sample_clean_conversation, monkeypatch):
    """Verify graceful fallback when GEMINI_API_KEY is not configured."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    report = execute_compliance_audit(sample_clean_conversation)

    assert report.score == 0
    assert report.security_violation is True
    assert "GEMINI_API_KEY" in report.violations[0]
    assert report.eval_metric_pass is False


@patch("src.langchain_backend.ChatGoogleGenerativeAI")
def test_execute_audit_with_mocked_llm(
    mock_llm_cls,
    sample_clean_conversation,
    mock_gemini_chain_response,
    monkeypatch
):
    """Verify end-to-end audit pipeline execution with mocked LLM (zero token cost, deterministic)."""
    monkeypatch.setenv("GEMINI_API_KEY", "mock_key_for_testing")

    with patch("langchain_core.prompts.PromptTemplate.__or__") as mock_pipeline:
        mock_chain = mock_pipeline.return_value.__or__.return_value
        mock_chain.invoke.return_value = mock_gemini_chain_response

        report = execute_compliance_audit(sample_clean_conversation)

        assert report.score == 95
        assert report.security_violation is False
        assert report.eval_metric_pass is True
        assert "Excellent" in report.coaching_feedback
