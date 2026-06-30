from pathlib import Path
import re

import pandas as pd
import streamlit as st

from agent_hub.agent_interface import (
    build_action_center_items,
    build_agent_contract,
    build_agent_manifests,
    build_connector_overview,
    build_future_plugin_interface,
    build_workflow_catalog,
    format_category_label,
)
from agent_hub.action_registry import (
    build_action_registry,
    build_action_registry_summary,
    find_action_policy_violations,
    get_actions_for_agent,
    get_codex_prompt_actions,
    group_actions_by_agent,
)
from agent_hub.agent_onboarding import build_agent_onboarding
from agent_hub.approval_gate_engine import (
    build_approval_gate_registry,
    build_approval_gate_summary,
    find_approval_gate_policy_violations,
)
from agent_hub.codex_prompt_generator import (
    ALL_PROMPT_TYPES,
    PROMPT_TYPE_DETAILS,
    RESERVED_PROMPT_TYPE_DETAILS,
    build_codex_prompt_package,
)
from agent_hub.command_builder import (
    build_open_github_command,
    build_project_command_pack,
)
from agent_hub.connector_readiness_engine import (
    build_connector_readiness_registry,
    build_connector_readiness_summary,
    connector_readiness_to_useful_signals,
    filter_connector_readiness,
    find_connector_policy_violations,
    get_connector_risk_options,
    get_connector_status_options,
)
from agent_hub.demo_report_builder import build_demo_report_package, build_report_previews
from agent_hub.demo_report_exporter import get_public_reports_dir
from agent_hub.external_agent_summary import (
    build_agent_summary_metrics,
    build_external_summary_index,
    build_summary_display_rows,
)
from agent_hub.health_checker import check_all_agents_health
from agent_hub.next_action_planner import build_next_action_plan, summarize_next_actions
from agent_hub.portfolio_matrix import (
    build_capability_summary,
    build_category_matrix,
    build_portfolio_positioning,
    build_priority_summary,
    build_project_matrix_view,
)
from agent_hub.registry_loader import (
    get_registry_summary,
    load_agent_registry,
    validate_registry,
)
from agent_hub.report_builder import (
    build_command_center_summary,
    build_portfolio_markdown_report,
    build_showcase_asset_checklist,
)
from agent_hub.report_exporter import build_report_file_name, save_markdown_report
from agent_hub.stage_status import get_stage_snapshot
from agent_hub.ui_i18n import (
    LANGUAGE_LABELS,
    display_text,
    get_language,
    set_language,
    t,
    translate_action_label,
    translate_agent_description,
    translate_agent_display_name,
    translate_category,
    translate_column_label,
    translate_connector,
    translate_filter_option,
    translate_list_values,
    translate_next_step,
    translate_status,
)
from agent_hub.ui_helpers import (
    build_metric_display_value,
    safe_display,
    safe_list_join,
    truncate_text,
)
from agent_hub.useful_signal_engine import (
    build_signal_summary,
    build_useful_signal_registry,
    filter_useful_signals,
    get_signal_category_options,
    get_signal_status_options,
    group_signal_buckets,
)
from agent_hub.useful_signal_schema import DISPLAY_ONLY_EXECUTION_POLICY
from agent_hub.workflow_simulation_engine import (
    build_workflow_simulation_registry,
    build_workflow_simulation_summary,
    filter_workflow_simulations,
    find_workflow_policy_violations,
    get_workflow_status_options,
    get_workflow_type_options,
    workflow_simulation_to_useful_signals,
)
from agent_hub.report_export_schema import REPORT_FORMATS, REPORT_SECTION_OPTIONS


BASE_DIR = Path(__file__).resolve().parent
AI_PROJECTS_ROOT = BASE_DIR.parent
REGISTRY_PATH = BASE_DIR / "data" / "agent_registry.csv"
OUTPUTS_DIR = BASE_DIR / "outputs"
STAGE_SNAPSHOT = get_stage_snapshot(BASE_DIR)
PRODUCT_STATUS = STAGE_SNAPSHOT["product_status"]
LATEST_CHECKPOINT = STAGE_SNAPSHOT["latest_checkpoint"]
MANIFEST_VERSION = STAGE_SNAPSHOT["manifest_version"]
PRIORITY_SORT = {"High": 0, "Medium": 1, "Low": 2, "None": 3}


st.set_page_config(
    page_title="Personal AI Command Center",
    page_icon="\U0001f9e9",
    layout="wide",
)


def inject_global_styles() -> None:
    """Inject lightweight dashboard CSS for a screenshot-friendly product UI."""
    st.markdown(
        """
        <style>
        .stApp {
            background: #f6f7f9;
            color: #18212f;
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e3e7ee;
            border-radius: 8px;
            padding: 16px 18px;
            box-shadow: 0 8px 24px rgba(22, 31, 46, 0.06);
        }
        .hero-card {
            background: linear-gradient(135deg, #ffffff 0%, #eef6ff 100%);
            border: 1px solid #dfe7f2;
            border-radius: 8px;
            padding: 28px 30px;
            box-shadow: 0 14px 34px rgba(22, 31, 46, 0.08);
            margin: 4px 0 18px 0;
        }
        .hero-title {
            font-size: 42px;
            font-weight: 760;
            color: #121a26;
            margin-bottom: 8px;
        }
        .hero-subtitle {
            font-size: 19px;
            font-weight: 620;
            color: #2d394b;
            margin-bottom: 10px;
        }
        .hero-copy {
            font-size: 15px;
            color: #566274;
            max-width: 940px;
            line-height: 1.55;
        }
        .badge {
            display: inline-block;
            margin: 14px 8px 0 0;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid #d7deea;
            background: #ffffff;
            color: #28364a;
            font-size: 13px;
            font-weight: 650;
        }
        .health-badge {
            display: inline-block;
            padding: 5px 9px;
            border-radius: 999px;
            background: #eef8f3;
            border: 1px solid #bfe6d0;
            color: #1f6b43;
            font-size: 12px;
            font-weight: 700;
        }
        .priority-badge {
            display: inline-block;
            padding: 5px 9px;
            border-radius: 999px;
            background: #fff4e5;
            border: 1px solid #ffd9a3;
            color: #7a4a00;
            font-size: 12px;
            font-weight: 700;
        }
        .section-card {
            background: #ffffff;
            border: 1px solid #e2e7ef;
            border-radius: 8px;
            padding: 18px 20px;
            box-shadow: 0 8px 22px rgba(22, 31, 46, 0.05);
            margin-bottom: 16px;
        }
        .section-card h3 {
            font-size: 18px;
            margin: 0 0 8px 0;
        }
        .section-card p {
            color: #566274;
            line-height: 1.55;
            margin: 0;
        }
        .mini-card {
            background: #ffffff;
            border: 1px solid #e4e9f1;
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 6px 18px rgba(22, 31, 46, 0.04);
            min-height: 116px;
            margin-bottom: 12px;
        }
        .mini-card-title {
            font-weight: 720;
            color: #172033;
            margin-bottom: 8px;
        }
        .mini-card-meta {
            color: #596579;
            font-size: 13px;
            line-height: 1.55;
        }
        .command-card {
            background: #101722;
            border: 1px solid #253244;
            border-radius: 8px;
            padding: 12px 14px;
            color: #e8edf6;
            font-family: Consolas, Monaco, monospace;
            font-size: 13px;
            overflow-wrap: anywhere;
            margin-bottom: 10px;
        }
        .disclaimer-box {
            background: #fff8e5;
            border: 1px solid #f2d891;
            border-radius: 8px;
            padding: 14px 16px;
            color: #5d4a12;
            margin: 14px 0;
        }
        .note-box {
            background: #eef8f3;
            border: 1px solid #cae9d8;
            border-radius: 8px;
            padding: 14px 16px;
            color: #1f5e3c;
            margin-bottom: 12px;
        }
        .priority-high {
            border-left: 4px solid #d92d20;
        }
        .priority-medium {
            border-left: 4px solid #dc8a00;
        }
        .priority-low {
            border-left: 4px solid #276ef1;
        }
        .priority-none {
            border-left: 4px solid #1f9d55;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def as_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert rows to a DataFrame for Streamlit display."""
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def display_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert list and dict fields into readable DataFrame cell text."""
    df = as_dataframe(rows)
    if df.empty:
        return df
    for column in df.columns:
        df[column] = df[column].apply(format_cell)
    return df


def format_cell(value: object) -> object:
    """Format nested values for compact Streamlit tables."""
    if isinstance(value, list):
        return safe_list_join([str(item) for item in value])
    if isinstance(value, dict):
        parts = []
        for key, values in value.items():
            if isinstance(values, list):
                parts.append(f"{key}: {safe_list_join([str(item) for item in values])}")
            else:
                parts.append(f"{key}: {values}")
        return "; ".join(parts)
    return value


COLUMN_VALUE_DOMAINS = {
    "agent_name": "agent",
    "source_agent": "agent",
    "target_agent": "agent",
    "source": "source",
    "source_type": "source",
    "category": "category",
    "category_label": "category",
    "status": "status",
    "showcase_status": "showcase",
    "pin_status": "pin",
    "health_status": "health",
    "priority": "priority",
    "next_action": "next_step",
    "next_recommended_action": "next_step",
    "recommended_action": "next_step",
    "suggested_fix": "next_step",
    "recommended_fix": "next_step",
    "label": "action_label",
    "action_type": "generic",
    "execution_mode": "generic",
    "risk_level": "generic",
    "requires_approval": "generic",
    "approval_required": "generic",
    "approval_status": "status",
    "connector_required": "connector",
    "connector_name": "connector",
    "provider": "connector",
    "readiness_status": "status",
    "live_connection_status": "status",
    "data_access_level": "generic",
    "write_access": "generic",
    "demo_mode_available": "generic",
    "read_only_mode_available": "generic",
    "manifest_status": "status",
    "available_actions": "generic",
    "execution_policy": "generic",
    "workflow_status": "status",
    "allowed_execution_mode": "generic",
    "required_checks": "generic",
    "warnings": "generic",
    "validation_notes": "generic",
    "missing_required_fields": "generic",
    "missing_items": "generic",
    "title": "generic",
    "purpose": "generic",
    "reason": "generic",
    "related_issue": "generic",
}


def display_list(values, language: str, domain: str = "generic") -> str:
    """Translate and join list values for UI display."""
    translated = translate_list_values(list(values or []), language, domain=domain)
    return safe_list_join(translated)


def display_value(value, language: str, domain: str = "generic") -> str:
    """Translate one dynamic display value without mutating source data."""
    if isinstance(value, list):
        return display_list(value, language, domain=domain)
    if isinstance(value, tuple):
        return display_list(list(value), language, domain=domain)
    if isinstance(value, set):
        return display_list(sorted(value), language, domain=domain)
    return safe_display(display_text(value, language, domain=domain))


def display_agent_title(agent_name: str, language: str) -> str:
    """Return the localized Agent title while preserving repo names."""
    if language == "zh":
        return translate_agent_display_name(agent_name, language)
    return format_agent_card_title(agent_name)


def localize_dataframe(
    df: pd.DataFrame,
    language: str,
    domains: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Return a copy of a dataframe with localized display values and headers."""
    if df.empty:
        return df.copy()
    domains = domains or {}
    localized = df.copy()
    for column in localized.columns:
        domain = domains.get(column) or COLUMN_VALUE_DOMAINS.get(column, "generic")
        localized[column] = localized[column].map(
            lambda value, current_domain=domain: display_value(value, language, current_domain)
        )
    return localized.rename(columns=lambda column: translate_column_label(column, language))


def render_html_card(title: str, body: str, class_name: str = "section-card") -> None:
    """Render a small HTML card through Streamlit markdown."""
    st.markdown(
        f"""
        <div class="{class_name}">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(metrics: list[tuple[str, object]]) -> None:
    """Render metric cards in a responsive six-column row."""
    columns = st.columns(len(metrics))
    for index, (label, value) in enumerate(metrics):
        columns[index].metric(label, build_metric_display_value(value))


def render_external_agent_summary(summary_record: dict, title: str) -> None:
    """Render read-only summary metrics from an imported Agent output."""
    language = get_language()
    if not summary_record or not summary_record.get("available"):
        return

    summary_data = summary_record.get("data", {})
    metrics = build_agent_summary_metrics(summary_data)
    st.markdown(f"### {display_text(title, language)}")
    render_metric_cards(
        [
            (display_text("Total items processed", language), metrics["total_items_processed"]),
            (display_text("High-value signals", language), metrics["high_value_signals"]),
            (display_text("Medium-value items", language), metrics["medium_value_items"]),
            (display_text("Low/noise/review items", language), metrics["low_value_or_noise_items"]),
            (display_text("Recommended actions", language), metrics["recommended_actions_count"]),
            (display_text("Top route", language), metrics["top_route"]),
        ]
    )
    summary_left, summary_right = st.columns(2)
    with summary_left:
        render_html_card(
            display_text("Latest report path", language),
            safe_display(metrics["latest_report_path"]),
        )
    with summary_right:
        top_routes = summary_data.get("top_routes", {})
        render_html_card(
            display_text("Top routes", language),
            safe_display(", ".join(f"{route}: {count}" for route, count in top_routes.items()) if isinstance(top_routes, dict) else ""),
        )

    st.dataframe(
        localize_dataframe(display_dataframe(build_summary_display_rows(summary_data)), language),
        width="stretch",
        hide_index=True,
    )


def format_agent_card_title(agent_name: str) -> str:
    """Return a readable title for compact Agent cards."""
    value = safe_display(agent_name)
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", value)
    spaced = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", spaced)
    return spaced


def render_manifest_cards(manifests: list[dict], max_items: int | None = None) -> None:
    """Render compact cards for V2 agent manifests."""
    language = get_language()
    visible_manifests = manifests if max_items is None else manifests[:max_items]
    columns = st.columns(3)
    for index, manifest in enumerate(visible_manifests):
        actions = [
            translate_action_label(action.get("label", ""), language)
            for action in manifest.get("actions", [])
            if action.get("enabled")
        ]
        connectors = [
            translate_connector(connector.get("label", ""), language)
            for connector in manifest.get("connectors", [])
            if connector.get("status") in {"available_local", "available_link", "manual_launch"}
        ]
        source = manifest.get("source", "static_registry")
        source_label = (
            t("source_local_manifest", language)
            if source == "local_manifest"
            else t("source_demo_manifest", language)
            if source == "demo_manifest"
            else t("source_static_registry", language)
        )
        safety_label = t("demo_mode", language) if manifest.get("demo_mode") else t("manual_review_mode", language)
        safety_label += f" / {t('safe_mode', language)}" if manifest.get("safe_mode") else f" / {t('review_required', language)}"
        with columns[index % 3]:
            render_html_card(
                display_agent_title(manifest.get("agent_name", "Unknown Agent"), language),
                (
                    f"<strong>{translate_category(manifest.get('category_label') or format_category_label(manifest.get('category', '')), language)}</strong><br>"
                    f"<span class='badge'>{safe_display(source_label)}</span>"
                    f"<span class='badge'>{safe_display(safety_label)}</span><br>"
                    f"{truncate_text(translate_agent_description(manifest.get('description', ''), language), 140)}<br>"
                    f"<strong>{t('field_status', language)}:</strong> {translate_status(manifest.get('status'), language)} | "
                    f"{translate_status(manifest.get('health_status'), language)}<br>"
                    f"<strong>{t('field_can_do', language)}:</strong> {safe_list_join(actions)}<br>"
                    f"<strong>{t('field_connectors', language)}:</strong> {safe_list_join(connectors)}<br>"
                    f"<strong>{t('field_next', language)}:</strong> {truncate_text(translate_next_step(manifest.get('next_recommended_action', ''), language), 120)}"
                ),
                "mini-card",
            )


def render_workflow_cards(workflows: list[dict]) -> None:
    """Render V2 workflow cards."""
    language = get_language()
    columns = st.columns(3)
    for index, workflow in enumerate(workflows):
        with columns[index % 3]:
            render_html_card(
                display_value(workflow.get("workflow_name", "Workflow"), language),
                (
                    f"{display_value(workflow.get('description'), language)}<br>"
                    f"<strong>{t('field_status', language)}:</strong> {translate_status(workflow.get('status'), language)}<br>"
                    f"<strong>{display_text('Scope', language)}:</strong> {display_list(workflow.get('agents', []), language, 'agent')}<br>"
                    f"<strong>{t('field_next', language)}:</strong> {translate_next_step(workflow.get('next_step'), language)}"
                ),
                "section-card",
            )


def render_workflow_simulation_cards(workflows: list[dict]) -> None:
    """Render HUB-V2-009 local workflow simulation cards."""
    language = get_language()
    if not workflows:
        st.info(t("no_workflows_match", language))
        return

    columns = st.columns(2)
    for index, workflow in enumerate(workflows):
        gate_results = [
            f"{display_value(gate.get('gate_name', ''), language)}: "
            f"{translate_status(gate.get('approval_status', ''), language)} / "
            f"{display_value(gate.get('allowed_execution_mode', ''), language)}"
            for gate in workflow.get("approval_gates", [])
        ]
        with columns[index % 2]:
            render_html_card(
                display_value(workflow.get("workflow_name", "Workflow Simulation"), language),
                (
                    f"<strong>{display_text('Input source', language)}:</strong> {display_value(workflow.get('input_source'), language)}<br>"
                    f"<strong>{display_text('Connected agents', language)}:</strong> {display_list(workflow.get('source_agents', []), language, 'agent')}<br>"
                    f"<strong>{display_text('Signals used', language)}:</strong> {display_list(workflow.get('signals_used', []), language)}<br>"
                    f"<strong>{display_text('Recommended actions', language)}:</strong> {display_list(workflow.get('recommended_actions', []), language, 'action')}<br>"
                    f"<strong>{display_text('Approval gate result', language)}:</strong> {safe_list_join(gate_results)}<br>"
                    f"<strong>{display_text('Blocked steps', language)}:</strong> {display_list(workflow.get('blocked_steps', []), language) or translate_status('None', language)}<br>"
                    f"<strong>{display_text('Generated outputs', language)}:</strong> {display_list(workflow.get('generated_outputs', []), language)}<br>"
                    f"<strong>{display_text('Readiness', language)}:</strong> {safe_display(workflow.get('workflow_readiness_score'))} / "
                    f"{translate_status(workflow.get('workflow_status'), language)}<br>"
                    f"<strong>{t('field_next', language)}:</strong> {translate_next_step(workflow.get('next_recommended_step'), language)}"
                ),
                "section-card",
            )


def render_demo_workflow_report_export(
    *,
    agent_manifests: list[dict],
    registry_summary: dict,
    onboarding_summary: dict,
    action_rows: list[dict],
    action_summary: dict,
    useful_signals: list[dict],
    useful_signal_summary: dict,
    connector_readiness: list[dict],
    connector_readiness_summary: dict,
    workflow_simulations: list[dict],
    workflow_simulation_summary: dict,
    approval_gates: list[dict],
    approval_gate_summary: dict,
    validation_snapshot: dict,
) -> None:
    """Render HUB-V2-010 public-safe demo workflow report export previews."""
    language = get_language()
    st.markdown(f"### {t('demo_workflow_report_export', language)}")
    st.caption(t("report_export_caption", language))

    section_id_to_label = {
        item["section_id"]: f"{item['label']} ({item['section_id']})"
        for item in REPORT_SECTION_OPTIONS
    }
    default_section_ids = list(section_id_to_label)
    selected_section_ids = st.multiselect(
        t("report_sections", language),
        options=default_section_ids,
        default=default_section_ids,
        format_func=lambda section_id: display_text(section_id_to_label[section_id], language),
        key="demo_report_export_sections",
    )

    report_package = build_demo_report_package(
        agent_manifests=agent_manifests,
        registry_summary=registry_summary,
        onboarding_summary=onboarding_summary,
        action_rows=action_rows,
        action_summary=action_summary,
        useful_signals=useful_signals,
        useful_signal_summary=useful_signal_summary,
        connector_readiness=connector_readiness,
        connector_readiness_summary=connector_readiness_summary,
        workflow_simulations=workflow_simulations,
        workflow_simulation_summary=workflow_simulation_summary,
        approval_gates=approval_gates,
        approval_gate_summary=approval_gate_summary,
        validation_snapshot=validation_snapshot,
        selected_sections=selected_section_ids,
    )
    report_previews = build_report_previews(report_package)
    public_report_dir = get_public_reports_dir(BASE_DIR)

    render_metric_cards(
        [
            (t("available_report_sections", language), len(REPORT_SECTION_OPTIONS)),
            (t("export_formats", language), len(REPORT_FORMATS)),
            (
                t("public_safe_status", language),
                translate_status("Pass" if report_package.get("schema_valid") else "Review", language),
            ),
            (t("last_generated_report_path", language), str(public_report_dir.relative_to(BASE_DIR))),
        ]
    )
    st.markdown(
        f'<div class="note-box">{t("report_export_note", language)}</div>',
        unsafe_allow_html=True,
    )

    preview_tabs = st.tabs(
        [
            t("markdown_preview", language),
            t("json_preview", language),
            t("csv_summary_preview", language),
        ]
    )
    with preview_tabs[0]:
        st.text_area(
            t("copy_ready_markdown_report", language),
            report_previews["markdown"],
            height=360,
            key="demo_report_markdown_preview",
        )
        st.download_button(
            t("download_markdown_report_text", language),
            report_previews["markdown"],
            file_name=f"{report_package['report_id']}.md",
            mime="text/markdown",
            key="download_demo_workflow_report_markdown",
        )
    with preview_tabs[1]:
        st.code(report_previews["json"], language="json")
        st.download_button(
            t("download_json_report_text", language),
            report_previews["json"],
            file_name=f"{report_package['report_id']}.json",
            mime="application/json",
            key="download_demo_workflow_report_json",
        )
    with preview_tabs[2]:
        st.code(report_previews["csv"], language="csv")
        st.download_button(
            t("download_csv_summary_text", language),
            report_previews["csv"],
            file_name=f"{report_package['report_id']}.csv",
            mime="text/csv",
            key="download_demo_workflow_report_csv",
        )

    st.markdown(f"#### {t('report_safety_checklist', language)}")
    checklist_cols = st.columns(5)
    for index, note in enumerate(report_package.get("safety_notes", [])):
        checklist_cols[index % 5].metric(display_text(note, language), translate_status("Pass", language))


def render_signal_cards(signals: list[dict]) -> None:
    """Render short useful-signal cards."""
    columns = st.columns(len(signals))
    for index, signal in enumerate(signals):
        with columns[index]:
            st.metric(signal.get("signal", ""), build_metric_display_value(signal.get("value", "")))
            st.caption(signal.get("meaning", ""))


def render_useful_signal_cards(signals: list[dict], empty_message: str = "No signals match this view.") -> None:
    """Render HUB-V2-007 scored useful signal cards."""
    language = get_language()
    if not signals:
        st.info(empty_message)
        return

    columns = st.columns(2)
    for index, signal in enumerate(signals):
        with columns[index % 2]:
            render_html_card(
                display_value(signal.get("title", "Useful signal"), language),
                (
                    f"<strong>{t('field_score', language)}:</strong> {signal.get('usefulness_score', 0)} "
                    f"(R {signal.get('relevance_score', 0)} / "
                    f"U {signal.get('urgency_score', 0)} / "
                    f"A {signal.get('actionability_score', 0)} / "
                    f"V {signal.get('value_score', 0)} / "
                    f"{t('field_risk', language)} {signal.get('risk_score', 0)})<br>"
                    f"<strong>{t('field_source', language)}:</strong> {translate_agent_display_name(signal.get('source_agent'), language)} "
                    f"/ {display_value(signal.get('source_type'), language, 'source')}<br>"
                    f"<strong>{t('category', language)}:</strong> {translate_category(signal.get('category'), language)} | "
                    f"<strong>{t('field_status', language)}:</strong> {translate_status(signal.get('status'), language)}<br>"
                    f"<strong>{t('field_why_important', language)}:</strong> {display_value(signal.get('why_important'), language)}<br>"
                    f"<strong>{t('field_recommended_next_step', language)}:</strong> {translate_next_step(signal.get('suggested_next_step'), language)}<br>"
                    f"<strong>{t('field_related_agent', language)}:</strong> {translate_agent_display_name(signal.get('target_agent'), language)}<br>"
                    f"<strong>{t('field_action_reference', language)}:</strong> {safe_display(signal.get('related_action_id') or 'none')}<br>"
                    f"<strong>{t('field_policy', language)}:</strong> {display_value(signal.get('execution_policy'), language)}"
                ),
                "section-card",
            )


def render_connector_readiness_cards(
    connectors: list[dict],
    empty_message: str = "No connector readiness records match this view.",
) -> None:
    """Render HUB-V2-008 design-only connector readiness cards."""
    language = get_language()
    if not connectors:
        st.info(empty_message)
        return

    columns = st.columns(2)
    for index, connector in enumerate(connectors):
        with columns[index % 2]:
            render_html_card(
                translate_connector(connector.get("connector_name", "Connector readiness"), language),
                (
                    f"<strong>{display_text('Purpose', language)}:</strong> {display_value(connector.get('purpose'), language)}<br>"
                    f"<strong>{t('field_risk', language)}:</strong> {display_value(connector.get('risk_level'), language)} | "
                    f"<strong>{t('field_score', language)}:</strong> {safe_display(connector.get('readiness_score'))} | "
                    f"<strong>{t('field_status', language)}:</strong> {translate_status(connector.get('readiness_status'), language)}<br>"
                    f"<strong>{display_text('Provider', language)}:</strong> {translate_connector(connector.get('provider'), language)} | "
                    f"<strong>{display_text('Data access', language)}:</strong> {display_value(connector.get('data_access_level'), language)}<br>"
                    f"<strong>{display_text('Approval required', language)}:</strong> {display_value(connector.get('approval_required'), language)} | "
                    f"<strong>{display_text('Live status', language)}:</strong> {translate_status(connector.get('live_connection_status'), language)}<br>"
                    f"<strong>{display_text('Permissions', language)}:</strong> {display_list(connector.get('required_permissions', []), language)}<br>"
                    f"<strong>{display_text('Safety gates', language)}:</strong> {display_list(connector.get('safety_gates', []), language)}<br>"
                    f"<strong>{display_text('Rollback plan', language)}:</strong> {display_list(connector.get('rollback_plan', []), language)}<br>"
                    f"<strong>{display_text('Test plan', language)}:</strong> {display_list(connector.get('test_plan', []), language)}<br>"
                    f"<strong>{t('field_recommended_next_step', language)}:</strong> {translate_next_step(connector.get('recommended_next_step'), language)}<br>"
                    f"<strong>{t('field_policy', language)}:</strong> {display_value(connector.get('execution_policy'), language)}"
                ),
                "section-card",
            )


def render_onboarding_metrics(summary: dict) -> None:
    """Render the V2 onboarding metric strip."""
    language = get_language()
    render_metric_cards(
        [
            (display_text("Projects Scanned", language), summary.get("total_projects_scanned", 0)),
            (display_text("Manifests Found", language), summary.get("manifests_found", 0)),
            (display_text("Valid Manifests", language), summary.get("valid_manifests", 0)),
            (t("imported_agents", language), summary.get("imported_agents", 0)),
        ]
    )
    render_metric_cards(
        [
            (t("invalid_manifests", language), summary.get("invalid_manifests", 0)),
            (t("missing_manifests", language), summary.get("missing_manifests", 0)),
            (display_text("Static Overrides", language), summary.get("duplicate_agent_ids", 0)),
        ]
    )


def filter_agents(
    agents: list[dict],
    category_filter: str,
    status_filter: str,
    pin_status_filter: str,
) -> list[dict]:
    """Filter registry agents by sidebar registry filters."""
    filtered = agents
    if category_filter != "All":
        filtered = [agent for agent in filtered if agent.get("category") == category_filter]
    if status_filter != "All":
        filtered = [agent for agent in filtered if agent.get("status") == status_filter]
    if pin_status_filter != "All":
        filtered = [agent for agent in filtered if agent.get("pin_status") == pin_status_filter]
    return filtered


def filter_named_rows(rows: list[dict], allowed_names: set[str]) -> list[dict]:
    """Filter rows that include an agent_name field by allowed agent names."""
    return [row for row in rows if row.get("agent_name", "") in allowed_names]


def filter_health(rows: list[dict], health_status_filter: str) -> list[dict]:
    """Filter health results by selected health status."""
    if health_status_filter == "All":
        return rows
    return [row for row in rows if row.get("health_status") == health_status_filter]


def filter_actions(rows: list[dict], action_priority_filter: str) -> list[dict]:
    """Filter action plan rows by selected priority."""
    if action_priority_filter == "All":
        return rows
    return [row for row in rows if row.get("priority") == action_priority_filter]


def render_command_pack(command_pack: dict) -> None:
    """Render a command pack as display-only command cards."""
    language = get_language()
    st.markdown(f"**{t('commands_manual_only', language)}**")
    for label, command in command_pack.items():
        st.markdown(
            f"""
            <div class="command-card">
                <strong>{display_value(label, language, 'action')}</strong><br>{safe_display(command)}
            </div>
            """,
            unsafe_allow_html=True,
        )


def priority_class(priority: str) -> str:
    """Return a CSS class name for a priority value."""
    return {
        "High": "priority-high",
        "Medium": "priority-medium",
        "Low": "priority-low",
        "None": "priority-none",
    }.get(priority, "priority-none")


def render_action_cards(action_rows: list[dict]) -> None:
    """Render next-action cards grouped by priority."""
    language = get_language()
    groups = [
        ("High Priority", "High"),
        ("Medium Priority", "Medium"),
        ("Low Priority", "Low"),
        ("No Immediate Action", "None"),
    ]
    for group_title, priority in groups:
        st.markdown(f"### {display_text(group_title, language)}")
        group_rows = [row for row in action_rows if row.get("priority") == priority]
        if not group_rows:
            st.caption(t("no_items_group", language))
            continue
        for row in group_rows:
            render_html_card(
                display_agent_title(row.get("agent_name", "Unknown Agent"), language),
                (
                    f"<strong>{display_text('Priority', language)}: {translate_status(priority, language)}</strong><br>"
                    f"{translate_next_step(row.get('recommended_action'), language)}<br>"
                    f"{display_text('Reason', language)}: {display_value(row.get('reason'), language)}<br>"
                    f"{display_text('Issue', language)}: {display_value(row.get('related_issue'), language)}"
                ),
                f"section-card {priority_class(priority)}",
            )


def render_local_action_cards(action_rows: list[dict]) -> None:
    """Render HUB-V2-005 local action schema cards grouped by Agent."""
    language = get_language()
    grouped_actions = group_actions_by_agent(action_rows)
    for group in grouped_actions:
        actions = group.get("actions", [])
        with st.expander(
            f"{display_agent_title(group.get('agent_name', 'Unknown Agent'), language)} - {len(actions)} {t('available_actions', language)}",
            expanded=False,
        ):
            action_columns = st.columns(2)
            for index, action in enumerate(actions):
                approval = t("approval_required", language) if action.get("requires_approval") else t("approval_not_required", language)
                with action_columns[index % 2]:
                    render_html_card(
                        translate_action_label(action.get("label", "Action"), language),
                        (
                            f"<strong>{t('field_type', language)}:</strong> {display_value(action.get('action_type'), language)}<br>"
                            f"<strong>{t('field_execution_mode', language)}:</strong> {display_value(action.get('execution_mode'), language)}<br>"
                            f"<strong>{t('field_risk_level', language)}:</strong> {display_value(action.get('risk_level'), language)}<br>"
                            f"<strong>{t('field_approval', language)}:</strong> {approval}<br>"
                            f"<strong>{t('field_status', language)}:</strong> {translate_status(action.get('status'), language)}<br>"
                            f"<strong>{t('field_expected_output', language)}:</strong> {display_value(action.get('expected_output'), language)}<br>"
                            f"<strong>{t('field_runbook', language)}:</strong> {safe_display(action.get('runbook_ref'))}<br>"
                            f"<strong>{t('field_safety', language)}:</strong> {display_value(action.get('safety_note'), language)}"
                        ),
                        "section-card",
                    )


def prompt_type_display_label(prompt_type: str) -> str:
    """Return a readable label for prompt type selectors."""
    details = PROMPT_TYPE_DETAILS.get(prompt_type) or RESERVED_PROMPT_TYPE_DETAILS.get(prompt_type, {})
    label = details.get("label", prompt_type.replace("_", " ").title())
    status = details.get("status", "supported")
    return f"{label} - {prompt_type} ({status})"


def render_codex_prompt_generator(manifests: list[dict], action_rows: list[dict]) -> None:
    """Render a template-only Codex prompt generator without execution controls."""
    language = get_language()
    st.markdown(f"### {t('codex_prompt_generator', language)}")
    st.caption(t("codex_prompt_caption", language))

    if not manifests:
        st.info(display_text("No Agent manifests are available for prompt generation.", language))
        return

    sorted_manifests = sorted(manifests, key=lambda item: item.get("agent_name", "").lower())
    agent_options = {
        f"{display_agent_title(manifest.get('agent_name', 'Unknown Agent'), language)} ({manifest.get('agent_id', 'unknown')})": manifest
        for manifest in sorted_manifests
    }

    selector_left, selector_right = st.columns([1.1, 1])
    with selector_left:
        selected_agent_label = st.selectbox(
            t("agent_selector", language),
            list(agent_options.keys()),
            key="codex_prompt_agent_selector",
        )
    with selector_right:
        selected_prompt_type = st.selectbox(
            t("prompt_type_selector", language),
            list(ALL_PROMPT_TYPES),
            format_func=prompt_type_display_label,
            key="codex_prompt_type_selector",
        )

    selected_manifest = agent_options[selected_agent_label]
    selected_actions = get_actions_for_agent(
        action_rows,
        agent_id=selected_manifest.get("agent_id", ""),
        agent_name=selected_manifest.get("agent_name", ""),
    )
    prompt_package = build_codex_prompt_package(
        selected_manifest,
        action_rows=selected_actions,
        prompt_type=selected_prompt_type,
    )
    codex_prompt_actions = get_codex_prompt_actions(selected_actions)

    overview_left, overview_right = st.columns(2)
    with overview_left:
        render_html_card(
            t("selected_agent", language),
            (
                f"<strong>{display_text('Project path', language)}:</strong> {safe_display(selected_manifest.get('project_path'))}<br>"
                f"<strong>{t('category', language)}:</strong> {translate_category(selected_manifest.get('category_label') or selected_manifest.get('category'), language)}<br>"
                f"<strong>{t('field_status', language)}:</strong> {translate_status(selected_manifest.get('status'), language)}<br>"
                f"<strong>{display_text('Checkpoint', language)}:</strong> {safe_display(prompt_package.get('current_checkpoint'))}"
            ),
            "section-card",
        )
    with overview_right:
        render_html_card(
            t("next_recommended_action", language),
            (
                f"{translate_next_step(selected_manifest.get('next_recommended_action'), language)}<br>"
                f"<strong>{t('available_actions', language)}:</strong> {len(selected_actions)}<br>"
                f"<strong>{display_text('Codex prompt actions', language)}:</strong> {len(codex_prompt_actions)}<br>"
                f"<strong>{display_text('Execution', language)}:</strong> {display_text('template-only / no execution', language)}"
            ),
            "section-card",
        )

    if prompt_package.get("warnings"):
        for warning in prompt_package["warnings"]:
            st.warning(warning)

    st.markdown(f"#### {t('available_actions', language)}")
    selected_action_df = display_dataframe(selected_actions)
    if selected_action_df.empty:
        st.info(display_text("This Agent has no declared action rows.", language))
    else:
        st.dataframe(
            localize_dataframe(
                selected_action_df[
                    [
                        "action_id",
                        "label",
                        "action_type",
                        "execution_mode",
                        "risk_level",
                        "status",
                    ]
                ],
                language,
            ),
            width="stretch",
            hide_index=True,
        )

    safety_left, safety_right = st.columns(2)
    with safety_left:
        st.markdown(f"#### {t('safety_checklist', language)}")
        for item in prompt_package["safety_checklist"]:
            st.markdown(f"- {item}")
    with safety_right:
        st.markdown(f"#### {t('validation_checklist', language)}")
        for item in prompt_package["validation_requirements"]:
            st.markdown(f"- {item}")

    st.markdown(f"#### {t('generated_prompt_preview', language)}")
    st.text_area(
        t("copy_ready_generated_prompt", language),
        value=prompt_package["generated_prompt"],
        height=520,
        key="codex_prompt_generated_text",
        help=t("copy_prompt_help", language),
    )
    safe_agent_id = selected_manifest.get("agent_id", "agent").replace(" ", "_")
    st.download_button(
        t("download_prompt_text", language),
        data=prompt_package["generated_prompt"],
        file_name=f"{safe_agent_id}_{selected_prompt_type}_codex_prompt.txt",
        mime="text/plain",
        key="codex_prompt_download",
        help=t("download_prompt_help", language),
    )


def health_counts(health_results: list[dict]) -> dict:
    """Count health result statuses for overview cards."""
    statuses = {
        "Showcase Ready": 0,
        "Healthy": 0,
        "Partial": 0,
        "Missing or Incomplete": 0,
    }
    for result in health_results:
        status = result.get("health_status", "")
        if status in statuses:
            statuses[status] += 1
    return statuses


inject_global_styles()

static_agents = load_agent_registry(REGISTRY_PATH)
onboarding_result = build_agent_onboarding(AI_PROJECTS_ROOT, static_agents)
agents = onboarding_result["merged_agents"]
external_summary_index = build_external_summary_index(agents)
registry_summary = get_registry_summary(agents)
validation_results = validate_registry(agents)
health_results = check_all_agents_health(agents)
capability_summary = build_capability_summary(agents)
category_matrix = build_category_matrix(agents)
portfolio_positioning = build_portfolio_positioning(agents)
action_plan = build_next_action_plan(agents, health_results, validation_results)
action_summary = summarize_next_actions(action_plan)
health_summary = health_counts(health_results)
project_matrix_view = build_project_matrix_view(agents)
priority_summary = build_priority_summary(agents, action_plan)
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
agent_manifests = build_agent_manifests(agents, health_results, action_plan)
agent_contract = build_agent_contract()
workflow_catalog = build_workflow_catalog(agent_manifests)
action_center_items = build_action_center_items(agent_manifests, action_plan)
local_action_registry = build_action_registry(agent_manifests)
local_action_summary = build_action_registry_summary(local_action_registry)
connector_readiness_registry = build_connector_readiness_registry()
connector_readiness_summary = build_connector_readiness_summary(connector_readiness_registry)
connector_generated_signal_seeds = connector_readiness_to_useful_signals(connector_readiness_registry)
workflow_simulation_registry = build_workflow_simulation_registry()
workflow_simulation_summary = build_workflow_simulation_summary(workflow_simulation_registry)
approval_gate_registry = build_approval_gate_registry(workflow_simulation_registry)
approval_gate_summary = build_approval_gate_summary(approval_gate_registry)
workflow_generated_signal_seeds = workflow_simulation_to_useful_signals(workflow_simulation_registry)
useful_signal_registry = build_useful_signal_registry(
    agent_manifests,
    local_action_registry,
    extra_signals=connector_generated_signal_seeds + workflow_generated_signal_seeds,
)
useful_signal_summary = build_signal_summary(useful_signal_registry)
unsafe_execution_modes = [
    action
    for action in local_action_registry
    if action.get("execution_mode") not in {"not_executable", "manual_only", "template_only", "planned"}
]
signal_policy_violations = [
    signal
    for signal in useful_signal_registry
    if not signal.get("schema_valid")
    or signal.get("execution_policy") != DISPLAY_ONLY_EXECUTION_POLICY
]
report_validation_snapshot = {
    "valid_manifests": onboarding_result["summary"].get("valid_manifests", 0),
    "invalid_manifests": onboarding_result["summary"].get("invalid_manifests", 0),
    "missing_manifests": onboarding_result["summary"].get("missing_manifests", 0),
    "unsafe_execution_modes": len(unsafe_execution_modes),
    "action_policy_violations": len(find_action_policy_violations(local_action_registry)),
    "signal_policy_violations": len(signal_policy_violations),
    "connector_policy_violations": len(find_connector_policy_violations(connector_readiness_registry)),
    "workflow_policy_violations": len(find_workflow_policy_violations(workflow_simulation_registry)),
    "approval_gate_policy_violations": len(find_approval_gate_policy_violations(approval_gate_registry)),
    "report_export_policy_violations": 0,
}
connector_overview = build_connector_overview(agent_manifests)
future_plugin_interface = build_future_plugin_interface()

registry_df = as_dataframe(agents)

language = get_language()

with st.sidebar:
    language_options = list(LANGUAGE_LABELS.values())
    selected_language_label = st.radio(
        t("language_toggle_label", language),
        options=language_options,
        index=language_options.index(LANGUAGE_LABELS.get(language, "中文")),
        horizontal=True,
        key="ui_language_selector",
    )
    language = set_language(selected_language_label)
    st.caption(t("language_caption", language))

    st.markdown(f"### {t('sidebar_title', language)}")
    st.write(f"{t('product_status', language)}: {translate_status(PRODUCT_STATUS, language)}")
    st.write(f"{t('latest_checkpoint', language)}: {LATEST_CHECKPOINT}")
    st.write(f"{t('manifest_version', language)}: {MANIFEST_VERSION}")
    st.write(f"{t('mode', language)}: {t('local_demo_safe_mode', language)}")
    st.write(f"{t('api', language)}: {t('api_not_required', language)}")
    st.write(f"{t('data_source', language)}: {t('csv_local_manifests', language)}")
    st.write(f"{t('scan_root', language)}: {AI_PROJECTS_ROOT}")
    st.write(f"{t('external_actions', language)}: {t('external_actions_disabled', language)}")
    st.write(f"{t('launcher_port', language)}: 8525")

    st.markdown(f"### {t('filters', language)}")
    category_options = ["All"] + sorted({agent.get("category", "") for agent in agents if agent.get("category")})
    status_options = ["All"] + sorted({agent.get("status", "") for agent in agents if agent.get("status")})
    pin_options = ["All"] + sorted({agent.get("pin_status", "") for agent in agents if agent.get("pin_status")})
    health_options = ["All"] + sorted({row.get("health_status", "") for row in health_results if row.get("health_status")})
    priority_options = ["All", "High", "Medium", "Low", "None"]

    category_filter = st.selectbox(
        t("category", language),
        category_options,
        format_func=lambda value: translate_category(value, language) if value != "All" else translate_filter_option(value, language),
        key="category_filter",
    )
    status_filter = st.selectbox(
        t("status", language),
        status_options,
        format_func=lambda value: translate_filter_option(value, language),
        key="status_filter",
    )
    pin_status_filter = st.selectbox(
        t("pin_status", language),
        pin_options,
        format_func=lambda value: translate_filter_option(value, language),
        key="pin_status_filter",
    )
    health_status_filter = st.selectbox(
        t("health_status", language),
        health_options,
        format_func=lambda value: translate_filter_option(value, language),
        key="health_status_filter",
    )
    action_priority_filter = st.selectbox(
        t("action_priority", language),
        priority_options,
        format_func=lambda value: translate_filter_option(value, language),
        key="action_priority_filter",
    )

filtered_agents = filter_agents(agents, category_filter, status_filter, pin_status_filter)
filtered_names = {agent.get("agent_name", "") for agent in filtered_agents}
filtered_validation = filter_named_rows(validation_results, filtered_names)
filtered_health = filter_health(filter_named_rows(health_results, filtered_names), health_status_filter)
filtered_actions = filter_actions(filter_named_rows(action_plan, filtered_names), action_priority_filter)
sorted_filtered_actions = sorted(
    filtered_actions,
    key=lambda item: (PRIORITY_SORT.get(item.get("priority", "None"), 3), item.get("agent_name", "")),
)

st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-title">{t('hero_title', language)}</div>
        <div class="hero-subtitle">{t('hero_subtitle', language)}</div>
        <div class="hero-copy">
            {t('hero_copy', language)}
        </div>
        <span class="badge">{translate_status(PRODUCT_STATUS, language)}</span>
        <span class="badge">{t('badge_local_first', language)}</span>
        <span class="badge">{t('badge_agent_os', language)}</span>
        <span class="badge">{t('badge_safe_demo', language)}</span>
        <span class="badge">{t('badge_manifest_onboarding', language)}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

render_metric_cards(
    [
        (t("available_tools", language), registry_summary["total_agents"]),
        (t("completed_tools", language), registry_summary["completed_agents"]),
        (t("public_showcase", language), registry_summary["public_showcase_agents"]),
        (t("pinned", language), registry_summary["pinned_agents"]),
        (t("public_not_pinned", language), registry_summary["public_not_pinned_agents"]),
        (t("paused_complete", language), registry_summary["paused_or_completed_agents"]),
    ]
)

(
    command_overview_tab,
    tools_tab,
    workflows_tab,
    signals_tab,
    action_center_tab,
    connectors_tab,
    plugin_tab,
) = st.tabs(
    [
        t("tab_command_overview", language),
        t("tab_tools", language),
        t("tab_workflows", language),
        t("tab_useful_signals", language),
        t("tab_action_center", language),
        t("tab_connectors", language),
        t("tab_future_plugin", language),
    ]
)

with command_overview_tab:
    st.markdown(f"## {t('command_overview_title', language)}")
    st.write(t("command_overview_intro", language))

    st.markdown(f"### {t('what_you_can_use_now', language)}")
    render_manifest_cards(agent_manifests, max_items=6)

    d2i_summary_record = external_summary_index.get("data_to_insight_workflow_agent")
    if d2i_summary_record:
        render_external_agent_summary(
            d2i_summary_record,
            "DataToInsightWorkflowAgent AgentHub Summary",
        )

    st.markdown(f"### {t('command_center_summary', language)}")
    summary_left, summary_right = st.columns(2)
    with summary_left:
        render_html_card(t("portfolio_overview", language), display_value(command_center_summary["portfolio_overview"], language))
        render_html_card(t("health_snapshot", language), display_value(command_center_summary["health_snapshot"], language))
        render_html_card(t("strategic_summary", language), display_value(command_center_summary["strategic_summary"], language))
    with summary_right:
        render_html_card(t("showcase_status", language), display_value(command_center_summary["showcase_status"], language))
        render_html_card(t("priority_actions", language), display_value(command_center_summary["priority_actions"], language))
        render_html_card(t("next_best_move", language), translate_next_step(command_center_summary["next_best_move"], language))

    render_html_card(
        t("portfolio_positioning", language),
        display_value(portfolio_positioning["positioning_statement"], language),
    )

    col_strengths, col_gaps = st.columns(2)
    with col_strengths:
        render_html_card(
            t("showcase_strengths", language),
            display_list(portfolio_positioning["showcase_strengths"], language),
        )
    with col_gaps:
        render_html_card(
            t("portfolio_gaps", language),
            display_list(portfolio_positioning["portfolio_gaps"], language),
        )

    st.markdown(f"### {t('capability_overview', language)}")
    capability_cols = st.columns(4)
    for index, item in enumerate(capability_summary):
        with capability_cols[index % 4]:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div class="mini-card-title">{translate_category(item.get('category', 'Uncategorized'), language)}</div>
                    <div class="mini-card-meta">
                        {display_text('Agents', language)}: {item.get('agent_count', 0)}<br>
                        {display_text('Showcase', language)}: {item.get('showcase_count', 0)}<br>
                        {translate_status('Pinned', language)}: {item.get('pinned_count', 0)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(f"### {t('next_action_snapshot', language)}")
    render_metric_cards(
        [
            (translate_status("High", language), action_summary["high_priority"]),
            (translate_status("Medium", language), action_summary["medium_priority"]),
            (translate_status("Low", language), action_summary["low_priority"]),
            (translate_status("None", language), action_summary["no_action_needed"]),
        ]
    )

with tools_tab:
    st.markdown(f"## {t('tools_title', language)}")
    st.write(t("tools_intro", language))
    st.caption(t("metadata_only_caption", language))

    st.markdown(f"### {t('tool_cards', language)}")
    render_manifest_cards(
        [
            manifest
            for manifest in agent_manifests
            if manifest.get("agent_name") in filtered_names
        ]
    )

    registry_columns = [
        "agent_name",
        "source",
        "category",
        "project_type",
        "status",
        "stage",
        "showcase_status",
        "pin_status",
        "next_action",
    ]
    filtered_registry_df = as_dataframe(filtered_agents)
    if filtered_registry_df.empty:
        st.info(t("no_agents_match", language))
    else:
        filtered_registry_df["category"] = filtered_registry_df["category"].apply(
            lambda value: format_category_label(str(value))
        )
        st.markdown(f"### {t('registry_table', language)}")
        st.dataframe(
            localize_dataframe(filtered_registry_df[registry_columns], language),
            width="stretch",
            hide_index=True,
        )

        st.markdown(f"### {t('agent_detail_panel', language)}")
        selected_agent_name = st.selectbox(
            t("select_agent", language),
            filtered_registry_df["agent_name"].tolist(),
            format_func=lambda value: display_agent_title(value, language),
            key="agent_detail_select",
        )
        selected_agent = next(
            (agent for agent in filtered_agents if agent.get("agent_name") == selected_agent_name),
            {},
        )

        if selected_agent:
            agent_health = next(
                (row for row in health_results if row.get("agent_name") == selected_agent_name),
                {},
            )
            detail_cols = st.columns(3)
            detail_cols[0].markdown(
                f"**{t('field_status', language)}: {translate_status(selected_agent.get('status', ''), language)}**"
            )
            detail_cols[1].markdown(
                f"**{t('pin_status', language)}: {translate_status(selected_agent.get('pin_status'), language)}**"
            )
            detail_cols[2].markdown(
                f"**{t('health_status', language)}: {translate_status(agent_health.get('health_status', ''), language)}**"
            )

            detail_left, detail_right = st.columns([1.2, 1])
            with detail_left:
                render_html_card(
                    t("capability", language),
                    truncate_text(display_value(selected_agent.get("primary_capability", ""), language, "description"), 260),
                )
                render_html_card(
                    t("portfolio_value", language),
                    truncate_text(display_value(selected_agent.get("portfolio_value", ""), language), 260),
                )
                render_html_card(
                    t("notes", language),
                    truncate_text(display_value(selected_agent.get("notes", ""), language), 220),
                )
            with detail_right:
                render_html_card(t("tech_stack", language), safe_display(selected_agent.get("tech_stack")))
                render_html_card(t("local_path", language), safe_display(selected_agent.get("local_path")))
                render_html_card(
                    t("github_url", language),
                    safe_display(build_open_github_command(selected_agent)),
                )
                if selected_agent.get("dashboard_path"):
                    render_html_card(display_text("Dashboard path", language), safe_display(selected_agent.get("dashboard_path")))
                if selected_agent.get("report_path"):
                    render_html_card(display_text("Markdown report path", language), safe_display(selected_agent.get("report_path")))
                if selected_agent.get("agenthub_summary_path"):
                    render_html_card(display_text("AgentHub summary path", language), safe_display(selected_agent.get("agenthub_summary_path")))

            selected_summary_record = external_summary_index.get(selected_agent.get("agent_id", ""))
            if selected_summary_record:
                render_external_agent_summary(
                    selected_summary_record,
                    f"{selected_agent.get('agent_name', 'Agent')} Summary Metrics",
                )

            st.markdown(f"### {t('command_pack_panel', language)}")
            render_command_pack(build_project_command_pack(selected_agent))

    st.markdown(f"### {t('registry_validation_table', language)}")
    validation_columns = [
        "agent_name",
        "is_valid",
        "quality_score",
        "missing_required_fields",
        "validation_notes",
    ]
    validation_df = display_dataframe(filtered_validation)
    if validation_df.empty:
        st.info(t("no_validation_rows", language))
    else:
        st.dataframe(
            localize_dataframe(validation_df[validation_columns], language),
            width="stretch",
            hide_index=True,
        )

with signals_tab:
    st.markdown(f"## {t('useful_signals_title', language)}")
    st.write(t("useful_signals_intro", language))

    st.markdown(f"### {t('signal_metrics', language)}")
    render_metric_cards(
        [
            (display_text("Total signals", language), useful_signal_summary["total_signals"]),
            (display_text("High-value signals", language), useful_signal_summary["high_value_signals"]),
            (display_text("Needs action", language), useful_signal_summary["needs_action_signals"]),
            (display_text("Watchlist", language), useful_signal_summary["watchlist_signals"]),
            (display_text("Ignored / low priority", language), useful_signal_summary["ignored_low_priority_signals"]),
            (display_text("Avg usefulness", language), useful_signal_summary["average_usefulness_score"]),
        ]
    )
    st.caption(
        display_text("HUB-V2-007 signals are local/demo/template-only recommendations. They do not execute actions or connect external services.", language)
    )

    st.markdown(f"### {t('signal_filters', language)}")
    signal_filter_cols = st.columns(4)
    with signal_filter_cols[0]:
        signal_category_filter = st.selectbox(
            display_text("Signal category", language),
            get_signal_category_options(),
            format_func=lambda value: translate_category(value, language) if value != "All" else translate_filter_option(value, language),
            key="signal_category_filter",
        )
    with signal_filter_cols[1]:
        signal_status_filter = st.selectbox(
            display_text("Signal status", language),
            get_signal_status_options(),
            format_func=lambda value: translate_status(value, language),
            key="signal_status_filter",
        )
    with signal_filter_cols[2]:
        signal_source_options = ["All"] + sorted(
            {signal.get("source_agent", "") for signal in useful_signal_registry if signal.get("source_agent")}
        )
        signal_source_filter = st.selectbox(
            display_text("Source agent", language),
            signal_source_options,
            format_func=lambda value: translate_filter_option(value, language) if value == "All" else translate_agent_display_name(value, language),
            key="signal_source_filter",
        )
    with signal_filter_cols[3]:
        signal_min_score = st.slider(
            display_text("Min usefulness", language),
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            key="signal_min_score_filter",
        )

    filtered_signal_registry = filter_useful_signals(
        useful_signal_registry,
        category=signal_category_filter,
        status=signal_status_filter,
        source_agent=signal_source_filter,
        min_usefulness_score=signal_min_score,
    )
    signal_buckets = group_signal_buckets(filtered_signal_registry)

    st.markdown(f"### {t('top_useful_signals', language)}")
    render_useful_signal_cards(
        signal_buckets["top"],
        empty_message=display_text("No top signals match the current filters.", language),
    )

    st.markdown(f"### {t('needs_action', language)}")
    render_useful_signal_cards(
        signal_buckets["needs_action"],
        empty_message=display_text("No needs-action signals match the current filters.", language),
    )

    st.markdown(f"### {t('watchlist', language)}")
    render_useful_signal_cards(
        signal_buckets["watchlist"],
        empty_message=display_text("No watchlist signals match the current filters.", language),
    )

    with st.expander(t("low_priority_ignored", language), expanded=False):
        render_useful_signal_cards(
            signal_buckets["low_priority"],
            empty_message=display_text("No low-priority signals match the current filters.", language),
        )

    st.markdown(f"### {t('signal_table', language)}")
    signal_df = display_dataframe(filtered_signal_registry)
    if signal_df.empty:
        st.info(t("no_signals_match", language))
    else:
        st.dataframe(
            localize_dataframe(
                signal_df[
                    [
                        "title",
                        "source_agent",
                        "source_type",
                        "category",
                        "usefulness_score",
                        "relevance_score",
                        "urgency_score",
                        "actionability_score",
                        "value_score",
                        "risk_score",
                        "recommended_action",
                        "target_agent",
                        "status",
                        "bucket",
                    ]
                ],
                language,
            ),
            width="stretch",
            hide_index=True,
        )

    st.markdown(f"### {t('health_overview', language)}")
    render_metric_cards(
        [
            (translate_status("Showcase Ready", language), health_summary["Showcase Ready"]),
            (translate_status("Healthy", language), health_summary["Healthy"]),
            (translate_status("Partial", language), health_summary["Partial"]),
            (translate_status("Missing / Incomplete", language), health_summary["Missing or Incomplete"]),
        ]
    )

    health_columns = [
        "agent_name",
        "health_score",
        "health_status",
        "path_exists",
        "readme_exists",
        "requirements_exists",
        "app_exists",
        "tests_folder_exists",
        "docs_folder_exists",
        "project_status_exists",
        "portfolio_folder_exists",
        "missing_items",
        "suggested_fix",
    ]
    health_df = display_dataframe(filtered_health)
    st.markdown(f"### {t('health_table', language)}")
    if health_df.empty:
        st.info(display_text("No health rows match the selected filters.", language))
    else:
        st.dataframe(
            localize_dataframe(health_df[health_columns], language),
            width="stretch",
            hide_index=True,
        )

    st.markdown(f"### {t('health_detail', language)}")
    for result in filtered_health:
        with st.expander(
            f"{display_agent_title(result.get('agent_name', 'Unknown Agent'), language)} - "
            f"{translate_status(result.get('health_status', ''), language)}"
        ):
            st.write(f"{display_text('Missing items', language)}: {display_list(result.get('missing_items', []), language)}")
            st.write(f"{display_text('Warnings', language)}: {display_value(result.get('warnings'), language)}")
            st.write(f"{display_text('Suggested fix', language)}: {display_value(result.get('suggested_fix'), language)}")
            st.write(f"{display_text('Last checked', language)}: {display_value(result.get('last_checked_note'), language)}")

with workflows_tab:
    st.markdown(f"## {t('workflows_title', language)}")
    st.write(t("workflows_intro", language))

    st.markdown(f"### {t('local_workflow_simulation', language)}")
    st.caption(t("local_simulation_caption", language))
    render_metric_cards(
        [
            (display_text("Total demo workflows", language), workflow_simulation_summary["total_demo_workflows"]),
            (
                display_text("Ready for manual review", language),
                workflow_simulation_summary["ready_for_manual_review_workflows"],
            ),
            (display_text("Blocked steps", language), workflow_simulation_summary["blocked_steps"]),
            (display_text("Manual-only steps", language), workflow_simulation_summary["manual_only_steps"]),
            (display_text("Template-only outputs", language), workflow_simulation_summary["template_only_outputs"]),
            (display_text("Approval gates required", language), workflow_simulation_summary["approval_gates_required"]),
            (
                display_text("Avg workflow readiness", language),
                workflow_simulation_summary["average_workflow_readiness_score"],
            ),
        ]
    )

    workflow_filter_cols = st.columns(2)
    with workflow_filter_cols[0]:
        workflow_type_filter = st.selectbox(
            display_text("Workflow type", language),
            get_workflow_type_options(),
            format_func=lambda value: translate_filter_option(value, language),
            key="workflow_type_filter",
        )
    with workflow_filter_cols[1]:
        workflow_status_filter = st.selectbox(
            display_text("Workflow status", language),
            get_workflow_status_options(),
            format_func=lambda value: translate_status(value, language),
            key="workflow_status_filter",
        )

    filtered_workflow_simulations = filter_workflow_simulations(
        workflow_simulation_registry,
        workflow_type=workflow_type_filter,
        workflow_status=workflow_status_filter,
    )
    render_workflow_simulation_cards(filtered_workflow_simulations)

    st.markdown(f"### {t('approval_gates', language)}")
    st.caption(
        display_text(
            f"Approval gates are metadata only. Total gates: {approval_gate_summary['total_approval_gates']}. "
            f"Blocked gates: {approval_gate_summary['blocked_gates']}. "
            "Allowed modes are display_only, manual_only, template_only, dry_run_only, or blocked.",
            language,
        )
    )
    approval_gate_df = display_dataframe(approval_gate_registry)
    if approval_gate_df.empty:
        st.info(display_text("No approval gates are available.", language))
    else:
        st.dataframe(
            localize_dataframe(
                approval_gate_df[
                    [
                        "workflow_name",
                        "gate_name",
                        "target_action_id",
                        "target_connector_id",
                        "risk_level",
                        "approval_status",
                        "required_checks",
                        "allowed_execution_mode",
                        "block_reason",
                    ]
                ],
                language,
            ),
            width="stretch",
            hide_index=True,
        )

    st.markdown(f"### {t('workflow_generated_signals', language)}")
    workflow_signal_df = display_dataframe(workflow_generated_signal_seeds)
    if workflow_signal_df.empty:
        st.info(display_text("No workflow-generated signals are available.", language))
    else:
        st.dataframe(
            localize_dataframe(
                workflow_signal_df[
                    [
                        "title",
                        "category",
                        "status",
                        "risk_score",
                        "recommended_action",
                    ]
                ],
                language,
            ),
            width="stretch",
            hide_index=True,
        )

    render_demo_workflow_report_export(
        agent_manifests=agent_manifests,
        registry_summary=registry_summary,
        onboarding_summary=onboarding_result["summary"],
        action_rows=local_action_registry,
        action_summary=local_action_summary,
        useful_signals=useful_signal_registry,
        useful_signal_summary=useful_signal_summary,
        connector_readiness=connector_readiness_registry,
        connector_readiness_summary=connector_readiness_summary,
        workflow_simulations=workflow_simulation_registry,
        workflow_simulation_summary=workflow_simulation_summary,
        approval_gates=approval_gate_registry,
        approval_gate_summary=approval_gate_summary,
        validation_snapshot=report_validation_snapshot,
    )

    st.markdown(f"### {t('workflow_catalog', language)}")
    render_workflow_cards(workflow_catalog)

    st.markdown(f"### {t('project_matrix_view', language)}")
    matrix_cols = st.columns(2)
    for index, item in enumerate(project_matrix_view):
        project_names = [project.get("name", "") for project in item.get("projects", [])]
        projects_text = display_list(project_names, language, "agent") if project_names else display_text("No registered project yet.", language)
        with matrix_cols[index % 2]:
            render_html_card(
                translate_category(item.get("category_group", "Uncategorized"), language),
                (
                    f"<strong>{display_text('Projects', language)}:</strong> {projects_text}<br>"
                    f"<strong>{display_text('Status', language)}:</strong> {display_value(item.get('status_summary'), language)}<br>"
                    f"<strong>{display_text('Next', language)}:</strong> {translate_next_step(item.get('next_step'), language)}<br>"
                    f"<strong>{display_text('Role', language)}:</strong> {display_value(item.get('portfolio_role'), language)}"
                ),
            )

    st.markdown(f"### {t('capability_cluster_cards', language)}")
    cluster_items = list(portfolio_positioning["capability_clusters"].items())
    cluster_cols = st.columns(4)
    for index, (cluster, agent_names) in enumerate(cluster_items):
        with cluster_cols[index % 4]:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div class="mini-card-title">{translate_category(cluster, language)}</div>
                    <div class="mini-card-meta">{display_list(agent_names, language, "agent")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_html_card(
        t("strongest_categories", language),
        display_list(portfolio_positioning["strongest_categories"], language, "category"),
    )

    st.markdown(f"### {t('category_matrix', language)}")
    for item in capability_summary:
        render_html_card(
            translate_category(item.get("category", "Uncategorized"), language),
            (
                f"{display_text('Agents', language)}: {display_list(item.get('agents', []), language, 'agent')}<br>"
                f"{display_text('Capabilities', language)}: {display_list(item.get('capabilities', []), language, 'description')}<br>"
                f"{display_text('Showcase count', language)}: {item.get('showcase_count', 0)} | "
                f"{display_text('Pinned count', language)}: {item.get('pinned_count', 0)}"
            ),
        )

    st.markdown(f"### {t('portfolio_gaps', language)}")
    for gap in portfolio_positioning["portfolio_gaps"]:
        st.markdown(f'<div class="note-box">{gap}</div>', unsafe_allow_html=True)

with action_center_tab:
    st.markdown(f"## {t('action_center_title', language)}")
    st.write(t("action_center_intro", language))

    st.markdown(f"### {t('priority_summary', language)}")
    render_metric_cards(
        [
            (translate_status("High", language), action_summary["high_priority"]),
            (translate_status("Medium", language), action_summary["medium_priority"]),
            (translate_status("Low", language), action_summary["low_priority"]),
            (translate_status("None", language), action_summary["no_action_needed"]),
        ]
    )

    priority_left, priority_right = st.columns(2)
    with priority_left:
        render_html_card(
            t("current_next_project", language),
            (
                f"{display_agent_title(priority_summary['next_best_project'], language)}<br>"
                f"{translate_next_step(priority_summary['next_best_action'], language)}"
            ),
        )
        render_html_card(
            t("paused_projects", language),
            display_list(priority_summary["paused_projects"], language, "agent"),
        )
        render_html_card(
            t("github_showcase_projects", language),
            display_list(priority_summary["github_showcase_projects"], language, "agent"),
        )
    with priority_right:
        commercial_names = [
            item.get("agent_name", "")
            for item in priority_summary["commercialization_candidates"]
        ]
        render_html_card(
            t("portfolio_follow_up", language),
            translate_next_step(priority_summary["portfolio_follow_up"], language),
        )
        render_html_card(
            t("future_commercial_candidates", language),
            display_list(commercial_names, language, "agent"),
        )
        render_html_card(
            t("future_agenthub_integration", language),
            display_list(priority_summary["agenthub_integration_candidates"], language, "agent"),
        )

    st.markdown(f'<div class="note-box">{display_value(priority_summary["pause_rule"], language)}</div>', unsafe_allow_html=True)

    st.markdown(f"### {t('local_action_schema_metrics', language)}")
    render_metric_cards(
        [
            (t("total_actions", language), local_action_summary["total_actions"]),
            (t("manual_only_actions", language), local_action_summary["manual_only_actions"]),
            (t("display_only_actions", language), local_action_summary["display_only_actions"]),
            (t("future_connector_actions", language), local_action_summary["future_connector_actions"]),
            (t("requires_approval", language), local_action_summary["requires_approval_actions"]),
            (t("blocked_actions", language), local_action_summary["blocked_actions"]),
        ]
    )
    st.caption(
        display_text(
            "HUB-V2-005 actions are metadata, instructions, command templates, links, report views, Codex prompts, or future connector placeholders only.",
            language,
        )
    )

    st.markdown(f"### {t('local_action_schema_table', language)}")
    local_action_df = display_dataframe(local_action_registry)
    st.dataframe(
        localize_dataframe(
            local_action_df[
                [
                    "agent_name",
                    "action_id",
                    "label",
                    "action_type",
                    "execution_mode",
                    "risk_level",
                    "requires_approval",
                    "status",
                    "connector_required",
                    "runbook_ref",
                ]
            ],
            language,
        ),
        width="stretch",
        hide_index=True,
    )

    st.markdown(f"### {t('local_action_cards', language)}")
    render_local_action_cards(local_action_registry)

    render_codex_prompt_generator(agent_manifests, local_action_registry)

    st.markdown(f"### {t('available_actions', language)}")
    action_center_df = display_dataframe(action_center_items)
    st.dataframe(
        localize_dataframe(
            action_center_df[
                [
                    "agent_name",
                    "priority",
                    "status",
                    "health_status",
                    "next_recommended_action",
                    "available_actions",
                    "execution_policy",
                ]
            ],
            language,
        ),
        width="stretch",
        hide_index=True,
    )

    action_columns = [
        "agent_name",
        "priority",
        "recommended_action",
        "reason",
        "category",
        "related_issue",
    ]
    action_df = display_dataframe(sorted_filtered_actions)
    st.markdown(f"### {t('action_plan_table', language)}")
    if action_df.empty:
        st.info(display_text("No action rows match the selected filters.", language))
    else:
        st.dataframe(
            localize_dataframe(action_df[action_columns], language),
            width="stretch",
            hide_index=True,
        )

    st.markdown(f"### {t('action_cards', language)}")
    render_action_cards(sorted_filtered_actions)

with connectors_tab:
    st.markdown(f"## {t('connectors_title', language)}")
    st.write(t("connectors_intro", language))
    st.caption(t("connectors_caption", language))

    st.markdown(f"### {t('connector_readiness_simulator', language)}")
    render_metric_cards(
        [
            (display_text("Total connectors", language), connector_readiness_summary["total_connectors"]),
            (display_text("Design-only connectors", language), connector_readiness_summary["design_only_connectors"]),
            (display_text("Ready for demo", language), connector_readiness_summary["ready_for_demo_connectors"]),
            (display_text("Needs review", language), connector_readiness_summary["needs_review_connectors"]),
            (
                display_text("Blocked until approved", language),
                connector_readiness_summary["blocked_until_approved_connectors"],
            ),
            (display_text("High-risk connectors", language), connector_readiness_summary["high_risk_connectors"]),
            (display_text("Avg readiness", language), connector_readiness_summary["average_readiness_score"]),
        ]
    )

    st.markdown(f"### {t('readiness_filters', language)}")
    connector_filter_cols = st.columns(3)
    with connector_filter_cols[0]:
        connector_risk_filter = st.selectbox(
            display_text("Connector risk", language),
            get_connector_risk_options(),
            format_func=lambda value: translate_filter_option(value, language),
            key="connector_risk_filter",
        )
    with connector_filter_cols[1]:
        connector_status_filter = st.selectbox(
            display_text("Readiness status", language),
            get_connector_status_options(),
            format_func=lambda value: translate_status(value, language),
            key="connector_status_filter",
        )
    with connector_filter_cols[2]:
        connector_provider_options = ["All"] + sorted(
            {connector.get("provider", "") for connector in connector_readiness_registry if connector.get("provider")}
        )
        connector_provider_filter = st.selectbox(
            display_text("Provider", language),
            connector_provider_options,
            format_func=lambda value: translate_filter_option(value, language) if value == "All" else translate_connector(value, language),
            key="connector_provider_filter",
        )

    filtered_connector_readiness = filter_connector_readiness(
        connector_readiness_registry,
        risk_level=connector_risk_filter,
        readiness_status=connector_status_filter,
        provider=connector_provider_filter,
    )

    st.markdown(f"### {t('connector_cards', language)}")
    render_connector_readiness_cards(
        filtered_connector_readiness,
        empty_message=t("no_connectors_match", language),
    )

    st.markdown(f"### {t('readiness_table', language)}")
    readiness_df = display_dataframe(filtered_connector_readiness)
    if readiness_df.empty:
        st.info(display_text("No connector readiness rows match the selected filters.", language))
    else:
        st.dataframe(
            localize_dataframe(
                readiness_df[
                    [
                        "connector_name",
                        "provider",
                        "purpose",
                        "data_access_level",
                        "write_access",
                        "risk_level",
                        "approval_required",
                        "demo_mode_available",
                        "read_only_mode_available",
                        "readiness_score",
                        "readiness_status",
                        "live_connection_status",
                        "recommended_next_step",
                    ]
                ],
                language,
            ),
            width="stretch",
            hide_index=True,
        )

    st.markdown(f"### {t('connector_generated_signals', language)}")
    connector_signal_df = display_dataframe(connector_generated_signal_seeds)
    if connector_signal_df.empty:
        st.info(display_text("No connector-generated signals are available.", language))
    else:
        st.dataframe(
            localize_dataframe(
                connector_signal_df[
                    [
                        "title",
                        "category",
                        "status",
                        "risk_score",
                        "recommended_action",
                    ]
                ],
                language,
            ),
            width="stretch",
            hide_index=True,
        )

    st.markdown(f"### {t('existing_connector_overview', language)}")
    st.write(
        display_text("Manifest-declared connector surfaces remain local, link-based, planned, optional, or not connected.", language)
    )

    connector_df = display_dataframe(connector_overview)
    st.dataframe(
        localize_dataframe(
            connector_df[
                [
                    "connector_id",
                    "label",
                    "status",
                    "mode",
                    "agent_count",
                    "safe_mode",
                ]
            ],
            language,
            domains={"label": "connector"},
        ),
        width="stretch",
        hide_index=True,
    )

    st.markdown(f"### {t('connector_policy', language)}")
    render_html_card(
        t("current_boundary", language),
        display_text(
            "Local filesystem checks, GitHub links, and Streamlit launch commands are available as safe display-only surfaces. "
            "Live account connectors remain disabled until a future explicit integration stage.",
            language,
        ),
    )
    render_html_card(
        t("planned_connectors", language),
        display_text(
            "Gmail, Google Sheets, Google Drive, Notion, Airtable, Telegram, GitHub, n8n, Make, and Zapier are reserved for future opt-in connector work.",
            language,
        ),
    )

with plugin_tab:
    st.markdown(f"## {t('future_plugin_title', language)}")
    st.write(t("future_plugin_intro", language))

    st.markdown(f"### {t('agent_onboarding', language)}")
    st.caption(t("agent_onboarding_caption", language))
    render_onboarding_metrics(onboarding_result["summary"])
    render_html_card(
        display_text("Recommended Fixes", language),
        display_list(onboarding_result["summary"]["recommended_fixes"], language, "next_step"),
    )

    st.markdown(f"### {t('discovery_results', language)}")
    project_rows_df = display_dataframe(onboarding_result["project_rows"])
    if project_rows_df.empty:
        st.info(display_text("No project folders were found under the scan root.", language))
    else:
        st.dataframe(
            localize_dataframe(
                project_rows_df[
                    [
                        "project_name",
                        "manifest_status",
                        "source",
                        "imported_agents",
                        "invalid_agents",
                        "warnings",
                        "recommended_fix",
                    ]
                ],
                language,
            ),
            width="stretch",
            hide_index=True,
        )

    imported_agents_df = display_dataframe(onboarding_result["imported_agents"])
    st.markdown(f"### {t('imported_agents', language)}")
    if imported_agents_df.empty:
        st.info(display_text("No valid local manifests were imported yet.", language))
    else:
        st.dataframe(
            localize_dataframe(
                imported_agents_df[
                    [
                        "agent_id",
                        "agent_name",
                        "source",
                        "category",
                        "status",
                        "next_action",
                    ]
                ],
                language,
            ),
            width="stretch",
            hide_index=True,
        )

    with st.expander(display_text("Local path details for manual review", language)):
        st.caption(
            display_text("Path details are intentionally collapsed for public-safe screenshots.", language)
        )
        if not project_rows_df.empty:
            st.dataframe(
                localize_dataframe(
                    project_rows_df[["project_name", "project_path", "manifest_path"]],
                    language,
                ),
                width="stretch",
                hide_index=True,
            )

    duplicate_ids_df = display_dataframe(onboarding_result["duplicate_agent_ids"])
    st.markdown(f"### {t('duplicate_agent_ids', language)}")
    if duplicate_ids_df.empty:
        st.info(display_text("No duplicate agent_id conflicts found.", language))
    else:
        st.caption(
            display_text("Static registry overrides are expected while AgentHub keeps CSV data as a baseline and local manifests as the richer runtime source.", language)
        )
        st.dataframe(localize_dataframe(duplicate_ids_df, language), width="stretch", hide_index=True)

    missing_df = display_dataframe(onboarding_result["missing_manifest_projects"])
    invalid_df = display_dataframe(onboarding_result["invalid_manifest_projects"])
    missing_col, invalid_col = st.columns(2)
    with missing_col:
        st.markdown(f"### {t('missing_manifests', language)}")
        if missing_df.empty:
            st.info(display_text("No missing manifests.", language))
        else:
            st.dataframe(
                localize_dataframe(missing_df[["project_name", "recommended_fix"]], language),
                width="stretch",
                hide_index=True,
            )
    with invalid_col:
        st.markdown(f"### {t('invalid_manifests', language)}")
        if invalid_df.empty:
            st.info(display_text("No invalid manifests.", language))
        else:
            st.dataframe(
                localize_dataframe(invalid_df[["project_name", "warnings", "recommended_fix"]], language),
                width="stretch",
                hide_index=True,
            )

    st.markdown(f"### {t('agent_contract', language)}")
    contract_left, contract_right = st.columns(2)
    with contract_left:
        render_html_card(
            display_text("Required Fields", language),
            display_list(agent_contract["required_fields"], language),
        )
        render_html_card(
            display_text("Execution Policy", language),
            (
                f"{display_text('Default mode', language)}: {display_value(agent_contract['execution_policy']['default_mode'], language)}<br>"
                f"{display_text('External API calls', language)}: {display_value(agent_contract['execution_policy']['external_api_calls'], language)}<br>"
                f"{display_text('Actions', language)}: {display_value(agent_contract['execution_policy']['actions'], language)}"
            ),
        )
    with contract_right:
        render_html_card(
            display_text("Connector Policy", language),
            (
                f"{display_text('Current stage', language)}: {translate_status(agent_contract['connector_policy']['current_stage'], language)}<br>"
                f"{display_text('Live connectors', language)}: {display_value(agent_contract['connector_policy']['live_connectors'], language)}<br>"
                f"{display_text('Planned', language)}: {display_list(agent_contract['connector_policy']['planned_connectors'], language, 'connector')}"
            ),
        )
        render_html_card(
            display_text("Manifest Files", language),
            display_text("Use agent_manifest.json, agent_contract.json, docs/AGENT_INTERFACE_STANDARD.md, and docs/FUTURE_PLUGIN_INTERFACE.md as the onboarding baseline.", language),
        )

    st.markdown(f"### {t('plugin_interface_roadmap', language)}")
    st.dataframe(
        localize_dataframe(display_dataframe(future_plugin_interface), language),
        width="stretch",
        hide_index=True,
    )

    st.markdown(f"### {t('export_report', language)}")
    st.write(t("export_report_intro", language))

    report = build_portfolio_markdown_report(
        agents=agents,
        registry_summary=registry_summary,
        capability_summary=capability_summary,
        health_results=health_results,
        validation_results=validation_results,
        action_plan=action_plan,
        portfolio_positioning=portfolio_positioning,
    )
    report_file_name = build_report_file_name()

    st.markdown(f"### {t('command_center_export_summary', language)}")
    render_metric_cards(
        [
            (display_text("Tracked Agents", language), command_center_summary["tracked_agents"]),
            (display_text("Public Showcase", language), command_center_summary["public_showcase_agents"]),
            (translate_status("Showcase Ready", language), command_center_summary["showcase_ready_agents"]),
            (display_text("High Priority", language), command_center_summary["high_priority_actions"]),
        ]
    )

    render_html_card(
        display_text("Report Summary", language),
        (
            f"{display_text('Agents', language)}: {registry_summary['total_agents']} | "
            f"{display_text('Actions', language)}: {action_summary['total_actions']} | "
            f"{translate_status('Showcase Ready', language)}: {health_summary['Showcase Ready']} | "
            f"{translate_status('Partial', language)}: {health_summary['Partial']} | "
            f"{translate_status('Missing / Incomplete', language)}: {health_summary['Missing or Incomplete']}"
        ),
    )

    st.markdown(f'<div class="disclaimer-box">{t("disclaimer", language)}</div>', unsafe_allow_html=True)

    export_left, export_right = st.columns(2)
    with export_left:
        st.download_button(
            t("download_markdown_report", language),
            data=report,
            file_name=report_file_name,
            mime="text/markdown",
        )
    with export_right:
        if st.button(t("save_report_local_outputs", language)):
            try:
                saved_path = save_markdown_report(report, OUTPUTS_DIR, report_file_name)
                st.success(f"{display_text('Saved local report', language)}: {saved_path}")
            except OSError as exc:
                st.error(f"{display_text('Could not save local report', language)}: {exc}")

    st.caption(t("saved_report_caption", language))

    st.markdown(f"### {t('showcase_asset_checklist', language)}")
    st.dataframe(
        localize_dataframe(display_dataframe(showcase_asset_checklist), language),
        width="stretch",
        hide_index=True,
    )

    st.markdown(f"### {t('markdown_report_preview', language)}")
    st.markdown(display_value(report, language))
