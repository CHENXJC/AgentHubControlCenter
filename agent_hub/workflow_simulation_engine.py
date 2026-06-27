from __future__ import annotations

from statistics import mean
from typing import Any

from agent_hub.approval_gate_engine import evaluate_approval_gate
from agent_hub.approval_gate_schema import ALLOWED_EXECUTION_MODES
from agent_hub.useful_signal_schema import clamp_score
from agent_hub.workflow_simulation_data import DEMO_WORKFLOW_SIMULATION_SEEDS
from agent_hub.workflow_simulation_schema import (
    WORKFLOW_EXECUTION_POLICY,
    WORKFLOW_STATUSES,
    normalize_workflow_simulation,
    validate_workflow_simulation,
)


def calculate_workflow_readiness_score(workflow: dict[str, Any]) -> int:
    """Calculate readiness for a local simulation workflow."""
    score = 20
    if workflow.get("source_agents"):
        score += 12
    if workflow.get("signals_used"):
        score += 12
    if workflow.get("recommended_actions"):
        score += 12
    if workflow.get("manual_steps"):
        score += 10
    if workflow.get("generated_outputs"):
        score += 10

    gates = workflow.get("approval_gates", [])
    if gates and all(gate.get("schema_valid") for gate in gates):
        score += 12

    blocked_gates = [
        gate
        for gate in gates
        if gate.get("approval_status") == "blocked"
        or gate.get("allowed_execution_mode") == "blocked"
    ]
    high_risk_gates = [
        gate
        for gate in gates
        if gate.get("risk_level") in {"high", "blocked"}
    ]
    score -= len(blocked_gates) * 8
    score -= len(high_risk_gates) * 5
    score -= len(workflow.get("blocked_steps", [])) * 5
    return clamp_score(score)


def determine_workflow_status(workflow: dict[str, Any]) -> str:
    """Determine display status without changing any execution mode."""
    gates = workflow.get("approval_gates", [])
    score = clamp_score(workflow.get("workflow_readiness_score"))
    if any(
        gate.get("approval_status") == "blocked"
        or gate.get("allowed_execution_mode") == "blocked"
        for gate in gates
    ):
        return "blocked_until_approval"
    if any(gate.get("approval_required") or gate.get("human_review_required") for gate in gates):
        return "ready_for_manual_review"
    if score >= 75:
        return "simulation_ready"
    return "needs_review"


def evaluate_workflow_simulation(workflow: dict[str, Any]) -> dict[str, Any]:
    """Normalize, gate-check, score, and validate one workflow simulation."""
    normalized = normalize_workflow_simulation(workflow)
    normalized["approval_gates"] = [
        evaluate_approval_gate(gate)
        for gate in normalized.get("approval_gates", [])
    ]
    normalized["workflow_readiness_score"] = calculate_workflow_readiness_score(normalized)
    normalized["workflow_status"] = determine_workflow_status(normalized)
    normalized["execution_policy"] = WORKFLOW_EXECUTION_POLICY
    validation = validate_workflow_simulation(normalized)
    normalized["schema_valid"] = validation["is_valid"]
    normalized["schema_warnings"] = validation["warnings"]
    normalized["missing_schema_fields"] = validation["missing_fields"]
    return normalized


def build_workflow_simulation_registry(
    extra_workflows: list[dict] | None = None,
) -> list[dict]:
    """Build the HUB-V2-009 local workflow simulation registry."""
    seeds = list(DEMO_WORKFLOW_SIMULATION_SEEDS)
    if extra_workflows:
        seeds.extend(extra_workflows)
    workflows = [evaluate_workflow_simulation(seed) for seed in seeds]
    return sorted(workflows, key=lambda item: item.get("workflow_name", ""))


def build_workflow_simulation_summary(workflows: list[dict]) -> dict[str, Any]:
    """Summarize workflow simulation records for My Workflows metrics."""
    if not workflows:
        return {
            "total_demo_workflows": 0,
            "ready_for_manual_review_workflows": 0,
            "blocked_steps": 0,
            "manual_only_steps": 0,
            "template_only_outputs": 0,
            "approval_gates_required": 0,
            "average_workflow_readiness_score": 0,
        }

    all_gates = [
        gate
        for workflow in workflows
        for gate in workflow.get("approval_gates", [])
    ]
    return {
        "total_demo_workflows": len(workflows),
        "ready_for_manual_review_workflows": sum(
            1
            for workflow in workflows
            if workflow.get("workflow_status") == "ready_for_manual_review"
        ),
        "blocked_steps": sum(len(workflow.get("blocked_steps", [])) for workflow in workflows),
        "manual_only_steps": sum(len(workflow.get("manual_steps", [])) for workflow in workflows),
        "template_only_outputs": sum(
            len(workflow.get("generated_outputs", []))
            for workflow in workflows
            if any(
                gate.get("allowed_execution_mode") == "template_only"
                for gate in workflow.get("approval_gates", [])
            )
        ),
        "approval_gates_required": sum(1 for gate in all_gates if gate.get("approval_required") is True),
        "average_workflow_readiness_score": round(
            mean(workflow["workflow_readiness_score"] for workflow in workflows),
            1,
        ),
    }


def filter_workflow_simulations(
    workflows: list[dict],
    *,
    workflow_type: str = "All",
    workflow_status: str = "All",
) -> list[dict]:
    """Filter workflow simulations for display only."""
    filtered = []
    for workflow in workflows:
        if workflow_type != "All" and workflow.get("workflow_type") != workflow_type:
            continue
        if workflow_status != "All" and workflow.get("workflow_status") != workflow_status:
            continue
        filtered.append(workflow)
    return filtered


def find_workflow_policy_violations(workflows: list[dict]) -> list[dict]:
    """Return workflow rows that violate the local simulation-only contract."""
    violations: list[dict] = []
    for workflow in workflows:
        if not workflow.get("schema_valid"):
            violations.append(workflow)
            continue
        if workflow.get("execution_policy") != WORKFLOW_EXECUTION_POLICY:
            violations.append(workflow)
            continue
        if workflow.get("workflow_status") not in WORKFLOW_STATUSES:
            violations.append(workflow)
            continue
        for gate in workflow.get("approval_gates", []):
            if not gate.get("schema_valid"):
                violations.append(workflow)
                break
            if gate.get("allowed_execution_mode") not in ALLOWED_EXECUTION_MODES:
                violations.append(workflow)
                break
    return violations


def workflow_simulation_to_useful_signals(workflows: list[dict]) -> list[dict]:
    """Convert selected workflow simulation outcomes into Useful Signal seeds."""
    by_id = {workflow.get("workflow_id"): workflow for workflow in workflows}
    seeds: list[dict] = []

    project_review = by_id.get("project_progress_review")
    if project_review:
        seeds.append(
            {
                "signal_id": "workflow_project_review_next_steps",
                "title": "Project review workflow can summarize next steps across 11 agents",
                "source_agent": "AgentHubControlCenter",
                "source_type": "workflow_simulation",
                "category": "workflow_automation",
                "summary": (
                    "Local project review workflow combines manifests, useful signals, "
                    "Action Center metadata, and report outputs without execution."
                ),
                "relevance_score": 92,
                "urgency_score": 72,
                "actionability_score": 86,
                "value_score": 90,
                "risk_score": 20,
                "recommended_action": project_review.get("next_recommended_step", ""),
                "target_agent": "AgentHubControlCenter",
                "status": "watchlist",
                "related_action_id": "export_summary",
            }
        )

    connector_review = by_id.get("connector_readiness_review")
    if connector_review:
        seeds.append(
            {
                "signal_id": "workflow_connector_gate_blocks",
                "title": "Connector approval gates should block Gmail Send and GitHub Push",
                "source_agent": "AgentHubControlCenter",
                "source_type": "workflow_simulation",
                "category": "risk_warning",
                "summary": (
                    "The connector readiness workflow keeps Gmail Send and GitHub Push / "
                    "Release blocked until a separate approved stage exists."
                ),
                "relevance_score": 94,
                "urgency_score": 90,
                "actionability_score": 82,
                "value_score": 88,
                "risk_score": 95,
                "recommended_action": connector_review.get("next_recommended_step", ""),
                "target_agent": "AgentHubControlCenter",
                "status": "needs_action",
                "related_action_id": "plan_approval_gates",
            }
        )

    codex_handoff = by_id.get("codex_handoff")
    if codex_handoff:
        seeds.append(
            {
                "signal_id": "workflow_codex_handoff_ready",
                "title": "Codex handoff workflow is ready for manual use",
                "source_agent": "AgentHubControlCenter",
                "source_type": "workflow_simulation",
                "category": "workflow_automation",
                "summary": (
                    "The Codex handoff workflow can produce copy-ready prompt text "
                    "without auto-sending or executing instructions."
                ),
                "relevance_score": 90,
                "urgency_score": 78,
                "actionability_score": 88,
                "value_score": 86,
                "risk_score": 25,
                "recommended_action": codex_handoff.get("next_recommended_step", ""),
                "target_agent": "AgentHubControlCenter",
                "status": "new",
                "related_action_id": "generate_codex_prompt",
            }
        )

    return seeds


def get_workflow_type_options() -> list[str]:
    return ["All", "codex_handoff", "connector_review", "project_review", "signal_review"]


def get_workflow_status_options() -> list[str]:
    return ["All"] + sorted(WORKFLOW_STATUSES)
