from agent_hub.useful_signal_schema import (
    DISPLAY_ONLY_EXECUTION_POLICY,
    SIGNAL_CATEGORIES,
    SIGNAL_STATUSES,
    SOURCE_TYPES,
    USEFUL_SIGNAL_FIELDS,
    clamp_score,
    normalize_signal,
    validate_signal_schema,
)


def test_useful_signal_enums_match_hub_v2_007_contract():
    assert SIGNAL_CATEGORIES == {
        "project_progress",
        "action_required",
        "business_opportunity",
        "learning_value",
        "portfolio_improvement",
        "connector_readiness",
        "workflow_automation",
        "risk_warning",
    }
    assert SIGNAL_STATUSES == {
        "new",
        "reviewed",
        "needs_action",
        "watchlist",
        "ignored",
        "archived",
    }
    assert "agent_manifest" in SOURCE_TYPES
    assert "local_csv" in SOURCE_TYPES
    assert "connector_readiness" in SOURCE_TYPES
    assert "workflow_simulation" in SOURCE_TYPES


def test_clamp_score_handles_invalid_values():
    assert clamp_score(120) == 100
    assert clamp_score(-5) == 0
    assert clamp_score("87") == 87
    assert clamp_score("not-a-score", default=42) == 42


def test_normalize_signal_adds_required_display_only_fields():
    signal = normalize_signal(
        {
            "title": "Demo signal",
            "source_agent": "DemoAgent",
            "source_type": "agent_manifest",
            "category": "project_progress",
            "summary": "A useful local signal.",
            "recommended_action": "Review manually.",
            "target_agent": "DemoAgent",
            "status": "new",
            "why_important": "It informs planning.",
            "suggested_next_step": "Keep visible.",
            "score_explanation": "Visible score formula.",
        }
    )

    for field in USEFUL_SIGNAL_FIELDS:
        assert field in signal

    assert signal["signal_id"] == "demo_signal"
    assert signal["execution_policy"] == DISPLAY_ONLY_EXECUTION_POLICY
    assert validate_signal_schema(signal)["is_valid"] is True


def test_validate_signal_schema_rejects_bad_enums_and_execution_policy():
    signal = normalize_signal({"title": "Bad signal"})
    signal["category"] = "bad_category"
    signal["status"] = "bad_status"
    signal["execution_policy"] = "auto_execute"

    validation = validate_signal_schema(signal)

    assert validation["is_valid"] is False
    assert any("category" in warning for warning in validation["warnings"])
    assert any("status" in warning for warning in validation["warnings"])
    assert any("display-only" in warning for warning in validation["warnings"])
