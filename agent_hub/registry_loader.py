from __future__ import annotations

import csv
from pathlib import Path


REQUIRED_REGISTRY_FIELDS = [
    "agent_id",
    "agent_name",
    "category",
    "project_type",
    "local_path",
    "github_url",
    "status",
    "stage",
    "primary_capability",
    "tech_stack",
    "run_command",
    "portfolio_value",
    "next_action",
    "showcase_status",
    "pin_status",
]


def load_agent_registry(csv_path: str | Path = "data/agent_registry.csv") -> list[dict]:
    """Load the local agent registry CSV as a list of dictionaries."""
    path = Path(csv_path)
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as registry_file:
        reader = csv.DictReader(registry_file)
        rows: list[dict] = []
        for row in reader:
            clean_row = {}
            for key, value in row.items():
                clean_key = key.strip() if key else ""
                clean_value = value.strip() if isinstance(value, str) else value
                clean_row[clean_key] = clean_value
            rows.append(clean_row)
    return rows


def _count_by_field(agents: list[dict], field_name: str) -> dict:
    """Count non-empty registry values for one field."""
    counts: dict[str, int] = {}
    for agent in agents:
        value = agent.get(field_name, "").strip()
        if value:
            counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def validate_agent_record(agent: dict) -> dict:
    """Validate one registry record and calculate a metadata quality score."""
    agent_name = agent.get("agent_name", "").strip() or "Unknown Agent"
    missing_required_fields = [
        field for field in REQUIRED_REGISTRY_FIELDS if not agent.get(field, "").strip()
    ]
    warning_fields: list[str] = []
    validation_notes: list[str] = []
    quality_score = 100

    if missing_required_fields:
        quality_score -= len(missing_required_fields) * 8
        validation_notes.append(
            "Missing required fields: " + ", ".join(missing_required_fields)
        )

    github_url = agent.get("github_url", "").strip()
    local_path = agent.get("local_path", "").strip()
    portfolio_value = agent.get("portfolio_value", "").strip()
    primary_capability = agent.get("primary_capability", "").strip()
    stage = agent.get("stage", "").strip()

    if not github_url:
        quality_score -= 10
        warning_fields.append("github_url")
        validation_notes.append("GitHub URL is empty.")
    if not local_path:
        quality_score -= 10
        warning_fields.append("local_path")
        validation_notes.append("Local path is empty.")
    if len(portfolio_value) < 20:
        quality_score -= 10
        warning_fields.append("portfolio_value")
        validation_notes.append("Portfolio value should be more descriptive.")
    if len(primary_capability) < 20:
        quality_score -= 10
        warning_fields.append("primary_capability")
        validation_notes.append("Primary capability should be more descriptive.")
    if not stage:
        quality_score -= 8
        warning_fields.append("stage")
        validation_notes.append("Stage is empty.")

    quality_score = max(0, quality_score)
    is_valid = quality_score >= 70 and not missing_required_fields

    if not validation_notes:
        validation_notes.append("Registry metadata looks complete.")

    return {
        "agent_name": agent_name,
        "is_valid": is_valid,
        "missing_required_fields": missing_required_fields,
        "warning_fields": sorted(set(warning_fields)),
        "quality_score": quality_score,
        "validation_notes": validation_notes,
    }


def validate_registry(agents: list[dict]) -> list[dict]:
    """Validate every record in the local agent registry."""
    return [validate_agent_record(agent) for agent in agents]


def get_registry_summary(agents: list[dict]) -> dict:
    """Return high-level counts for the local agent registry."""
    categories = sorted(
        {
            agent.get("category", "").strip()
            for agent in agents
            if agent.get("category", "").strip()
        }
    )
    completed_agents = sum(
        1 for agent in agents if agent.get("status", "").strip().lower() == "complete"
    )
    paused_agents = sum(
        1 for agent in agents if "paused" in agent.get("next_action", "").strip().lower()
    )
    pinned_agents = sum(
        1 for agent in agents if agent.get("pin_status", "").strip().lower() == "pinned"
    )
    public_showcase_agents = [
        agent
        for agent in agents
        if agent.get("showcase_status", "").strip().lower() == "github public showcase"
    ]
    public_not_pinned_agents = sum(
        1
        for agent in public_showcase_agents
        if agent.get("pin_status", "").strip().lower() != "pinned"
    )
    paused_or_completed_agents = sum(
        1
        for agent in agents
        if agent.get("status", "").strip().lower() == "complete"
        or "paused" in agent.get("next_action", "").strip().lower()
    )

    return {
        "total_agents": len(agents),
        "completed_agents": completed_agents,
        "active_agents": sum(
            1 for agent in agents if "active" in agent.get("status", "").strip().lower()
        ),
        "paused_agents": paused_agents,
        "pinned_agents": pinned_agents,
        "public_showcase_agents": len(public_showcase_agents),
        "public_not_pinned_agents": public_not_pinned_agents,
        "paused_or_completed_agents": paused_or_completed_agents,
        "categories": categories,
        "categories_count": len(categories),
        "project_types_count": _count_by_field(agents, "project_type"),
        "pin_pending_agents": sum(
            1
            for agent in agents
            if "pin pending" in agent.get("pin_status", "").strip().lower()
        ),
        "screenshot_pending_agents": sum(
            1
            for agent in agents
            if "screenshots pending" in agent.get("next_action", "").strip().lower()
            or "screenshots pending" in agent.get("notes", "").strip().lower()
        ),
        "next_actions_count": _count_by_field(agents, "next_action"),
    }
