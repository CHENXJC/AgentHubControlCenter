from __future__ import annotations

from datetime import date
from pathlib import Path
import re


def build_report_file_name(
    stage: str = "HUB-005-REPORT",
    report_date: date | str | None = None,
) -> str:
    """Build a Windows-safe Markdown report file name."""
    if report_date is None:
        date_text = date.today().isoformat()
    elif isinstance(report_date, date):
        date_text = report_date.isoformat()
    else:
        date_text = str(report_date)

    stage_slug = re.sub(r"[^A-Za-z0-9_-]+", "-", stage).strip("-") or "report"
    return f"agent_hub_portfolio_report_{stage_slug}_{date_text}.md"


def save_markdown_report(
    markdown_text: str,
    output_dir: str | Path,
    file_name: str | None = None,
) -> Path:
    """Save a Markdown report to a local output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    report_file_name = file_name or build_report_file_name()
    report_path = output_path / report_file_name
    report_path.write_text(markdown_text, encoding="utf-8")
    return report_path
