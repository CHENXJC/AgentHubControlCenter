from datetime import date

from agent_hub.report_exporter import build_report_file_name, save_markdown_report


def test_build_report_file_name_is_windows_safe():
    file_name = build_report_file_name("HUB-005 REPORT", date(2026, 6, 24))

    assert file_name == "agent_hub_portfolio_report_HUB-005-REPORT_2026-06-24.md"
    assert ":" not in file_name
    assert "\\" not in file_name


def test_save_markdown_report_writes_to_output_dir(tmp_path):
    report_path = save_markdown_report(
        "# Demo Report\n",
        tmp_path,
        "demo_report.md",
    )

    assert report_path == tmp_path / "demo_report.md"
    assert report_path.read_text(encoding="utf-8") == "# Demo Report\n"
