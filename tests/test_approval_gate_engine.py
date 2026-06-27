from agent_hub.approval_gate_engine import (
    build_approval_gate_registry,
    build_approval_gate_summary,
    evaluate_approval_gate,
    find_approval_gate_policy_violations,
)
from agent_hub.approval_gate_schema import (
    ALLOWED_EXECUTION_MODES,
    APPROVAL_GATE_EXECUTION_POLICY,
    APPROVAL_STATUSES,
)
from agent_hub.workflow_simulation_engine import build_workflow_simulation_registry


def test_approval_gate_enums_match_hub_v2_009_contract():
    assert APPROVAL_STATUSES == {
        "not_required",
        "required",
        "blocked",
        "ready_for_manual_review",
        "approved_demo_only",
        "rejected",
    }
    assert ALLOWED_EXECUTION_MODES == {
        "display_only",
        "manual_only",
        "template_only",
        "dry_run_only",
        "blocked",
    }


def test_evaluate_approval_gate_adds_no_execution_policy():
    gate = evaluate_approval_gate(
        {
            "gate_id": "demo_gate",
            "gate_name": "Demo Gate",
            "target_action_id": "view_project_status",
            "target_connector_id": "none",
            "risk_level": "low",
            "approval_required": False,
            "approval_status": "not_required",
            "required_checks": ["Review metadata"],
            "dry_run_required": False,
            "rollback_required": False,
            "human_review_required": False,
            "block_reason": "Display-only.",
            "allowed_execution_mode": "display_only",
        }
    )

    assert gate["schema_valid"] is True
    assert gate["execution_policy"] == APPROVAL_GATE_EXECUTION_POLICY


def test_build_approval_gate_registry_blocks_high_risk_mutations():
    workflows = build_workflow_simulation_registry()
    gates = build_approval_gate_registry(workflows)
    summary = build_approval_gate_summary(gates)

    assert gates
    assert summary["approval_required_gates"] >= 1
    assert summary["blocked_gates"] >= 2
    assert find_approval_gate_policy_violations(gates) == []

    blocked_targets = {gate["target_connector_id"] for gate in gates if gate["approval_status"] == "blocked"}
    assert "gmail_send" in blocked_targets
    assert "github_push_release" in blocked_targets


def test_approval_gate_policy_check_rejects_real_execution_mode():
    gate = evaluate_approval_gate(
        {
            "gate_name": "Unsafe Gate",
            "target_action_id": "send_email",
            "target_connector_id": "gmail_send",
            "risk_level": "blocked",
            "approval_required": True,
            "approval_status": "blocked",
            "required_checks": ["None"],
            "dry_run_required": True,
            "rollback_required": True,
            "human_review_required": True,
            "block_reason": "Unsafe.",
            "allowed_execution_mode": "live_execute",
        }
    )

    assert gate["schema_valid"] is False
