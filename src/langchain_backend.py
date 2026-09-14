"""
Enterprise compliance audit engine utilizing LangChain LCEL and Google Gemini.
Executes deterministic PII guardrails followed by structured LLM evaluation.
"""

import logging
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.guardrails.pii_sanitizer import sanitize_text_and_extract_violations
from src.models.schemas import AuditReport, AuditRequest

load_dotenv()
logger = logging.getLogger("qualityops.audit_engine")

AUDIT_PROMPT_TEMPLATE = """You are QualityOps AI, an enterprise compliance and information security auditor for customer support operations.

Analyze the following sanitized support conversation:
----------------------------------------
{sanitized_conversation}
----------------------------------------

Evaluate the customer service representative's performance against:
1. Identity verification protocols before disclosing sensitive data (LGPD / GDPR / internal compliance).
2. Adherence to operational security protocols (PCI-DSS standards for payment data, credentials, PINs).
3. Professionalism, clarity, and problem resolution quality.

You MUST respond strictly in valid JSON format with the following exact keys:
{{
    "score": <integer from 0 to 100>,
    "security_violation": <true if a security/compliance breach occurred, false otherwise>,
    "violations": [<list of strings detailing detected infractions>],
    "coaching_feedback": "<actionable constructive guidance for the representative>",
    "corrected_response": "<recommended safe and compliant phrasing for the representative>",
    "eval_metric_pass": <true if score >= 70 and security_violation is false, else false>
}}
"""


def execute_compliance_audit(request: AuditRequest) -> AuditReport:
    """
    Executes the compliance audit pipeline:
    1. Interception and sanitization of PII via deterministic guardrails.
    2. Contextual compliance evaluation via Gemini 2.5 Flash.
    3. Strict validation of output against Pydantic AuditReport schema.

    Args:
        request: Validated AuditRequest payload.

    Returns:
        AuditReport: Validated audit report model.
    """
    # 1. Deterministic PII guardrail execution
    sanitized_text, detected_pii = sanitize_text_and_extract_violations(request.conversation_text)
    has_critical_pii = any(item.severity == "CRITICAL" for item in detected_pii)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Returning structured environment fallback.")
        return AuditReport(
            score=0,
            security_violation=True,
            pii_detected=detected_pii,
            violations=["Missing environment configuration: GEMINI_API_KEY"],
            coaching_feedback="Please configure GEMINI_API_KEY in .env or environment variables before running audits.",
            corrected_response="N/A",
            eval_metric_pass=False
        )

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.0,
            max_retries=2
        )

        prompt = PromptTemplate(
            template=AUDIT_PROMPT_TEMPLATE,
            input_variables=["sanitized_conversation"]
        )

        parser = JsonOutputParser()
        chain = prompt | llm | parser

        # Synchronous invocation
        raw_result = chain.invoke({"sanitized_conversation": sanitized_text})

        # Strict contract validation via Pydantic
        report = AuditReport(
            score=int(raw_result.get("score", 50)),
            security_violation=bool(raw_result.get("security_violation", has_critical_pii)),
            pii_detected=detected_pii,
            violations=raw_result.get("violations", []),
            coaching_feedback=str(raw_result.get("coaching_feedback", "")),
            corrected_response=str(raw_result.get("corrected_response", "")),
            eval_metric_pass=bool(raw_result.get("eval_metric_pass", False))
        )

        # Force penalty if critical PII was exposed
        if has_critical_pii and report.score > 40:
            report.score = 30
            report.security_violation = True
            report.eval_metric_pass = False

        return report

    except Exception as exc:
        logger.error(f"Audit pipeline execution failed: {exc!s}", exc_info=True)
        return AuditReport(
            score=0,
            security_violation=True,
            pii_detected=detected_pii,
            violations=[f"Inference pipeline failure: {exc!s}"],
            coaching_feedback="The audit pipeline encountered an execution error. Please retry.",
            corrected_response="N/A",
            eval_metric_pass=False
        )


def run_audit_chain(chat_text: str) -> dict:
    """
    Backward-compatible entrypoint for Streamlit UI integration.
    Wraps execute_compliance_audit and serializes output to dictionary.
    """
    req = AuditRequest(conversation_text=chat_text)
    report = execute_compliance_audit(req)
    return report.model_dump()
