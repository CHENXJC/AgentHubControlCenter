from agent_hub.approval_gate_engine import build_approval_gate_registry
from agent_hub.workflow_simulation_engine import (
    build_workflow_simulation_registry,
    build_workflow_simulation_summary,
    filter_workflow_simulations,
    find_workflow_policy_violations,
    workflow_simulation_to_useful_signals,
)
from agent_hub.workflow_simulation_schema import WORKFLOW_EXECUTION_POLICY
from agent_hub.useful_signal_engine import build_useful_signal_registry


def test_build_workflow_simulation_registry_creates_four_demo_workflows():
    workflows = build_workflow_simulation_registry()

    assert len(workflows) >= 4
    assert all(workflow["schema_valid"] is True for workflow in workflows)
    assert all(workflow["execution_policy"] == WORKFLOW_EXECUTION_POLICY for workflow in workflows)
    assert all(workflow["approval_gates"] for workflow in workflows)
    assert find_workflow_policy_violations(workflows) == []


def test_connector_workflow_blocks_gmail_send_and_github_push():
    workflows = build_workflow_simulation_registry()
    connector_workflow = next(
        workflow for workflow in workflows if workflow["workflow_id"] == "connector_readiness_review"
    )

    assert connector_workflow["workflow_status"] == "blocked_until_approval"
    assert "Gmail Send" in connector_workflow["blocked_steps"]
    assert "GitHub Push / Release" in connector_workflow["blocked_steps"]

    blocked_connectors = {
        gate["target_connector_id"]
        for gate in connector_workflow["approval_gates"]
        if gate["allowed_execution_mode"] == "blocked"
    }
    assert blocked_connectors == {"gmail_send", "github_push_release"}


def test_workflow_summary_and_filters():
    workflows = build_workflow_simulation_registry()
    summary = build_workflow_simulation_summary(workflows)

    assert summary["total_demo_workflows"] >= 4
    assert summary["ready_for_manual_review_workflows"] >= 1
    assert summary["blocked_steps"] >= 2
    assert summary["manual_only_steps"] >= 4
    assert summary["template_only_outputs"] >= 1
    assert summary["approval_gates_required"] >= 1
    assert summary["average_workflow_readiness_score"] > 0

    filtered = filter_workflow_simulations(
        workflows,
        workflow_type="codex_handoff",
        workflow_status="simulation_ready",
    )
    assert len(filtered) == 1
    assert filtered[0]["workflow_id"] == "codex_handoff"


def test_workflow_approval_gate_registry_is_display_safe():
    workflows = build_workflow_simulation_registry()
    gates = build_approval_gate_registry(workflows)

    assert gates
    assert all(
        gate["allowed_execution_mode"]
        in {"display_only", "manual_only", "template_only", "dry_run_only", "blocked"}
        for gate in gates
    )
    assert not any(gate["allowed_execution_mode"] in {"live_execute", "auto_execute", "send", "push", "delete"} for gate in gates)


def test_workflow_simulation_can_generate_useful_signals():
    workflows = build_workflow_simulation_registry()
    signal_seeds = workflow_simulation_to_useful_signals(workflows)
    signals = build_useful_signal_registry(extra_signals=signal_seeds)

    assert len(signal_seeds) >= 3
    assert any(signal["source_type"] == "workflow_simulation" for signal in signals)
    assert any("Codex handoff workflow" in signal["title"] for signal in signals)
    assert all(signal["execution_policy"] == "display_only_text_recommendation_no_execution" for signal in signals)
