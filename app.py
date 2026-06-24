from pathlib import Path

import pandas as pd
import streamlit as st

from agent_hub.command_builder import (
    build_open_github_command,
    build_project_command_pack,
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
from agent_hub.ui_helpers import (
    build_metric_display_value,
    render_health_label_text,
    render_priority_label_text,
    render_status_label_text,
    safe_display,
    safe_list_join,
    truncate_text,
)


BASE_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = BASE_DIR / "data" / "agent_registry.csv"
OUTPUTS_DIR = BASE_DIR / "outputs"
DISCLAIMER_TEXT = (
    "This dashboard is for local portfolio management and workflow planning only. "
    "It does not execute external actions or access private credentials."
)
PRIORITY_SORT = {"High": 0, "Medium": 1, "Low": 2, "None": 3}


st.set_page_config(
    page_title="AgentHubControlCenter",
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
    st.markdown("**Commands are displayed for manual use only.**")
    for label, command in command_pack.items():
        st.markdown(
            f"""
            <div class="command-card">
                <strong>{label}</strong><br>{safe_display(command)}
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
    groups = [
        ("High Priority", "High"),
        ("Medium Priority", "Medium"),
        ("Low Priority", "Low"),
        ("No Immediate Action", "None"),
    ]
    for group_title, priority in groups:
        st.markdown(f"### {group_title}")
        group_rows = [row for row in action_rows if row.get("priority") == priority]
        if not group_rows:
            st.caption("No items in this group.")
            continue
        for row in group_rows:
            render_html_card(
                row.get("agent_name", "Unknown Agent"),
                (
                    f"<strong>{render_priority_label_text(priority)}</strong><br>"
                    f"{safe_display(row.get('recommended_action'))}<br>"
                    f"Reason: {safe_display(row.get('reason'))}<br>"
                    f"Issue: {safe_display(row.get('related_issue'))}"
                ),
                f"section-card {priority_class(priority)}",
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

agents = load_agent_registry(REGISTRY_PATH)
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

registry_df = as_dataframe(agents)

with st.sidebar:
    st.markdown("### AgentHub")
    st.write("Project Stage: HUB-005")
    st.write("Mode: Local Demo")
    st.write("API: Not required")
    st.write("Data Source: data/agent_registry.csv")
    st.write("External actions: Disabled")

    st.markdown("### Filters")
    category_options = ["All"] + sorted({agent.get("category", "") for agent in agents if agent.get("category")})
    status_options = ["All"] + sorted({agent.get("status", "") for agent in agents if agent.get("status")})
    pin_options = ["All"] + sorted({agent.get("pin_status", "") for agent in agents if agent.get("pin_status")})
    health_options = ["All"] + sorted({row.get("health_status", "") for row in health_results if row.get("health_status")})
    priority_options = ["All", "High", "Medium", "Low", "None"]

    category_filter = st.selectbox("Category", category_options, key="category_filter")
    status_filter = st.selectbox("Status", status_options, key="status_filter")
    pin_status_filter = st.selectbox("Pin Status", pin_options, key="pin_status_filter")
    health_status_filter = st.selectbox("Health Status", health_options, key="health_status_filter")
    action_priority_filter = st.selectbox("Action Priority", priority_options, key="action_priority_filter")

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
    """
    <div class="hero-card">
        <div class="hero-title">AgentHubControlCenter</div>
        <div class="hero-subtitle">Local-first AgentOps dashboard for AI workflow portfolios</div>
        <div class="hero-copy">
            Manage your AI agent ecosystem from one dashboard: registry, health checks,
            portfolio matrix, launch commands, and next-action planning.
        </div>
        <span class="badge">Local-first</span>
        <span class="badge">Agent registry</span>
        <span class="badge">Health checks</span>
        <span class="badge">PortfolioOps</span>
    </div>
    """,
    unsafe_allow_html=True,
)

render_metric_cards(
    [
        ("Total Agents", registry_summary["total_agents"]),
        ("Completed Agents", registry_summary["completed_agents"]),
        ("Public Showcase", registry_summary["public_showcase_agents"]),
        ("Pinned", registry_summary["pinned_agents"]),
        ("Public Not Pinned", registry_summary["public_not_pinned_agents"]),
        ("Paused / Complete", registry_summary["paused_or_completed_agents"]),
    ]
)

overview_tab, registry_tab, health_tab, matrix_tab, actions_tab, export_tab = st.tabs(
    [
        "Overview",
        "Agent Registry",
        "Health Check",
        "Portfolio Matrix",
        "Next Actions",
        "Export Report",
    ]
)

with overview_tab:
    st.markdown("## Overview")
    st.write("A portfolio command center view for registry status, local readiness, capability coverage, and planning.")

    st.markdown("### Command Center Summary")
    summary_left, summary_right = st.columns(2)
    with summary_left:
        render_html_card("Portfolio Overview", command_center_summary["portfolio_overview"])
        render_html_card("Health Snapshot", command_center_summary["health_snapshot"])
        render_html_card("Strategic Summary", command_center_summary["strategic_summary"])
    with summary_right:
        render_html_card("Showcase Status", command_center_summary["showcase_status"])
        render_html_card("Priority Actions", command_center_summary["priority_actions"])
        render_html_card("Next Best Move", command_center_summary["next_best_move"])

    render_html_card(
        "Portfolio Positioning",
        portfolio_positioning["positioning_statement"],
    )

    col_strengths, col_gaps = st.columns(2)
    with col_strengths:
        render_html_card(
            "Showcase Strengths",
            safe_list_join(portfolio_positioning["showcase_strengths"]),
        )
    with col_gaps:
        render_html_card(
            "Portfolio Gaps",
            safe_list_join(portfolio_positioning["portfolio_gaps"]),
        )

    st.markdown("### Capability Overview")
    capability_cols = st.columns(4)
    for index, item in enumerate(capability_summary):
        with capability_cols[index % 4]:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div class="mini-card-title">{item.get('category', 'Uncategorized')}</div>
                    <div class="mini-card-meta">
                        Agents: {item.get('agent_count', 0)}<br>
                        Showcase: {item.get('showcase_count', 0)}<br>
                        Pinned: {item.get('pinned_count', 0)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### Next Action Snapshot")
    render_metric_cards(
        [
            ("High", action_summary["high_priority"]),
            ("Medium", action_summary["medium_priority"]),
            ("Low", action_summary["low_priority"]),
            ("None", action_summary["no_action_needed"]),
        ]
    )

with registry_tab:
    st.markdown("## Agent Registry")
    st.write("Filtered registry view, agent detail panel, display-only command pack, and metadata validation.")

    registry_columns = [
        "agent_name",
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
        st.info("No agents match the selected registry filters.")
    else:
        st.markdown("### Registry Table")
        st.dataframe(
            filtered_registry_df[registry_columns],
            width="stretch",
            hide_index=True,
        )

        st.markdown("### Agent Detail Panel")
        selected_agent_name = st.selectbox(
            "Select agent",
            filtered_registry_df["agent_name"].tolist(),
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
            detail_cols[0].markdown(f"**{render_status_label_text(selected_agent.get('status', ''))}**")
            detail_cols[1].markdown(f"**Pin: {safe_display(selected_agent.get('pin_status'))}**")
            detail_cols[2].markdown(
                f"**{render_health_label_text(agent_health.get('health_status', ''))}**"
            )

            detail_left, detail_right = st.columns([1.2, 1])
            with detail_left:
                render_html_card(
                    "Capability",
                    truncate_text(selected_agent.get("primary_capability", ""), 260),
                )
                render_html_card(
                    "Portfolio Value",
                    truncate_text(selected_agent.get("portfolio_value", ""), 260),
                )
                render_html_card(
                    "Notes",
                    truncate_text(selected_agent.get("notes", ""), 220),
                )
            with detail_right:
                render_html_card("Tech Stack", safe_display(selected_agent.get("tech_stack")))
                render_html_card("Local Path", safe_display(selected_agent.get("local_path")))
                render_html_card(
                    "GitHub URL",
                    safe_display(build_open_github_command(selected_agent)),
                )

            st.markdown("### Command Pack Panel")
            render_command_pack(build_project_command_pack(selected_agent))

    st.markdown("### Registry Validation Table")
    validation_columns = [
        "agent_name",
        "is_valid",
        "quality_score",
        "missing_required_fields",
        "validation_notes",
    ]
    validation_df = display_dataframe(filtered_validation)
    if validation_df.empty:
        st.info("No validation rows match the selected registry filters.")
    else:
        st.dataframe(validation_df[validation_columns], width="stretch", hide_index=True)

with health_tab:
    st.markdown("## Health Check")
    st.write("Local filesystem readiness checks for public-showcase structure and documentation.")

    st.markdown("### Health Overview")
    render_metric_cards(
        [
            ("Showcase Ready", health_summary["Showcase Ready"]),
            ("Healthy", health_summary["Healthy"]),
            ("Partial", health_summary["Partial"]),
            ("Missing / Incomplete", health_summary["Missing or Incomplete"]),
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
    st.markdown("### Health Table")
    if health_df.empty:
        st.info("No health rows match the selected filters.")
    else:
        st.dataframe(health_df[health_columns], width="stretch", hide_index=True)

    st.markdown("### Health Detail")
    for result in filtered_health:
        with st.expander(f"{result.get('agent_name', 'Unknown Agent')} - {result.get('health_status', '')}"):
            st.write(f"Missing items: {safe_list_join(result.get('missing_items', []))}")
            st.write(f"Warnings: {safe_display(result.get('warnings'))}")
            st.write(f"Suggested fix: {safe_display(result.get('suggested_fix'))}")
            st.write(f"Last checked: {safe_display(result.get('last_checked_note'))}")

with matrix_tab:
    st.markdown("## Portfolio Matrix")
    st.write("Capability clusters, strongest categories, category cards, and portfolio gaps.")

    st.markdown("### Project Matrix View")
    matrix_cols = st.columns(2)
    for index, item in enumerate(project_matrix_view):
        project_names = [project.get("name", "") for project in item.get("projects", [])]
        projects_text = safe_list_join(project_names) if project_names else "No registered project yet."
        with matrix_cols[index % 2]:
            render_html_card(
                item.get("category_group", "Uncategorized"),
                (
                    f"<strong>Projects:</strong> {projects_text}<br>"
                    f"<strong>Status:</strong> {safe_display(item.get('status_summary'))}<br>"
                    f"<strong>Next:</strong> {safe_display(item.get('next_step'))}<br>"
                    f"<strong>Role:</strong> {safe_display(item.get('portfolio_role'))}"
                ),
            )

    st.markdown("### Capability Cluster Cards")
    cluster_items = list(portfolio_positioning["capability_clusters"].items())
    cluster_cols = st.columns(4)
    for index, (cluster, agent_names) in enumerate(cluster_items):
        with cluster_cols[index % 4]:
            st.markdown(
                f"""
                <div class="mini-card">
                    <div class="mini-card-title">{cluster}</div>
                    <div class="mini-card-meta">{safe_list_join(agent_names)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_html_card(
        "Strongest Categories",
        safe_list_join(portfolio_positioning["strongest_categories"]),
    )

    st.markdown("### Category Matrix")
    for item in capability_summary:
        render_html_card(
            item.get("category", "Uncategorized"),
            (
                f"Agents: {safe_list_join(item.get('agents', []))}<br>"
                f"Capabilities: {safe_list_join(item.get('capabilities', []))}<br>"
                f"Showcase count: {item.get('showcase_count', 0)} | "
                f"Pinned count: {item.get('pinned_count', 0)}"
            ),
        )

    st.markdown("### Portfolio Gaps")
    for gap in portfolio_positioning["portfolio_gaps"]:
        st.markdown(f'<div class="note-box">{gap}</div>', unsafe_allow_html=True)

with actions_tab:
    st.markdown("## Next Actions")
    st.write("Planning and tracking view for registry, health, screenshots, and pin decisions. No automation is executed.")

    st.markdown("### Priority Summary")
    render_metric_cards(
        [
            ("High", action_summary["high_priority"]),
            ("Medium", action_summary["medium_priority"]),
            ("Low", action_summary["low_priority"]),
            ("None", action_summary["no_action_needed"]),
        ]
    )

    priority_left, priority_right = st.columns(2)
    with priority_left:
        render_html_card(
            "Current Next Project",
            (
                f"{priority_summary['next_best_project']}<br>"
                f"{priority_summary['next_best_action']}"
            ),
        )
        render_html_card(
            "Paused Projects",
            safe_list_join(priority_summary["paused_projects"]),
        )
        render_html_card(
            "GitHub Showcase Projects",
            safe_list_join(priority_summary["github_showcase_projects"]),
        )
    with priority_right:
        commercial_names = [
            item.get("agent_name", "")
            for item in priority_summary["commercialization_candidates"]
        ]
        render_html_card(
            "Portfolio Follow-up",
            priority_summary["portfolio_follow_up"],
        )
        render_html_card(
            "Future Commercial Candidates",
            safe_list_join(commercial_names),
        )
        render_html_card(
            "Future AgentHub Integration",
            safe_list_join(priority_summary["agenthub_integration_candidates"]),
        )

    st.markdown(f'<div class="note-box">{priority_summary["pause_rule"]}</div>', unsafe_allow_html=True)

    action_columns = [
        "agent_name",
        "priority",
        "recommended_action",
        "reason",
        "category",
        "related_issue",
    ]
    action_df = display_dataframe(sorted_filtered_actions)
    st.markdown("### Action Plan Table")
    if action_df.empty:
        st.info("No action rows match the selected filters.")
    else:
        st.dataframe(action_df[action_columns], width="stretch", hide_index=True)

    st.markdown("### Action Cards")
    render_action_cards(sorted_filtered_actions)

with export_tab:
    st.markdown("## Export Report")
    st.write("Generate and preview the enhanced local Markdown report.")

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

    st.markdown("### Command Center Export Summary")
    render_metric_cards(
        [
            ("Tracked Agents", command_center_summary["tracked_agents"]),
            ("Public Showcase", command_center_summary["public_showcase_agents"]),
            ("Showcase Ready", command_center_summary["showcase_ready_agents"]),
            ("High Priority", command_center_summary["high_priority_actions"]),
        ]
    )

    render_html_card(
        "Report Summary",
        (
            f"Agents: {registry_summary['total_agents']} | "
            f"Actions: {action_summary['total_actions']} | "
            f"Showcase Ready: {health_summary['Showcase Ready']} | "
            f"Partial: {health_summary['Partial']} | "
            f"Missing / Incomplete: {health_summary['Missing or Incomplete']}"
        ),
    )

    st.markdown(f'<div class="disclaimer-box">{DISCLAIMER_TEXT}</div>', unsafe_allow_html=True)

    export_left, export_right = st.columns(2)
    with export_left:
        st.download_button(
            "Download Markdown Report",
            data=report,
            file_name=report_file_name,
            mime="text/markdown",
        )
    with export_right:
        if st.button("Save Report to Local Outputs"):
            try:
                saved_path = save_markdown_report(report, OUTPUTS_DIR, report_file_name)
                st.success(f"Saved local report: {saved_path}")
            except OSError as exc:
                st.error(f"Could not save local report: {exc}")

    st.caption("Saved reports stay local in outputs/ and are ignored by git except outputs/.gitkeep.")

    st.markdown("### Showcase Asset Checklist")
    st.dataframe(
        as_dataframe(showcase_asset_checklist),
        width="stretch",
        hide_index=True,
    )

    st.markdown("### Markdown Report Preview")
    st.markdown(report)
