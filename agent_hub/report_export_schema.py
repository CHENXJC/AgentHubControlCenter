from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


REPORT_EXPORT_SCHEMA_VERSION = "HUB-V2-010"
REPORT_EXPORT_POLICY = "public_safe_demo_report_metadata_only_no_execution"
REPORT_OUTPUT_DIR = "outputs/public_reports"

REPORT_FORMATS = ("markdown", "json", "csv")

REPORT_SECTION_OPTIONS = [
    {"section_id": "agents", "label": "Agents"},
    {"section_id": "actions", "label": "Actions"},
    {"section_id": "useful_signals", "label": "Useful Signals"},
    {"section_id": "connectors", "label": "Connectors"},
    {"section_id": "workflows", "label": "Workflows"},
    {"section_id": "approval_gates", "label": "Approval Gates"},
    {"section_id": "safety_snapshot", "label": "Safety Snapshot"},
]

REPORT_SECTION_IDS = tuple(item["section_id"] for item in REPORT_SECTION_OPTIONS)
REPORT_SECTION_LABELS = {item["section_id"]: item["label"] for item in REPORT_SECTION_OPTIONS}

REPORT_REQUIRED_SECTIONS = [
    "Executive Summary",
    "Agent Registry Summary",
    "Useful Signals Summary",
    "Top Useful Signals",
    "Connector Readiness Summary",
    "Workflow Simulation Summary",
    "Approval Gates Summary",
    "Blocked / Manual / Template-only Actions",
    "Recommended Next Steps",
    "Safety Notes",
    "Validation Snapshot",
]

REPORT_SAFETY_NOTES = [
    "Demo/local metadata only",
    "No live connector connected",
    "No credentials loaded",
    "No real action executed",
    "No external API called",
]

REPORT_SCHEMA_FIELDS = [
    "report_id",
    "title",
    "schema_version",
    "generated_at",
    "export_policy",
    "formats",
    "selected_sections",
    "public_safe",
    "safety_notes",
    "validation_snapshot",
    "sections",
]


def current_report_timestamp() -> str:
    """Return a stable UTC timestamp for public-safe report metadata."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_report_sections(selected_sections: list[str] | tuple[str, ...] | None = None) -> list[str]:
    """Return supported report section IDs, preserving the canonical order."""
    if not selected_sections:
        return list(REPORT_SECTION_IDS)
    selected = {str(section).strip() for section in selected_sections}
    return [section for section in REPORT_SECTION_IDS if section in selected]


def build_report_metadata(
    *,
    selected_sections: list[str] | tuple[str, ...] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build metadata for a demo workflow report export package."""
    timestamp = generated_at or current_report_timestamp()
    safe_timestamp = timestamp[:10] if timestamp else "local"
    return {
        "report_id": f"agenthub_v2_demo_workflow_report_{safe_timestamp}",
        "title": "AgentHubControlCenter V2 Demo Workflow Report",
        "schema_version": REPORT_EXPORT_SCHEMA_VERSION,
        "generated_at": timestamp,
        "export_policy": REPORT_EXPORT_POLICY,
        "formats": list(REPORT_FORMATS),
        "selected_sections": normalize_report_sections(selected_sections),
        "output_dir": REPORT_OUTPUT_DIR,
        "public_safe": True,
        "execution_mode": "template_only_no_execution",
    }


def validate_report_package(package: dict[str, Any]) -> dict[str, Any]:
    """Validate one report package against the HUB-V2-010 display-only policy."""
    missing_fields = [
        field
        for field in REPORT_SCHEMA_FIELDS
        if field not in package or package.get(field) in (None, "", [])
    ]
    warnings: list[str] = []

    if package.get("schema_version") != REPORT_EXPORT_SCHEMA_VERSION:
        warnings.append("schema_version must be HUB-V2-010.")
    if package.get("export_policy") != REPORT_EXPORT_POLICY:
        warnings.append("export_policy must stay public-safe and no-execution.")
    if package.get("public_safe") is not True:
        warnings.append("public_safe must be true.")

    formats = package.get("formats", [])
    if not isinstance(formats, list) or any(item not in REPORT_FORMATS for item in formats):
        warnings.append("formats must be limited to markdown, json, and csv.")

    selected_sections = package.get("selected_sections", [])
    if not isinstance(selected_sections, list) or any(item not in REPORT_SECTION_IDS for item in selected_sections):
        warnings.append("selected_sections contains unsupported section IDs.")

    safety_notes = package.get("safety_notes", [])
    for required_note in REPORT_SAFETY_NOTES:
        if required_note not in safety_notes:
            warnings.append(f"Missing safety note: {required_note}")

    if str(package.get("output_dir", REPORT_OUTPUT_DIR)).replace("\\", "/") != REPORT_OUTPUT_DIR:
        warnings.append("output_dir must be outputs/public_reports.")

    return {
        "is_valid": not missing_fields and not warnings,
        "missing_fields": missing_fields,
        "warnings": warnings,
    }


def find_report_export_policy_violations(package: dict[str, Any] | list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return report packages that violate the public-safe no-execution policy."""
    packages = package if isinstance(package, list) else [package]
    violations = []
    for item in packages:
        validation = validate_report_package(item)
        if not validation["is_valid"]:
            violations.append(
                {
                    "report_id": item.get("report_id", ""),
                    "missing_fields": validation["missing_fields"],
                    "warnings": validation["warnings"],
                }
            )
    return violations
