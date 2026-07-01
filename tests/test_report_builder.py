from agent_hub.report_builder import (
    build_command_center_summary,
    build_portfolio_markdown_report,
    build_showcase_asset_checklist,
)


def test_build_portfolio_markdown_report_contains_required_sections():
    agents = [
        {
            "agent_name": "Demo Agent",
            "category": "Demo",
            "status": "Complete",
            "stage": "DEMO-001",
            "github_url": "https://github.com/example/demo",
            "next_action": "Paused",
            "showcase_status": "GitHub Public Showcase",
            "portfolio_value": "Shows a complete local-first demo workflow.",
        }
    ]
    registry_summary = {
        "total_agents": 1,
        "completed_agents": 1,
        "public_showcase_agents": 1,
        "pinned_agents": 1,
        "public_not_pinned_agents": 0,
        "paused_or_completed_agents": 1,
        "categories": ["Demo"],
    }
    capability_summary = [
        {
            "category": "Demo",
            "agent_count": 1,
            "agents": ["Demo Agent"],
            "capabilities": ["Demo workflow"],
            "showcase_count": 1,
            "pinned_count": 1,
        }
    ]
    health_results = [
        {
            "agent_name": "Demo Agent",
            "health_score": 100,
            "health_status": "Showcase Ready",
            "missing_items": [],
        }
    ]
    validation_results = [
        {
            "agent_name": "Demo Agent",
            "quality_score": 100,
            "is_valid": True,
            "missing_required_fields": [],
            "validation_notes": ["Registry metadata looks complete."],
        }
    ]
    action_plan = [
        {
            "agent_name": "Demo Agent",
            "priority": "None",
            "recommended_action": "No immediate action",
            "reason": "Agent is complete and showcase-ready.",
            "related_issue": "",
        }
    ]
    portfolio_positioning = {
        "positioning_statement": "Demo positioning statement.",
        "showcase_strengths": ["Local-first AI workflows"],
        "portfolio_gaps": ["Production deployment not yet included"],
    }

    report = build_portfolio_markdown_report(
        agents=agents,
        registry_summary=registry_summary,
        capability_summary=capability_summary,
        health_results=health_results,
        validation_results=validation_results,
        action_plan=action_plan,
        portfolio_positioning=portfolio_positioning,
        workflow_pack_integration={
            "integration_status": "available",
            "total_workflow_packs": 23,
            "metadata_enriched_agents": 12,
            "safe_metadata_integration": True,
            "source_metadata_stats": {
                "loaded_metadata_files": 35,
                "missing_metadata_files": 37,
                "rejected_metadata_files": 0,
            },
            "top_workflow_packs": [{"pack_name": "Codex Project Builder Pack"}],
            "summary_path": "F:/AIProjects/WorkflowPackAgent/outputs/agenthub_summary.json",
            "safety_note": "Only local JSON summaries are read.",
        },
        generated_at="2026-06-24 10:00:00",
    )

    assert "Generated Time: 2026-06-24 10:00:00" in report
    assert "## Project Overview" in report
    assert "## Portfolio Overview" in report
    assert "## Command Center Summary" in report
    assert "### Next Best Move" in report
    assert "## Agent Matrix" in report
    assert "| Name | Category | Status | Showcase Status | Priority | Next Action | Public Value |" in report
    assert "## Registry Validation" in report
    assert "## Priority Action Plan" in report
    assert "## Public Showcase Readiness" in report
    assert "## Workflow Pack Integration" in report
    assert "- Total Workflow Packs: 23" in report
    assert "Codex Project Builder Pack" in report
    assert "## Portfolio Positioning" in report
    assert "## Disclaimer" in report


def test_build_command_center_summary_counts_export_metrics():
    summary = build_command_center_summary(
        registry_summary={
            "total_agents": 2,
            "completed_agents": 1,
            "public_showcase_agents": 1,
            "pinned_agents": 1,
            "public_not_pinned_agents": 0,
            "paused_or_completed_agents": 1,
        },
        health_results=[
            {"health_status": "Showcase Ready"},
            {"health_status": "Missing or Incomplete"},
        ],
        validation_results=[
            {"is_valid": True},
            {"is_valid": False},
        ],
        action_plan=[
            {"priority": "High"},
            {"priority": "Low"},
        ],
        portfolio_positioning={
            "strongest_categories": ["Business Discovery"],
            "portfolio_gaps": ["Screenshots pending"],
        },
    )

    assert summary["tracked_agents"] == 2
    assert summary["public_not_pinned_agents"] == 0
    assert summary["paused_or_completed_agents"] == 1
    assert summary["showcase_ready_agents"] == 1
    assert summary["health_issue_count"] == 1
    assert summary["registry_issue_count"] == 1
    assert summary["high_priority_actions"] == 1
    assert "Next best move:" in summary["priority_actions"]
    assert isinstance(summary["next_best_move"], str)


def test_build_showcase_asset_checklist_flags_review_items():
    checklist = build_showcase_asset_checklist(
        registry_summary={"total_agents": 1},
        health_results=[{"health_status": "Missing or Incomplete"}],
        action_plan=[{"priority": "High"}],
    )

    statuses_by_asset = {item["asset"]: item["status"] for item in checklist}

    assert statuses_by_asset["Markdown portfolio report"] == "Ready"
    assert statuses_by_asset["Health check dashboard screenshot"] == "Review Needed"
    assert statuses_by_asset["Next actions screenshot"] == "Review Needed"
