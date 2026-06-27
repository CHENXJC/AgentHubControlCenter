from agent_hub.action_schema import (
    ACTION_SCHEMA_FIELDS,
    ACTION_TYPES,
    EXECUTION_MODES,
    RISK_LEVELS,
    normalize_action,
    summarize_actions,
    validate_action_schema,
)


def test_action_schema_enums_match_hub_v2_005_contract():
    assert ACTION_TYPES == {
        "display_only",
        "manual_instruction",
        "command_template",
        "local_link",
        "report_view",
        "codex_prompt",
        "future_connector",
    }
    assert EXECUTION_MODES == {
        "not_executable",
        "manual_only",
        "template_only",
        "planned",
    }
    assert RISK_LEVELS == {"low", "medium", "high", "blocked"}


def test_normalize_action_adds_required_schema_fields():
    action = normalize_action(
        {"action_id": "view_project_status", "label": "View project status"},
        agent_id="demo_agent",
        agent_name="DemoAgent",
        project_path="F:\\AIProjects\\DemoAgent",
    )

    for field in ACTION_SCHEMA_FIELDS:
        assert field in action

    assert action["action_type"] == "report_view"
    assert action["execution_mode"] == "not_executable"
    assert action["risk_level"] == "low"
    assert action["requires_approval"] is False
    assert action["runbook_ref"] == "docs/MANUAL_RUNBOOK.md#demo-agent-view-project-status"
    assert validate_action_schema(action)["is_valid"] is True


def test_blocked_action_requires_approval_and_cannot_execute():
    action = normalize_action(
        {"action_id": "git_push", "label": "Git push"},
        agent_id="demo_agent",
        project_path="F:\\AIProjects\\DemoAgent",
    )

    assert action["risk_level"] == "blocked"
    assert action["requires_approval"] is True
    assert action["status"] == "blocked"
    assert "Blocked" in action["safety_note"]
    assert validate_action_schema(action)["is_valid"] is True


def test_summarize_actions_counts_manual_display_future_and_blocked():
    actions = [
        normalize_action({"action_id": "open_project_folder", "label": "Open folder"}),
        normalize_action({"action_id": "view_project_status", "label": "View status"}),
        normalize_action({"action_id": "send_to_agent_hub", "label": "Send metadata"}),
        normalize_action({"action_id": "delete_files", "label": "Delete files"}),
    ]

    summary = summarize_actions(actions)

    assert summary["total_actions"] == 4
    assert summary["manual_only_actions"] == 1
    assert summary["display_only_actions"] == 1
    assert summary["future_connector_actions"] == 1
    assert summary["requires_approval_actions"] == 2
    assert summary["blocked_actions"] == 1
