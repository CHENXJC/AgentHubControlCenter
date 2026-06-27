from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_MANIFEST_FIELDS = [
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

OPTIONAL_MANIFEST_FIELDS = [
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

SKIP_DIRECTORY_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "outputs",
    "private_outputs",
    "private",
    "secrets",
}


def _string_value(value: Any) -> str:
    """Return stripped string values for registry fields."""
    return value.strip() if isinstance(value, str) else ""


def _list_value(values: Any) -> list[str]:
    """Format manifest list values into compact registry strings."""
    if not isinstance(values, list):
        return []
    formatted = []
    for value in values:
        if isinstance(value, str):
            formatted.append(value.strip())
        elif isinstance(value, dict):
            label = value.get("label") or value.get("action_id") or value.get("connector_id")
            if label:
                formatted.append(str(label).strip())
    return [value for value in formatted if value]


def _is_missing_value(value: Any) -> bool:
    """Return whether a manifest field should count as missing."""
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list):
        return len(value) == 0
    return False


def is_safe_project_dir(project_dir: Path) -> bool:
    """Return whether a directory should be scanned as a project root."""
    name = project_dir.name.strip().lower()
    if not name or name in SKIP_DIRECTORY_NAMES:
        return False
    if name.startswith(".") and name not in {".codex"}:
        return False
    return project_dir.is_dir()


def discover_project_directories(ai_projects_root: str | Path) -> list[Path]:
    """Discover immediate child project directories without recursive scanning."""
    root = Path(ai_projects_root)
    if not root.exists() or not root.is_dir():
        return []
    return sorted(
        [path for path in root.iterdir() if is_safe_project_dir(path)],
        key=lambda item: item.name.lower(),
    )


def _manifest_source(manifest_data: dict, manifest_path: Path) -> str:
    """Classify a manifest source for the command center registry."""
    mode = _string_value(manifest_data.get("mode")).lower()
    if mode in {"demo_static_contract", "demo", "demo_manifest"}:
        return "demo_manifest"
    if manifest_path.parent.name == "AgentHubControlCenter" and "future_agent_template" in manifest_data:
        return "demo_manifest"
    return "local_manifest"


def read_manifest_json(manifest_path: str | Path) -> tuple[dict | None, str | None]:
    """Read one manifest JSON file and return data or a safe error message."""
    path = Path(manifest_path)
    try:
        with path.open("r", encoding="utf-8-sig") as manifest_file:
            data = json.load(manifest_file)
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON: {exc.msg}"
    except OSError as exc:
        return None, f"Could not read manifest: {exc}"

    if not isinstance(data, dict):
        return None, "Manifest root must be a JSON object."
    return data, None


def extract_manifest_records(manifest_data: dict) -> list[dict]:
    """Extract Agent records from a manifest object."""
    agents = manifest_data.get("agents")
    if isinstance(agents, list):
        return [item for item in agents if isinstance(item, dict)]
    if "agent_id" in manifest_data:
        return [manifest_data]
    return []


def validate_manifest_record(record: dict) -> dict:
    """Validate one manifest Agent record without raising on bad input."""
    missing_fields = [
        field
        for field in REQUIRED_MANIFEST_FIELDS
        if field not in record or _is_missing_value(record.get(field))
    ]
    warnings: list[str] = []

    for field in ["inputs", "outputs", "actions", "connectors"]:
        if field in record and not isinstance(record.get(field), list):
            warnings.append(f"{field} must be a list.")

    if "demo_mode" in record and not isinstance(record.get("demo_mode"), bool):
        warnings.append("demo_mode must be true or false.")
    if record.get("safe_mode") is not True:
        warnings.append("safe_mode must be true for HUB-V2-002 import.")

    agent_id = _string_value(record.get("agent_id"))
    if agent_id and any(char.isspace() for char in agent_id):
        warnings.append("agent_id should not contain whitespace.")

    is_valid = not missing_fields and not warnings
    return {
        "agent_id": agent_id,
        "agent_name": _string_value(record.get("agent_name")) or "Unknown Agent",
        "is_valid": is_valid,
        "missing_fields": missing_fields,
        "warnings": warnings,
        "recommended_fix": build_manifest_fix(missing_fields, warnings),
    }


def build_manifest_fix(missing_fields: list[str], warnings: list[str]) -> str:
    """Build a short actionable fix message for invalid manifests."""
    if missing_fields:
        return "Add required fields: " + ", ".join(missing_fields)
    if warnings:
        return warnings[0]
    return "Manifest is ready for import."


def manifest_record_to_registry_record(
    record: dict,
    manifest_path: str | Path,
    source: str = "local_manifest",
) -> dict:
    """Convert one valid manifest record into an AgentHub registry record."""
    path = Path(manifest_path)
    actions = _list_value(record.get("actions"))
    connectors = _list_value(record.get("connectors"))
    tags = _list_value(record.get("tags"))
    project_path = _string_value(record.get("project_path")) or str(path.parent)
    github_url = _string_value(record.get("github_repo"))
    public_showcase_status = _string_value(record.get("public_showcase_status"))

    return {
        "agent_id": _string_value(record.get("agent_id")),
        "agent_name": _string_value(record.get("agent_name")),
        "category": _string_value(record.get("category")),
        "project_type": _string_value(record.get("project_type")) or "Agent",
        "local_path": project_path,
        "github_url": github_url,
        "status": _string_value(record.get("status")),
        "stage": _string_value(record.get("version")) or "manifest-import",
        "primary_capability": _string_value(record.get("description")),
        "tech_stack": ", ".join(tags),
        "run_command": "streamlit run app.py",
        "portfolio_value": _string_value(record.get("description")),
        "next_action": _string_value(record.get("next_recommended_action")) or "Review imported manifest",
        "showcase_status": public_showcase_status or "Manifest Imported",
        "pin_status": _string_value(record.get("pin_status")) or "Not pinned",
        "notes": (
            f"Imported from {source}: {path}. "
            f"Actions: {', '.join(actions) or 'not declared'}. "
            f"Connectors: {', '.join(connectors) or 'not declared'}."
        ),
        "source": source,
        "manifest_path": str(path),
        "manifest_inputs": record.get("inputs") if isinstance(record.get("inputs"), list) else [],
        "manifest_outputs": record.get("outputs") if isinstance(record.get("outputs"), list) else [],
        "manifest_actions": record.get("actions") if isinstance(record.get("actions"), list) else [],
        "manifest_connectors": record.get("connectors") if isinstance(record.get("connectors"), list) else [],
        "action_schema_version": _string_value(record.get("action_schema_version")),
        "demo_mode": record.get("demo_mode") if isinstance(record.get("demo_mode"), bool) else True,
        "safe_mode": record.get("safe_mode") if isinstance(record.get("safe_mode"), bool) else True,
        "last_run": _string_value(record.get("last_run")) or "Not tracked yet",
        "dashboard_url": _string_value(record.get("dashboard_url")),
        "owner": _string_value(record.get("owner")),
    }


def scan_project_manifest(project_dir: str | Path) -> dict:
    """Scan one project directory for agent_manifest.json only."""
    project_path = Path(project_dir)
    manifest_path = project_path / "agent_manifest.json"
    base_result = {
        "project_name": project_path.name,
        "project_path": str(project_path),
        "manifest_path": str(manifest_path),
        "manifest_status": "missing",
        "source": "",
        "agent_records": [],
        "valid_agent_records": [],
        "invalid_agent_records": [],
        "warnings": ["agent_manifest.json not found."],
        "recommended_fix": "Add a valid agent_manifest.json using docs/AGENT_INTERFACE_STANDARD.md.",
    }

    if not manifest_path.is_file():
        return base_result

    manifest_data, error = read_manifest_json(manifest_path)
    if error:
        base_result.update(
            {
                "manifest_status": "invalid",
                "warnings": [error],
                "recommended_fix": "Fix agent_manifest.json so it is valid JSON.",
            }
        )
        return base_result

    assert manifest_data is not None
    source = _manifest_source(manifest_data, manifest_path)
    records = extract_manifest_records(manifest_data)
    if not records:
        base_result.update(
            {
                "manifest_status": "invalid",
                "source": source,
                "warnings": ["No Agent records found in manifest."],
                "recommended_fix": "Add an agent object or an agents list.",
            }
        )
        return base_result

    valid_records = []
    invalid_records = []
    warnings = []
    for record in records:
        validation = validate_manifest_record(record)
        record_result = {
            "agent_id": validation["agent_id"],
            "agent_name": validation["agent_name"],
            "validation": validation,
            "record": record,
        }
        if validation["is_valid"]:
            valid_records.append(
                manifest_record_to_registry_record(record, manifest_path, source=source)
            )
        else:
            invalid_records.append(record_result)
            warnings.append(
                f"{validation['agent_name']}: {validation['recommended_fix']}"
            )

    status = "valid" if valid_records and not invalid_records else "invalid"
    recommended_fix = "Manifest is ready for import."
    if invalid_records:
        recommended_fix = "Fix invalid Agent records before import."

    return {
        "project_name": project_path.name,
        "project_path": str(project_path),
        "manifest_path": str(manifest_path),
        "manifest_status": status,
        "source": source,
        "agent_records": records,
        "valid_agent_records": valid_records,
        "invalid_agent_records": invalid_records,
        "warnings": warnings,
        "recommended_fix": recommended_fix,
    }


def scan_ai_projects_manifests(ai_projects_root: str | Path) -> dict:
    """Scan immediate AIProjects child folders for agent_manifest.json files."""
    project_dirs = discover_project_directories(ai_projects_root)
    project_results = [scan_project_manifest(project_dir) for project_dir in project_dirs]
    valid_records = [
        record
        for result in project_results
        for record in result.get("valid_agent_records", [])
    ]

    summary = {
        "root_path": str(Path(ai_projects_root)),
        "total_projects_scanned": len(project_results),
        "manifests_found": sum(1 for item in project_results if item["manifest_status"] != "missing"),
        "valid_manifests": sum(1 for item in project_results if item["manifest_status"] == "valid"),
        "invalid_manifests": sum(1 for item in project_results if item["manifest_status"] == "invalid"),
        "missing_manifests": sum(1 for item in project_results if item["manifest_status"] == "missing"),
        "valid_agent_records": len(valid_records),
    }

    return {
        "summary": summary,
        "project_results": project_results,
        "valid_registry_records": valid_records,
    }
