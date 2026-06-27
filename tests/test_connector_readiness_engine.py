from agent_hub.connector_readiness_engine import (
    build_connector_readiness_registry,
    build_connector_readiness_summary,
    calculate_readiness_score,
    connector_readiness_to_useful_signals,
    filter_connector_readiness,
    find_connector_policy_violations,
)
from agent_hub.connector_readiness_schema import (
    CONNECTOR_EXECUTION_POLICY,
    LIVE_CONNECTION_STATUS,
)
from agent_hub.useful_signal_engine import build_useful_signal_registry


def test_build_connector_readiness_registry_creates_demo_connectors():
    connectors = build_connector_readiness_registry()

    assert len(connectors) >= 14
    assert all(connector["schema_valid"] is True for connector in connectors)
    assert all(connector["live_connection_status"] == LIVE_CONNECTION_STATUS for connector in connectors)
    assert all(connector["execution_policy"] == CONNECTOR_EXECUTION_POLICY for connector in connectors)
    assert all(connector["rollback_plan"] for connector in connectors)
    assert all(connector["test_plan"] for connector in connectors)
    assert all(connector["safety_gates"] for connector in connectors)
    assert find_connector_policy_violations(connectors) == []


def test_high_risk_or_write_connectors_require_approval():
    connectors = build_connector_readiness_registry()
    risky = [
        connector
        for connector in connectors
        if connector["risk_level"] in {"high", "blocked"}
        or connector["data_access_level"] in {"write_limited", "write_sensitive"}
    ]

    assert risky
    assert all(connector["approval_required"] is True for connector in risky)


def test_readiness_score_is_bounded_and_read_only_can_be_demo_ready():
    connector = {
        "demo_mode_available": True,
        "read_only_mode_available": True,
        "write_access": False,
        "approval_required": False,
        "risk_level": "low",
        "data_access_level": "read_only_metadata",
        "rollback_plan": ["Disable"],
        "test_plan": ["Fixture"],
        "safety_gates": ["No token"],
    }

    score = calculate_readiness_score(connector)

    assert 0 <= score <= 100
    assert score >= 75


def test_connector_summary_and_filters():
    connectors = build_connector_readiness_registry()
    summary = build_connector_readiness_summary(connectors)

    assert summary["total_connectors"] >= 14
    assert summary["ready_for_demo_connectors"] >= 1
    assert summary["blocked_until_approved_connectors"] >= 1
    assert summary["high_risk_connectors"] >= 1
    assert summary["average_readiness_score"] > 0

    blocked = filter_connector_readiness(
        connectors,
        risk_level="blocked",
        readiness_status="blocked_until_approved",
    )

    assert blocked
    assert all(connector["risk_level"] == "blocked" for connector in blocked)
    assert all(connector["readiness_status"] == "blocked_until_approved" for connector in blocked)


def test_connector_readiness_can_generate_useful_signals():
    connectors = build_connector_readiness_registry()
    signal_seeds = connector_readiness_to_useful_signals(connectors)
    signals = build_useful_signal_registry(extra_signals=signal_seeds)

    assert len(signal_seeds) >= 3
    assert any(signal["source_type"] == "connector_readiness" for signal in signals)
    assert any("Gmail Send" in signal["title"] for signal in signals)
    assert all(signal["execution_policy"] == "display_only_text_recommendation_no_execution" for signal in signals)
