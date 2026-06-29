from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


DEFAULT_PRODUCT_STATUS = "Maintain / Showcase Ready"
UNKNOWN_VALUE = "Unknown"
CURRENT_STATUS_PATTERN = re.compile(r"^Current status:\s*(?P<checkpoint>.+?)\s*$", re.MULTILINE)


def _project_root(project_root: str | Path) -> Path:
    return Path(project_root)


def load_project_status_checkpoint(project_root: str | Path) -> str:
    """Load the latest checkpoint from PROJECT_STATUS.md without executing anything."""
    status_path = _project_root(project_root) / "PROJECT_STATUS.md"
    if not status_path.exists():
        return ""
    try:
        text = status_path.read_text(encoding="utf-8-sig")
    except OSError:
        return ""
    match = CURRENT_STATUS_PATTERN.search(text)
    return match.group("checkpoint").strip() if match else ""


def _load_manifest(project_root: str | Path) -> dict[str, Any]:
    manifest_path = _project_root(project_root) / "agent_manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def load_manifest_version(project_root: str | Path) -> str:
    """Load the root manifest version or first Agent version."""
    manifest = _load_manifest(project_root)
    for key in ("manifest_version", "current_checkpoint"):
        value = manifest.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    agents = manifest.get("agents")
    if isinstance(agents, list):
        for agent in agents:
            if isinstance(agent, dict):
                version = agent.get("version")
                if isinstance(version, str) and version.strip():
                    return version.strip()
    return ""


def _load_root_agent_status(project_root: str | Path) -> str:
    manifest = _load_manifest(project_root)
    agents = manifest.get("agents")
    if isinstance(agents, list):
        for agent in agents:
            if isinstance(agent, dict) and agent.get("agent_id") == "agent_hub_control_center":
                status = agent.get("status")
                return status.strip() if isinstance(status, str) else ""
    return ""


def get_product_status_label(project_root: str | Path) -> str:
    """Return the stable product status separate from the latest checkpoint."""
    checkpoint = load_project_status_checkpoint(project_root).lower()
    manifest_status = _load_root_agent_status(project_root).lower()
    maintain_markers = (
        "maintain",
        "pause",
        "showcase",
        "clientdeliverykit",
        "hub-v2-020",
        "hub-v2-021",
        "hub-v2-022",
        "hub-v2-024",
        "bilingual_ui_stage_sync_ready",
        "deep_chinese_ui_coverage_ready",
    )
    if any(marker in checkpoint for marker in maintain_markers):
        return DEFAULT_PRODUCT_STATUS
    if any(marker in manifest_status for marker in maintain_markers):
        return DEFAULT_PRODUCT_STATUS
    return DEFAULT_PRODUCT_STATUS


def get_stage_snapshot(project_root: str | Path) -> dict[str, str]:
    """Return UI-ready stage/status values for sidebar and hero display."""
    latest_checkpoint = load_project_status_checkpoint(project_root)
    manifest_version = load_manifest_version(project_root)
    return {
        "product_status": get_product_status_label(project_root),
        "latest_checkpoint": latest_checkpoint or UNKNOWN_VALUE,
        "latest_checkpoint_source": "PROJECT_STATUS.md" if latest_checkpoint else "fallback",
        "manifest_version": manifest_version or UNKNOWN_VALUE,
        "manifest_version_source": "agent_manifest.json" if manifest_version else "fallback",
    }
