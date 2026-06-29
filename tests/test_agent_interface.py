from agent_hub.agent_interface import (
    OPTIONAL_AGENT_FIELDS,
    STANDARD_AGENT_FIELDS,
    build_action_center_items,
    build_agent_contract,
    build_agent_manifest,
    build_agent_manifests,
    build_connector_overview,
    format_category_label,
    build_future_plugin_interface,
    build_useful_signals,
    build_workflow_catalog,
)


def _demo_agent():
    return {
        "agent_id": "demo_agent",
        "agent_name": "DemoAgent",
        "category": "Workflow Automation",
        "project_type": "Agent",
        "local_path": "F:\\AIProjects\\DemoAgent",
        "github_url": "https://github.com/example/demo",
        "status": "Complete",
        "stage": "DEMO-001",
        "primary_capability": "Demo workflow automation capability",
        "tech_stack": "Python, Streamlit",
        "next_action": "Paused",
    }


def test_build_agent_manifest_contains_standard_fields():
    manifest = build_agent_manifest(
        _demo_agent(),
        health_result={"health_status": "Showcase Ready"},
        action_item={"recommended_action": "No immediate action"},
    )

    for field in STANDARD_AGENT_FIELDS:
        assert field in manifest

    assert manifest["agent_id"] == "demo_agent"
    assert manifest["category_label"] == "Workflow Automation"
    assert manifest["source"] == "static_registry"
    assert manifest["project_path"] == "F:\\AIProjects\\DemoAgent"
    assert manifest["demo_mode"] is True
    assert manifest["safe_mode"] is True
    assert manifest["last_run"] == "Not tracked yet"
    assert "workflow_steps" in manifest["inputs"]
    assert "automation_score" in manifest["outputs"]


def test_build_agent_manifest_prefers_imported_manifest_declarations():
    agent = _demo_agent()
    agent.update(
        {
            "category": "idea_validation",
            "manifest_inputs": ["idea_brief", "target_user"],
            "manifest_outputs": ["opportunity_score", "validation_plan"],
            "manifest_actions": [
                {
                    "action_id": "generate_demo_report",
                    "label": "Generate demo report",
                    "execution": "display_only",
                }
            ],
            "manifest_connectors": [
                {
                    "connector_id": "local_filesystem",
                    "label": "Local project files",
                    "status": "available_local",
                }
            ],
        }
    )

    manifest = build_agent_manifest(agent)

    assert manifest["inputs"] == ["idea_brief", "target_user"]
    assert manifest["category_label"] == "Idea Validation"
    assert manifest["outputs"] == ["opportunity_score", "validation_plan"]
    assert manifest["actions"][0]["enabled"] is True
    assert manifest["actions"][0]["label"] == "Generate demo report"
    assert manifest["connectors"][0]["mode"] == "not_connected"


def test_format_category_label_handles_standard_manifest_categories():
    assert format_category_label("sme_operations") == "SME Operations"
    assert format_category_label("quant_research") == "Quant Research"


def test_build_agent_contract_disables_live_external_actions_by_default():
    contract = build_agent_contract()

    assert contract["contract_version"] == "HUB-V2-024-DEEP-CHINESE-UI-COVERAGE-CHECK-COMPLETE"
    assert contract["required_fields"] == STANDARD_AGENT_FIELDS
    assert contract["optional_fields"] == OPTIONAL_AGENT_FIELDS
    assert "action_schema_fields" in contract
    assert "useful_signal_schema_fields" in contract
    assert "connector_readiness_schema_fields" in contract
    assert "workflow_simulation_schema_fields" in contract
    assert "approval_gate_schema_fields" in contract
    assert "report_export_schema_fields" in contract
    assert contract["execution_policy"]["external_api_calls"] == "disabled_by_default"
    assert contract["execution_policy"]["actions"] == "metadata_instruction_template_only"
    assert contract["execution_policy"]["useful_signals"] == "display_only_text_recommendation_no_execution"
    assert contract["execution_policy"]["connector_readiness"] == "design_only_readiness_simulation_no_live_connection"
    assert contract["execution_policy"]["workflow_simulation"] == "local_simulation_only_no_live_connector_no_real_action_no_credentials"
    assert contract["execution_policy"]["approval_gates"] == "approval_gate_metadata_only_no_execution"
    assert contract["execution_policy"]["report_export"] == "public_safe_demo_report_metadata_only_no_execution"
    assert contract["connector_policy"]["current_stage"] == "deep_chinese_ui_coverage_check"
    assert contract["codex_prompt_generator"]["current_stage"] == "HUB-V2-006"
    assert "continue_next_stage" in contract["codex_prompt_generator"]["supported_prompt_types"]
    assert contract["useful_signals_engine"]["current_stage"] == "HUB-V2-007"
    assert contract["connector_readiness_simulator"]["current_stage"] == "HUB-V2-008"
    assert contract["local_workflow_simulation"]["current_stage"] == "HUB-V2-009"
    assert contract["demo_workflow_report_export"]["current_stage"] == "HUB-V2-010"
    assert contract["demo_workflow_report_export"]["formats"] == ["markdown", "json", "csv"]
    assert contract["demo_workflow_report_export"]["output_dir"] == "outputs/public_reports"
    assert contract["showcase_screenshot_refresh"]["current_stage"] == "HUB-V2-011"
    assert contract["showcase_screenshot_refresh"]["canonical_screenshot_count"] == 10
    assert contract["public_release_check"]["current_stage"] == "HUB-V2-012"
    assert contract["public_release_check"]["readiness_report"] == "docs/V2_RELEASE_READINESS_REPORT.md"
    assert contract["bilingual_ui"]["current_stage"] == "HUB-V2-024"
    assert contract["bilingual_ui"]["default_language"] == "zh"
    assert contract["bilingual_ui"]["translation_policy"] == "local_dictionary_only_no_external_translation_api"
    assert contract["bilingual_ui"]["stage_status_helper"] == "agent_hub/stage_status.py"
    assert "agent_display_name" in contract["bilingual_ui"]["dynamic_display_translation"]
    assert "risk_warning" in contract["useful_signal_categories"]
    assert "needs_action" in contract["useful_signal_status_enum"]
    assert "blocked_until_approved" in contract["connector_readiness_status_enum"]
    assert "workflow_simulation" in contract["useful_signal_source_types"]
    assert "blocked" in contract["approval_status_enum"]
    assert "dry_run_only" in contract["allowed_execution_mode_enum"]


def test_v2_collections_are_demo_safe():
    manifests = build_agent_manifests(
        [_demo_agent()],
        [{"agent_name": "DemoAgent", "health_status": "Showcase Ready"}],
        [{"agent_name": "DemoAgent", "priority": "None", "recommended_action": "No immediate action"}],
    )
    workflows = build_workflow_catalog(manifests)
    signals = build_useful_signals(
        {"total_agents": 1},
        [{"agent_name": "DemoAgent", "health_status": "Showcase Ready"}],
        {"high_priority": 0, "medium_priority": 0},
        manifests,
    )
    action_items = build_action_center_items(
        manifests,
        [{"agent_name": "DemoAgent", "priority": "None"}],
    )
    connectors = build_connector_overview(manifests)
    plugin_stages = build_future_plugin_interface()

    assert workflows[0]["workflow_id"] == "portfolio_review"
    assert signals[0]["signal"] == "Available tools"
    assert action_items[0]["execution_policy"] == "display_only"
    assert any(item["connector_id"] == "github_showcase" for item in connectors)
    assert plugin_stages[-1]["current_status"] == "not_enabled_in_hub_v2_009"
