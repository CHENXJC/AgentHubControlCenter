from __future__ import annotations

from statistics import mean
from typing import Any

from agent_hub.connector_readiness_data import DEMO_CONNECTOR_READINESS_SEEDS
from agent_hub.connector_readiness_schema import (
    CONNECTOR_EXECUTION_POLICY,
    DATA_ACCESS_LEVELS,
    LIVE_CONNECTION_STATUS,
    READINESS_STATUSES,
    RISK_LEVELS,
    normalize_connector_readiness,
    validate_connector_readiness,
)
from agent_hub.useful_signal_schema import clamp_score


RISK_PENALTY = {
    "low": 0,
    "medium": 8,
    "high": 22,
    "blocked": 45,
}

DATA_ACCESS_PENALTY = {
    "none": 0,
    "local_demo": 0,
    "read_only_metadata": 2,
    "read_only_content": 6,
    "write_limited": 10,
    "write_sensitive": 18,
}


def calculate_readiness_score(connector: dict[str, Any]) -> int:
    """Calculate a design-only readiness score from visible metadata."""
    score = 20
    if connector.get("demo_mode_available"):
        score += 15
    if connector.get("read_only_mode_available"):
        score += 15
    if not connector.get("write_access"):
        score += 8
    if connector.get("approval_required") and connector.get("risk_level") in {"medium", "high", "blocked"}:
        score += 5

    for field in ["rollback_plan", "test_plan", "safety_gates"]:
        if connector.get(field):
            score += 12

    score -= RISK_PENALTY.get(connector.get("risk_level"), 8)
    score -= DATA_ACCESS_PENALTY.get(connector.get("data_access_level"), 0)
    if connector.get("write_access"):
        score -= 8

    return clamp_score(score)


def determine_readiness_status(connector: dict[str, Any]) -> str:
    """Return a readiness status without ever marking the connector connected."""
    declared_status = connector.get("readiness_status", "design_only")
    risk_level = connector.get("risk_level", "medium")
    data_access_level = connector.get("data_access_level", "none")
    score = clamp_score(connector.get("readiness_score"))

    if risk_level == "blocked":
        return "blocked_until_approved"
    if data_access_level == "write_sensitive" and connector.get("approval_required"):
        return "blocked_until_approved"
    if declared_status in {"design_only", "future", "blocked_until_approved", "needs_review"}:
        return declared_status
    if score >= 75 and connector.get("demo_mode_available") and connector.get("read_only_mode_available"):
        return "ready_for_demo"
    if score >= 55:
        return "needs_review"
    return "design_only"


def build_readiness_reason(connector: dict[str, Any]) -> str:
    """Explain the readiness score in plain language."""
    return (
        "Readiness score starts from demo/read-only availability, rollback plan, "
        "test plan, and safety gates, then subtracts visible risk, write-access, "
        "and data-access penalties. The connector remains not_connected."
    )


def evaluate_connector_readiness(connector: dict[str, Any]) -> dict[str, Any]:
    """Normalize, score, status, and validate one connector readiness record."""
    normalized = normalize_connector_readiness(connector)
    normalized["readiness_score"] = calculate_readiness_score(normalized)
    normalized["readiness_status"] = determine_readiness_status(normalized)
    normalized["readiness_reason"] = build_readiness_reason(normalized)
    normalized["live_connection_status"] = LIVE_CONNECTION_STATUS
    normalized["execution_policy"] = CONNECTOR_EXECUTION_POLICY
    validation = validate_connector_readiness(normalized)
    normalized["schema_valid"] = validation["is_valid"]
    normalized["schema_warnings"] = validation["warnings"]
    normalized["missing_schema_fields"] = validation["missing_fields"]
    return normalized


def build_connector_readiness_registry(
    extra_connectors: list[dict] | None = None,
) -> list[dict]:
    """Build the HUB-V2-008 connector readiness registry from demo metadata."""
    seeds = list(DEMO_CONNECTOR_READINESS_SEEDS)
    if extra_connectors:
        seeds.extend(extra_connectors)
    connectors = [evaluate_connector_readiness(seed) for seed in seeds]
    return sorted(
        connectors,
        key=lambda item: (
            item.get("provider", "").lower(),
            item.get("connector_name", "").lower(),
        ),
    )


def build_connector_readiness_summary(connectors: list[dict]) -> dict[str, Any]:
    """Summarize connector readiness records for metric cards."""
    if not connectors:
        return {
            "total_connectors": 0,
            "design_only_connectors": 0,
            "ready_for_demo_connectors": 0,
            "needs_review_connectors": 0,
            "blocked_until_approved_connectors": 0,
            "high_risk_connectors": 0,
            "average_readiness_score": 0,
        }

    return {
        "total_connectors": len(connectors),
        "design_only_connectors": sum(
            1 for connector in connectors if connector.get("readiness_status") == "design_only"
        ),
        "ready_for_demo_connectors": sum(
            1 for connector in connectors if connector.get("readiness_status") == "ready_for_demo"
        ),
        "needs_review_connectors": sum(
            1 for connector in connectors if connector.get("readiness_status") == "needs_review"
        ),
        "blocked_until_approved_connectors": sum(
            1 for connector in connectors if connector.get("readiness_status") == "blocked_until_approved"
        ),
        "high_risk_connectors": sum(
            1 for connector in connectors if connector.get("risk_level") in {"high", "blocked"}
        ),
        "average_readiness_score": round(mean(connector["readiness_score"] for connector in connectors), 1),
    }


def filter_connector_readiness(
    connectors: list[dict],
    *,
    risk_level: str = "All",
    readiness_status: str = "All",
    provider: str = "All",
) -> list[dict]:
    """Filter connector readiness rows without changing the registry."""
    filtered = []
    for connector in connectors:
        if risk_level != "All" and connector.get("risk_level") != risk_level:
            continue
        if readiness_status != "All" and connector.get("readiness_status") != readiness_status:
            continue
        if provider != "All" and connector.get("provider") != provider:
            continue
        filtered.append(connector)
    return filtered


def find_connector_policy_violations(connectors: list[dict]) -> list[dict]:
    """Return connector readiness rows that violate the design-only contract."""
    violations = []
    for connector in connectors:
        if not connector.get("schema_valid"):
            violations.append(connector)
            continue
        if connector.get("live_connection_status") != LIVE_CONNECTION_STATUS:
            violations.append(connector)
            continue
        if connector.get("execution_policy") != CONNECTOR_EXECUTION_POLICY:
            violations.append(connector)
            continue
        if connector.get("risk_level") in {"high", "blocked"} and connector.get("approval_required") is not True:
            violations.append(connector)
            continue
        if connector.get("data_access_level") in {"write_limited", "write_sensitive"} and connector.get("approval_required") is not True:
            violations.append(connector)
    return violations


def connector_readiness_to_useful_signals(connectors: list[dict]) -> list[dict]:
    """Convert selected connector readiness results into Useful Signal seeds."""
    by_id = {connector.get("connector_id"): connector for connector in connectors}
    selected_ids = ["gmail_send", "google_sheets_read", "telegram_alert"]
    signals = []
    for connector_id in selected_ids:
        connector = by_id.get(connector_id)
        if not connector:
            continue
        risk_score = {
            "low": 25,
            "medium": 55,
            "high": 82,
            "blocked": 95,
        }.get(connector.get("risk_level"), 55)
        category = "risk_warning" if connector.get("risk_level") in {"high", "blocked"} else "connector_readiness"
        status = "needs_action" if connector.get("readiness_status") == "blocked_until_approved" else "watchlist"
        signals.append(
            {
                "signal_id": f"connector_{connector['connector_id']}_readiness",
                "title": f"{connector['connector_name']} readiness needs review",
                "source_agent": "AgentHubControlCenter",
                "source_type": "connector_readiness",
                "category": category,
                "summary": (
                    f"{connector['connector_name']} is {connector['readiness_status']} "
                    f"with live status {connector['live_connection_status']}."
                ),
                "relevance_score": 88,
                "urgency_score": 86 if status == "needs_action" else 58,
                "actionability_score": 80,
                "value_score": 84,
                "risk_score": risk_score,
                "recommended_action": connector.get("recommended_next_step", "Review connector readiness manually."),
                "target_agent": "AgentHubControlCenter",
                "status": status,
                "related_action_id": "send_to_agent_hub",
            }
        )
    return signals


def get_connector_risk_options() -> list[str]:
    return ["All"] + sorted(RISK_LEVELS)


def get_connector_status_options() -> list[str]:
    return ["All"] + sorted(READINESS_STATUSES)


def get_connector_data_access_options() -> list[str]:
    return ["All"] + sorted(DATA_ACCESS_LEVELS)
