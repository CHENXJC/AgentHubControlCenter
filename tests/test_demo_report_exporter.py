from pathlib import Path

import pytest

from agent_hub.demo_report_exporter import (
    assert_public_report_path,
    build_public_report_file_name,
    ensure_public_reports_dir,
    export_report_bundle,
    find_report_file_policy_violations,
    get_public_reports_dir,
)


def test_get_public_reports_dir_targets_outputs_public_reports(tmp_path):
    public_reports_dir = get_public_reports_dir(tmp_path)

    assert public_reports_dir == tmp_path / "outputs" / "public_reports"


def test_export_report_bundle_writes_only_public_report_formats(tmp_path):
    report_contents = {
        "markdown": "# Demo\n",
        "json": "{\"demo\": true}\n",
        "csv": "section,item_id,title,status,score_or_risk,execution_policy,recommended_next_step\n",
    }

    exported = export_report_bundle(
        report_contents,
        project_root=tmp_path,
        report_id="agenthub:test report",
    )

    assert set(exported) == {"markdown", "json", "csv"}
    assert all(path.exists() for path in exported.values())
    assert exported["markdown"].name == "agenthub-test-report.md"
    assert find_report_file_policy_violations(exported) == []
    assert not (tmp_path / "outputs" / "private").exists()


def test_ensure_public_reports_dir_does_not_create_private_outputs(tmp_path):
    public_reports_dir = ensure_public_reports_dir(tmp_path)

    assert public_reports_dir.exists()
    assert public_reports_dir.name == "public_reports"
    assert not (tmp_path / "outputs" / "private").exists()


def test_build_public_report_file_name_rejects_unsupported_format():
    with pytest.raises(ValueError):
        build_public_report_file_name("demo", "html")


def test_assert_public_report_path_rejects_private_or_outside_paths(tmp_path):
    public_reports_dir = tmp_path / "outputs" / "public_reports"
    public_reports_dir.mkdir(parents=True)

    assert_public_report_path(public_reports_dir / "safe.md", public_reports_dir)

    with pytest.raises(ValueError):
        assert_public_report_path(tmp_path / "outputs" / "private" / "unsafe.md", public_reports_dir)

    with pytest.raises(ValueError):
        assert_public_report_path(Path(tmp_path) / "unsafe.md", public_reports_dir)
