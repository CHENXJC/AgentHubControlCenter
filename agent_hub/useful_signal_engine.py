from __future__ import annotations

from statistics import mean
from typing import Any

from agent_hub.useful_signal_data import DEMO_USEFUL_SIGNAL_SEEDS
from agent_hub.useful_signal_schema import (
    DISPLAY_ONLY_EXECUTION_POLICY,
    SIGNAL_CATEGORIES,
    SIGNAL_STATUSES,
    clamp_score,
    normalize_signal,
    validate_signal_schema,
)


SCORE_WEIGHTS = {
    "relevance_score": 0.28,
    "urgency_score": 0.24,
    "actionability_score": 0.24,
    "value_score": 0.24,
}

HIGH_VALUE_THRESHOLD = 75
WATCHLIST_THRESHOLD = 55


def calculate_usefulness_score(signal: dict[str, Any]) -> int:
    """Calculate an explainable score from visible component scores."""
    weighted_score = sum(
        clamp_score(signal.get(field)) * weight
        for field, weight in SCORE_WEIGHTS.items()
    )
    risk_score = clamp_score(signal.get("risk_score"))
    category = signal.get("category", "")

    if category == "risk_warning":
        weighted_score += risk_score * 0.08
    elif risk_score >= 75:
        weighted_score -= (risk_score - 75) * 0.12

    return clamp_score(weighted_score)


def build_score_explanation(signal: dict[str, Any]) -> str:
    """Explain the scoring formula in plain language."""
    risk_score = clamp_score(signal.get("risk_score"))
    category = signal.get("category", "")
    risk_note = "Risk warning signals receive a small risk-awareness bonus."
    if category != "risk_warning":
        risk_note = "High non-warning risk slightly lowers the final score."
    if risk_score < 75 and category != "risk_warning":
        risk_note = "Risk is tracked but does not reduce this score."

    return (
        "Usefulness = 28% relevance + 24% urgency + 24% actionability + "
        "24% value, then a visible risk adjustment. "
        f"{risk_note}"
    )


def generate_why_important(signal: dict[str, Any]) -> str:
    """Generate one clear reason why a signal matters."""
    category = signal.get("category", "")
    category_reason = {
        "project_progress": "It shows whether the AgentHub system is becoming more complete and usable.",
        "action_required": "It points to a decision or build step that can move the current checkpoint forward.",
        "business_opportunity": "It can reveal reusable service or portfolio value without starting commercialization now.",
        "learning_value": "It helps convert project work into durable learning and reusable knowledge.",
        "portfolio_improvement": "It improves how the portfolio is presented and understood.",
        "connector_readiness": "It clarifies what must be designed before live connector work is safe.",
        "workflow_automation": "It can reduce manual planning work while staying local and controlled.",
        "risk_warning": "It prevents unsafe automation from being treated as a normal next action.",
    }
    return category_reason.get(category, "It helps rank local AgentHub information by practical value.")


def generate_suggested_next_step(signal: dict[str, Any]) -> str:
    """Generate a short next-step sentence without creating an executable action."""
    recommended = str(signal.get("recommended_action", "")).strip()
    if recommended:
        return recommended
    return "Review this signal manually and decide whether it should stay visible, move to watchlist, or be ignored."


def score_signal(signal: dict[str, Any]) -> dict[str, Any]:
    """Normalize, score, explain, and validate one useful signal."""
    normalized = normalize_signal(signal)
    normalized["usefulness_score"] = calculate_usefulness_score(normalized)
    normalized["why_important"] = normalized.get("why_important") or generate_why_important(normalized)
    normalized["suggested_next_step"] = normalized.get("suggested_next_step") or generate_suggested_next_step(normalized)
    normalized["score_explanation"] = build_score_explanation(normalized)
    normalized["execution_policy"] = DISPLAY_ONLY_EXECUTION_POLICY
    validation = validate_signal_schema(normalized)
    normalized["schema_valid"] = validation["is_valid"]
    normalized["schema_warnings"] = validation["warnings"]
    normalized["missing_schema_fields"] = validation["missing_fields"]
    normalized["bucket"] = bucket_signal(normalized)
    return normalized


def bucket_signal(signal: dict[str, Any]) -> str:
    """Assign a display bucket for the Useful Signals page."""
    status = signal.get("status", "")
    usefulness_score = clamp_score(signal.get("usefulness_score"))
    urgency_score = clamp_score(signal.get("urgency_score"))
    actionability_score = clamp_score(signal.get("actionability_score"))

    if status == "ignored" or usefulness_score < WATCHLIST_THRESHOLD:
        return "low_priority"
    if status == "needs_action" or (urgency_score >= 75 and actionability_score >= 65):
        return "needs_action"
    if usefulness_score >= HIGH_VALUE_THRESHOLD:
        return "high_value"
    return "watchlist"


def build_useful_signal_registry(
    manifests: list[dict] | None = None,
    action_rows: list[dict] | None = None,
    extra_signals: list[dict] | None = None,
) -> list[dict]:
    """Build scored useful signals from demo/local metadata only."""
    _ = manifests or []
    _ = action_rows or []
    seeds = list(DEMO_USEFUL_SIGNAL_SEEDS)
    if extra_signals:
        seeds.extend(extra_signals)
    signals = [score_signal(seed) for seed in seeds]
    return sorted(signals, key=lambda item: (-item["usefulness_score"], item["title"].lower()))


def build_signal_summary(signals: list[dict]) -> dict[str, Any]:
    """Summarize signal buckets and scores for metric cards."""
    if not signals:
        return {
            "total_signals": 0,
            "high_value_signals": 0,
            "needs_action_signals": 0,
            "watchlist_signals": 0,
            "ignored_low_priority_signals": 0,
            "average_usefulness_score": 0,
        }

    return {
        "total_signals": len(signals),
        "high_value_signals": sum(1 for signal in signals if signal.get("bucket") == "high_value"),
        "needs_action_signals": sum(1 for signal in signals if signal.get("bucket") == "needs_action"),
        "watchlist_signals": sum(1 for signal in signals if signal.get("bucket") == "watchlist"),
        "ignored_low_priority_signals": sum(1 for signal in signals if signal.get("bucket") == "low_priority"),
        "average_usefulness_score": round(mean(signal["usefulness_score"] for signal in signals), 1),
    }


def filter_useful_signals(
    signals: list[dict],
    *,
    category: str = "All",
    status: str = "All",
    source_agent: str = "All",
    min_usefulness_score: int = 0,
) -> list[dict]:
    """Filter signals for display without changing the underlying registry."""
    min_score = clamp_score(min_usefulness_score)
    filtered = []
    for signal in signals:
        if category != "All" and signal.get("category") != category:
            continue
        if status != "All" and signal.get("status") != status:
            continue
        if source_agent != "All" and signal.get("source_agent") != source_agent:
            continue
        if signal.get("usefulness_score", 0) < min_score:
            continue
        filtered.append(signal)
    return filtered


def group_signal_buckets(signals: list[dict]) -> dict[str, list[dict]]:
    """Group signals into Useful Signals page buckets."""
    return {
        "top": sorted(signals, key=lambda item: (-item["usefulness_score"], item["title"].lower()))[:5],
        "needs_action": [signal for signal in signals if signal.get("bucket") == "needs_action"],
        "watchlist": [signal for signal in signals if signal.get("bucket") == "watchlist"],
        "low_priority": [signal for signal in signals if signal.get("bucket") == "low_priority"],
        "high_value": [signal for signal in signals if signal.get("bucket") == "high_value"],
    }


def get_signal_category_options() -> list[str]:
    return ["All"] + sorted(SIGNAL_CATEGORIES)


def get_signal_status_options() -> list[str]:
    return ["All"] + sorted(SIGNAL_STATUSES)
