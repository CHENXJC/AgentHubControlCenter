from __future__ import annotations

from typing import Any


APPROVAL_GATE_SCHEMA_VERSION = "HUB-V2-009"
APPROVAL_GATE_EXECUTION_POLICY = "approval_gate_metadata_only_no_execution"

APPROVAL_GATE_FIELDS = [
    "gate_id",
    "gate_name",
    "target_action_id",
    "target_connector_id",
    "risk_level",
    "approval_required",
    "approval_status",
    "required_checks",
    "dry_run_required",
    "rollback_required",
    "human_review_required",
    "block_reason",
    "allowed_execution_mode",
]

APPROVAL_STATUSES = {
    "not_required",
    "required",
    "blocked",
    "ready_for_manual_review",
    "approved_demo_only",
    "rejected",
}

ALLOWED_EXECUTION_MODES = {
    "display_only",
    "manual_only",
    "template_only",
    "dry_run_only",
    "blocked",
}

RISK_LEVELS = {
    "low",
    "medium",
    "high",
    "blocked",
}

UNSAFE_EXECUTION_MODES = {
    "live_execute",
    "auto_execute",
    "execute",
    "send",
    "push",
    "delete",
}


def _string_value(value: Any, default: str = "") -> str:
    return value.strip() if isinstance(value, str) and value.strip() else default


def _bool_value(value: Any, default: bool = False) -> bool:
    return value if isinstance(value, bool) else default


def _list_value(value: Any, default: list[str] | None = None) -> list[str]:
    if isinstance(value, list):
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return list(default or [])


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
    return "".join(output).strip("_") or "approval_gate"


def normalize_approval_gate(gate: dict[str, Any]) -> dict[str, Any]:
    """Normalize one approval gate as metadata only."""
    source = dict(gate) if isinstance(gate, dict) else {}
    gate_name = _string_value(source.get("gate_name"), "Approval gate")
    gate_id = _string_value(source.get("gate_id"), _slug(gate_name))
    risk_level = _string_value(source.get("risk_level"), "low")
    approval_status = _string_value(source.get("approval_status"), "not_required")
    allowed_execution_mode = _string_value(source.get("allowed_execution_mode"), "display_only")

    normalized = dict(source)
    normalized.update(
        {
            "gate_id": gate_id,
            "gate_name": gate_name,
            "target_action_id": _string_value(source.get("target_action_id"), "none"),
            "target_connector_id": _string_value(source.get("target_connector_id"), "none"),
            "risk_level": risk_level if risk_level in RISK_LEVELS else "low",
            "approval_required": _bool_value(
                source.get("approval_required"),
                risk_level in {"high", "blocked"},
            ),
            "approval_status": (
                approval_status if approval_status in APPROVAL_STATUSES else "not_required"
            ),
            "required_checks": _list_value(
                source.get("required_checks"),
                ["Review gate metadata", "Confirm no live execution"],
            ),
            "dry_run_required": _bool_value(source.get("dry_run_required"), False),
            "rollback_required": _bool_value(source.get("rollback_required"), False),
            "human_review_required": _bool_value(
                source.get("human_review_required"),
                risk_level in {"medium", "high", "blocked"},
            ),
            "block_reason": _string_value(
                source.get("block_reason"),
                "No block reason. Gate is display-only metadata.",
            ),
            "allowed_execution_mode": (
                allowed_execution_mode
                if allowed_execution_mode in ALLOWED_EXECUTION_MODES
                else "display_only"
            ),
            "execution_policy": APPROVAL_GATE_EXECUTION_POLICY,
        }
    )
    return normalized


def validate_approval_gate(gate: dict[str, Any]) -> dict[str, Any]:
    """Validate one approval gate without approving real execution."""
    def is_missing(field: str) -> bool:
        if field not in gate:
            return True
        value = gate.get(field)
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        return False

    missing_fields = [
        field
        for field in APPROVAL_GATE_FIELDS
        if is_missing(field)
    ]
    warnings: list[str] = []

    if gate.get("risk_level") not in RISK_LEVELS:
        warnings.append("risk_level must use the approved risk enum.")
    if gate.get("approval_status") not in APPROVAL_STATUSES:
        warnings.append("approval_status must use the HUB-V2-009 enum.")
    if gate.get("allowed_execution_mode") not in ALLOWED_EXECUTION_MODES:
        warnings.append("allowed_execution_mode must be display/manual/template/dry-run/blocked only.")
    if gate.get("allowed_execution_mode") in UNSAFE_EXECUTION_MODES:
        warnings.append("real execution modes are forbidden in approval gates.")
    if gate.get("execution_policy") != APPROVAL_GATE_EXECUTION_POLICY:
        warnings.append("approval gates must remain metadata-only and no-execution.")
    if not isinstance(gate.get("required_checks"), list) or not gate.get("required_checks"):
        warnings.append("required_checks must be a non-empty list.")
    if gate.get("risk_level") in {"high", "blocked"} and gate.get("approval_required") is not True:
        warnings.append("high-risk or blocked gates require approval_required=true.")
    if gate.get("risk_level") in {"high", "blocked"} and gate.get("human_review_required") is not True:
        warnings.append("high-risk or blocked gates require human_review_required=true.")
    if gate.get("risk_level") == "blocked" and gate.get("allowed_execution_mode") != "blocked":
        warnings.append("blocked gates must use allowed_execution_mode=blocked.")
    if gate.get("approval_status") == "blocked" and gate.get("allowed_execution_mode") != "blocked":
        warnings.append("blocked approval status must use allowed_execution_mode=blocked.")

    return {
        "is_valid": not missing_fields and not warnings,
        "missing_fields": missing_fields,
        "warnings": warnings,
    }
