/**
 * Dependency-free browser demonstration of the three deterministic Python workers.
 * No network requests, signing keys, audit log persistence, or LLM calls.
 */
export function evaluateTask(input) {
  const taskId = String(input.task_id ?? "").trim();
  const targetId = String(input.target_identifier ?? "").trim();
  const descriptor = String(input.status_descriptor ?? "NOMINAL").trim();
  const primary = Number(input.primary_metric);
  const secondary = Number(input.secondary_metric ?? 0);
  const critical = input.is_critical_flag === true;

  if (!taskId || !targetId || !descriptor) {
    throw new Error("Task ID, target identifier, and status descriptor are required.");
  }
  if (![primary, secondary].every(Number.isFinite)) {
    throw new Error("Both metrics must be finite numbers.");
  }

  const alerts = [];
  function addAlert(origin_worker, urgency, summary, technical_details, actionable_remediation) {
    alerts.push({ origin_worker, urgency, summary, technical_details, actionable_remediation });
  }
  if (primary > 25) {
    addAlert(
      "InvariantQCWorker", "ELEVATED_RISK", "Primary Metric Threshold Exceeded",
      `Primary measurement (${primary.toFixed(2)}) exceeds upper reference limit (25.00).`,
      "Initiate recalibration workflow and review secondary parameters."
    );
  }
  if (critical || secondary > 12) {
    addAlert(
      "SafetyEscalationWorker", critical ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
      "Critical Safety Interlock Triggered",
      `CriticalFlag=${critical} with secondary index ${secondary.toFixed(2)}.`,
      "Execute immediate closed-loop escalation and notify attending supervisor."
    );
  }
  if (["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"]
      .some(word => descriptor.toUpperCase().includes(word))) {
    addAlert(
      "ProtocolConformanceWorker", "ELEVATED_RISK",
      "Protocol Conformance Discordance Detected",
      `Descriptor '${descriptor}' indicates discordance.`,
      "Re-evaluate input or rerun secondary confirmation."
    );
  }

  const criticalCount = alerts.filter(item => item.urgency === "CRITICAL_STAT_PANIC").length;
  const overallUrgency = criticalCount
    ? "CRITICAL_STAT_PANIC"
    : alerts.length ? "ELEVATED_RISK" : "ROUTINE";
  const integrityStatus = criticalCount
    ? "RECALIBRATION_REQUIRED"
    : alerts.length ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL";

  return {
    mode: "Local browser demonstration (not server-verified)",
    task_id: taskId,
    target_identifier: targetId,
    overall_urgency: overallUrgency,
    integrity_status: integrityStatus,
    total_alerts: alerts.length,
    critical_alerts_count: criticalCount,
    alerts,
    consensus_summary: `Three deterministic rules evaluated. Status: ${overallUrgency}.`,
    limitations: "No server, HMAC audit trail, user authentication, or external LLM."
  };
}
