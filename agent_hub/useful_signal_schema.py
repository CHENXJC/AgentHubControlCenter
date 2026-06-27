from __future__ import annotations

from typing import Any


USEFUL_SIGNAL_SCHEMA_VERSION = "HUB-V2-007"

USEFUL_SIGNAL_FIELDS = [
    "signal_id",
    "title",
    "source_agent",
    "source_type",
    "category",
    "summary",
    "usefulness_score",
    "relevance_score",
    "urgency_score",
    "actionability_score",
    "value_score",
    "risk_score",
    "recommended_action",
    "target_agent",
    "status",
    "why_important",
    "suggested_next_step",
    "score_explanation",
    "execution_policy",
]

SIGNAL_CATEGORIES = {
    "project_progress",
    "action_required",
    "business_opportunity",
    "learning_value",
    "portfolio_improvement",
    "connector_readiness",
    "workflow_automation",
    "risk_warning",
}

SIGNAL_STATUSES = {
    "new",
    "reviewed",
    "needs_action",
    "watchlist",
    "ignored",
    "archived",
}

SOURCE_TYPES = {
    "agent_manifest",
    "project_status",
    "report",
    "manual_demo_data",
    "local_json",
    "local_csv",
    "action_registry",
    "codex_prompt_generator",
    "connector_readiness",
    "workflow_simulation",
}

DISPLAY_ONLY_EXECUTION_POLICY = "display_only_text_recommendation_no_execution"


def clamp_score(value: Any, default: int = 0) -> int:
    """Return an integer score between 0 and 100."""
    if isinstance(value, bool):
        return default
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        return default
    return max(0, min(100, score))


def _string_value(value: Any, default: str = "") -> str:
    return value.strip() if isinstance(value, str) and value.strip() else default


def slugify_signal_id(value: str) -> str:
    """Create a stable signal_id from a title."""
    output = []
    previous_was_separator = False
    for char in value.strip().lower():
        if char.isalnum():
            output.append(char)
            previous_was_separator = False
        elif not previous_was_separator:
            output.append("_")
            previous_was_separator = True
    return "".join(output).strip("_") or "useful_signal"


def normalize_signal(signal: dict[str, Any]) -> dict[str, Any]:
    """Normalize one useful signal into the HUB-V2-007 display schema."""
    source = dict(signal) if isinstance(signal, dict) else {}
    title = _string_value(source.get("title"), "Untitled useful signal")
    category = _string_value(source.get("category"), "project_progress")
    status = _string_value(source.get("status"), "new")
    source_type = _string_value(source.get("source_type"), "manual_demo_data")

    normalized = dict(source)
    normalized.update(
        {
            "signal_id": _string_value(source.get("signal_id"), slugify_signal_id(title)),
            "title": title,
            "source_agent": _string_value(source.get("source_agent"), "AgentHubControlCenter"),
            "source_type": source_type if source_type in SOURCE_TYPES else "manual_demo_data",
            "category": category if category in SIGNAL_CATEGORIES else "project_progress",
            "summary": _string_value(source.get("summary"), "No summary provided."),
            "usefulness_score": clamp_score(source.get("usefulness_score"), 0),
            "relevance_score": clamp_score(source.get("relevance_score"), 50),
            "urgency_score": clamp_score(source.get("urgency_score"), 50),
            "actionability_score": clamp_score(source.get("actionability_score"), 50),
            "value_score": clamp_score(source.get("value_score"), 50),
            "risk_score": clamp_score(source.get("risk_score"), 20),
            "recommended_action": _string_value(
                source.get("recommended_action"),
                "Review this signal manually in AgentHub.",
            ),
            "target_agent": _string_value(source.get("target_agent"), _string_value(source.get("source_agent"), "")),
            "status": status if status in SIGNAL_STATUSES else "new",
            "why_important": _string_value(source.get("why_important"), ""),
            "suggested_next_step": _string_value(source.get("suggested_next_step"), ""),
            "score_explanation": _string_value(source.get("score_explanation"), ""),
            "related_action_id": _string_value(source.get("related_action_id"), ""),
            "execution_policy": DISPLAY_ONLY_EXECUTION_POLICY,
        }
    )
    return normalized


def validate_signal_schema(signal: dict[str, Any]) -> dict[str, Any]:
    """Validate one normalized signal without executing recommended actions."""
    missing_fields = [
        field
        for field in USEFUL_SIGNAL_FIELDS
        if field not in signal or signal.get(field) in {None, ""}
    ]
    warnings: list[str] = []

    if signal.get("category") not in SIGNAL_CATEGORIES:
        warnings.append("category must use a HUB-V2-007 signal category.")
    if signal.get("status") not in SIGNAL_STATUSES:
        warnings.append("status must use a HUB-V2-007 signal status.")
    if signal.get("source_type") not in SOURCE_TYPES:
        warnings.append("source_type must use a HUB-V2-007 source type.")

    for field in [
        "usefulness_score",
        "relevance_score",
        "urgency_score",
        "actionability_score",
        "value_score",
        "risk_score",
    ]:
        value = signal.get(field)
        if not isinstance(value, int) or value < 0 or value > 100:
            warnings.append(f"{field} must be an integer from 0 to 100.")

    if signal.get("execution_policy") != DISPLAY_ONLY_EXECUTION_POLICY:
        warnings.append("signals must remain display-only text recommendations.")

    return {
        "is_valid": not missing_fields and not warnings,
        "missing_fields": missing_fields,
        "warnings": warnings,
    }
