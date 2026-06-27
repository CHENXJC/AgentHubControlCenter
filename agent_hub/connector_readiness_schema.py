from __future__ import annotations

from typing import Any

from agent_hub.useful_signal_schema import clamp_score


CONNECTOR_READINESS_SCHEMA_VERSION = "HUB-V2-008"
CONNECTOR_EXECUTION_POLICY = "design_only_readiness_simulation_no_live_connection"
LIVE_CONNECTION_STATUS = "not_connected"

CONNECTOR_READINESS_FIELDS = [
    "connector_id",
    "connector_name",
    "provider",
    "purpose",
    "required_permissions",
    "data_access_level",
    "write_access",
    "risk_level",
    "approval_required",
    "demo_mode_available",
    "read_only_mode_available",
    "rollback_plan",
    "test_plan",
    "safety_gates",
    "readiness_score",
    "readiness_status",
    "recommended_next_step",
]

READINESS_STATUSES = {
    "design_only",
    "not_connected",
    "ready_for_demo",
    "needs_review",
    "blocked_until_approved",
    "future",
}

DATA_ACCESS_LEVELS = {
    "none",
    "local_demo",
    "read_only_metadata",
    "read_only_content",
    "write_limited",
    "write_sensitive",
}

RISK_LEVELS = {
    "low",
    "medium",
    "high",
    "blocked",
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


def normalize_connector_readiness(connector: dict[str, Any]) -> dict[str, Any]:
    """Normalize one connector readiness record without opening a connection."""
    source = dict(connector) if isinstance(connector, dict) else {}
    connector_name = _string_value(source.get("connector_name"), "Unnamed connector")
    connector_id = _string_value(
        source.get("connector_id"),
        connector_name.lower().replace("/", " ").replace("-", " ").replace(" ", "_"),
    )
    data_access_level = _string_value(source.get("data_access_level"), "none")
    risk_level = _string_value(source.get("risk_level"), "medium")
    readiness_status = _string_value(source.get("readiness_status"), "design_only")

    normalized = dict(source)
    normalized.update(
        {
            "connector_id": connector_id,
            "connector_name": connector_name,
            "provider": _string_value(source.get("provider"), connector_name.split()[0]),
            "purpose": _string_value(source.get("purpose"), "Design-only connector readiness review."),
            "required_permissions": _list_value(source.get("required_permissions"), ["none"]),
            "data_access_level": data_access_level if data_access_level in DATA_ACCESS_LEVELS else "none",
            "write_access": _bool_value(source.get("write_access"), False),
            "risk_level": risk_level if risk_level in RISK_LEVELS else "medium",
            "approval_required": _bool_value(source.get("approval_required"), False),
            "demo_mode_available": _bool_value(source.get("demo_mode_available"), True),
            "read_only_mode_available": _bool_value(source.get("read_only_mode_available"), False),
            "rollback_plan": _list_value(
                source.get("rollback_plan"),
                ["Disable the connector plan and keep it disconnected."],
            ),
            "test_plan": _list_value(
                source.get("test_plan"),
                ["Review readiness metadata without calling the provider API."],
            ),
            "safety_gates": _list_value(
                source.get("safety_gates"),
                ["No credentials loaded", "No live API call", "No automatic execution"],
            ),
            "readiness_score": clamp_score(source.get("readiness_score"), 0),
            "readiness_status": (
                readiness_status if readiness_status in READINESS_STATUSES else "design_only"
            ),
            "recommended_next_step": _string_value(
                source.get("recommended_next_step"),
                "Keep this connector in design-only review.",
            ),
            "live_connection_status": LIVE_CONNECTION_STATUS,
            "execution_policy": CONNECTOR_EXECUTION_POLICY,
        }
    )
    return normalized


def validate_connector_readiness(connector: dict[str, Any]) -> dict[str, Any]:
    """Validate connector readiness metadata without contacting a provider."""
    def is_missing(field: str) -> bool:
        if field not in connector:
            return True
        value = connector.get(field)
        if value is None:
            return True
        if isinstance(value, str) and not value.strip():
            return True
        return False

    missing_fields = [
        field
        for field in CONNECTOR_READINESS_FIELDS
        if is_missing(field)
    ]
    warnings: list[str] = []

    for field in ["required_permissions", "rollback_plan", "test_plan", "safety_gates"]:
        value = connector.get(field)
        if not isinstance(value, list) or not value:
            warnings.append(f"{field} must be a non-empty list.")

    if connector.get("data_access_level") not in DATA_ACCESS_LEVELS:
        warnings.append("data_access_level must use a HUB-V2-008 data access enum.")
    if connector.get("readiness_status") not in READINESS_STATUSES:
        warnings.append("readiness_status must use a HUB-V2-008 readiness status.")
    if connector.get("risk_level") not in RISK_LEVELS:
        warnings.append("risk_level must use the approved risk enum.")
    if not isinstance(connector.get("readiness_score"), int) or not 0 <= connector.get("readiness_score", -1) <= 100:
        warnings.append("readiness_score must be an integer from 0 to 100.")

    if connector.get("live_connection_status") != LIVE_CONNECTION_STATUS:
        warnings.append("connectors must remain not_connected in HUB-V2-008.")
    if connector.get("execution_policy") != CONNECTOR_EXECUTION_POLICY:
        warnings.append("connectors must remain design-only readiness simulations.")
    if connector.get("risk_level") in {"high", "blocked"} and connector.get("approval_required") is not True:
        warnings.append("high-risk or blocked connectors require approval_required=true.")
    if connector.get("data_access_level") in {"write_limited", "write_sensitive"} and connector.get("approval_required") is not True:
        warnings.append("write-capable connectors require approval_required=true.")

    return {
        "is_valid": not missing_fields and not warnings,
        "missing_fields": missing_fields,
        "warnings": warnings,
    }
