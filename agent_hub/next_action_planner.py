from __future__ import annotations


PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2, "None": 3}


def _by_agent_name(rows: list[dict]) -> dict:
    """Index dictionaries by agent name."""
    return {row.get("agent_name", ""): row for row in rows}


def build_next_action_plan(
    agents: list[dict],
    health_results: list[dict],
    validation_results: list[dict],
) -> list[dict]:
    """Build prioritized next actions from registry, health, and validation data."""
    health_by_name = _by_agent_name(health_results)
    validation_by_name = _by_agent_name(validation_results)
    action_plan = []

    for agent in agents:
        agent_name = agent.get("agent_name", "")
        health = health_by_name.get(agent_name, {})
        validation = validation_by_name.get(agent_name, {})
        status = agent.get("status", "")
        health_status = health.get("health_status", "")
        next_action = agent.get("next_action", "").lower()
        pin_status = agent.get("pin_status", "").lower()

        priority = "None"
        recommended_action = "No immediate action"
        reason = "Project is complete and showcase-ready."
        related_issue = ""

        if validation and not validation.get("is_valid", False):
            priority = "High"
            recommended_action = "Fix registry metadata"
            reason = "Registry validation failed."
            related_issue = ", ".join(validation.get("missing_required_fields", [])) or "Low quality score"
        elif health_status == "Missing or Incomplete":
            priority = "High"
            recommended_action = "Fix local project path or missing core files"
            reason = "Health check found missing local project structure."
            related_issue = ", ".join(health.get("missing_items", []))
        elif health_status == "Partial":
            priority = "Medium"
            recommended_action = "Complete missing project structure files"
            reason = "Health check is partial."
            related_issue = ", ".join(health.get("missing_items", []))
        elif "screenshots pending" in next_action:
            priority = "Medium"
            recommended_action = "Capture showcase screenshots"
            reason = "Next action indicates screenshot work is pending."
            related_issue = agent.get("next_action", "")
        elif "not pinned" in pin_status or "pin pending" in pin_status:
            priority = "Low"
            recommended_action = "Review GitHub profile pin decision"
            reason = "Pin status is not finalized."
            related_issue = agent.get("pin_status", "")
        elif status.lower() == "complete" and health_status == "Showcase Ready":
            priority = "None"
            recommended_action = "No immediate action"
            reason = "Agent is complete and showcase-ready."
            related_issue = ""

        action_plan.append(
            {
                "agent_name": agent_name,
                "current_status": status,
                "priority": priority,
                "recommended_action": recommended_action,
                "reason": reason,
                "category": agent.get("category", ""),
                "related_issue": related_issue,
            }
        )

    return sorted(action_plan, key=lambda item: (PRIORITY_ORDER[item["priority"]], item["agent_name"]))


def summarize_next_actions(action_plan: list[dict]) -> dict:
    """Summarize next-action priorities and top recommendations."""
    actionable = [item for item in action_plan if item.get("priority") != "None"]
    top_recommendations = []
    for item in actionable[:5]:
        top_recommendations.append(
            f"{item.get('agent_name', '')}: {item.get('recommended_action', '')}"
        )

    return {
        "total_actions": len(actionable),
        "high_priority": sum(1 for item in action_plan if item.get("priority") == "High"),
        "medium_priority": sum(1 for item in action_plan if item.get("priority") == "Medium"),
        "low_priority": sum(1 for item in action_plan if item.get("priority") == "Low"),
        "no_action_needed": sum(1 for item in action_plan if item.get("priority") == "None"),
        "top_recommendations": top_recommendations,
    }
