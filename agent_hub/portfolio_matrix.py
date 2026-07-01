from __future__ import annotations


PROJECT_MATRIX_GROUPS = [
    {
        "category_group": "Finance / Market",
        "categories": {"Finance Automation", "Quant Research", "market_intelligence", "quant_research"},
        "portfolio_role": "Market monitoring, quant research, and financial education showcase.",
        "empty_next_step": "No finance or market project is registered yet.",
    },
    {
        "category_group": "Media / OCR / Extraction",
        "categories": {"Media Intelligence", "content_intelligence"},
        "portfolio_role": "Multimodal extraction, OCR, transcription, and structured report workflow.",
        "empty_next_step": "No media extraction project is registered yet.",
    },
    {
        "category_group": "Career",
        "categories": {"Career Automation", "career_operations"},
        "portfolio_role": "Career workflow planning and job-search support.",
        "empty_next_step": "No career workflow project is registered yet.",
    },
    {
        "category_group": "News / Signal",
        "categories": {"News Intelligence", "news_intelligence"},
        "portfolio_role": "News signal extraction and structured intelligence analysis.",
        "empty_next_step": "No news signal project is registered yet.",
    },
    {
        "category_group": "SME Automation",
        "categories": {
            "Business Discovery",
            "Business Operations",
            "Workflow Automation",
            "opportunity_discovery",
            "sme_operations",
            "idea_validation",
        },
        "portfolio_role": "SME workflow diagnosis, operations analysis, and business opportunity scoring.",
        "empty_next_step": "No SME automation project is registered yet.",
    },
    {
        "category_group": "Client Delivery / AI Consulting",
        "categories": {
            "client_delivery",
            "Client Delivery",
            "Client delivery / AI automation consulting",
        },
        "portfolio_role": "Client-facing AI automation consulting delivery workflow and report packaging.",
        "empty_next_step": "No client delivery project is registered yet.",
    },
    {
        "category_group": "Knowledge Base",
        "categories": {"Knowledge Base", "knowledge_management"},
        "portfolio_role": "Future local personal knowledge base and retrieval workflow.",
        "empty_next_step": "Future candidate. Keep it as a portfolio gap until the current showcase pass is complete.",
    },
    {
        "category_group": "Data Workflow / Insight Engine",
        "categories": {"Data Workflow / Insight Engine", "data_workflow", "insight_engine"},
        "portfolio_role": "Data-to-insight workflow, value scoring, action recommendations, and AgentHub-ready reporting.",
        "empty_next_step": "No data workflow insight engine is registered yet.",
    },
    {
        "category_group": "Workflow Orchestration / AgentOps",
        "categories": {
            "Workflow Orchestration / AgentOps / Project Command",
            "workflow-orchestration",
            "workflow_orchestration",
            "project-execution-command-center",
        },
        "portfolio_role": "Project execution command systems for Codex-ready instructions, workflow packs, checklists, and delivery reports.",
        "empty_next_step": "No workflow orchestration command project is registered yet.",
    },
    {
        "category_group": "Control Center / Meta Agent",
        "categories": {"Control Center", "Meta Agent", "AgentOps / PortfolioOps", "agent_ops"},
        "portfolio_role": "Portfolio command center, AgentOps dashboard, and project matrix hub.",
        "empty_next_step": "Continue AgentHubControlCenter as the central portfolio command center.",
    },
]

CONTROL_CENTER_VIRTUAL_PROJECT = {
    "agent_name": "AgentHubControlCenter",
    "category": "Control Center / Meta Agent",
    "status": "In Progress",
    "stage": "HUB-V2-009",
    "showcase_status": "GitHub Public Showcase + V2 Local Upgrade",
    "pin_status": "Not pinned",
    "next_action": "HUB-V2-010 Demo Workflow Report Export",
    "portfolio_value": "Shows how the AI Agent portfolio can be managed from one local-first personal command center.",
}


def _is_public_showcase(agent: dict) -> bool:
    public_statuses = {
        "github public showcase",
        "live_showcase_verified",
        "public_repo_first_commit_complete",
        "public showcase verified",
        "published public showcase",
    }
    return agent.get("showcase_status", "").strip().lower() in public_statuses


def _is_pinned(agent: dict) -> bool:
    return agent.get("pin_status", "").strip().lower() == "pinned"


def _is_paused(agent: dict) -> bool:
    return "paused" in agent.get("next_action", "").strip().lower()


def build_category_matrix(agents: list[dict]) -> dict:
    """Group registered agents by category."""
    matrix: dict[str, list[dict]] = {}
    for agent in agents:
        category = agent.get("category", "").strip() or "Uncategorized"
        matrix.setdefault(category, []).append(agent)
    return matrix


def build_capability_summary(agents: list[dict]) -> list[dict]:
    """Summarize capabilities and showcase status for each category."""
    matrix = build_category_matrix(agents)
    summary = []

    for category, category_agents in matrix.items():
        summary.append(
            {
                "category": category,
                "agent_count": len(category_agents),
                "agents": [agent.get("agent_name", "") for agent in category_agents],
                "capabilities": [
                    agent.get("primary_capability", "")
                    for agent in category_agents
                    if agent.get("primary_capability", "")
                ],
                "showcase_count": sum(
                    1 for agent in category_agents if _is_public_showcase(agent)
                ),
                "pinned_count": sum(
                    1 for agent in category_agents if _is_pinned(agent)
                ),
            }
        )

    return summary


def _build_project_display(agent: dict) -> dict:
    """Create a compact project card for the fixed portfolio matrix."""
    return {
        "name": agent.get("agent_name", ""),
        "status": agent.get("status", ""),
        "showcase_status": agent.get("showcase_status", ""),
        "pin_status": agent.get("pin_status", ""),
        "next_action": agent.get("next_action", ""),
        "public_value": agent.get("portfolio_value", ""),
    }


def _summarize_group_status(group_agents: list[dict]) -> str:
    """Summarize one matrix group in product-dashboard language."""
    if not group_agents:
        return "No registered project yet."

    complete_count = sum(
        1 for agent in group_agents if agent.get("status", "").strip().lower() == "complete"
    )
    public_count = sum(1 for agent in group_agents if _is_public_showcase(agent))
    pinned_count = sum(1 for agent in group_agents if _is_pinned(agent))
    paused_count = sum(1 for agent in group_agents if _is_paused(agent))

    return (
        f"{len(group_agents)} project(s): {complete_count} complete, "
        f"{public_count} public showcase, {pinned_count} pinned, {paused_count} paused."
    )


def _summarize_group_next_step(
    category_group: str,
    group_agents: list[dict],
    empty_next_step: str,
) -> str:
    """Choose a matrix-level next step without expanding paused showcase projects."""
    if not group_agents:
        return empty_next_step

    if category_group == "Control Center / Meta Agent":
        return "Use HUB-V2-009 Local Workflow Simulation + Approval Gates as the safety design layer; next recommended stage is HUB-V2-010 demo workflow report export."

    for agent in group_agents:
        next_action = agent.get("next_action", "").strip()
        notes = agent.get("notes", "").strip()
        combined_text = f"{next_action} {notes}".lower()
        if "screenshots pending" in combined_text:
            return f"Complete public-safe screenshots for {agent.get('agent_name', '')}."

    for agent in group_agents:
        if _is_public_showcase(agent) and not _is_pinned(agent):
            return (
                f"Review GitHub profile pin decision for {agent.get('agent_name', '')}; "
                "do not expand features unless explicitly requested."
            )

    if all(_is_paused(agent) or (_is_public_showcase(agent) and _is_pinned(agent)) for agent in group_agents):
        return "Paused after public showcase/profile pin; no immediate expansion needed."

    return group_agents[0].get("next_action", "") or "Review next action after current showcase pass."


def build_project_matrix_view(agents: list[dict]) -> list[dict]:
    """Build the fixed portfolio matrix requested for the command center UI."""
    rows = []
    for group in PROJECT_MATRIX_GROUPS:
        group_agents = [
            agent
            for agent in agents
            if agent.get("category", "").strip() in group["categories"]
        ]
        has_control_center = any(
            agent.get("agent_name", "").strip() == CONTROL_CENTER_VIRTUAL_PROJECT["agent_name"]
            for agent in group_agents
        )
        if group["category_group"] == "Control Center / Meta Agent" and not has_control_center:
            group_agents = group_agents + [CONTROL_CENTER_VIRTUAL_PROJECT]

        rows.append(
            {
                "category_group": group["category_group"],
                "projects": [_build_project_display(agent) for agent in group_agents],
                "status_summary": _summarize_group_status(group_agents),
                "next_step": _summarize_group_next_step(
                    group["category_group"],
                    group_agents,
                    group["empty_next_step"],
                ),
                "portfolio_role": group["portfolio_role"],
            }
        )

    return rows


def build_priority_summary(agents: list[dict], action_plan: list[dict]) -> dict:
    """Build strategic portfolio priorities for the command center dashboard/report use."""
    actionable_items = [item for item in action_plan if item.get("priority") != "None"]
    top_action = actionable_items[0] if actionable_items else {}
    paused_projects = [
        agent.get("agent_name", "")
        for agent in agents
        if _is_paused(agent) or (_is_public_showcase(agent) and _is_pinned(agent))
    ]
    commercialization_categories = {
        "Business Discovery",
        "Business Operations",
        "Workflow Automation",
        "Media Intelligence",
        "opportunity_discovery",
        "sme_operations",
        "content_intelligence",
        "idea_validation",
    }
    commercialization_candidates = [
        {
            "agent_name": agent.get("agent_name", ""),
            "category": agent.get("category", ""),
            "reason": (
                "Future service/product candidate. Keep the GitHub portfolio version paused "
                "until a separate commercial stage is explicitly started."
            ),
        }
        for agent in agents
        if agent.get("category", "") in commercialization_categories
    ]
    github_showcase_projects = [
        agent.get("agent_name", "") for agent in agents if _is_public_showcase(agent)
    ]
    agenthub_integration_candidates = [
        agent.get("agent_name", "")
        for agent in agents
        if agent.get("status", "").strip().lower() == "complete"
    ]

    portfolio_follow_up = "No urgent child-project action."
    if top_action:
        portfolio_follow_up = (
            f"{top_action.get('agent_name', '')}: {top_action.get('recommended_action', '')}"
        )

    return {
        "next_best_project": "AgentHubControlCenter",
        "next_best_action": "HUB-V2-009 Local Workflow Simulation + Approval Gates",
        "portfolio_follow_up": portfolio_follow_up,
        "paused_projects": paused_projects,
        "commercialization_candidates": commercialization_candidates,
        "github_showcase_projects": github_showcase_projects,
        "agenthub_integration_candidates": agenthub_integration_candidates,
        "pause_rule": (
            "Projects that reached GitHub Public Showcase and Profile Pin stay paused "
            "unless a new stage is explicitly requested."
        ),
    }


def build_portfolio_positioning(agents: list[dict]) -> dict:
    """Build a high-level positioning summary for the portfolio ecosystem."""
    category_matrix = build_category_matrix(agents)
    category_counts = {
        category: len(category_agents)
        for category, category_agents in category_matrix.items()
    }
    strongest_categories = [
        category
        for category, _count in sorted(
            category_counts.items(),
            key=lambda item: (-item[1], item[0]),
        )[:3]
    ]

    capability_clusters = {
        "Media Intelligence": [],
        "Finance & Quant Research": [],
        "Business Discovery": [],
        "Workflow Automation": [],
        "Career Automation": [],
        "News Intelligence": [],
        "Business Operations": [],
        "Client Delivery": [],
        "Data Workflow / Insight Engine": [],
        "Workflow Orchestration / Project Command": [],
        "AgentOps / PortfolioOps": ["AgentHubControlCenter"],
    }

    for agent in agents:
        name = agent.get("agent_name", "")
        category = agent.get("category", "")
        if category in {"Media Intelligence", "content_intelligence"}:
            capability_clusters["Media Intelligence"].append(name)
        elif category in {"Finance Automation", "Quant Research", "market_intelligence", "quant_research"}:
            capability_clusters["Finance & Quant Research"].append(name)
        elif category in {"Business Discovery", "opportunity_discovery", "idea_validation"}:
            capability_clusters["Business Discovery"].append(name)
        elif category in {"Workflow Automation", "sme_operations"}:
            capability_clusters["Workflow Automation"].append(name)
        elif category in {"Career Automation", "career_operations"}:
            capability_clusters["Career Automation"].append(name)
        elif category in {"News Intelligence", "news_intelligence"}:
            capability_clusters["News Intelligence"].append(name)
        elif category in {"Business Operations", "sme_operations"}:
            capability_clusters["Business Operations"].append(name)
        elif category in {"client_delivery", "Client Delivery", "Client delivery / AI automation consulting"}:
            capability_clusters["Client Delivery"].append(name)
        elif category in {"Knowledge Base", "knowledge_management"}:
            capability_clusters.setdefault("Knowledge Management", []).append(name)
        elif category in {"Data Workflow / Insight Engine", "data_workflow", "insight_engine"}:
            capability_clusters["Data Workflow / Insight Engine"].append(name)
        elif category in {
            "Workflow Orchestration / AgentOps / Project Command",
            "workflow-orchestration",
            "workflow_orchestration",
            "project-execution-command-center",
        }:
            capability_clusters["Workflow Orchestration / Project Command"].append(name)

    showcase_strengths = [
        "Local-first AI workflows",
        "Streamlit dashboards",
        "Business-oriented automation",
        "Report generation",
        "Finance and market analysis",
        "Workflow diagnosis",
    ]

    portfolio_gaps = [
        "Knowledge base workflow not yet represented as a dedicated project",
        "AI persona / avatar content workflow pending",
        "Multi-agent orchestration still early-stage",
        "Production deployment not yet included",
        "Real client case studies not included",
    ]

    return {
        "positioning_statement": (
            "AgentHubControlCenter frames the portfolio as a local-first AI Agent "
            "and Skill ecosystem spanning media intelligence, finance research, "
            "business discovery, workflow automation, news analysis, career workflows, "
            "and AgentOps / PortfolioOps management."
        ),
        "capability_clusters": capability_clusters,
        "strongest_categories": strongest_categories,
        "showcase_strengths": showcase_strengths,
        "portfolio_gaps": portfolio_gaps,
    }
