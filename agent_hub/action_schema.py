from __future__ import annotations

import re
from typing import Any


ACTION_SCHEMA_VERSION = "HUB-V2-005"

ACTION_SCHEMA_FIELDS = [
    "action_id",
    "label",
    "description",
    "action_type",
    "execution_mode",
    "risk_level",
    "requires_approval",
    "command_template",
    "runbook_ref",
    "expected_output",
    "safety_note",
    "connector_required",
    "status",
]

ACTION_TYPES = {
    "display_only",
    "manual_instruction",
    "command_template",
    "local_link",
    "report_view",
    "codex_prompt",
    "future_connector",
}

EXECUTION_MODES = {
    "not_executable",
    "manual_only",
    "template_only",
    "planned",
}

RISK_LEVELS = {
    "low",
    "medium",
    "high",
    "blocked",
}

BLOCKED_ACTION_IDS = {
    "send_email",
    "delete_files",
    "modify_git_remote",
    "git_push",
    "connect_real_gmail",
    "connect_real_sheets",
    "run_external_script",
}

ACTION_TYPE_BY_ID = {
    "launch_command_center": "manual_instruction",
    "open_dashboard": "manual_instruction",
    "manual_run_dashboard": "manual_instruction",
    "review_agent_registry": "display_only",
    "view_project_status": "report_view",
    "view_agent_manifest": "report_view",
    "view_latest_report": "report_view",
    "open_project_folder": "local_link",
    "open_github_showcase": "local_link",
    "generate_demo_report": "command_template",
    "export_summary": "command_template",
    "run_tests": "command_template",
    "generate_codex_prompt": "codex_prompt",
    "send_to_agent_hub": "future_connector",
}

ACTION_DESCRIPTION_BY_ID = {
    "launch_command_center": "Show the local command center launcher instructions.",
    "open_dashboard": "Show the manual steps for opening the Agent dashboard.",
    "manual_run_dashboard": "Show the manual dashboard launch runbook for the Agent.",
    "review_agent_registry": "Display the registry metadata already loaded in AgentHub.",
    "view_project_status": "Review the local PROJECT_STATUS.md checkpoint file.",
    "view_agent_manifest": "Review the local agent_manifest.json metadata file.",
    "view_latest_report": "Review the latest public-safe sample report or exported summary.",
    "open_project_folder": "Open the local project folder manually outside AgentHub.",
    "open_github_showcase": "Open the GitHub showcase link manually in a browser.",
    "generate_demo_report": "Use the copied command template or project UI to generate a demo report manually.",
    "export_summary": "Use the copied command template or project UI to export a public-safe summary manually.",
    "run_tests": "Use the copied command template to run local tests manually.",
    "generate_codex_prompt": "Generate a copyable Codex prompt for the next safe project task.",
    "send_to_agent_hub": "Reserved placeholder for future metadata handoff into AgentHub.",
}


def slugify(value: str) -> str:
    """Return a stable anchor-friendly slug for docs references."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    return slug.strip("-") or "action"


def _string_value(value: Any) -> str:
    """Return stripped string values for schema fields."""
    return value.strip() if isinstance(value, str) else ""


def _bool_value(value: Any, default: bool) -> bool:
    """Return boolean values without accepting string truthiness."""
    return value if isinstance(value, bool) else default


def infer_action_type(action_id: str, action: dict[str, Any] | None = None) -> str:
    """Infer an action type from a known action id or older manifest fields."""
    action = action or {}
    declared_type = _string_value(action.get("action_type"))
    if declared_type in ACTION_TYPES:
        return declared_type

    if action_id in BLOCKED_ACTION_IDS:
        if action_id.startswith("connect_"):
            return "future_connector"
        return "command_template"

    if action_id in ACTION_TYPE_BY_ID:
        return ACTION_TYPE_BY_ID[action_id]

    legacy_mode = _string_value(action.get("mode")).lower()
    if legacy_mode in {"metadata_only", "future_connector"}:
        return "future_connector"
    if legacy_mode in {"manual_review", "streamlit_view"}:
        return "report_view"
    if legacy_mode in {"external_link", "local_link"}:
        return "local_link"
    if legacy_mode in {"manual_command", "local_cmd"}:
        return "command_template"

    return "display_only"


def infer_execution_mode(action_type: str, action: dict[str, Any] | None = None) -> str:
    """Infer the safe execution mode for a metadata-only action."""
    action = action or {}
    declared_mode = _string_value(action.get("execution_mode"))
    if declared_mode in EXECUTION_MODES:
        return declared_mode

    if action_type in {"display_only", "report_view"}:
        return "not_executable"
    if action_type in {"manual_instruction", "local_link"}:
        return "manual_only"
    if action_type in {"command_template", "codex_prompt"}:
        return "template_only"
    if action_type == "future_connector":
        return "planned"
    return "not_executable"


def infer_risk_level(action_id: str, action_type: str, action: dict[str, Any] | None = None) -> str:
    """Infer the risk level for display/manual/template-only actions."""
    action = action or {}
    declared_risk = _string_value(action.get("risk_level"))
    if declared_risk in RISK_LEVELS:
        return declared_risk
    if action_id in BLOCKED_ACTION_IDS:
        return "blocked"
    if action_type == "future_connector":
        return "medium"
    return "low"


def infer_status(action_type: str, execution_mode: str, risk_level: str, action: dict[str, Any] | None = None) -> str:
    """Infer a display status for Action Center cards."""
    action = action or {}
    declared_status = _string_value(action.get("status"))
    if declared_status:
        return declared_status
    if risk_level == "blocked":
        return "blocked"
    if execution_mode == "planned" or action_type == "future_connector":
        return "planned"
    if execution_mode == "manual_only":
        return "manual_ready"
    if execution_mode == "template_only":
        return "template_ready"
    return "display_only"


def default_command_template(action_id: str, action_type: str, project_path: str) -> str:
    """Return a non-executed command or instruction string for display."""
    if action_id == "launch_command_center":
        return ".\\launch_command_center.cmd"
    if action_id in {"open_dashboard", "manual_run_dashboard"}:
        return f'cd /d "{project_path}" && streamlit run app.py' if project_path else "streamlit run app.py"
    if action_id == "open_project_folder":
        return f'explorer "{project_path}"' if project_path else "Open the project folder manually."
    if action_id == "open_github_showcase":
        return "Open the GitHub showcase URL manually."
    if action_id == "view_project_status":
        return "Open PROJECT_STATUS.md in the project folder."
    if action_id == "view_agent_manifest":
        return "Open agent_manifest.json in the project folder."
    if action_id == "view_latest_report":
        return "Review the latest public-safe report or README demo output manually."
    if action_id == "run_tests":
        return f'cd /d "{project_path}" && python -m pytest' if project_path else "python -m pytest"
    if action_id == "generate_codex_prompt":
        return "Copy the Agent metadata into the next Codex task prompt."
    if action_id == "send_to_agent_hub":
        return "Future placeholder only. No connector is active in HUB-V2-005."
    if action_id in BLOCKED_ACTION_IDS:
        return "Blocked by Action Safety Policy. Do not execute from AgentHub."
    if action_type == "codex_prompt":
        return "Copy a generated Codex prompt template."
    if action_type == "future_connector":
        return "Future connector placeholder only."
    if action_type == "command_template":
        return "Copy the command template and run manually only after review."
    return "Display metadata only."


def default_expected_output(action_id: str, action_type: str) -> str:
    """Return a plain-English expected output for an action."""
    if action_id == "view_project_status":
        return "User can see the current checkpoint, validation status, and next stage."
    if action_id == "view_agent_manifest":
        return "User can inspect declared inputs, outputs, actions, connectors, and safety mode."
    if action_id == "view_latest_report":
        return "User can review a public-safe report or sample output reference."
    if action_id in {"open_dashboard", "manual_run_dashboard", "launch_command_center"}:
        return "User manually opens the local Streamlit dashboard outside automated execution."
    if action_id == "open_project_folder":
        return "User manually opens the local project folder."
    if action_id == "generate_codex_prompt":
        return "A copyable prompt template for the next safe Codex task."
    if action_id == "send_to_agent_hub":
        return "No output now; reserved for future metadata handoff design."
    if action_id in BLOCKED_ACTION_IDS:
        return "No output. This action is blocked."
    if action_type == "command_template":
        return "A command string or manual instruction that the user may copy after review."
    if action_type == "future_connector":
        return "Future connector placeholder; no live account action occurs."
    return "Metadata or instruction is displayed in AgentHub."


def default_safety_note(action_id: str, action_type: str, risk_level: str) -> str:
    """Return a safety note for the Action Center and manifest docs."""
    if risk_level == "blocked":
        return "Blocked in HUB-V2-005. Requires a separate explicit approval stage and safety tests."
    if action_type == "future_connector":
        return "Future connector placeholder only. AgentHub does not connect live accounts in this stage."
    if action_type == "command_template":
        return "Command template is shown as text only; AgentHub does not execute it."
    if action_type == "codex_prompt":
        return "Prompt is for manual copy into Codex; it does not execute project code."
    return "Display/manual metadata only; AgentHub does not execute this action."


def normalize_action(
    action: dict[str, Any],
    *,
    agent_id: str = "",
    agent_name: str = "",
    project_path: str = "",
) -> dict[str, Any]:
    """Normalize one manifest action into the HUB-V2-005 action schema."""
    source = dict(action) if isinstance(action, dict) else {}
    action_id = _string_value(source.get("action_id"))
    label = _string_value(source.get("label"))
    if not action_id:
        action_id = slugify(label).replace("-", "_") if label else "unnamed_action"
    if not label:
        label = action_id.replace("_", " ").title()

    action_type = infer_action_type(action_id, source)
    execution_mode = infer_execution_mode(action_type, source)
    risk_level = infer_risk_level(action_id, action_type, source)
    requires_approval = _bool_value(
        source.get("requires_approval"),
        risk_level in {"high", "blocked"} or action_type == "future_connector",
    )
    status = infer_status(action_type, execution_mode, risk_level, source)
    connector_required = source.get("connector_required", "none")
    if isinstance(connector_required, list):
        connector_required = ", ".join(str(item) for item in connector_required)
    connector_required = _string_value(connector_required) or "none"

    description = (
        _string_value(source.get("description"))
        or ACTION_DESCRIPTION_BY_ID.get(action_id)
        or f"{label} action metadata for {agent_name or agent_id or 'this Agent'}."
    )
    command_template = _string_value(source.get("command_template")) or default_command_template(
        action_id,
        action_type,
        project_path,
    )
    runbook_ref = _string_value(source.get("runbook_ref")) or (
        f"docs/MANUAL_RUNBOOK.md#{slugify(agent_id or agent_name)}-{slugify(action_id)}"
    )
    expected_output = _string_value(source.get("expected_output")) or default_expected_output(
        action_id,
        action_type,
    )
    safety_note = _string_value(source.get("safety_note")) or default_safety_note(
        action_id,
        action_type,
        risk_level,
    )

    normalized = dict(source)
    normalized.update(
        {
            "action_id": action_id,
            "label": label,
            "description": description,
            "action_type": action_type,
            "execution_mode": execution_mode,
            "risk_level": risk_level,
            "requires_approval": requires_approval,
            "command_template": command_template,
            "runbook_ref": runbook_ref,
            "expected_output": expected_output,
            "safety_note": safety_note,
            "connector_required": connector_required,
            "status": status,
            "enabled": _bool_value(source.get("enabled"), risk_level != "blocked"),
            "safe_mode": _bool_value(source.get("safe_mode"), True),
        }
    )
    return normalized


def validate_action_schema(action: dict[str, Any]) -> dict[str, Any]:
    """Validate one normalized action without executing anything."""
    missing_fields = [
        field
        for field in ACTION_SCHEMA_FIELDS
        if field not in action or action.get(field) in {None, ""}
    ]
    warnings: list[str] = []

    if action.get("action_type") not in ACTION_TYPES:
        warnings.append("action_type must use a HUB-V2-005 enum value.")
    if action.get("execution_mode") not in EXECUTION_MODES:
        warnings.append("execution_mode must use a HUB-V2-005 enum value.")
    if action.get("risk_level") not in RISK_LEVELS:
        warnings.append("risk_level must use a HUB-V2-005 enum value.")
    if not isinstance(action.get("requires_approval"), bool):
        warnings.append("requires_approval must be true or false.")
    if action.get("action_id") in BLOCKED_ACTION_IDS and action.get("risk_level") != "blocked":
        warnings.append("blocked action ids must use risk_level=blocked.")
    if action.get("risk_level") in {"high", "blocked"} and action.get("requires_approval") is not True:
        warnings.append("high or blocked actions must require approval.")
    if action.get("execution_mode") not in EXECUTION_MODES:
        warnings.append("real execution modes are not allowed in HUB-V2-005.")

    return {
        "is_valid": not missing_fields and not warnings,
        "missing_fields": missing_fields,
        "warnings": warnings,
    }


def summarize_actions(actions: list[dict[str, Any]]) -> dict[str, int]:
    """Summarize normalized action rows for Action Center metrics."""
    return {
        "total_actions": len(actions),
        "manual_only_actions": sum(1 for action in actions if action.get("execution_mode") == "manual_only"),
        "display_only_actions": sum(
            1
            for action in actions
            if action.get("action_type") == "display_only"
            or action.get("execution_mode") == "not_executable"
        ),
        "future_connector_actions": sum(
            1
            for action in actions
            if action.get("action_type") == "future_connector"
            or action.get("execution_mode") == "planned"
        ),
        "requires_approval_actions": sum(1 for action in actions if action.get("requires_approval") is True),
        "blocked_actions": sum(
            1
            for action in actions
            if action.get("risk_level") == "blocked" or action.get("status") == "blocked"
        ),
    }
