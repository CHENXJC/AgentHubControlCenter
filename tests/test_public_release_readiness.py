import json
import re
import subprocess
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

REQUIRED_PUBLIC_SAFE_PHRASES = [
    "Demo/local metadata only",
    "No live connector connected",
    "No credentials loaded",
    "No real action executed",
    "No external API called",
]

PUBLIC_DOCS = [
    "README.md",
    "PROJECT_STATUS.md",
    "agent_manifest.json",
    "agent_contract.json",
    "docs/PUBLIC_SHOWCASE_MANIFEST.md",
    "docs/SHOWCASE_ASSET_CHECKLIST.md",
    "docs/SCREENSHOTS_GUIDE.md",
    "docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md",
    "docs/DEMO_WORKFLOW_REPORT_EXPORT.md",
    "docs/PUBLIC_RELEASE_CHECKLIST.md",
    "docs/V2_RELEASE_READINESS_REPORT.md",
    "docs/GITHUB_SHOWCASE_UPDATE_DECISION.md",
    "docs/PUBLIC_COMMIT_FILE_MANIFEST.md",
    "docs/PUBLIC_EXCLUSION_MANIFEST.md",
    "docs/CLIENTDELIVERYKIT_PUBLISHED_STATUS_SYNC.md",
    "docs/BILINGUAL_UI_GUIDE.md",
    "docs/STAGE_STATUS_SYNC.md",
    "docs/CHINESE_UI_COVERAGE_CHECKLIST.md",
]

SECRET_LIKE_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|password|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{8,}"),
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_public_release_docs_exist_and_have_required_sections():
    checklist = _read("docs/PUBLIC_RELEASE_CHECKLIST.md")
    report = _read("docs/V2_RELEASE_READINESS_REPORT.md")

    assert "HUB-V2-012-PUBLIC-SHOWCASE-RELEASE-CHECK-COMPLETE" in checklist
    assert "HUB-V2-012-PUBLIC-SHOWCASE-RELEASE-CHECK-COMPLETE" in report
    for heading in [
        "Feature Snapshot",
        "Showcase Assets Status",
        "Screenshot Inventory",
        "Public-Safe Report Summary Status",
        "Manifest / Contract Validation Status",
        "Test Status",
        "Security / Policy Status",
        "Git Hygiene Status",
        "Known Limitations",
        "Release Recommendation",
        "Suggested Commit Message",
        "Suggested Next Stage",
    ]:
        assert heading in report


def test_readme_screenshot_paths_match_canonical_inventory():
    readme = _read("README.md")
    screenshot_guide = _read("docs/SCREENSHOTS_GUIDE.md")
    checklist = _read("docs/PUBLIC_RELEASE_CHECKLIST.md")

    for filename in CANONICAL_SCREENSHOTS:
        relative_path = f"docs/images/{filename}"
        image_path = ROOT / relative_path
        assert relative_path in readme
        assert relative_path in screenshot_guide
        assert relative_path in checklist
        assert image_path.exists()
        assert image_path.stat().st_size > 10_000


def test_public_safe_phrases_are_visible_in_release_surface():
    combined = "\n".join(
        _read(path)
        for path in [
            "README.md",
            "docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md",
            "docs/PUBLIC_RELEASE_CHECKLIST.md",
            "docs/V2_RELEASE_READINESS_REPORT.md",
        ]
    )
    for phrase in REQUIRED_PUBLIC_SAFE_PHRASES:
        assert phrase in combined
    assert "Public-safe demo reports" in combined


def test_output_and_environment_boundaries_are_ignored():
    gitignore = _read(".gitignore")

    assert ".venv/" in gitignore
    assert ".env" in gitignore
    assert "credentials.json" in gitignore
    assert "token.json" in gitignore
    assert "outputs/*" in gitignore
    assert "!outputs/public_reports/" in gitignore
    assert "outputs/public_reports/*" in gitignore
    assert "!outputs/public_reports/.gitkeep" in gitignore
    assert not (ROOT / "outputs" / "private").exists()

    public_report = ROOT / "outputs" / "public_reports" / "agenthub_v2_demo_workflow_report_2026-06-28.md"
    if public_report.exists():
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", public_report.relative_to(ROOT).as_posix()],
            cwd=ROOT,
            check=False,
        )
        assert ignored.returncode == 0


def test_manifest_contract_and_immediate_project_manifests_load():
    root_manifest = json.loads((ROOT / "agent_manifest.json").read_text(encoding="utf-8"))
    root_contract = json.loads((ROOT / "agent_contract.json").read_text(encoding="utf-8"))

    assert root_manifest["manifest_version"] == "HUB-V2-024-DEEP-CHINESE-UI-COVERAGE-CHECK-COMPLETE"
    assert root_contract["contract_version"] == "HUB-V2-024-DEEP-CHINESE-UI-COVERAGE-CHECK-COMPLETE"
    assert root_contract["execution_policy"]["current_stage"] == "deep_chinese_ui_coverage_check"
    assert root_contract["bilingual_ui"]["default_language"] == "zh"
    assert root_contract["bilingual_ui"]["current_stage"] == "HUB-V2-024"
    assert root_manifest["agents"][0]["status"] == "deep_chinese_ui_coverage_ready"

    project_root = ROOT.parent
    manifest_paths = sorted(project_root.glob("*/agent_manifest.json"))
    loaded = [json.loads(path.read_text(encoding="utf-8")) for path in manifest_paths]

    assert len(loaded) >= 13
    client_manifest = next(
        item for item in loaded if item.get("agent_id") == "client_delivery_kit_agent"
    )
    assert client_manifest["github_repo"] == "https://github.com/CHENXJC/ClientDeliveryKitAgent"
    assert client_manifest["public_showcase_status"] == "live_showcase_verified"
    assert client_manifest["pin_status"] == "recommend_pin"
    d2i_manifest = next(
        item for item in loaded if item.get("agent_id") == "data_to_insight_workflow_agent"
    )
    assert d2i_manifest["display_name_zh"] == "数据洞察工作流智能体"
    assert d2i_manifest["agenthub_summary_path"] == "outputs/agenthub_summary.json"


def test_launcher_keeps_local_venv_and_fixed_port():
    launcher = _read("launch_command_center.cmd")

    assert 'set "PORT=8525"' in launcher
    assert ".venv\\Scripts\\python.exe" in launcher
    assert ".venv\\Scripts\\streamlit.exe" in launcher
    assert "--server.port %PORT%" in launcher
    assert "AGENTHUB_NO_BROWSER" in launcher


def test_public_docs_do_not_contain_secret_like_values():
    for path in PUBLIC_DOCS:
        text = _read(path)
        for pattern in SECRET_LIKE_PATTERNS:
            assert not pattern.search(text), path
