"""Regression tests for package-facing workflows, validation and audit safety."""
import csv
from pathlib import Path

import pytest
from pydantic import ValidationError

from agents.base import AuditTrail, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from blackboard_bus.csv_utils import parse_csv_bool


@pytest.mark.parametrize("raw,expected", [
    ("False", False), ("false", False), ("0", False), ("no", False),
    ("", False), ("TRUE", True), ("1", True), ("yes", True), (True, True),
])
def test_csv_boolean_conversion(raw, expected):
    assert parse_csv_bool(raw) is expected


def test_csv_boolean_invalid():
    with pytest.raises(ValueError, match="Invalid is_critical_flag"):
        parse_csv_bool("maybe")


@pytest.mark.parametrize("value", ["nan", "inf", "-inf", float("nan")])
def test_non_finite_metrics_rejected(value):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="T1", target_identifier="KEY-1", primary_metric=value)


def test_supervisor_rejects_sensitive_nested_attributes():
    payload = SystemTaskPayload(
        task_id="T1", target_identifier="KEY-1", primary_metric=4.0,
        attributes={"contact": {"email": "patient@example.org"}},
    )
    with pytest.raises(SecurityException):
        SystemSupervisor().process_task(payload)


def test_audit_records_are_returned_as_copies():
    trail = AuditTrail(secret_key="unit-test-key")
    trail.log("tester", "unit-test", "EVENT", {"status": "OK"})
    external = trail.get_trail()
    external[0]["current_hash"] = "tampered"
    external.clear()
    assert trail.verify_integrity()
    assert len(trail.get_trail()) == 1


def test_http_api_validation_and_metrics():
    from fastapi.testclient import TestClient
    from agents.api import app
    client = TestClient(app)
    valid = {
        "task_id": "API-T1", "target_identifier": "KEY-1", "primary_metric": 12,
        "secondary_metric": 4, "status_descriptor": "NOMINAL",
    }
    response = client.post("/api/audit", json=valid)
    assert response.status_code == 200
    assert response.json()["overall_urgency"] == "ROUTINE"
    assert client.post("/api/audit", json={**valid, "task_id": "patient@example.org"}).status_code == 422
    assert client.post("/api/audit", json={**valid, "attributes": {"contact": "patient@example.org"}}).status_code == 422
    prometheus = client.get("/metrics/prometheus")
    assert prometheus.status_code == 200
    assert "system_tasks_total" in prometheus.text


@pytest.mark.parametrize("main_module,urgency_column,routine_value", [
    ("cli", "overall_urgency", "ROUTINE"),
    ("blackboard_bus.cli", "overall_status", "NOMINAL_OPTIMAL"),
])
def test_csv_batch_false_is_not_critical(tmp_path, main_module, urgency_column, routine_value):
    from importlib import import_module
    main = import_module(main_module).main
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "result.csv"
    input_path.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "T1,KEY-1,10,4,False,NOMINAL\n", encoding="utf-8"
    )
    assert main(["batch", "-i", str(input_path), "-o", str(output_path)]) == 0
    with output_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0][urgency_column] == routine_value
