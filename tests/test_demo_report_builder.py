import json

from agent_hub.action_registry import build_action_registry, build_action_registry_summary
from agent_hub.agent_interface import build_agent_manifest
from agent_hub.approval_gate_engine import build_approval_gate_registry, build_approval_gate_summary
from agent_hub.connector_readiness_engine import build_connector_readiness_registry, build_connector_readiness_summary
from agent_hub.demo_report_builder import (
    build_csv_summary,
    build_demo_report_package,
    build_json_report,
    build_markdown_report,
    build_report_previews,
)
from agent_hub.report_export_schema import find_report_export_policy_violations
from agent_hub.useful_signal_engine import build_signal_summary, build_useful_signal_registry
from agent_hub.workflow_simulation_engine import build_workflow_simulation_registry, build_workflow_simulation_summary


def _demo_report_package():
    manifest = build_agent_manifest(
        {
            "agent_id": "demo_agent",
            "agent_name": "DemoAgent",
            "category": "Workflow Automation",
            "local_path": "F:\\AIProjects\\DemoAgent",
            "status": "Active",
            "primary_capability": "Demo workflow automation capability",
            "next_action": "Review next report export.",
        }
    )
    action_rows = build_action_registry([manifest])
    connectors = build_connector_readiness_registry()
    workflows = build_workflow_simulation_registry()
    gates = build_approval_gate_registry(workflows)
    signals = build_useful_signal_registry(manifests=[manifest], action_rows=action_rows)
    return build_demo_report_package(
        agent_manifests=[manifest],
        registry_summary={"total_agents": 1, "completed_agents": 0, "public_showcase_agents": 0},
        onboarding_summary={"valid_manifests": 1, "invalid_manifests": 0, "missing_manifests": 0},
        action_rows=action_rows,
        action_summary=build_action_registry_summary(action_rows),
        useful_signals=signals,
        useful_signal_summary=build_signal_summary(signals),
        connector_readiness=connectors,
        connector_readiness_summary=build_connector_readiness_summary(connectors),
        workflow_simulations=workflows,
        workflow_simulation_summary=build_workflow_simulation_summary(workflows),
        approval_gates=gates,
        approval_gate_summary=build_approval_gate_summary(gates),
        generated_at="2026-06-28T00:00:00+00:00",
    )


def test_build_demo_report_package_is_public_safe_and_policy_valid():
    package = _demo_report_package()

    assert package["schema_version"] == "HUB-V2-010"
    assert package["public_safe"] is True
    assert package["export_policy"] == "public_safe_demo_report_metadata_only_no_execution"
    assert package["validation_snapshot"]["report_export_policy_violations"] == 0
    assert find_report_export_policy_violations(package) == []
    assert "No credentials loaded" in package["safety_notes"]
    assert "No real action executed" in package["safety_notes"]


def test_markdown_report_contains_required_sections_and_disclaimer():
    markdown = build_markdown_report(_demo_report_package())

    assert "# AgentHubControlCenter V2 Demo Workflow Report" in markdown
    assert "## 1. Executive Summary" in markdown
    assert "## 4. Useful Signals" in markdown
    assert "## 7. Approval Gates" in markdown
    assert "Blocked / Manual / Template-only Actions" in markdown
    assert "No live connector connected" in markdown
    assert "No external API called" in markdown


def test_json_and_csv_reports_are_structured_copy_ready():
    package = _demo_report_package()
    parsed = json.loads(build_json_report(package))
    csv_summary = build_csv_summary(package)

    assert parsed["report_id"] == package["report_id"]
    assert parsed["sections"]["executive_summary"]["tracked_agents"] == 1
    assert "section,item_id,title,status,score_or_risk,execution_policy,recommended_next_step" in csv_summary
    assert "useful_signals" in csv_summary
    assert "approval_gates" in csv_summary


def test_report_previews_include_all_three_formats():
    previews = build_report_previews(_demo_report_package())

    assert set(previews) == {"markdown", "json", "csv"}
    assert previews["markdown"].startswith("# AgentHubControlCenter V2 Demo Workflow Report")
    assert previews["json"].startswith("{")
    assert previews["csv"].startswith("section,item_id")


def test_report_policy_validator_rejects_wrong_output_dir():
    package = _demo_report_package()
    package["output_dir"] = "outputs/private"

    violations = find_report_export_policy_violations(package)

    assert violations
    assert "output_dir must be outputs/public_reports." in violations[0]["warnings"]
