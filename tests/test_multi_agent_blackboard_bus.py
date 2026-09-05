"""
Automated Pytest Test Suite for Multi Agent Blackboard Bus.
Domain: Long-Horizon Agent Context & State Architecture
Standard: Autonomous Agent State Machine & Token Economy RFC
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException
from agents.models import SystemTaskPayload, UrgencyLevel, SystemIntegrityStatus
from agents.workers import InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
from agents.supervisor import SystemSupervisor
from cli import main


def test_phi_guard_enforcement():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive for Staphylococcus")

    # Clean text passes
    PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")


def test_specialized_workers():
    # Worker 1: QC Invariant
    p1 = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=35.0)
    alerts1 = InvariantQCWorker.evaluate(p1)
    assert len(alerts1) == 1
    assert alerts1[0].urgency == UrgencyLevel.ELEVATED

    # Worker 2: Safety
    p2 = SystemTaskPayload(task_id="T2", target_identifier="KEY-02", primary_metric=10.0, is_critical_flag=True)
    alerts2 = SafetyEscalationWorker.evaluate(p2)
    assert len(alerts2) == 1
    assert alerts2[0].urgency == UrgencyLevel.CRITICAL_STAT

    # Worker 3: Protocol Conformance
    p3 = SystemTaskPayload(task_id="T3", target_identifier="KEY-03", primary_metric=10.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = ProtocolConformanceWorker.evaluate(p3)
    assert len(alerts3) == 1


def test_supervisor_consensus_and_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="TASK-PROD-01",
        target_identifier="KEY-PROD-01",
        primary_metric=12.0,
        secondary_metric=4.0,
        status_descriptor="NOMINAL"
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.ROUTINE
    assert dossier.integrity_status == SystemIntegrityStatus.VALIDATED
    assert dossier.audit_hash != ""

    # Verify cryptographic audit trail
    assert AuditLogger.verify_integrity() is True

    # CLI tests
    assert main(["audit", "--task-id", "CLI-TEST-01"]) == 0
    assert main(["chat", "Explain", "specifications"]) == 0
    assert main(["verify-audit"]) == 0


def test_phi_redaction():
    """PHI guard should redact sensitive patterns instead of only raising."""
    redacted = PHIGuard.redact_phi("Contact patient at 555-123-4567 or MRN-12345")
    assert "555-123-4567" not in redacted
    assert "MRN-12345" not in redacted
    assert "[REDACTED_IDENTIFIER]" in redacted


def test_audit_integrity_tamper_detection():
    """Audit trail should detect tampered entries."""
    from agents.base import AuditTrail
    trail = AuditTrail(secret_key="test-key-for-integrity")
    trail.log("test-actor", "test-tier", "TEST_EVENT", {"data": "original"})
    trail.log("test-actor", "test-tier", "TEST_EVENT_2", {"data": "second"})

    # Integrity should pass for unmodified trail
    assert trail.verify_integrity() is True

    # Tamper with an entry
    trail.logs[0]["payload_hash"] = "tampered_hash"
    assert trail.verify_integrity() is False


def test_supervisor_critical_escalation():
    """Supervisor should escalate to CRITICAL_STAT when safety worker triggers."""
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="CRITICAL-01",
        target_identifier="KEY-CRIT",
        primary_metric=10.0,
        secondary_metric=5.0,
        status_descriptor="NOMINAL",
        is_critical_flag=True,
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.CRITICAL_STAT
    assert dossier.integrity_status == SystemIntegrityStatus.RECALIBRATION_REQUIRED
    assert dossier.critical_alerts_count > 0


def test_llm_factory_providers():
    """LLM factory should handle all provider types without error."""
    from agents.llm_factory import LLMFactory
    for provider in ["mock", "deterministic", "test", "ollama", "local", "claude", "anthropic", "openai", "gpt4", "unknown"]:
        llm = LLMFactory.create(provider)
        result = llm.invoke("Test prompt")
        assert isinstance(result, str)
        assert len(result) > 0


def test_phi_guard_email_pattern():
    """PHI guard should catch email addresses."""
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Send report to doctor@hospital.org")


def test_phi_guard_dob_pattern():
    """PHI guard should catch date of birth patterns."""
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient DOB 01/15/1985")
