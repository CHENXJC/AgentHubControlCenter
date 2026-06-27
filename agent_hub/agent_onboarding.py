from __future__ import annotations

from pathlib import Path

from agent_hub.manifest_loader import scan_ai_projects_manifests


def _static_registry_record(agent: dict) -> dict:
    """Return a static registry record with source metadata."""
    record = dict(agent)
    record.setdefault("source", "static_registry")
    record.setdefault("manifest_path", "")
    return record


def merge_registry_with_manifest_records(
    static_agents: list[dict],
    manifest_records: list[dict],
) -> dict:
    """Merge CSV registry records with valid manifest records.

    Manifest records override static records with the same agent_id. Duplicate
    manifest IDs are not imported twice; the first manifest record is kept.
    """
    merged_by_id: dict[str, dict] = {}
    duplicate_rows: list[dict] = []

    for agent in static_agents:
        agent_id = agent.get("agent_id", "").strip()
        if not agent_id:
            continue
        merged_by_id[agent_id] = _static_registry_record(agent)

    for record in manifest_records:
        agent_id = record.get("agent_id", "").strip()
        if not agent_id:
            continue

        existing = merged_by_id.get(agent_id)
        if existing:
            duplicate_rows.append(
                {
                    "agent_id": agent_id,
                    "existing_agent_name": existing.get("agent_name", ""),
                    "existing_source": existing.get("source", "static_registry"),
                    "incoming_agent_name": record.get("agent_name", ""),
                    "incoming_source": record.get("source", "local_manifest"),
                    "resolution": (
                        "manifest_overrides_static_registry"
                        if existing.get("source") == "static_registry"
                        else "first_manifest_kept"
                    ),
                }
            )

        if existing and existing.get("source") != "static_registry":
            continue

        merged_record = dict(record)
        merged_record["duplicate_agent_id"] = bool(existing)
        merged_record["source_note"] = (
            "Manifest data overrides static registry data."
            if existing
            else "Imported from local manifest discovery."
        )
        merged_by_id[agent_id] = merged_record

    merged_agents = sorted(
        merged_by_id.values(),
        key=lambda item: item.get("agent_name", "").lower(),
    )
    return {
        "merged_agents": merged_agents,
        "duplicate_agent_ids": duplicate_rows,
        "imported_agents": [item for item in merged_agents if item.get("source") != "static_registry"],
    }


def build_onboarding_project_rows(project_results: list[dict]) -> list[dict]:
    """Build UI-friendly project discovery rows."""
    rows = []
    for result in project_results:
        imported_names = [
            record.get("agent_name", "")
            for record in result.get("valid_agent_records", [])
        ]
        invalid_names = [
            item.get("agent_name", "")
            for item in result.get("invalid_agent_records", [])
        ]
        rows.append(
            {
                "project_name": result.get("project_name", ""),
                "manifest_status": result.get("manifest_status", ""),
                "source": result.get("source", ""),
                "imported_agents": imported_names,
                "invalid_agents": invalid_names,
                "warnings": result.get("warnings", []),
                "recommended_fix": result.get("recommended_fix", ""),
                "project_path": result.get("project_path", ""),
                "manifest_path": result.get("manifest_path", ""),
            }
        )
    return rows


def build_onboarding_summary(
    scan_summary: dict,
    imported_agents: list[dict],
    duplicate_agent_ids: list[dict],
    project_rows: list[dict],
) -> dict:
    """Build aggregate onboarding metrics and recommendations."""
    invalid_rows = [row for row in project_rows if row["manifest_status"] == "invalid"]
    missing_rows = [row for row in project_rows if row["manifest_status"] == "missing"]
    static_override_rows = [
        row
        for row in duplicate_agent_ids
        if row.get("resolution") == "manifest_overrides_static_registry"
    ]
    actionable_duplicate_rows = [
        row
        for row in duplicate_agent_ids
        if row.get("resolution") != "manifest_overrides_static_registry"
    ]
    recommended_fixes = []

    if missing_rows:
        recommended_fixes.append(
            f"Add agent_manifest.json to {len(missing_rows)} project(s) that are missing one."
        )
    if invalid_rows:
        recommended_fixes.append(
            f"Fix {len(invalid_rows)} invalid manifest file(s) before import."
        )
    if actionable_duplicate_rows:
        recommended_fixes.append(
            f"Review {len(actionable_duplicate_rows)} duplicate agent_id conflict(s)."
        )
    if static_override_rows:
        recommended_fixes.append(
            f"{len(static_override_rows)} static registry record(s) are overridden by local manifests; no manifest fix is required."
        )
    if not recommended_fixes:
        recommended_fixes.append("All discovered manifests are ready for onboarding.")

    return {
        "total_projects_scanned": scan_summary.get("total_projects_scanned", 0),
        "manifests_found": scan_summary.get("manifests_found", 0),
        "valid_manifests": scan_summary.get("valid_manifests", 0),
        "invalid_manifests": scan_summary.get("invalid_manifests", 0),
        "missing_manifests": scan_summary.get("missing_manifests", 0),
        "imported_agents": len(imported_agents),
        "duplicate_agent_ids": len(duplicate_agent_ids),
        "recommended_fixes": recommended_fixes,
    }


def build_agent_onboarding(
    ai_projects_root: str | Path,
    static_agents: list[dict],
) -> dict:
    """Build the full HUB-V2-002 onboarding model for app/UI use."""
    scan_result = scan_ai_projects_manifests(ai_projects_root)
    merge_result = merge_registry_with_manifest_records(
        static_agents,
        scan_result["valid_registry_records"],
    )
    project_rows = build_onboarding_project_rows(scan_result["project_results"])
    summary = build_onboarding_summary(
        scan_result["summary"],
        merge_result["imported_agents"],
        merge_result["duplicate_agent_ids"],
        project_rows,
    )

    return {
        "ai_projects_root": str(Path(ai_projects_root)),
        "summary": summary,
        "project_rows": project_rows,
        "merged_agents": merge_result["merged_agents"],
        "imported_agents": merge_result["imported_agents"],
        "duplicate_agent_ids": merge_result["duplicate_agent_ids"],
        "valid_manifest_records": scan_result["valid_registry_records"],
        "missing_manifest_projects": [
            row for row in project_rows if row["manifest_status"] == "missing"
        ],
        "invalid_manifest_projects": [
            row for row in project_rows if row["manifest_status"] == "invalid"
        ],
    }
