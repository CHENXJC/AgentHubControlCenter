from __future__ import annotations

import re
from pathlib import Path

from agent_hub.report_export_schema import REPORT_FORMATS


REPORT_FILE_EXTENSIONS = {
    "markdown": ".md",
    "json": ".json",
    "csv": ".csv",
}


def _slugify_file_part(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return slug.strip(".-") or "agenthub-v2-demo-workflow-report"


def get_public_reports_dir(project_root: str | Path) -> Path:
    """Return the only local output directory allowed for demo report exports."""
    root = Path(project_root)
    if root.name == "public_reports" and root.parent.name == "outputs":
        return root
    return root / "outputs" / "public_reports"


def ensure_public_reports_dir(project_root: str | Path) -> Path:
    """Create outputs/public_reports without touching private output folders."""
    public_reports_dir = get_public_reports_dir(project_root)
    public_reports_dir.mkdir(parents=True, exist_ok=True)
    return public_reports_dir


def build_public_report_file_name(report_id: str, report_format: str) -> str:
    """Build a Windows-safe public report file name."""
    if report_format not in REPORT_FORMATS:
        raise ValueError(f"Unsupported report format: {report_format}")
    return f"{_slugify_file_part(report_id)}{REPORT_FILE_EXTENSIONS[report_format]}"


def assert_public_report_path(path: str | Path, public_reports_dir: str | Path) -> Path:
    """Ensure a target path stays inside outputs/public_reports."""
    resolved_path = Path(path).resolve()
    resolved_dir = Path(public_reports_dir).resolve()
    if resolved_path != resolved_dir and resolved_dir not in resolved_path.parents:
        raise ValueError("Report exports may only be written inside outputs/public_reports.")
    if "private" in {part.lower() for part in resolved_path.parts}:
        raise ValueError("Report exports may not target private output folders.")
    return resolved_path


def export_report_bundle(
    report_contents: dict[str, str],
    *,
    project_root: str | Path,
    report_id: str,
) -> dict[str, Path]:
    """Write public-safe report content to outputs/public_reports only."""
    public_reports_dir = ensure_public_reports_dir(project_root)
    exported_paths: dict[str, Path] = {}
    for report_format in REPORT_FORMATS:
        if report_format not in report_contents:
            continue
        file_name = build_public_report_file_name(report_id, report_format)
        report_path = assert_public_report_path(public_reports_dir / file_name, public_reports_dir)
        report_path.write_text(report_contents[report_format], encoding="utf-8")
        exported_paths[report_format] = report_path
    return exported_paths


def find_report_file_policy_violations(exported_paths: dict[str, Path]) -> list[dict[str, str]]:
    """Return exported paths that violate the public_reports-only policy."""
    violations: list[dict[str, str]] = []
    for report_format, path in exported_paths.items():
        normalized = str(Path(path)).replace("\\", "/")
        if report_format not in REPORT_FORMATS:
            violations.append({"format": report_format, "path": normalized, "reason": "unsupported_format"})
            continue
        if f"outputs/public_reports/" not in normalized and not normalized.endswith("outputs/public_reports"):
            violations.append({"format": report_format, "path": normalized, "reason": "outside_public_reports"})
            continue
        if "outputs/private" in normalized or "/private/" in normalized.lower():
            violations.append({"format": report_format, "path": normalized, "reason": "private_output_path"})
            continue
        if Path(path).suffix != REPORT_FILE_EXTENSIONS[report_format]:
            violations.append({"format": report_format, "path": normalized, "reason": "wrong_extension"})
    return violations
