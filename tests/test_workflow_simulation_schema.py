from agent_hub.workflow_simulation_schema import (
    WORKFLOW_EXECUTION_POLICY,
    WORKFLOW_SIMULATION_FIELDS,
    WORKFLOW_STATUSES,
    WORKFLOW_TYPES,
    normalize_workflow_simulation,
    validate_workflow_simulation,
)


def test_workflow_simulation_enums_match_hub_v2_009_contract():
    assert WORKFLOW_TYPES == {
        "project_review",
        "signal_review",
        "connector_review",
        "codex_handoff",
    }
    assert WORKFLOW_STATUSES == {
        "simulation_ready",
        "ready_for_manual_review",
        "blocked_until_approval",
        "needs_review",
    }


def test_normalize_workflow_simulation_adds_required_safe_fields():
    workflow = normalize_workflow_simulation(
        {
            "workflow_id": "demo_workflow",
            "workflow_name": "Demo Workflow",
            "workflow_type": "project_review",
            "input_source": "local_demo_metadata",
            "source_agents": ["AgentHubControlCenter"],
            "signals_used": ["Demo signal"],
            "recommended_actions": ["view_project_status"],
            "approval_gates": [
                {
                    "gate_name": "Demo Gate",
                }
            ],
            "blocked_steps": [],
            "manual_steps": ["Review manually"],
            "generated_outputs": ["Summary"],
            "risk_summary": "Low risk.",
            "next_recommended_step": "Keep it local.",
        }
    )

    for field in WORKFLOW_SIMULATION_FIELDS:
        assert field in workflow

    assert workflow["execution_policy"] == WORKFLOW_EXECUTION_POLICY
    assert "No live connector" in workflow["simulation_flags"]


def test_validate_workflow_simulation_rejects_non_simulation_policy():
    workflow = normalize_workflow_simulation({"workflow_name": "Unsafe Workflow"})
    workflow["approval_gates"] = []
    workflow["execution_policy"] = "auto_execute"
    workflow["workflow_status"] = "needs_review"

    validation = validate_workflow_simulation(workflow)

    assert validation["is_valid"] is False
    assert any("local simulation" in warning for warning in validation["warnings"])
    assert any("approval_gates" in warning for warning in validation["warnings"])
