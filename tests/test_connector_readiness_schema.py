from agent_hub.connector_readiness_schema import (
    CONNECTOR_EXECUTION_POLICY,
    CONNECTOR_READINESS_FIELDS,
    DATA_ACCESS_LEVELS,
    LIVE_CONNECTION_STATUS,
    READINESS_STATUSES,
    RISK_LEVELS,
    normalize_connector_readiness,
    validate_connector_readiness,
)


def test_connector_readiness_enums_match_hub_v2_008_contract():
    assert READINESS_STATUSES == {
        "design_only",
        "not_connected",
        "ready_for_demo",
        "needs_review",
        "blocked_until_approved",
        "future",
    }
    assert DATA_ACCESS_LEVELS == {
        "none",
        "local_demo",
        "read_only_metadata",
        "read_only_content",
        "write_limited",
        "write_sensitive",
    }
    assert RISK_LEVELS == {"low", "medium", "high", "blocked"}


def test_normalize_connector_readiness_adds_required_safe_fields():
    connector = normalize_connector_readiness(
        {
            "connector_id": "demo_connector",
            "connector_name": "Demo Connector",
            "provider": "Demo",
            "purpose": "Review demo connector readiness.",
            "required_permissions": ["demo.read"],
            "data_access_level": "read_only_metadata",
            "write_access": False,
            "risk_level": "low",
            "approval_required": False,
            "demo_mode_available": True,
            "read_only_mode_available": True,
            "rollback_plan": ["Disable demo connector"],
            "test_plan": ["Use fixture only"],
            "safety_gates": ["No token loaded"],
            "readiness_score": 80,
            "readiness_status": "ready_for_demo",
            "recommended_next_step": "Keep it as a fixture demo.",
        }
    )

    for field in CONNECTOR_READINESS_FIELDS:
        assert field in connector

    assert connector["live_connection_status"] == LIVE_CONNECTION_STATUS
    assert connector["execution_policy"] == CONNECTOR_EXECUTION_POLICY
    assert validate_connector_readiness(connector)["is_valid"] is True


def test_validate_connector_readiness_rejects_live_or_unsafe_records():
    connector = normalize_connector_readiness({"connector_name": "Unsafe Connector"})
    connector["risk_level"] = "high"
    connector["approval_required"] = False
    connector["live_connection_status"] = "connected"
    connector["execution_policy"] = "execute_live_connector"

    validation = validate_connector_readiness(connector)

    assert validation["is_valid"] is False
    assert any("not_connected" in warning for warning in validation["warnings"])
    assert any("design-only" in warning for warning in validation["warnings"])
    assert any("approval_required" in warning for warning in validation["warnings"])
