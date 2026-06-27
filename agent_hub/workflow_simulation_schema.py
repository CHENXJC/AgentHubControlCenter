from __future__ import annotations

from typing import Any

from agent_hub.useful_signal_schema import clamp_score


WORKFLOW_SIMULATION_SCHEMA_VERSION = "HUB-V2-009"
WORKFLOW_EXECUTION_POLICY = "local_simulation_only_no_live_connector_no_real_action_no_credentials"

WORKFLOW_SIMULATION_FIELDS = [
    "workflow_id",
    "workflow_name",
    "workflow_type",
    "input_source",
    "source_agents",
    "signals_used",
    "recommended_actions",
    "approval_gates",
    "blocked_steps",
    "manual_steps",
    "generated_outputs",
    "risk_summary",
    "next_recommended_step",
    "execution_policy",
]

WORKFLOW_TYPES = {
    "project_review",
    "signal_review",
    "connector_review",
    "codex_handoff",
}

WORKFLOW_STATUSES = {
    "simulation_ready",
    "ready_for_manual_review",
    "blocked_until_approval",
    "needs_review",
}


def _string_value(value: Any, default: str = "") -> str:
    return value.strip() if isinstance(value, str) and value.strip() else default


def _list_of_strings(value: Any, default: list[str] | None = None) -> list[str]:
    if isinstance(value, list):
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return list(default or [])


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _slug(value: str) -> str:
    output: list[str] = []
    previous_separator = False
    for char in value.strip().lower():
        if char.isalnum():
            output.append(char)
            previous_separator = False
        elif not previous_separator:
            output.append("_")
            previous_separator = True
    return "".join(output).strip("_") or "workflow"


def normalize_workflow_simulation(workflow: dict[str, Any]) -> dict[str, Any]:
    """Normalize one local workflow simulation record."""
    source = dict(workflow) if isinstance(workflow, dict) else {}
    workflow_name = _string_value(source.get("workflow_name"), "Local workflow simulation")
    workflow_id = _string_value(source.get("workflow_id"), _slug(workflow_name))
    workflow_type = _string_value(source.get("workflow_type"), "project_review")

    normalized = dict(source)
    normalized.update(
        {
            "workflow_id": workflow_id,
            "workflow_name": workflow_name,
            "workflow_type": workflow_type if workflow_type in WORKFLOW_TYPES else "project_review",
            "input_source": _string_value(source.get("input_source"), "local_demo_metadata"),
            "source_agents": _list_of_strings(source.get("source_agents"), ["AgentHubControlCenter"]),
            "signals_used": _list_of_strings(source.get("signals_used"), ["local_demo_signal"]),
            "recommended_actions": _list_of_strings(source.get("recommended_actions"), ["manual_review"]),
            "approval_gates": _list_of_dicts(source.get("approval_gates")),
            "blocked_steps": _list_of_strings(source.get("blocked_steps")),
            "manual_steps": _list_of_strings(source.get("manual_steps"), ["Review workflow manually"]),
            "generated_outputs": _list_of_strings(
                source.get("generated_outputs"),
                ["Manual summary"],
            ),
            "risk_summary": _string_value(source.get("risk_summary"), "Low risk local simulation."),
            "next_recommended_step": _string_value(
                source.get("next_recommended_step"),
                "Review this workflow manually before any future execution stage.",
            ),
            "execution_policy": WORKFLOW_EXECUTION_POLICY,
            "workflow_readiness_score": clamp_score(source.get("workflow_readiness_score"), 0),
            "workflow_status": _string_value(source.get("workflow_status"), "needs_review"),
            "simulation_flags": [
                "Local simulation only",
                "No live connector",
                "No real action execution",
                "No credentials loaded",
            ],
        }
    )
    return normalized


def validate_workflow_simulation(workflow: dict[str, Any]) -> dict[str, Any]:
    """Validate one workflow simulation without running workflow steps."""
    def is_missing(field: str) -> bool:
        if field not in workflow:
            return True
        value = workflow.get(field)
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        return False

    missing_fields = [
        field
        for field in WORKFLOW_SIMULATION_FIELDS
        if is_missing(field)
    ]
    warnings: list[str] = []

    if workflow.get("workflow_type") not in WORKFLOW_TYPES:
        warnings.append("workflow_type must use a HUB-V2-009 enum value.")
    if workflow.get("workflow_status") not in WORKFLOW_STATUSES:
        warnings.append("workflow_status must use a HUB-V2-009 workflow status.")
    if workflow.get("execution_policy") != WORKFLOW_EXECUTION_POLICY:
        warnings.append("workflow simulation must remain local simulation only.")
    if not isinstance(workflow.get("approval_gates"), list) or not workflow.get("approval_gates"):
        warnings.append("approval_gates must contain at least one gate.")
    for field in ["source_agents", "signals_used", "recommended_actions", "manual_steps", "generated_outputs"]:
        if not isinstance(workflow.get(field), list) or not workflow.get(field):
            warnings.append(f"{field} must be a non-empty list.")
    if not isinstance(workflow.get("workflow_readiness_score"), int) or not 0 <= workflow.get("workflow_readiness_score", -1) <= 100:
        warnings.append("workflow_readiness_score must be an integer from 0 to 100.")
    for gate in workflow.get("approval_gates", []):
        if isinstance(gate, dict) and gate.get("schema_valid") is False:
            warnings.append(f"approval gate {gate.get('gate_id', 'unknown')} is invalid.")

    return {
        "is_valid": not missing_fields and not warnings,
        "missing_fields": missing_fields,
        "warnings": warnings,
    }
