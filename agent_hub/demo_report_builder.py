from __future__ import annotations

import csv
import io
import json
from typing import Any

from agent_hub.report_export_schema import (
    REPORT_EXPORT_POLICY,
    REPORT_REQUIRED_SECTIONS,
    REPORT_SAFETY_NOTES,
    build_report_metadata,
    find_report_export_policy_violations,
    normalize_report_sections,
    validate_report_package,
)


CSV_COLUMNS = [
    "section",
    "item_id",
    "title",
    "status",
    "score_or_risk",
    "execution_policy",
    "recommended_next_step",
]


def _safe_text(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    if isinstance(value, list):
        return ", ".join(_safe_text(item) for item in value if _safe_text(item))
    if isinstance(value, dict):
        return "; ".join(f"{key}: {_safe_text(item)}" for key, item in value.items())
    return str(value).strip() or fallback


def _metric(summary: dict[str, Any], key: str, fallback: int | str = 0) -> Any:
    return summary.get(key, fallback) if isinstance(summary, dict) else fallback


def _short_agent(agent: dict[str, Any]) -> dict[str, Any]:
    return {
        "agent_id": agent.get("agent_id", ""),
        "agent_name": agent.get("agent_name", ""),
        "category": agent.get("category_label") or agent.get("category", ""),
        "status": agent.get("status", ""),
        "project_path": agent.get("project_path", ""),
        "next_recommended_action": agent.get("next_recommended_action", ""),
        "actions": len(agent.get("actions", [])),
        "connectors": len(agent.get("connectors", [])),
        "safe_mode": agent.get("safe_mode", True),
        "demo_mode": agent.get("demo_mode", True),
    }


def _short_signal(signal: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_id": signal.get("signal_id", ""),
        "title": signal.get("title", ""),
        "category": signal.get("category", ""),
        "status": signal.get("status", ""),
        "bucket": signal.get("bucket", ""),
        "usefulness_score": signal.get("usefulness_score", 0),
        "risk_score": signal.get("risk_score", 0),
        "source_agent": signal.get("source_agent", ""),
        "recommended_action": signal.get("recommended_action", ""),
        "execution_policy": signal.get("execution_policy", ""),
    }


def _short_connector(connector: dict[str, Any]) -> dict[str, Any]:
    return {
        "connector_id": connector.get("connector_id", ""),
        "connector_name": connector.get("connector_name", ""),
        "provider": connector.get("provider", ""),
        "risk_level": connector.get("risk_level", ""),
        "readiness_status": connector.get("readiness_status", ""),
        "readiness_score": connector.get("readiness_score", 0),
        "live_connection_status": connector.get("live_connection_status", ""),
        "recommended_next_step": connector.get("recommended_next_step", ""),
        "execution_policy": connector.get("execution_policy", ""),
    }


def _short_workflow(workflow: dict[str, Any]) -> dict[str, Any]:
    return {
        "workflow_id": workflow.get("workflow_id", ""),
        "workflow_name": workflow.get("workflow_name", ""),
        "workflow_type": workflow.get("workflow_type", ""),
        "workflow_status": workflow.get("workflow_status", ""),
        "workflow_readiness_score": workflow.get("workflow_readiness_score", 0),
        "blocked_steps": workflow.get("blocked_steps", []),
        "manual_steps": workflow.get("manual_steps", []),
        "generated_outputs": workflow.get("generated_outputs", []),
        "next_recommended_step": workflow.get("next_recommended_step", ""),
        "execution_policy": workflow.get("execution_policy", ""),
    }


def _short_gate(gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "gate_id": gate.get("gate_id", ""),
        "gate_name": gate.get("gate_name", ""),
        "workflow_name": gate.get("workflow_name", ""),
        "target_action_id": gate.get("target_action_id", ""),
        "target_connector_id": gate.get("target_connector_id", ""),
        "risk_level": gate.get("risk_level", ""),
        "approval_required": gate.get("approval_required", False),
        "approval_status": gate.get("approval_status", ""),
        "allowed_execution_mode": gate.get("allowed_execution_mode", ""),
        "block_reason": gate.get("block_reason", ""),
    }


def _build_action_execution_summary(action_rows: list[dict[str, Any]]) -> dict[str, Any]:
    blocked = [
        row
        for row in action_rows
        if row.get("risk_level") == "blocked"
        or row.get("status") == "blocked"
        or row.get("execution_mode") == "blocked"
    ]
    manual_only = [row for row in action_rows if row.get("execution_mode") == "manual_only"]
    display_only = [row for row in action_rows if row.get("execution_mode") == "not_executable"]
    template_only = [row for row in action_rows if row.get("execution_mode") == "template_only"]
    planned = [row for row in action_rows if row.get("execution_mode") == "planned"]
    return {
        "total_actions": len(action_rows),
        "blocked_actions": len(blocked),
        "manual_only_actions": len(manual_only),
        "display_only_actions": len(display_only),
        "template_only_actions": len(template_only),
        "planned_actions": len(planned),
        "blocked_action_examples": [_short_action(row) for row in blocked[:10]],
        "manual_only_examples": [_short_action(row) for row in manual_only[:10]],
        "template_only_examples": [_short_action(row) for row in template_only[:10]],
    }


def _short_action(action: dict[str, Any]) -> dict[str, Any]:
    return {
        "agent_name": action.get("agent_name", ""),
        "action_id": action.get("action_id", ""),
        "label": action.get("label", ""),
        "action_type": action.get("action_type", ""),
        "execution_mode": action.get("execution_mode", ""),
        "risk_level": action.get("risk_level", ""),
        "requires_approval": action.get("requires_approval", False),
        "status": action.get("status", ""),
        "expected_output": action.get("expected_output", ""),
        "safety_note": action.get("safety_note", ""),
    }


def _build_recommended_next_steps(
    *,
    useful_signals: list[dict[str, Any]],
    connectors: list[dict[str, Any]],
    workflows: list[dict[str, Any]],
    approval_gates: list[dict[str, Any]],
) -> list[str]:
    steps: list[str] = []
    for signal in useful_signals[:3]:
        step = _safe_text(signal.get("suggested_next_step") or signal.get("recommended_action"))
        if step and step not in steps:
            steps.append(step)
    for workflow in workflows:
        step = _safe_text(workflow.get("next_recommended_step"))
        if step and step not in steps:
            steps.append(step)
    if any(gate.get("approval_status") == "blocked" for gate in approval_gates):
        steps.append("Keep blocked Approval Gates blocked until a separate approved execution stage exists.")
    if any(connector.get("readiness_status") == "blocked_until_approved" for connector in connectors):
        steps.append("Review blocked connector plans manually; do not connect live accounts in this stage.")
    return steps[:8]


def build_demo_report_package(
    *,
    agent_manifests: list[dict[str, Any]],
    registry_summary: dict[str, Any],
    onboarding_summary: dict[str, Any],
    action_rows: list[dict[str, Any]],
    action_summary: dict[str, Any],
    useful_signals: list[dict[str, Any]],
    useful_signal_summary: dict[str, Any],
    connector_readiness: list[dict[str, Any]],
    connector_readiness_summary: dict[str, Any],
    workflow_simulations: list[dict[str, Any]],
    workflow_simulation_summary: dict[str, Any],
    approval_gates: list[dict[str, Any]],
    approval_gate_summary: dict[str, Any],
    validation_snapshot: dict[str, Any] | None = None,
    selected_sections: list[str] | tuple[str, ...] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a structured public-safe demo workflow report package."""
    normalized_sections = normalize_report_sections(selected_sections)
    metadata = build_report_metadata(
        selected_sections=normalized_sections,
        generated_at=generated_at,
    )
    top_useful_signals = sorted(
        useful_signals,
        key=lambda item: (-int(item.get("usefulness_score", 0)), _safe_text(item.get("title")).lower()),
    )[:5]
    action_execution_summary = _build_action_execution_summary(action_rows)

    sections: dict[str, Any] = {
        "executive_summary": {
            "summary": (
                "AgentHubControlCenter V2 exports local/demo workflow metadata, "
                "useful signals, connector readiness, approval gates, and action "
                "safety summaries for portfolio review."
            ),
            "tracked_agents": _metric(registry_summary, "total_agents"),
            "total_actions": action_summary.get("total_actions", len(action_rows)),
            "total_useful_signals": useful_signal_summary.get("total_signals", len(useful_signals)),
            "total_connectors": connector_readiness_summary.get("total_connectors", len(connector_readiness)),
            "total_demo_workflows": workflow_simulation_summary.get("total_demo_workflows", len(workflow_simulations)),
            "total_approval_gates": approval_gate_summary.get("total_approval_gates", len(approval_gates)),
        },
        "system_snapshot": {
            "stage": "HUB-V2-010-DEMO-WORKFLOW-REPORT-EXPORT",
            "mode": "local_demo_public_safe",
            "live_connector_status": "not_connected",
            "real_action_execution": "disabled",
            "external_api_calls": "disabled",
        },
    }

    if "agents" in normalized_sections:
        sections["agent_registry_summary"] = {
            "registry_summary": registry_summary,
            "onboarding_summary": onboarding_summary,
            "agents": [_short_agent(agent) for agent in agent_manifests],
        }
    if "actions" in normalized_sections:
        sections["action_execution_summary"] = action_execution_summary
    if "useful_signals" in normalized_sections:
        sections["useful_signals_summary"] = {
            "summary": useful_signal_summary,
            "top_useful_signals": [_short_signal(signal) for signal in top_useful_signals],
        }
    if "connectors" in normalized_sections:
        sections["connector_readiness_summary"] = {
            "summary": connector_readiness_summary,
            "connectors": [_short_connector(connector) for connector in connector_readiness],
        }
    if "workflows" in normalized_sections:
        sections["workflow_simulation_summary"] = {
            "summary": workflow_simulation_summary,
            "workflows": [_short_workflow(workflow) for workflow in workflow_simulations],
        }
    if "approval_gates" in normalized_sections:
        sections["approval_gates_summary"] = {
            "summary": approval_gate_summary,
            "approval_gates": [_short_gate(gate) for gate in approval_gates],
        }

    recommended_next_steps = _build_recommended_next_steps(
        useful_signals=top_useful_signals,
        connectors=connector_readiness,
        workflows=workflow_simulations,
        approval_gates=approval_gates,
    )
    default_validation_snapshot = {
        "valid_manifests": onboarding_summary.get("valid_manifests", 0),
        "invalid_manifests": onboarding_summary.get("invalid_manifests", 0),
        "missing_manifests": onboarding_summary.get("missing_manifests", 0),
        "unsafe_execution_modes": 0,
        "action_policy_violations": 0,
        "signal_policy_violations": 0,
        "connector_policy_violations": 0,
        "workflow_policy_violations": 0,
        "approval_gate_policy_violations": 0,
        "report_export_policy_violations": 0,
    }
    if validation_snapshot:
        default_validation_snapshot.update(validation_snapshot)

    package = {
        **metadata,
        "required_report_sections": REPORT_REQUIRED_SECTIONS,
        "safety_notes": list(REPORT_SAFETY_NOTES),
        "validation_snapshot": default_validation_snapshot,
        "recommended_next_steps": recommended_next_steps,
        "sections": sections,
    }
    validation = validate_report_package(package)
    package["schema_valid"] = validation["is_valid"]
    package["schema_warnings"] = validation["warnings"]
    package["missing_schema_fields"] = validation["missing_fields"]
    package["validation_snapshot"]["report_export_policy_violations"] = len(
        find_report_export_policy_violations(package)
    )
    return package


def _markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "No rows available.\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = _safe_text(row.get(column, ""))
            values.append(value.replace("|", "/"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def build_markdown_report(package: dict[str, Any]) -> str:
    """Render a GitHub-friendly Markdown report from a report package."""
    sections = package.get("sections", {})
    executive = sections.get("executive_summary", {})
    system = sections.get("system_snapshot", {})
    lines = [
        "# AgentHubControlCenter V2 Demo Workflow Report",
        "",
        f"Generated Time: {package.get('generated_at', '')}",
        f"Schema Version: {package.get('schema_version', '')}",
        f"Export Policy: {package.get('export_policy', REPORT_EXPORT_POLICY)}",
        "",
        "## 1. Executive Summary",
        "",
        _safe_text(executive.get("summary")),
        "",
        f"- Tracked Agents: {executive.get('tracked_agents', 0)}",
        f"- Total Actions: {executive.get('total_actions', 0)}",
        f"- Useful Signals: {executive.get('total_useful_signals', 0)}",
        f"- Demo Connectors: {executive.get('total_connectors', 0)}",
        f"- Demo Workflows: {executive.get('total_demo_workflows', 0)}",
        f"- Approval Gates: {executive.get('total_approval_gates', 0)}",
        "",
        "## 2. System Snapshot",
        "",
        f"- Stage: {_safe_text(system.get('stage'))}",
        f"- Mode: {_safe_text(system.get('mode'))}",
        f"- Live Connector Status: {_safe_text(system.get('live_connector_status'))}",
        f"- Real Action Execution: {_safe_text(system.get('real_action_execution'))}",
        f"- External API Calls: {_safe_text(system.get('external_api_calls'))}",
        "",
        "## 3. Agent Registry Summary",
        "",
    ]

    agent_section = sections.get("agent_registry_summary")
    if agent_section:
        onboarding = agent_section.get("onboarding_summary", {})
        lines.extend(
            [
                f"- Valid Manifests: {onboarding.get('valid_manifests', 0)}",
                f"- Invalid Manifests: {onboarding.get('invalid_manifests', 0)}",
                f"- Missing Manifests: {onboarding.get('missing_manifests', 0)}",
                "",
                _markdown_table(
                    agent_section.get("agents", []),
                    ["agent_name", "category", "status", "actions", "connectors", "next_recommended_action"],
                ),
            ]
        )
    else:
        lines.append("Agent section was not selected for this preview.\n")

    lines.extend(["", "## 4. Useful Signals", ""])
    signal_section = sections.get("useful_signals_summary")
    if signal_section:
        summary = signal_section.get("summary", {})
        lines.extend(
            [
                f"- Total Signals: {summary.get('total_signals', 0)}",
                f"- High Value: {summary.get('high_value_signals', 0)}",
                f"- Needs Action: {summary.get('needs_action_signals', 0)}",
                f"- Watchlist: {summary.get('watchlist_signals', 0)}",
                f"- Average Usefulness: {summary.get('average_usefulness_score', 0)}",
                "",
                "### Top Useful Signals",
                "",
                _markdown_table(
                    signal_section.get("top_useful_signals", []),
                    ["title", "category", "status", "usefulness_score", "risk_score", "recommended_action"],
                ),
            ]
        )
    else:
        lines.append("Useful Signals section was not selected for this preview.\n")

    lines.extend(["", "## 5. Connector Readiness", ""])
    connector_section = sections.get("connector_readiness_summary")
    if connector_section:
        summary = connector_section.get("summary", {})
        lines.extend(
            [
                f"- Total Connectors: {summary.get('total_connectors', 0)}",
                f"- Ready For Demo: {summary.get('ready_for_demo_connectors', 0)}",
                f"- Needs Review: {summary.get('needs_review_connectors', 0)}",
                f"- Blocked Until Approved: {summary.get('blocked_until_approved_connectors', 0)}",
                "",
                _markdown_table(
                    connector_section.get("connectors", []),
                    ["connector_name", "provider", "risk_level", "readiness_status", "readiness_score", "live_connection_status"],
                ),
            ]
        )
    else:
        lines.append("Connector Readiness section was not selected for this preview.\n")

    lines.extend(["", "## 6. Local Workflow Simulation", ""])
    workflow_section = sections.get("workflow_simulation_summary")
    if workflow_section:
        summary = workflow_section.get("summary", {})
        lines.extend(
            [
                f"- Demo Workflows: {summary.get('total_demo_workflows', 0)}",
                f"- Ready For Manual Review: {summary.get('ready_for_manual_review_workflows', 0)}",
                f"- Blocked Steps: {summary.get('blocked_steps', 0)}",
                f"- Average Readiness: {summary.get('average_workflow_readiness_score', 0)}",
                "",
                _markdown_table(
                    workflow_section.get("workflows", []),
                    ["workflow_name", "workflow_type", "workflow_status", "workflow_readiness_score", "blocked_steps", "next_recommended_step"],
                ),
            ]
        )
    else:
        lines.append("Workflow Simulation section was not selected for this preview.\n")

    lines.extend(["", "## 7. Approval Gates", ""])
    gate_section = sections.get("approval_gates_summary")
    if gate_section:
        summary = gate_section.get("summary", {})
        lines.extend(
            [
                f"- Total Approval Gates: {summary.get('total_approval_gates', 0)}",
                f"- Approval Required: {summary.get('approval_required_gates', 0)}",
                f"- Blocked Gates: {summary.get('blocked_gates', 0)}",
                f"- Dry Run Required: {summary.get('dry_run_required_gates', 0)}",
                "",
                _markdown_table(
                    gate_section.get("approval_gates", []),
                    ["gate_name", "workflow_name", "target_action_id", "target_connector_id", "risk_level", "approval_status", "allowed_execution_mode"],
                ),
            ]
        )
    else:
        lines.append("Approval Gates section was not selected for this preview.\n")

    action_section = sections.get("action_execution_summary", {})
    validation_snapshot = package.get("validation_snapshot", {})
    lines.extend(
        [
            "",
            "## 8. Safety Snapshot",
            "",
            "### Blocked / Manual / Template-only Actions",
            "",
            f"- Blocked Actions: {action_section.get('blocked_actions', 0)}",
            f"- Manual-only Actions: {action_section.get('manual_only_actions', 0)}",
            f"- Display-only Actions: {action_section.get('display_only_actions', 0)}",
            f"- Template-only Actions: {action_section.get('template_only_actions', 0)}",
            f"- Planned Actions: {action_section.get('planned_actions', 0)}",
            "",
            "### Safety Notes",
            "",
        ]
    )
    lines.extend(f"- {note}" for note in package.get("safety_notes", []))
    lines.extend(["", "### Validation Snapshot", ""])
    lines.extend(f"- {key}: {value}" for key, value in validation_snapshot.items())

    lines.extend(["", "## 9. Recommended Next Steps", ""])
    steps = package.get("recommended_next_steps", [])
    if steps:
        lines.extend(f"{index}. {step}" for index, step in enumerate(steps, 1))
    else:
        lines.append("1. Review the generated report manually and keep all real execution disabled.")

    lines.extend(
        [
            "",
            "## 10. Public-Safe Disclaimer",
            "",
            "This report is generated from demo/local metadata only. It does not include credentials, tokens, private outputs, live connector data, or external API results. It is intended for portfolio review, manual planning, and public-safe showcase documentation.",
            "",
        ]
    )
    return "\n".join(lines)


def build_json_report(package: dict[str, Any]) -> str:
    """Render a structured JSON report for future AgentHub re-import."""
    return json.dumps(package, indent=2, sort_keys=True)


def build_csv_summary(package: dict[str, Any]) -> str:
    """Render a compact CSV summary of report rows."""
    rows: list[dict[str, Any]] = []
    sections = package.get("sections", {})

    executive = sections.get("executive_summary", {})
    for key, value in executive.items():
        if key == "summary":
            continue
        rows.append(
            {
                "section": "executive_summary",
                "item_id": key,
                "title": key.replace("_", " ").title(),
                "status": value,
                "score_or_risk": "",
                "execution_policy": package.get("export_policy", ""),
                "recommended_next_step": "",
            }
        )

    for signal in sections.get("useful_signals_summary", {}).get("top_useful_signals", []):
        rows.append(
            {
                "section": "useful_signals",
                "item_id": signal.get("signal_id", ""),
                "title": signal.get("title", ""),
                "status": signal.get("status", ""),
                "score_or_risk": signal.get("usefulness_score", ""),
                "execution_policy": signal.get("execution_policy", ""),
                "recommended_next_step": signal.get("recommended_action", ""),
            }
        )
    for connector in sections.get("connector_readiness_summary", {}).get("connectors", []):
        rows.append(
            {
                "section": "connectors",
                "item_id": connector.get("connector_id", ""),
                "title": connector.get("connector_name", ""),
                "status": connector.get("readiness_status", ""),
                "score_or_risk": connector.get("risk_level", ""),
                "execution_policy": connector.get("execution_policy", ""),
                "recommended_next_step": connector.get("recommended_next_step", ""),
            }
        )
    for workflow in sections.get("workflow_simulation_summary", {}).get("workflows", []):
        rows.append(
            {
                "section": "workflows",
                "item_id": workflow.get("workflow_id", ""),
                "title": workflow.get("workflow_name", ""),
                "status": workflow.get("workflow_status", ""),
                "score_or_risk": workflow.get("workflow_readiness_score", ""),
                "execution_policy": workflow.get("execution_policy", ""),
                "recommended_next_step": workflow.get("next_recommended_step", ""),
            }
        )
    for gate in sections.get("approval_gates_summary", {}).get("approval_gates", []):
        rows.append(
            {
                "section": "approval_gates",
                "item_id": gate.get("gate_id", ""),
                "title": gate.get("gate_name", ""),
                "status": gate.get("approval_status", ""),
                "score_or_risk": gate.get("risk_level", ""),
                "execution_policy": gate.get("allowed_execution_mode", ""),
                "recommended_next_step": gate.get("block_reason", ""),
            }
        )

    action_summary = sections.get("action_execution_summary", {})
    for key in ["blocked_actions", "manual_only_actions", "display_only_actions", "template_only_actions", "planned_actions"]:
        rows.append(
            {
                "section": "actions",
                "item_id": key,
                "title": key.replace("_", " ").title(),
                "status": action_summary.get(key, 0),
                "score_or_risk": "",
                "execution_policy": "metadata_instruction_template_only",
                "recommended_next_step": "Review in Action Center. Do not execute from report export.",
            }
        )

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({column: _safe_text(row.get(column, "")) for column in CSV_COLUMNS})
    return output.getvalue()


def build_report_previews(package: dict[str, Any]) -> dict[str, str]:
    """Return all copy/download-ready report formats."""
    return {
        "markdown": build_markdown_report(package),
        "json": build_json_report(package),
        "csv": build_csv_summary(package),
    }
