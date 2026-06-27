from agent_hub.action_registry import (
    build_action_registry,
    build_action_registry_summary,
    find_action_policy_violations,
    get_actions_for_agent,
    get_codex_prompt_actions,
    group_actions_by_agent,
)


def _manifest():
    return {
        "agent_id": "demo_agent",
        "agent_name": "DemoAgent",
        "category": "Workflow Automation",
        "category_label": "Workflow Automation",
        "project_path": "F:\\AIProjects\\DemoAgent",
        "actions": [
            {
                "action_id": "view_project_status",
                "label": "View project status",
            },
            {
                "action_id": "manual_run_dashboard",
                "label": "Manual run dashboard",
            },
            {
                "action_id": "generate_codex_prompt",
                "label": "Generate Codex prompt",
            },
        ],
    }


def test_build_action_registry_normalizes_rows():
    rows = build_action_registry([_manifest()])

    assert len(rows) == 3
    assert rows[0]["agent_name"] == "DemoAgent"
    assert rows[0]["schema_valid"] is True
    assert rows[0]["execution_mode"] in {
        "not_executable",
        "manual_only",
        "template_only",
        "planned",
    }
    assert rows[0]["command_template"]
    assert rows[0]["runbook_ref"].startswith("docs/MANUAL_RUNBOOK.md#demo-agent-")


def test_action_registry_summary_and_grouping():
    rows = build_action_registry([_manifest()])
    summary = build_action_registry_summary(rows)
    grouped = group_actions_by_agent(rows)

    assert summary["total_actions"] == 3
    assert summary["manual_only_actions"] == 1
    assert summary["display_only_actions"] == 1
    assert summary["future_connector_actions"] == 0
    assert grouped[0]["agent_name"] == "DemoAgent"
    assert len(grouped[0]["actions"]) == 3


def test_find_action_policy_violations_rejects_real_execution_mode():
    rows = build_action_registry([_manifest()])
    rows[0]["execution_mode"] = "auto_execute"

    violations = find_action_policy_violations(rows)

    assert violations[0]["agent_name"] == "DemoAgent"


def test_get_actions_for_agent_and_codex_prompt_actions():
    rows = build_action_registry([_manifest()])

    agent_rows = get_actions_for_agent(rows, agent_id="demo_agent")
    codex_rows = get_codex_prompt_actions(agent_rows)

    assert len(agent_rows) == 3
    assert len(codex_rows) == 1
    assert codex_rows[0]["action_id"] == "generate_codex_prompt"
    assert codex_rows[0]["execution_mode"] == "template_only"
