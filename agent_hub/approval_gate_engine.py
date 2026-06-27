from __future__ import annotations

from typing import Any

from agent_hub.approval_gate_schema import (
    ALLOWED_EXECUTION_MODES,
    APPROVAL_GATE_EXECUTION_POLICY,
    APPROVAL_STATUSES,
    normalize_approval_gate,
    validate_approval_gate,
)


def evaluate_approval_gate(gate: dict[str, Any]) -> dict[str, Any]:
    """Normalize and validate one approval gate without enabling execution."""
    normalized = normalize_approval_gate(gate)
    validation = validate_approval_gate(normalized)
    normalized["schema_valid"] = validation["is_valid"]
    normalized["schema_warnings"] = validation["warnings"]
    normalized["missing_schema_fields"] = validation["missing_fields"]
    return normalized


def build_approval_gate_registry(workflows: list[dict] | None = None) -> list[dict]:
    """Flatten workflow approval gates into a single display registry."""
    rows: list[dict] = []
    for workflow in workflows or []:
        workflow_id = workflow.get("workflow_id", "")
        workflow_name = workflow.get("workflow_name", "")
        for gate in workflow.get("approval_gates", []):
            evaluated = evaluate_approval_gate(gate)
            evaluated["workflow_id"] = workflow_id
            evaluated["workflow_name"] = workflow_name
            rows.append(evaluated)
    return sorted(rows, key=lambda row: (row.get("workflow_name", ""), row.get("gate_id", "")))


def build_approval_gate_summary(gates: list[dict]) -> dict[str, int]:
    """Summarize approval gates for workflow metrics."""
    return {
        "total_approval_gates": len(gates),
        "approval_required_gates": sum(1 for gate in gates if gate.get("approval_required") is True),
        "blocked_gates": sum(
            1
            for gate in gates
            if gate.get("approval_status") == "blocked"
            or gate.get("allowed_execution_mode") == "blocked"
        ),
        "ready_for_manual_review_gates": sum(
            1 for gate in gates if gate.get("approval_status") == "ready_for_manual_review"
        ),
        "demo_only_gates": sum(1 for gate in gates if gate.get("approval_status") == "approved_demo_only"),
        "dry_run_required_gates": sum(1 for gate in gates if gate.get("dry_run_required") is True),
    }


def find_approval_gate_policy_violations(gates: list[dict]) -> list[dict]:
    """Return gates that violate the HUB-V2-009 no-execution policy."""
    violations: list[dict] = []
    for gate in gates:
        if not gate.get("schema_valid"):
            violations.append(gate)
            continue
        if gate.get("execution_policy") != APPROVAL_GATE_EXECUTION_POLICY:
            violations.append(gate)
            continue
        if gate.get("approval_status") not in APPROVAL_STATUSES:
            violations.append(gate)
            continue
        if gate.get("allowed_execution_mode") not in ALLOWED_EXECUTION_MODES:
            violations.append(gate)
            continue
        if gate.get("risk_level") in {"high", "blocked"} and gate.get("approval_required") is not True:
            violations.append(gate)
            continue
        if gate.get("risk_level") == "blocked" and gate.get("allowed_execution_mode") != "blocked":
            violations.append(gate)
            continue
    return violations
