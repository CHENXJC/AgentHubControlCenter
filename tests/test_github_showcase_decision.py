from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_github_showcase_decision_docs_exist_and_block_execution():
    decision = _read("docs/GITHUB_SHOWCASE_UPDATE_DECISION.md")
    commit_manifest = _read("docs/PUBLIC_COMMIT_FILE_MANIFEST.md")
    exclusion = _read("docs/PUBLIC_EXCLUSION_MANIFEST.md")

    assert "HUB-V2-013-GITHUB-SHOWCASE-UPDATE-DECISION-COMPLETE" in decision
    assert "HUB-V2-014-GIT-COMMIT-PUSH" in decision
    assert "does not run `git add`" in decision
    assert "Do not run this command in HUB-V2-013" in commit_manifest
    assert "git add -- $files" in commit_manifest
    assert "outputs/public_reports/.gitkeep" in commit_manifest
    assert "outputs/public_reports/*.md" in exclusion
    assert "outputs/private/` is absent" in exclusion


def test_public_commit_manifest_has_required_categories():
    manifest = _read("docs/PUBLIC_COMMIT_FILE_MANIFEST.md")

    for heading in [
        "Core App",
        "New `agent_hub` Modules",
        "Manifests And Contracts",
        "Documentation",
        "Screenshots",
        "Launch Scripts",
        "Tests",
        "Output Boundary Marker",
        "Child Agent Manifest Inventory",
        "Suggested Staging Command",
    ]:
        assert heading in manifest

    for screenshot in [
        "docs/images/01_command_overview.png",
        "docs/images/02_agent_registry.png",
        "docs/images/03_action_center.png",
        "docs/images/04_codex_prompt_generator.png",
        "docs/images/05_useful_signals.png",
        "docs/images/06_workflow_simulation.png",
        "docs/images/07_connectors.png",
        "docs/images/08_agent_onboarding_metrics.png",
        "docs/images/09_report_export.png",
        "docs/images/10_approval_gates.png",
    ]:
        assert screenshot in manifest


def test_public_exclusion_manifest_keeps_private_and_generated_files_out():
    exclusion = _read("docs/PUBLIC_EXCLUSION_MANIFEST.md")

    for excluded in [
        ".env",
        ".venv/",
        "credentials.json",
        "token.json",
        "outputs/public_reports/*.json",
        "outputs/public_reports/*.csv",
        "AGENTS.md",
        "__pycache__/",
    ]:
        assert excluded in exclusion

    assert "Only `.gitkeep` is recommended for commit" in exclusion
