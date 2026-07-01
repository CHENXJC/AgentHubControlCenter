from __future__ import annotations

import json
from pathlib import Path
from typing import Any


WORKFLOW_PACK_AGENT_ROOT = Path("F:/AIProjects/WorkflowPackAgent")
DEFAULT_AGENTHUB_SUMMARY_PATH = WORKFLOW_PACK_AGENT_ROOT / "outputs" / "agenthub_summary.json"
DEFAULT_WORKFLOW_PACK_SUMMARY_PATH = WORKFLOW_PACK_AGENT_ROOT / "outputs" / "workflow_pack_summary.json"
ALLOWED_SUMMARY_FILENAMES = {"agenthub_summary.json", "workflow_pack_summary.json"}


def _empty_summary(path: str | Path, status: str, details: str) -> dict[str, Any]:
    return {
        "integration_status": status,
        "summary_path": str(path),
        "details": details,
        "data": {},
    }


def _load_json_summary(summary_path: str | Path, expected_filename: str) -> dict[str, Any]:
    path = Path(summary_path)
    if expected_filename not in ALLOWED_SUMMARY_FILENAMES or path.name != expected_filename:
        return _empty_summary(path, "invalid", "Summary path is not an allowed WorkflowPackAgent JSON summary file.")
    if not path.exists():
        return _empty_summary(path, "missing", "WorkflowPackAgent summary file is missing.")
    if not path.is_file():
        return _empty_summary(path, "invalid", "WorkflowPackAgent summary path is not a file.")

    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return _empty_summary(path, "invalid", f"WorkflowPackAgent summary JSON is invalid: {exc}")

    if not isinstance(data, dict):
        return _empty_summary(path, "invalid", "WorkflowPackAgent summary root is not a JSON object.")

    return {
        "integration_status": "available",
        "summary_path": str(path),
        "details": "WorkflowPackAgent JSON summary loaded.",
        "data": data,
    }


def load_workflow_pack_agent_summary(
    summary_path: str | Path = DEFAULT_AGENTHUB_SUMMARY_PATH,
) -> dict[str, Any]:
    return _load_json_summary(summary_path, "agenthub_summary.json")


def load_workflow_pack_summary(
    summary_path: str | Path = DEFAULT_WORKFLOW_PACK_SUMMARY_PATH,
) -> dict[str, Any]:
    return _load_json_summary(summary_path, "workflow_pack_summary.json")


def _first_available(*values: Any, fallback: Any = None) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return fallback


def _top_workflow_packs(agenthub_data: dict[str, Any], workflow_data: dict[str, Any]) -> list[dict[str, Any]]:
    top_packs = _first_available(
        agenthub_data.get("top_workflow_packs"),
        workflow_data.get("top_workflow_packs"),
        fallback=[],
    )
    if isinstance(top_packs, list):
        return [pack for pack in top_packs if isinstance(pack, dict)][:5]

    top_pack = workflow_data.get("top_pack")
    return [top_pack] if isinstance(top_pack, dict) else []


def build_workflow_pack_integration_card(
    agenthub_summary: dict[str, Any],
    workflow_pack_summary: dict[str, Any],
) -> dict[str, Any]:
    agenthub_status = agenthub_summary.get("integration_status", "missing")
    workflow_status = workflow_pack_summary.get("integration_status", "missing")
    agenthub_data = agenthub_summary.get("data", {}) if isinstance(agenthub_summary.get("data"), dict) else {}
    workflow_data = workflow_pack_summary.get("data", {}) if isinstance(workflow_pack_summary.get("data"), dict) else {}

    integration_status = "available"
    if agenthub_status == "invalid" or workflow_status == "invalid":
        integration_status = "invalid"
    elif agenthub_status != "available":
        integration_status = "missing"

    metadata_enriched_agents = _first_available(
        agenthub_data.get("metadata_enriched_agents"),
        workflow_data.get("metadata_enriched_agents"),
        fallback=[],
    )
    if not isinstance(metadata_enriched_agents, list):
        metadata_enriched_agents = []

    source_metadata_stats = _first_available(
        agenthub_data.get("source_metadata_stats"),
        workflow_data.get("source_metadata_stats"),
        fallback={},
    )
    if not isinstance(source_metadata_stats, dict):
        source_metadata_stats = {}

    return {
        "integration_status": integration_status,
        "agent_name": _first_available(agenthub_data.get("agent_name"), "WorkflowPackAgent"),
        "project_code": _first_available(agenthub_data.get("project_code"), "WPA-004"),
        "total_workflow_packs": _first_available(
            agenthub_data.get("total_workflow_packs"),
            workflow_data.get("total_packs"),
            fallback=0,
        ),
        "metadata_enriched_agents": len(metadata_enriched_agents),
        "metadata_enriched_agent_names": metadata_enriched_agents,
        "safe_metadata_integration": bool(
            _first_available(
                agenthub_data.get("safe_metadata_integration"),
                workflow_data.get("safe_metadata_integration"),
                fallback=False,
            )
        ),
        "top_workflow_packs": _top_workflow_packs(agenthub_data, workflow_data)[:3],
        "source_metadata_stats": source_metadata_stats,
        "recommended_next_actions": agenthub_data.get("recommended_next_actions", []),
        "summary_path": agenthub_summary.get("summary_path", ""),
        "workflow_pack_summary_path": workflow_pack_summary.get("summary_path", ""),
        "dashboard_hint": agenthub_data.get(
            "dashboard_hint",
            "WorkflowPackAgent turns existing agents into reusable client-ready workflow packs.",
        ),
        "showcase_summary": agenthub_data.get("showcase_summary", ""),
        "details": agenthub_summary.get("details") or workflow_pack_summary.get("details") or "",
        "safety_note": "Only local JSON summaries are read. No private files, credentials, APIs, or external network access are used.",
    }


def get_workflow_pack_integration_status(
    agenthub_summary_path: str | Path = DEFAULT_AGENTHUB_SUMMARY_PATH,
    workflow_pack_summary_path: str | Path = DEFAULT_WORKFLOW_PACK_SUMMARY_PATH,
) -> dict[str, Any]:
    agenthub_summary = load_workflow_pack_agent_summary(agenthub_summary_path)
    workflow_pack_summary = load_workflow_pack_summary(workflow_pack_summary_path)
    return build_workflow_pack_integration_card(agenthub_summary, workflow_pack_summary)
