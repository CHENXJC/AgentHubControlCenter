from __future__ import annotations

from agent_hub.action_schema import ACTION_SCHEMA_FIELDS, normalize_action
from agent_hub.approval_gate_schema import (
    ALLOWED_EXECUTION_MODES,
    APPROVAL_GATE_EXECUTION_POLICY,
    APPROVAL_GATE_FIELDS,
    APPROVAL_STATUSES,
)
from agent_hub.codex_prompt_generator import PROMPT_TYPES, RESERVED_PROMPT_TYPES
from agent_hub.connector_readiness_schema import (
    CONNECTOR_EXECUTION_POLICY,
    CONNECTOR_READINESS_FIELDS,
    DATA_ACCESS_LEVELS,
    READINESS_STATUSES,
)
from agent_hub.report_export_schema import (
    REPORT_EXPORT_POLICY,
    REPORT_EXPORT_SCHEMA_VERSION,
    REPORT_FORMATS,
    REPORT_OUTPUT_DIR,
    REPORT_SCHEMA_FIELDS,
    REPORT_SECTION_IDS,
)
from agent_hub.useful_signal_engine import HIGH_VALUE_THRESHOLD, SCORE_WEIGHTS, WATCHLIST_THRESHOLD
from agent_hub.useful_signal_schema import (
    DISPLAY_ONLY_EXECUTION_POLICY,
    SIGNAL_CATEGORIES,
    SIGNAL_STATUSES,
    SOURCE_TYPES,
    USEFUL_SIGNAL_FIELDS,
)
from agent_hub.workflow_simulation_schema import (
    WORKFLOW_EXECUTION_POLICY,
    WORKFLOW_SIMULATION_FIELDS,
    WORKFLOW_STATUSES,
    WORKFLOW_TYPES,
)


STANDARD_AGENT_FIELDS = [
    "agent_id",
    "agent_name",
    "category",
    "description",
    "project_path",
    "status",
    "inputs",
    "outputs",
    "actions",
    "connectors",
    "demo_mode",
    "safe_mode",
]


OPTIONAL_AGENT_FIELDS = [
    "version",
    "action_schema_version",
    "last_run",
    "next_recommended_action",
    "github_repo",
    "dashboard_url",
    "tags",
    "owner",
    "public_showcase_status",
    "pin_status",
]


AGENTHUB_CURRENT_CHECKPOINT = "HUB-V2-022-BILINGUAL-UI-TOGGLE-AND-STAGE-SYNC-CHECK-COMPLETE"


CATEGORY_IO_DEFAULTS = {
    "Media Intelligence": {
        "inputs": ["video_file", "image_file", "optional_prompt"],
        "outputs": ["transcript", "ocr_text", "structured_notes", "report"],
    },
    "content_intelligence": {
        "inputs": ["video_file", "image_file", "audio_file", "ocr_language", "optional_prompt"],
        "outputs": ["transcript", "ocr_text", "structured_notes", "word_report", "pdf_report"],
    },
    "Finance Automation": {
        "inputs": ["watchlist", "market_region", "schedule_config"],
        "outputs": ["market_brief", "risk_notes", "dashboard"],
    },
    "market_intelligence": {
        "inputs": ["watchlist", "market_region", "schedule_config", "risk_rules"],
        "outputs": ["market_brief", "risk_notes", "dashboard", "watchlist_summary"],
    },
    "Quant Research": {
        "inputs": ["ticker", "date_range", "strategy_config"],
        "outputs": ["backtest_result", "risk_metrics", "charts"],
    },
    "quant_research": {
        "inputs": ["ticker", "date_range", "strategy_config", "indicator_settings"],
        "outputs": ["backtest_result", "risk_metrics", "charts", "research_summary"],
    },
    "Business Discovery": {
        "inputs": ["raw_social_posts", "pain_point_rules", "scoring_weights"],
        "outputs": ["pain_points", "opportunity_scores", "export_report"],
    },
    "opportunity_discovery": {
        "inputs": ["raw_social_posts", "pain_point_rules", "scoring_weights", "target_user_context"],
        "outputs": ["pain_points", "opportunity_scores", "top_opportunities", "export_report"],
    },
    "Career Automation": {
        "inputs": ["profile_notes", "job_description", "application_goal"],
        "outputs": ["career_plan", "job_match_notes", "application_tasks"],
    },
    "career_operations": {
        "inputs": ["profile_notes", "job_description", "resume_draft", "application_goal"],
        "outputs": ["career_plan", "job_match_notes", "application_tasks"],
    },
    "News Intelligence": {
        "inputs": ["news_text", "source_notes", "signal_rules"],
        "outputs": ["signal_summary", "risk_flags", "structured_brief"],
    },
    "news_intelligence": {
        "inputs": ["news_text", "source_notes", "topic_rules", "signal_rules"],
        "outputs": ["signal_summary", "risk_flags", "structured_brief", "narrative_gap_notes"],
    },
    "Business Operations": {
        "inputs": ["operations_notes", "kpi_table", "workflow_context"],
        "outputs": ["ops_summary", "kpi_dashboard", "improvement_plan"],
    },
    "Workflow Automation": {
        "inputs": ["workflow_steps", "bottleneck_notes", "automation_rules"],
        "outputs": ["automation_score", "roi_estimate", "workflow_report"],
    },
    "sme_operations": {
        "inputs": ["workflow_steps", "operations_notes", "kpi_table", "business_context"],
        "outputs": ["workflow_report", "ops_summary", "automation_score", "improvement_plan"],
    },
    "idea_validation": {
        "inputs": ["idea_brief", "target_user", "problem_statement", "scoring_context"],
        "outputs": ["opportunity_score", "dimension_breakdown", "business_analysis", "validation_plan"],
    },
    "Knowledge Base": {
        "inputs": ["documents", "notes", "query"],
        "outputs": ["knowledge_summary", "retrieval_result", "source_map"],
    },
    "knowledge_management": {
        "inputs": ["documents", "notes", "query", "tags"],
        "outputs": ["knowledge_summary", "retrieval_plan", "source_map", "dashboard_view"],
    },
    "AgentOps / PortfolioOps": {
        "inputs": ["agent_registry", "project_status", "local_health_checks"],
        "outputs": ["command_overview", "action_center", "portfolio_report"],
    },
}


PLANNED_CONNECTORS = [
    "gmail",
    "google_sheets",
    "google_drive",
    "notion",
    "airtable",
    "telegram",
    "github",
    "n8n",
    "make",
    "zapier",
]


CATEGORY_LABELS = {
    "AgentOps / PortfolioOps": "AgentOps / PortfolioOps",
    "content_intelligence": "Content Intelligence",
    "market_intelligence": "Market Intelligence",
    "quant_research": "Quant Research",
    "opportunity_discovery": "Opportunity Discovery",
    "sme_operations": "SME Operations",
    "career_operations": "Career Operations",
    "news_intelligence": "News Intelligence",
    "knowledge_management": "Knowledge Management",
    "idea_validation": "Idea Validation",
}


def format_category_label(category: str) -> str:
    """Return a readable product label for manifest categories."""
    category = category.strip()
    return CATEGORY_LABELS.get(category, category.replace("_", " ").title())


def _category_defaults(category: str) -> dict:
    """Return input/output defaults for a portfolio category."""
    return CATEGORY_IO_DEFAULTS.get(
        category,
        {
            "inputs": ["local_file", "manual_notes", "configuration"],
            "outputs": ["dashboard", "summary", "export"],
        },
    )


def _build_connector_list(agent: dict) -> list[dict]:
    """Build connector declarations without enabling live external access."""
    github_url = agent.get("github_url", "").strip()
    tech_stack = agent.get("tech_stack", "").lower()
    connectors = [
        {
            "connector_id": "local_filesystem",
            "label": "Local Filesystem",
            "status": "available_local",
            "mode": "read_only_health_check",
            "safe_mode": True,
        },
        {
            "connector_id": "github_showcase",
            "label": "GitHub Showcase Link",
            "status": "available_link" if github_url else "not_configured",
            "mode": "display_only",
            "safe_mode": True,
        },
        {
            "connector_id": "streamlit_local_app",
            "label": "Streamlit Local App",
            "status": "manual_launch",
            "mode": "display_command_only",
            "safe_mode": True,
        },
    ]

    if "telegram" in tech_stack:
        connectors.append(
            {
                "connector_id": "telegram",
                "label": "Telegram",
                "status": "demo_disabled",
                "mode": "not_connected",
                "safe_mode": True,
            }
        )

    for connector_id in PLANNED_CONNECTORS:
        if connector_id not in {item["connector_id"] for item in connectors}:
            connectors.append(
                {
                    "connector_id": connector_id,
                    "label": connector_id.replace("_", " ").title(),
                    "status": "planned",
                    "mode": "not_connected",
                    "safe_mode": True,
                }
            )

    return connectors


def _build_action_list(agent: dict) -> list[dict]:
    """Build display-only local actions for the action center."""
    project_path = agent.get("local_path", "").strip()
    agent_id = agent.get("agent_id", "").strip()
    agent_name = agent.get("agent_name", "").strip()
    defaults = [
        {
            "action_id": "manual_run_dashboard",
            "label": "Manual run dashboard",
        },
        {
            "action_id": "open_project_folder",
            "label": "Open project folder",
            "enabled": bool(project_path),
        },
        {
            "action_id": "view_project_status",
            "label": "View project status",
        },
        {
            "action_id": "view_agent_manifest",
            "label": "View agent manifest",
        },
    ]
    if agent.get("github_url", "").strip():
        defaults.append(
            {
                "action_id": "open_github_showcase",
                "label": "Open GitHub showcase",
            }
        )
    return [
        normalize_action(
            action,
            agent_id=agent_id,
            agent_name=agent_name,
            project_path=project_path,
        )
        for action in defaults
    ]


def _string_list(values: object) -> list[str]:
    """Return non-empty string values from a manifest list."""
    if not isinstance(values, list):
        return []
    return [value.strip() for value in values if isinstance(value, str) and value.strip()]


def _normalize_declared_actions(
    actions: object,
    *,
    agent_id: str = "",
    agent_name: str = "",
    project_path: str = "",
) -> list[dict]:
    """Normalize manifest-declared actions for the Action Center."""
    if not isinstance(actions, list):
        return []

    normalized = []
    for action in actions:
        if not isinstance(action, dict):
            continue
        if not str(action.get("action_id", "")).strip() and not str(action.get("label", "")).strip():
            continue
        normalized.append(
            normalize_action(
                action,
                agent_id=agent_id,
                agent_name=agent_name,
                project_path=project_path,
            )
        )
    return normalized


def _normalize_declared_connectors(connectors: object) -> list[dict]:
    """Normalize manifest-declared connectors for connector overview cards."""
    if not isinstance(connectors, list):
        return []

    normalized = []
    for connector in connectors:
        if not isinstance(connector, dict):
            continue
        connector_id = str(connector.get("connector_id", "")).strip()
        label = str(connector.get("label", "")).strip()
        if not connector_id and not label:
            continue
        normalized_connector = dict(connector)
        normalized_connector["connector_id"] = connector_id or label.lower().replace(" ", "_")
        normalized_connector["label"] = label or connector_id.replace("_", " ").title()
        normalized_connector.setdefault("status", "planned")
        normalized_connector.setdefault("mode", "not_connected")
        normalized_connector.setdefault("safe_mode", True)
        normalized.append(normalized_connector)
    return normalized


def _health_by_name(health_results: list[dict]) -> dict:
    """Index health rows by agent name."""
    return {row.get("agent_name", ""): row for row in health_results}


def _actions_by_name(action_plan: list[dict]) -> dict:
    """Index action rows by agent name."""
    return {row.get("agent_name", ""): row for row in action_plan}


def build_agent_manifest(
    agent: dict,
    health_result: dict | None = None,
    action_item: dict | None = None,
) -> dict:
    """Build the V2 standard manifest for one registry agent."""
    category = agent.get("category", "").strip()
    defaults = _category_defaults(category)
    next_action = agent.get("next_action", "").strip()
    recommended_action = (action_item or {}).get("recommended_action", "").strip()
    declared_inputs = _string_list(agent.get("manifest_inputs"))
    declared_outputs = _string_list(agent.get("manifest_outputs"))
    declared_connectors = _normalize_declared_connectors(agent.get("manifest_connectors"))
    demo_mode = agent.get("demo_mode")
    safe_mode = agent.get("safe_mode")
    declared_actions = _normalize_declared_actions(
        agent.get("manifest_actions"),
        agent_id=agent.get("agent_id", "").strip(),
        agent_name=agent.get("agent_name", "").strip(),
        project_path=agent.get("local_path", "").strip(),
    )

    return {
        "agent_id": agent.get("agent_id", "").strip(),
        "agent_name": agent.get("agent_name", "").strip(),
        "category": category,
        "category_label": format_category_label(category),
        "description": agent.get("primary_capability", "").strip(),
        "project_path": agent.get("local_path", "").strip(),
        "github_url": agent.get("github_url", "").strip(),
        "github_repo": agent.get("github_url", "").strip(),
        "project_type": agent.get("project_type", "").strip(),
        "stage": agent.get("stage", "").strip(),
        "action_schema_version": agent.get("action_schema_version", "").strip(),
        "source": agent.get("source", "").strip() or "static_registry",
        "source_note": agent.get("source_note", "").strip(),
        "manifest_path": agent.get("manifest_path", "").strip(),
        "showcase_status": agent.get("showcase_status", "").strip(),
        "pin_status": agent.get("pin_status", "").strip(),
        "status": agent.get("status", "").strip(),
        "health_status": (health_result or {}).get("health_status", "Not checked"),
        "inputs": declared_inputs or defaults["inputs"],
        "outputs": declared_outputs or defaults["outputs"],
        "actions": declared_actions or _build_action_list(agent),
        "connectors": declared_connectors or _build_connector_list(agent),
        "demo_mode": demo_mode if isinstance(demo_mode, bool) else True,
        "safe_mode": safe_mode if isinstance(safe_mode, bool) else True,
        "last_run": agent.get("last_run", "").strip() or "Not tracked yet",
        "next_recommended_action": recommended_action or next_action or "Review next action",
    }


def build_agent_manifests(
    agents: list[dict],
    health_results: list[dict],
    action_plan: list[dict],
) -> list[dict]:
    """Build V2 manifests for all registered agents."""
    health_lookup = _health_by_name(health_results)
    action_lookup = _actions_by_name(action_plan)
    return [
        build_agent_manifest(
            agent,
            health_result=health_lookup.get(agent.get("agent_name", "")),
            action_item=action_lookup.get(agent.get("agent_name", "")),
        )
        for agent in agents
    ]


def build_agent_contract() -> dict:
    """Return the V2 interface contract for future Agent onboarding."""
    return {
        "contract_version": AGENTHUB_CURRENT_CHECKPOINT,
        "purpose": "Standard local-first declaration for AgentHubControlCenter tools, actions, Codex prompts, useful signals, connector readiness simulations, local workflow simulations, approval gates, public-safe demo workflow report exports, showcase screenshots, public release readiness metadata, and bilingual UI stage sync.",
        "required_fields": STANDARD_AGENT_FIELDS,
        "optional_fields": OPTIONAL_AGENT_FIELDS,
        "action_schema_fields": ACTION_SCHEMA_FIELDS,
        "useful_signal_schema_fields": USEFUL_SIGNAL_FIELDS,
        "useful_signal_categories": sorted(SIGNAL_CATEGORIES),
        "useful_signal_status_enum": sorted(SIGNAL_STATUSES),
        "useful_signal_source_types": sorted(SOURCE_TYPES),
        "connector_readiness_schema_fields": CONNECTOR_READINESS_FIELDS,
        "connector_readiness_status_enum": sorted(READINESS_STATUSES),
        "connector_data_access_level_enum": sorted(DATA_ACCESS_LEVELS),
        "workflow_simulation_schema_fields": WORKFLOW_SIMULATION_FIELDS,
        "workflow_type_enum": sorted(WORKFLOW_TYPES),
        "workflow_status_enum": sorted(WORKFLOW_STATUSES),
        "approval_gate_schema_fields": APPROVAL_GATE_FIELDS,
        "approval_status_enum": sorted(APPROVAL_STATUSES),
        "allowed_execution_mode_enum": sorted(ALLOWED_EXECUTION_MODES),
        "report_export_schema_fields": REPORT_SCHEMA_FIELDS,
        "report_export_format_enum": list(REPORT_FORMATS),
        "report_export_section_enum": list(REPORT_SECTION_IDS),
        "execution_policy": {
            "current_stage": "bilingual_ui_toggle_stage_sync_check",
            "default_mode": "demo_safe",
            "external_api_calls": "disabled_by_default",
            "secrets": "must_not_be_read_or_printed",
            "actions": "metadata_instruction_template_only",
            "command_template": "display_text_only_never_auto_execute",
            "useful_signals": DISPLAY_ONLY_EXECUTION_POLICY,
            "connector_readiness": CONNECTOR_EXECUTION_POLICY,
            "workflow_simulation": WORKFLOW_EXECUTION_POLICY,
            "approval_gates": APPROVAL_GATE_EXECUTION_POLICY,
            "report_export": REPORT_EXPORT_POLICY,
        },
        "connector_policy": {
            "current_stage": "bilingual_ui_toggle_stage_sync_check",
            "live_connectors": "not_enabled_in_hub_v2_022",
            "planned_connectors": PLANNED_CONNECTORS,
        },
        "codex_prompt_generator": {
            "current_stage": "HUB-V2-006",
            "supported_prompt_types": list(PROMPT_TYPES),
            "reserved_prompt_types": list(RESERVED_PROMPT_TYPES),
            "execution_policy": "generated_prompt_text_only_no_auto_send_no_action_execution",
        },
        "useful_signals_engine": {
            "current_stage": "HUB-V2-007",
            "data_sources": [
                "agent_manifest.json",
                "PROJECT_STATUS.md",
                "README.md",
                "manual_demo_data",
                "local_json",
                "local_csv",
                "action_registry",
            ],
            "scoring_weights": SCORE_WEIGHTS,
            "high_value_threshold": HIGH_VALUE_THRESHOLD,
            "watchlist_threshold": WATCHLIST_THRESHOLD,
            "recommendation_policy": "text_only_no_action_execution_no_connector_call",
            "execution_policy": DISPLAY_ONLY_EXECUTION_POLICY,
        },
        "connector_readiness_simulator": {
            "current_stage": "HUB-V2-008",
            "execution_policy": CONNECTOR_EXECUTION_POLICY,
            "live_connection_status": "not_connected",
            "data_policy": "demo_metadata_only_no_oauth_no_provider_api_call",
            "recommendation_policy": "readiness_simulation_and_useful_signal_generation_only",
        },
        "local_workflow_simulation": {
            "current_stage": "HUB-V2-009",
            "execution_policy": WORKFLOW_EXECUTION_POLICY,
            "approval_gate_policy": APPROVAL_GATE_EXECUTION_POLICY,
            "data_policy": "local_demo_metadata_only_no_live_connector_no_credentials",
            "recommendation_policy": "workflow_simulation_and_useful_signal_generation_only",
        },
        "demo_workflow_report_export": {
            "current_stage": REPORT_EXPORT_SCHEMA_VERSION,
            "formats": list(REPORT_FORMATS),
            "output_dir": REPORT_OUTPUT_DIR,
            "execution_policy": REPORT_EXPORT_POLICY,
            "data_policy": "public_safe_demo_metadata_summary_recommendations_only",
            "write_policy": "local_files_only_outputs_public_reports",
        },
        "showcase_screenshot_refresh": {
            "current_stage": "HUB-V2-011",
            "screenshot_dir": "docs/images",
            "canonical_screenshot_count": 10,
            "sample_report_summary": "docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md",
            "execution_policy": "public_safe_showcase_metadata_only_no_execution",
            "data_policy": "demo_metadata_and_public_reports_only_no_private_outputs",
        },
        "public_release_check": {
            "current_stage": "HUB-V2-012",
            "release_checklist": "docs/PUBLIC_RELEASE_CHECKLIST.md",
            "readiness_report": "docs/V2_RELEASE_READINESS_REPORT.md",
            "execution_policy": "public_safe_release_check_metadata_only_no_commit_no_push",
            "data_policy": "readme_docs_manifest_contract_screenshot_inventory_public_reports_only",
        },
        "bilingual_ui": {
            "current_stage": "HUB-V2-022",
            "default_language": "zh",
            "supported_languages": ["zh", "en"],
            "translation_policy": "local_dictionary_only_no_external_translation_api",
            "stage_status_helper": "agent_hub/stage_status.py",
            "stage_source_policy": "PROJECT_STATUS.md_first_agent_manifest_fallback",
            "execution_policy": "ui_display_only_no_action_execution",
        },
    }


def build_workflow_catalog(manifests: list[dict]) -> list[dict]:
    """Build lightweight workflow groups for the V2 command overview."""
    categories = sorted({item.get("category", "") for item in manifests if item.get("category")})
    showcase_ready = [
        item.get("agent_name", "")
        for item in manifests
        if item.get("health_status") == "Showcase Ready"
    ]
    return [
        {
            "workflow_id": "portfolio_review",
            "workflow_name": "Portfolio Review",
            "description": "Review all registered AI Agents and Skills from one command center.",
            "agents": [item.get("agent_name", "") for item in manifests],
            "status": "available_demo",
            "next_step": "Use filters and Action Center to choose the next local task.",
        },
        {
            "workflow_id": "showcase_readiness",
            "workflow_name": "GitHub Showcase Readiness",
            "description": "Check which tools are public-safe, documented, and screenshot-ready.",
            "agents": showcase_ready,
            "status": "available_demo",
            "next_step": "Keep completed and pinned projects paused unless a new stage is requested.",
        },
        {
            "workflow_id": "agent_integration",
            "workflow_name": "Future Agent Integration",
            "description": "Prepare future projects to declare inputs, outputs, actions, connectors, and safe mode.",
            "agents": categories,
            "status": "interface_ready",
            "next_step": "Onboard new tools through agent_manifest.json and the interface standard.",
        },
    ]


def build_useful_signals(
    registry_summary: dict,
    health_results: list[dict],
    action_summary: dict,
    manifests: list[dict],
) -> list[dict]:
    """Build short signal cards for the Useful Signals page."""
    connector_ready = sum(
        1
        for manifest in manifests
        if any(item.get("status") == "available_link" for item in manifest.get("connectors", []))
    )
    showcase_ready = sum(1 for row in health_results if row.get("health_status") == "Showcase Ready")
    attention_needed = action_summary.get("high_priority", 0) + action_summary.get("medium_priority", 0)

    return [
        {
            "signal": "Available tools",
            "value": registry_summary.get("total_agents", 0),
            "meaning": "AI Agents and Skills registered in the local command center.",
        },
        {
            "signal": "Showcase-ready tools",
            "value": showcase_ready,
            "meaning": "Projects with strong local file readiness for public showcase.",
        },
        {
            "signal": "Attention needed",
            "value": attention_needed,
            "meaning": "High or medium priority items in the Action Center.",
        },
        {
            "signal": "Connector-ready links",
            "value": connector_ready,
            "meaning": "Tools with GitHub showcase links available for user-click navigation.",
        },
        {
            "signal": "Safe-mode tools",
            "value": sum(1 for manifest in manifests if manifest.get("safe_mode") is True),
            "meaning": "Tools declared as demo/local-first safe mode in the V2 manifest.",
        },
    ]


def build_action_center_items(manifests: list[dict], action_plan: list[dict]) -> list[dict]:
    """Combine manifests and priorities into Action Center rows."""
    action_lookup = _actions_by_name(action_plan)
    items = []
    for manifest in manifests:
        plan_item = action_lookup.get(manifest.get("agent_name", ""), {})
        available_actions = [
            action.get("label", "")
            for action in manifest.get("actions", [])
            if action.get("enabled")
        ]
        items.append(
            {
                "agent_name": manifest.get("agent_name", ""),
                "priority": plan_item.get("priority", "None"),
                "status": manifest.get("status", ""),
                "health_status": manifest.get("health_status", ""),
                "next_recommended_action": manifest.get("next_recommended_action", ""),
                "available_actions": available_actions,
                "execution_policy": "display_only",
            }
        )
    return items


def build_connector_overview(manifests: list[dict]) -> list[dict]:
    """Summarize connector status without activating live integrations."""
    connector_counts: dict[str, dict] = {}
    for manifest in manifests:
        for connector in manifest.get("connectors", []):
            connector_id = connector.get("connector_id", "")
            entry = connector_counts.setdefault(
                connector_id,
                {
                    "connector_id": connector_id,
                    "label": connector.get("label", connector_id),
                    "status": connector.get("status", ""),
                    "mode": connector.get("mode", ""),
                    "agent_count": 0,
                    "safe_mode": connector.get("safe_mode", True),
                },
            )
            entry["agent_count"] += 1
            if connector.get("status") in {"available_local", "available_link", "manual_launch"}:
                entry["status"] = connector.get("status")
                entry["mode"] = connector.get("mode", entry["mode"])

    return sorted(connector_counts.values(), key=lambda item: item["connector_id"])


def build_future_plugin_interface() -> list[dict]:
    """Describe future plugin stages for docs and UI."""
    return [
        {
            "stage": "Declare",
            "description": "Each Agent ships a manifest with identity, IO, actions, connectors, and safe mode.",
            "current_status": "ready_as_standard",
        },
        {
            "stage": "Validate",
            "description": "AgentHub validates required fields and public-safe metadata before display.",
            "current_status": "local_demo_ready",
        },
        {
            "stage": "Preview",
            "description": "Actions and connector commands are shown as schema-backed cards before execution.",
            "current_status": "implemented_as_action_schema",
        },
        {
            "stage": "Execute",
            "description": "Future explicit opt-in stage for controlled local workflow execution.",
            "current_status": "not_enabled_in_hub_v2_009",
        },
    ]
