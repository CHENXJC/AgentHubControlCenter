from agent_hub.ui_helpers import (
    build_metric_display_value,
    render_health_label_text,
    render_priority_label_text,
    render_status_label_text,
    truncate_text,
)


def test_render_status_label_text():
    assert render_status_label_text("Complete") == "Status: Complete"
    assert render_status_label_text("") == "Status: Unknown"


def test_render_health_label_text():
    assert render_health_label_text("Showcase Ready") == "Health: Showcase Ready"
    assert render_health_label_text("") == "Health: Unknown"


def test_render_priority_label_text():
    assert render_priority_label_text("High") == "Priority: High"
    assert render_priority_label_text("") == "Priority: Unknown"


def test_build_metric_display_value():
    assert build_metric_display_value(1200) == "1,200"
    assert build_metric_display_value(3.5) == "3.5"
    assert build_metric_display_value(None) == "0"


def test_truncate_text():
    assert truncate_text("short text", 120) == "short text"
    assert truncate_text("abcdefghijklmnopqrstuvwxyz", 10) == "abcdefg..."
