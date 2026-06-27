from __future__ import annotations

from agent_hub.action_schema import normalize_action, summarize_actions, validate_action_schema


def build_action_registry(manifests: list[dict]) -> list[dict]:
    """Build a flat Action Center registry from normalized Agent manifests."""
    rows: list[dict] = []
    for manifest in manifests:
        agent_id = manifest.get("agent_id", "")
        agent_name = manifest.get("agent_name", "")
        project_path = manifest.get("project_path", "")
        for action in manifest.get("actions", []):
            normalized = normalize_action(
                action,
                agent_id=agent_id,
                agent_name=agent_name,
                project_path=project_path,
            )
            validation = validate_action_schema(normalized)
            rows.append(
                {
                    "agent_id": agent_id,
                    "agent_name": agent_name,
                    "category": manifest.get("category", ""),
                    "category_label": manifest.get("category_label", manifest.get("category", "")),
                    "project_path": project_path,
                    "action_id": normalized["action_id"],
                    "label": normalized["label"],
                    "description": normalized["description"],
                    "action_type": normalized["action_type"],
                    "execution_mode": normalized["execution_mode"],
                    "risk_level": normalized["risk_level"],
                    "requires_approval": normalized["requires_approval"],
                    "command_template": normalized["command_template"],
                    "runbook_ref": normalized["runbook_ref"],
                    "expected_output": normalized["expected_output"],
                    "safety_note": normalized["safety_note"],
                    "connector_required": normalized["connector_required"],
                    "status": normalized["status"],
                    "enabled": normalized["enabled"],
                    "safe_mode": normalized["safe_mode"],
                    "schema_valid": validation["is_valid"],
                    "schema_warnings": validation["warnings"],
                    "missing_schema_fields": validation["missing_fields"],
                }
            )
    return sorted(rows, key=lambda item: (item["agent_name"].lower(), item["action_id"]))


def build_action_registry_summary(action_rows: list[dict]) -> dict[str, int]:
    """Return aggregate Action Center metrics."""
    return summarize_actions(action_rows)


def group_actions_by_agent(action_rows: list[dict]) -> list[dict]:
    """Group action rows for display or docs."""
    grouped: dict[str, dict] = {}
    for row in action_rows:
        agent_name = row.get("agent_name", "")
        entry = grouped.setdefault(
            agent_name,
            {
                "agent_id": row.get("agent_id", ""),
                "agent_name": agent_name,
                "category_label": row.get("category_label", ""),
                "actions": [],
            },
        )
        entry["actions"].append(row)
    return [grouped[key] for key in sorted(grouped)]


def get_actions_for_agent(action_rows: list[dict], agent_id: str = "", agent_name: str = "") -> list[dict]:
    """Return normalized action rows for one Agent without executing anything."""
    normalized_agent_id = agent_id.strip().lower()
    normalized_agent_name = agent_name.strip().lower()
    return [
        row
        for row in action_rows
        if (
            normalized_agent_id
            and str(row.get("agent_id", "")).strip().lower() == normalized_agent_id
        )
        or (
            normalized_agent_name
            and str(row.get("agent_name", "")).strip().lower() == normalized_agent_name
        )
    ]


def get_codex_prompt_actions(action_rows: list[dict]) -> list[dict]:
    """Return template-only Codex prompt actions for policy checks and UI linking."""
    return [
        row
        for row in action_rows
        if row.get("action_type") == "codex_prompt"
        or row.get("action_id") == "generate_codex_prompt"
    ]


def find_action_policy_violations(action_rows: list[dict]) -> list[dict]:
    """Return action rows that violate the metadata-only safety contract."""
    violations = []
    for row in action_rows:
        if not row.get("schema_valid"):
            violations.append(row)
            continue
        if row.get("execution_mode") not in {"not_executable", "manual_only", "template_only", "planned"}:
            violations.append(row)
            continue
        if row.get("risk_level") in {"high", "blocked"} and row.get("requires_approval") is not True:
            violations.append(row)
    return violations
