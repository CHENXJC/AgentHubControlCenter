from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CANONICAL_SCREENSHOTS = [
    "01_command_overview.png",
    "02_agent_registry.png",
    "03_action_center.png",
    "04_codex_prompt_generator.png",
    "05_useful_signals.png",
    "06_workflow_simulation.png",
    "07_connectors.png",
    "08_agent_onboarding_metrics.png",
    "09_report_export.png",
    "10_approval_gates.png",
]

REQUIRED_SAFETY_NOTES = [
    "Demo/local metadata only",
    "No live connector connected",
    "No credentials loaded",
    "No real action executed",
    "No external API called",
]


def test_v2_011_canonical_screenshots_exist_and_are_referenced():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    for filename in CANONICAL_SCREENSHOTS:
        screenshot_path = ROOT / "docs" / "images" / filename
        assert screenshot_path.exists(), filename
        assert screenshot_path.stat().st_size > 10_000, filename
        assert f"docs/images/{filename}" in readme


def test_sample_demo_report_summary_is_public_safe_showcase_metadata():
    summary_path = ROOT / "docs" / "SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md"
    summary = summary_path.read_text(encoding="utf-8")

    assert "HUB-V2-012-PUBLIC-SHOWCASE-RELEASE-CHECK-COMPLETE" in summary
    assert "outputs/public_reports/agenthub_v2_demo_workflow_report_2026-06-28.md" in summary
    assert "No full large report dump in README." in summary

    for note in REQUIRED_SAFETY_NOTES:
        assert note in summary
