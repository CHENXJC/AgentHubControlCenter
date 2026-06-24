from __future__ import annotations


def status_badge_text(status: str) -> str:
    """Return a compact status label for dashboard display."""
    clean_status = (status or "").strip()
    return f"Status: {clean_status}" if clean_status else "Status: Unknown"


def pin_badge_text(pin_status: str) -> str:
    """Return a compact pin label for dashboard display."""
    clean_pin_status = (pin_status or "").strip()
    return f"Pin: {clean_pin_status}" if clean_pin_status else "Pin: Unknown"


def safe_display(value: str | None, fallback: str = "\u2014") -> str:
    """Return a user-facing value or fallback when the value is blank."""
    if value is None:
        return fallback
    clean_value = str(value).strip()
    return clean_value if clean_value else fallback


def health_badge_text(health_status: str) -> str:
    """Return a compact health status label for dashboard display."""
    clean_health_status = (health_status or "").strip()
    return f"Health: {clean_health_status}" if clean_health_status else "Health: Unknown"


def priority_badge_text(priority: str) -> str:
    """Return a compact priority label for dashboard display."""
    clean_priority = (priority or "").strip()
    return f"Priority: {clean_priority}" if clean_priority else "Priority: Unknown"


def format_count_label(label: str, value: int) -> str:
    """Format a metric label and count for compact text displays."""
    return f"{label}: {value}"


def safe_list_join(values: list[str], fallback: str = "\u2014") -> str:
    """Join list values for display, or return a fallback when empty."""
    clean_values = [str(value).strip() for value in values if str(value).strip()]
    return ", ".join(clean_values) if clean_values else fallback


def render_status_label_text(status: str) -> str:
    """Return normalized status label text for UI badges."""
    clean_status = (status or "").strip()
    return f"Status: {clean_status}" if clean_status else "Status: Unknown"


def render_health_label_text(health_status: str) -> str:
    """Return normalized health label text for UI badges."""
    clean_health_status = (health_status or "").strip()
    return f"Health: {clean_health_status}" if clean_health_status else "Health: Unknown"


def render_priority_label_text(priority: str) -> str:
    """Return normalized priority label text for UI badges."""
    clean_priority = (priority or "").strip()
    return f"Priority: {clean_priority}" if clean_priority else "Priority: Unknown"


def build_metric_display_value(value) -> str:
    """Format a metric value for dashboard display."""
    if value is None:
        return "0"
    if isinstance(value, float):
        return f"{value:,.1f}"
    if isinstance(value, int):
        return f"{value:,}"
    clean_value = str(value).strip()
    return clean_value if clean_value else "0"


def truncate_text(value: str, max_length: int = 120) -> str:
    """Trim text to a display-friendly length."""
    clean_value = (value or "").strip()
    if len(clean_value) <= max_length:
        return clean_value
    if max_length <= 3:
        return clean_value[:max_length]
    return clean_value[: max_length - 3].rstrip() + "..."
