from agent_hub.useful_signal_engine import (
    build_signal_summary,
    build_useful_signal_registry,
    calculate_usefulness_score,
    filter_useful_signals,
    group_signal_buckets,
)
from agent_hub.useful_signal_schema import DISPLAY_ONLY_EXECUTION_POLICY


def test_build_useful_signal_registry_creates_demo_signals():
    signals = build_useful_signal_registry()

    assert len(signals) >= 12
    assert all(signal["schema_valid"] is True for signal in signals)
    assert all("usefulness_score" in signal for signal in signals)
    assert all(signal["execution_policy"] == DISPLAY_ONLY_EXECUTION_POLICY for signal in signals)
    assert all(signal["recommended_action"] for signal in signals)
    assert all(signal["why_important"] for signal in signals)
    assert all(signal["suggested_next_step"] for signal in signals)
    assert all("Usefulness =" in signal["score_explanation"] for signal in signals)


def test_calculate_usefulness_score_is_explainable_and_bounded():
    signal = {
        "category": "project_progress",
        "relevance_score": 90,
        "urgency_score": 80,
        "actionability_score": 70,
        "value_score": 60,
        "risk_score": 10,
    }

    score = calculate_usefulness_score(signal)

    assert 0 <= score <= 100
    assert score == 76


def test_signal_summary_and_buckets():
    signals = build_useful_signal_registry()
    summary = build_signal_summary(signals)
    buckets = group_signal_buckets(signals)

    assert summary["total_signals"] >= 12
    assert summary["high_value_signals"] >= 1
    assert summary["needs_action_signals"] >= 1
    assert summary["watchlist_signals"] >= 1
    assert len(buckets["top"]) == 5
    assert buckets["needs_action"]
    assert buckets["watchlist"]


def test_filter_useful_signals_by_category_status_agent_and_score():
    signals = build_useful_signal_registry()

    filtered = filter_useful_signals(
        signals,
        category="risk_warning",
        status="needs_action",
        source_agent="AgentHubControlCenter",
        min_usefulness_score=80,
    )

    assert filtered
    assert all(signal["category"] == "risk_warning" for signal in filtered)
    assert all(signal["status"] == "needs_action" for signal in filtered)
    assert all(signal["source_agent"] == "AgentHubControlCenter" for signal in filtered)
    assert all(signal["usefulness_score"] >= 80 for signal in filtered)


def test_low_priority_bucket_accepts_ignored_or_low_score_signal():
    signals = build_useful_signal_registry(
        extra_signals=[
            {
                "signal_id": "ignored_demo_signal",
                "title": "Ignored demo signal",
                "source_agent": "DemoAgent",
                "source_type": "manual_demo_data",
                "category": "learning_value",
                "summary": "Low value placeholder.",
                "relevance_score": 20,
                "urgency_score": 10,
                "actionability_score": 15,
                "value_score": 25,
                "risk_score": 5,
                "recommended_action": "Ignore for now.",
                "target_agent": "DemoAgent",
                "status": "ignored",
            }
        ]
    )
    ignored = next(signal for signal in signals if signal["signal_id"] == "ignored_demo_signal")

    assert ignored["bucket"] == "low_priority"
    assert ignored["usefulness_score"] < 55
