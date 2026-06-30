from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SUMMARY_FIELDS = [
    "agent_id",
    "agent_name",
    "status",
    "demo_mode",
    "public_safe",
    "total_items_processed",
    "high_value_signals",
    "medium_value_items",
    "low_value_or_noise_items",
    "recommended_actions_count",
    "top_routes",
    "latest_report_path",
    "generated_at",
]


def resolve_agent_artifact_path(agent: dict[str, Any], path_field: str) -> Path | None:
    """Resolve a manifest-declared artifact path inside the Agent project folder."""

    raw_path = str(agent.get(path_field, "") or "").strip()
    local_path = str(agent.get("local_path", "") or "").strip()
    if not raw_path or not local_path:
        return None

    project_root = Path(local_path).resolve()
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    candidate = candidate.resolve()

    try:
        candidate.relative_to(project_root)
    except ValueError:
        return None
    return candidate


def read_agenthub_summary(agent: dict[str, Any]) -> dict[str, Any]:
    """Read an AgentHub summary JSON declared by an imported Agent manifest."""

    summary_path = resolve_agent_artifact_path(agent, "agenthub_summary_path")
    if summary_path is None:
        return {
            "available": False,
            "summary_path": "",
            "error": "No agenthub_summary_path declared.",
            "data": {},
        }
    if not summary_path.exists():
        return {
            "available": False,
            "summary_path": str(summary_path),
            "error": "Summary file does not exist.",
            "data": {},
        }

    try:
        data = json.loads(summary_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "available": False,
            "summary_path": str(summary_path),
            "error": f"Could not read summary JSON: {exc}",
            "data": {},
        }

    if not isinstance(data, dict):
        return {
            "available": False,
            "summary_path": str(summary_path),
            "error": "Summary root is not a JSON object.",
            "data": {},
        }

    return {
        "available": True,
        "summary_path": str(summary_path),
        "error": "",
        "data": data,
    }


def build_agent_summary_metrics(summary_data: dict[str, Any]) -> dict[str, Any]:
    """Build compact metric values for AgentHub UI display."""

    top_routes = summary_data.get("top_routes", {})
    top_route = "None"
    if isinstance(top_routes, dict) and top_routes:
        top_route = max(top_routes.items(), key=lambda item: item[1])[0]

    return {
        "total_items_processed": summary_data.get("total_items_processed", 0),
        "high_value_signals": summary_data.get("high_value_signals", 0),
        "medium_value_items": summary_data.get("medium_value_items", 0),
        "low_value_or_noise_items": summary_data.get("low_value_or_noise_items", 0),
        "recommended_actions_count": summary_data.get("recommended_actions_count", 0),
        "top_route": top_route,
        "latest_report_path": summary_data.get("latest_report_path", ""),
    }


def build_external_summary_index(agents: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Read available external AgentHub summaries and index them by agent_id."""

    summaries: dict[str, dict[str, Any]] = {}
    for agent in agents:
        agent_id = str(agent.get("agent_id", "") or "").strip()
        if not agent_id or not agent.get("agenthub_summary_path"):
            continue
        summary = read_agenthub_summary(agent)
        if summary.get("available"):
            summaries[agent_id] = summary
    return summaries


def build_summary_display_rows(summary_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Return UI-friendly rows for required summary fields."""

    return [
        {
            "field": field,
            "value": summary_data.get(field, ""),
        }
        for field in SUMMARY_FIELDS
    ]
