from __future__ import annotations

from datetime import datetime


def _markdown_cell(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _join_list(values: object) -> str:
    """Format a list-like value for Markdown tables."""
    if isinstance(values, list):
        return ", ".join(str(value) for value in values if str(value))
    return "" if values is None else str(values)


def _format_generated_at(generated_at: datetime | str | None) -> str:
    """Format report generation time for Markdown output."""
    if generated_at is None:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(generated_at, datetime):
        return generated_at.strftime("%Y-%m-%d %H:%M:%S")
    return str(generated_at)


def _select_next_best_move(action_plan: list[dict]) -> str:
    """Pick the most useful next portfolio action without expanding paused projects."""
    actionable_items = [item for item in action_plan if item.get("priority") != "None"]
    if actionable_items:
        top_action = actionable_items[0]
        return f"{top_action.get('agent_name', '')}: {top_action.get('recommended_action', '')}"
    return "Continue HUB-V2-002 Manifest Import + Agent Onboarding Flow."


def build_command_center_summary(
    registry_summary: dict,
    health_results: list[dict],
    validation_results: list[dict] | None = None,
    action_plan: list[dict] | None = None,
    portfolio_positioning: dict | None = None,
) -> dict:
    """Build a compact summary for the command center and report export."""
    validation_results = validation_results or []
    action_plan = action_plan or []
    portfolio_positioning = portfolio_positioning or {}

    health_ready_count = sum(
        1 for item in health_results if item.get("health_status") == "Showcase Ready"
    )
    health_issue_count = sum(
        1 for item in health_results if item.get("health_status") == "Missing or Incomplete"
    )
    registry_issue_count = sum(1 for item in validation_results if not item.get("is_valid", False))
    high_priority_actions = sum(1 for item in action_plan if item.get("priority") == "High")
    next_best_move = _select_next_best_move(action_plan)
    strongest_categories = portfolio_positioning.get("strongest_categories", [])
    portfolio_gaps = portfolio_positioning.get("portfolio_gaps", [])

    return {
        "tracked_agents": registry_summary.get("total_agents", 0),
        "completed_agents": registry_summary.get("completed_agents", 0),
        "public_showcase_agents": registry_summary.get("public_showcase_agents", 0),
        "pinned_agents": registry_summary.get("pinned_agents", 0),
        "public_not_pinned_agents": registry_summary.get("public_not_pinned_agents", 0),
        "paused_or_completed_agents": registry_summary.get("paused_or_completed_agents", 0),
        "showcase_ready_agents": health_ready_count,
        "health_issue_count": health_issue_count,
        "registry_issue_count": registry_issue_count,
        "high_priority_actions": high_priority_actions,
        "strongest_categories": strongest_categories,
        "portfolio_gaps": portfolio_gaps,
        "portfolio_overview": (
            f"{registry_summary.get('total_agents', 0)} tracked projects, "
            f"{registry_summary.get('completed_agents', 0)} complete, "
            f"{registry_summary.get('paused_or_completed_agents', 0)} paused or complete."
        ),
        "showcase_status": (
            f"{registry_summary.get('public_showcase_agents', 0)} public showcase projects, "
            f"{registry_summary.get('pinned_agents', 0)} pinned, "
            f"{registry_summary.get('public_not_pinned_agents', 0)} public but not pinned."
        ),
        "health_snapshot": (
            f"{health_ready_count} showcase-ready projects, "
            f"{health_issue_count} missing/incomplete health checks, "
            f"{registry_issue_count} registry metadata issue(s)."
        ),
        "priority_actions": (
            f"{high_priority_actions} high-priority action(s). Next best move: {next_best_move}"
        ),
        "strategic_summary": (
            "The portfolio is strongest where local-first AI workflows, business analysis, "
            "media extraction, finance research, and operations dashboards are already visible. "
            "The main gaps are dedicated knowledge-base workflows, deeper orchestration, "
            "and public showcase packaging for the hub itself."
        ),
        "next_best_move": next_best_move,
    }


def build_showcase_asset_checklist(
    registry_summary: dict,
    health_results: list[dict],
    action_plan: list[dict] | None = None,
) -> list[dict]:
    """Build a public-safe checklist for GitHub showcase asset preparation."""
    action_plan = action_plan or []
    high_priority_actions = sum(1 for item in action_plan if item.get("priority") == "High")
    missing_health_items = sum(
        1 for item in health_results if item.get("health_status") == "Missing or Incomplete"
    )

    report_status = "Ready" if registry_summary.get("total_agents", 0) else "Needs Registry Data"
    health_status = "Review Needed" if missing_health_items else "Ready"
    action_status = "Review Needed" if high_priority_actions else "Ready"

    return [
        {
            "asset": "Markdown portfolio report",
            "status": report_status,
            "public_safe_note": "Generated from local registry, health, validation, and planning metadata.",
        },
        {
            "asset": "Command center overview screenshot",
            "status": report_status,
            "public_safe_note": "Capture summary cards, positioning, capability overview, and action snapshot.",
        },
        {
            "asset": "Agent registry detail screenshot",
            "status": report_status,
            "public_safe_note": "Use registry rows and display-only command pack; do not expose private credentials.",
        },
        {
            "asset": "Health check dashboard screenshot",
            "status": health_status,
            "public_safe_note": "Review local path visibility before publishing screenshots.",
        },
        {
            "asset": "Portfolio matrix screenshot",
            "status": report_status,
            "public_safe_note": "Show capability clusters, strongest categories, and portfolio gaps.",
        },
        {
            "asset": "Next actions screenshot",
            "status": action_status,
            "public_safe_note": "Show planning priorities only; no automation is executed.",
        },
        {
            "asset": "Export report screenshot",
            "status": report_status,
            "public_safe_note": "Show report summary, local save flow, download control, and report preview.",
        },
    ]


def build_portfolio_markdown_report(
    agents: list[dict],
    registry_summary: dict,
    capability_summary: list[dict],
    health_results: list[dict],
    validation_results: list[dict] | None = None,
    action_plan: list[dict] | None = None,
    portfolio_positioning: dict | None = None,
    workflow_pack_integration: dict | None = None,
    generated_at: datetime | str | None = None,
) -> str:
    """Build a Markdown portfolio report from registry and health data."""
    validation_results = validation_results or []
    action_plan = action_plan or []
    portfolio_positioning = portfolio_positioning or {}
    workflow_pack_integration = workflow_pack_integration or {}
    high_priority_actions = sum(1 for item in action_plan if item.get("priority") == "High")
    command_center_summary = build_command_center_summary(
        registry_summary=registry_summary,
        health_results=health_results,
        validation_results=validation_results,
        action_plan=action_plan,
        portfolio_positioning=portfolio_positioning,
    )
    showcase_asset_checklist = build_showcase_asset_checklist(
        registry_summary=registry_summary,
        health_results=health_results,
        action_plan=action_plan,
    )
    action_by_name = {item.get("agent_name", ""): item for item in action_plan}
    generated_at_text = _format_generated_at(generated_at)

    lines = [
        "# AgentHubControlCenter Portfolio Report",
        "",
        f"Generated Time: {generated_at_text}",
        "",
        "## Project Overview",
        "AgentHubControlCenter is a local-first AI Portfolio Command Center for "
        "tracking, evaluating, and exporting the user's AI Agent / Skill project matrix.",
        "",
        "## Portfolio Overview",
        f"- Total Agents: {registry_summary.get('total_agents', 0)}",
        f"- Completed Agents: {registry_summary.get('completed_agents', 0)}",
        f"- Public Showcase Agents: {registry_summary.get('public_showcase_agents', 0)}",
        f"- Pinned Agents: {registry_summary.get('pinned_agents', 0)}",
        f"- Public But Not Pinned: {registry_summary.get('public_not_pinned_agents', 0)}",
        f"- Paused / Completed Agents: {registry_summary.get('paused_or_completed_agents', 0)}",
        "- Categories: " + ", ".join(registry_summary.get("categories", [])),
        f"- High Priority Actions: {high_priority_actions}",
        "",
        "## Command Center Summary",
        "### Portfolio Overview",
        command_center_summary["portfolio_overview"],
        "",
        "### Showcase Status",
        command_center_summary["showcase_status"],
        "",
        "### Health Snapshot",
        command_center_summary["health_snapshot"],
        "",
        "### Priority Actions",
        command_center_summary["priority_actions"],
        "",
        "### Strategic Summary",
        command_center_summary["strategic_summary"],
        "",
        "### Next Best Move",
        command_center_summary["next_best_move"],
        "",
        "| Area | Value |",
        "| --- | --- |",
        f"| Tracked Agents | {command_center_summary['tracked_agents']} |",
        f"| Completed Agents | {command_center_summary['completed_agents']} |",
        f"| Public Showcase Agents | {command_center_summary['public_showcase_agents']} |",
        f"| Pinned Agents | {command_center_summary['pinned_agents']} |",
        f"| Public But Not Pinned | {command_center_summary['public_not_pinned_agents']} |",
        f"| Paused / Completed | {command_center_summary['paused_or_completed_agents']} |",
        f"| Showcase Ready Agents | {command_center_summary['showcase_ready_agents']} |",
        f"| Health Issues | {command_center_summary['health_issue_count']} |",
        f"| Registry Issues | {command_center_summary['registry_issue_count']} |",
        f"| High Priority Actions | {command_center_summary['high_priority_actions']} |",
        "| Strongest Categories | "
        + _markdown_cell(_join_list(command_center_summary["strongest_categories"]))
        + " |",
        "| Portfolio Gaps | "
        + _markdown_cell(_join_list(command_center_summary["portfolio_gaps"]))
        + " |",
        "",
        "## Agent Matrix",
        "| Name | Category | Status | Showcase Status | Priority | Next Action | Public Value |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for agent in agents:
        action_item = action_by_name.get(agent.get("agent_name", ""), {})
        lines.append(
            "| {agent_name} | {category} | {status} | {showcase_status} | {priority} | "
            "{next_action} | {public_value} |".format(
                agent_name=_markdown_cell(agent.get("agent_name", "")),
                category=_markdown_cell(agent.get("category", "")),
                status=_markdown_cell(agent.get("status", "")),
                showcase_status=_markdown_cell(agent.get("showcase_status", "")),
                priority=_markdown_cell(action_item.get("priority", "None")),
                next_action=_markdown_cell(agent.get("next_action", "")),
                public_value=_markdown_cell(agent.get("portfolio_value", "")),
            )
        )

    lines.extend(
        [
            "",
            "## Registry Validation",
            "| Agent | Quality Score | Valid | Missing Required Fields | Validation Notes |",
            "| --- | ---: | --- | --- | --- |",
        ]
    )
    for result in validation_results:
        lines.append(
            "| {agent_name} | {quality_score} | {is_valid} | {missing} | {notes} |".format(
                agent_name=_markdown_cell(result.get("agent_name", "")),
                quality_score=_markdown_cell(result.get("quality_score", 0)),
                is_valid=_markdown_cell(result.get("is_valid", False)),
                missing=_markdown_cell(_join_list(result.get("missing_required_fields", []))),
                notes=_markdown_cell(_join_list(result.get("validation_notes", []))),
            )
        )

    lines.extend(["", "## Capability Matrix"])
    for item in capability_summary:
        lines.append(f"### {item.get('category', 'Uncategorized')}")
        lines.append(f"- Agent Count: {item.get('agent_count', 0)}")
        lines.append("- Agents: " + ", ".join(item.get("agents", [])))
        lines.append("- Capabilities: " + "; ".join(item.get("capabilities", [])))
        lines.append(f"- Showcase Count: {item.get('showcase_count', 0)}")
        lines.append(f"- Pinned Count: {item.get('pinned_count', 0)}")
        lines.append("")

    lines.extend(
        [
            "## Health Check Summary",
            "| Agent | Health Score | Health Status | Missing Items |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for result in health_results:
        lines.append(
            "| {agent_name} | {health_score} | {health_status} | {missing_items} |".format(
                agent_name=_markdown_cell(result.get("agent_name", "")),
                health_score=_markdown_cell(result.get("health_score", 0)),
                health_status=_markdown_cell(result.get("health_status", "")),
                missing_items=_markdown_cell(_join_list(result.get("missing_items", []))),
            )
        )

    lines.extend(
        [
            "",
            "## Priority Action Plan",
            "| Agent | Priority | Recommended Action | Reason | Related Issue |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in action_plan:
        lines.append(
            "| {agent_name} | {priority} | {recommended_action} | {reason} | {related_issue} |".format(
                agent_name=_markdown_cell(item.get("agent_name", "")),
                priority=_markdown_cell(item.get("priority", "")),
                recommended_action=_markdown_cell(item.get("recommended_action", "")),
                reason=_markdown_cell(item.get("reason", "")),
                related_issue=_markdown_cell(item.get("related_issue", "")),
            )
        )

    lines.extend(
        [
            "",
            "## Public Showcase Readiness",
            "| Asset | Status | Public-Safe Note |",
            "| --- | --- | --- |",
        ]
    )
    for item in showcase_asset_checklist:
        lines.append(
            "| {asset} | {status} | {note} |".format(
                asset=_markdown_cell(item.get("asset", "")),
                status=_markdown_cell(item.get("status", "")),
                note=_markdown_cell(item.get("public_safe_note", "")),
            )
        )

    if workflow_pack_integration:
        metadata_stats = workflow_pack_integration.get("source_metadata_stats", {})
        top_pack_names = [
            str(pack.get("pack_name", ""))
            for pack in workflow_pack_integration.get("top_workflow_packs", [])
            if isinstance(pack, dict) and pack.get("pack_name")
        ]
        lines.extend(
            [
                "",
                "## Workflow Pack Integration",
                f"- Integration Status: {_markdown_cell(workflow_pack_integration.get('integration_status', 'missing'))}",
                f"- Total Workflow Packs: {_markdown_cell(workflow_pack_integration.get('total_workflow_packs', 0))}",
                f"- Metadata Enriched Agents: {_markdown_cell(workflow_pack_integration.get('metadata_enriched_agents', 0))}",
                f"- Safe Metadata Integration: {_markdown_cell(workflow_pack_integration.get('safe_metadata_integration', False))}",
                f"- Loaded Metadata Files: {_markdown_cell(metadata_stats.get('loaded_metadata_files', 0))}",
                f"- Missing Metadata Files: {_markdown_cell(metadata_stats.get('missing_metadata_files', 0))}",
                f"- Rejected Metadata Files: {_markdown_cell(metadata_stats.get('rejected_metadata_files', 0))}",
                f"- Top Workflow Packs: {_markdown_cell(', '.join(top_pack_names) if top_pack_names else 'None')}",
                f"- Summary Path: {_markdown_cell(workflow_pack_integration.get('summary_path', ''))}",
                f"- Safety Note: {_markdown_cell(workflow_pack_integration.get('safety_note', ''))}",
            ]
        )

    positioning_statement = portfolio_positioning.get(
        "positioning_statement",
        (
            "AgentHubControlCenter presents a local-first AI Agent / Skill ecosystem "
            "that demonstrates AI workflow, business automation, media intelligence, "
            "finance research, news analysis, career workflow, and portfolio operations."
        ),
    )
    showcase_strengths = portfolio_positioning.get("showcase_strengths", [])
    portfolio_gaps = portfolio_positioning.get("portfolio_gaps", [])

    lines.extend(
        [
            "",
            "## Portfolio Positioning",
            positioning_statement,
            "",
            "### Showcase Strengths",
        ]
    )
    lines.extend([f"- {strength}" for strength in showcase_strengths])
    lines.extend(
        [
            "",
            "### Portfolio Gaps",
        ]
    )
    lines.extend([f"- {gap}" for gap in portfolio_gaps])
    lines.extend(
        [
            "",
            "## Disclaimer",
            "This is a local-first portfolio management tool. It does not include private "
            "API keys, does not read credentials, does not initialize remotes, and does "
            "not automatically push GitHub repositories.",
            "",
        ]
    )

    return "\n".join(lines)
