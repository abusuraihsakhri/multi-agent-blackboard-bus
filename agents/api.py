"""
FastAPI REST API Server for Multi Agent Blackboard Bus.
"""
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor
from .metrics import GLOBAL_METRICS

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Multi Agent Blackboard Bus API",
    description="Enterprise Distributed Component Platform (Long-Horizon Agent Context & State Architecture)",
    version="2.0.1",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "distributed component-blackboard-bus", "domain": "Long-Horizon Agent Context & State Architecture", "standard": "Autonomous Agent State Machine & Token Economy RFC", "version": "2.0.1"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "phi_blocks_total": GLOBAL_METRICS.phi_blocks_total,
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
    except SecurityException as exc:
        raise HTTPException(status_code=422, detail="Input contains a prohibited identifier") from exc
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except SecurityException as exc:
        raise HTTPException(status_code=422, detail="Input contains a prohibited identifier") from exc


@app.get("/metrics/prometheus", response_class=PlainTextResponse)
def prometheus_metrics():
    return GLOBAL_METRICS.export_prometheus_text()


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
