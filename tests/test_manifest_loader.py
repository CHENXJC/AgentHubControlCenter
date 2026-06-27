import json

from agent_hub.manifest_loader import (
    discover_project_directories,
    manifest_record_to_registry_record,
    scan_ai_projects_manifests,
    scan_project_manifest,
    validate_manifest_record,
)


def _valid_manifest(agent_id="demo_agent"):
    return {
        "agent_id": agent_id,
        "agent_name": "DemoAgent",
        "category": "Workflow Automation",
        "description": "Demo workflow automation assistant.",
        "project_path": "F:\\AIProjects\\DemoAgent",
        "status": "Active",
        "inputs": ["workflow_notes"],
        "outputs": ["dashboard"],
        "actions": [{"action_id": "launch", "label": "Launch local app"}],
        "connectors": [{"connector_id": "local_filesystem", "label": "Local Filesystem"}],
        "demo_mode": True,
        "safe_mode": True,
        "version": "DEMO-001",
        "next_recommended_action": "Review imported manifest",
        "github_repo": "https://github.com/example/demo",
        "tags": ["Python", "Streamlit"],
    }


def test_validate_manifest_record_accepts_required_fields():
    result = validate_manifest_record(_valid_manifest())

    assert result["is_valid"] is True
    assert result["missing_fields"] == []
    assert result["recommended_fix"] == "Manifest is ready for import."


def test_validate_manifest_record_reports_missing_fields():
    result = validate_manifest_record({"agent_id": "broken"})

    assert result["is_valid"] is False
    assert "agent_name" in result["missing_fields"]
    assert "Add required fields" in result["recommended_fix"]


def test_manifest_record_to_registry_record_maps_manifest_fields(tmp_path):
    manifest_path = tmp_path / "DemoAgent" / "agent_manifest.json"
    manifest_path.parent.mkdir()

    record = manifest_record_to_registry_record(
        _valid_manifest(),
        manifest_path,
        source="local_manifest",
    )

    assert record["agent_id"] == "demo_agent"
    assert record["agent_name"] == "DemoAgent"
    assert record["source"] == "local_manifest"
    assert record["github_url"] == "https://github.com/example/demo"
    assert record["stage"] == "DEMO-001"
    assert "Python" in record["tech_stack"]
    assert record["manifest_inputs"] == ["workflow_notes"]
    assert record["manifest_outputs"] == ["dashboard"]
    assert record["manifest_actions"][0]["action_id"] == "launch"
    assert record["manifest_connectors"][0]["connector_id"] == "local_filesystem"
    assert record["demo_mode"] is True
    assert record["safe_mode"] is True


def test_scan_project_manifest_handles_valid_agents_list(tmp_path):
    project_dir = tmp_path / "DemoAgent"
    project_dir.mkdir()
    (project_dir / "agent_manifest.json").write_text(
        json.dumps({"agents": [_valid_manifest()]}),
        encoding="utf-8",
    )

    result = scan_project_manifest(project_dir)

    assert result["manifest_status"] == "valid"
    assert result["valid_agent_records"][0]["agent_id"] == "demo_agent"


def test_scan_project_manifest_handles_missing_and_invalid_json(tmp_path):
    missing_dir = tmp_path / "MissingAgent"
    missing_dir.mkdir()
    invalid_dir = tmp_path / "InvalidAgent"
    invalid_dir.mkdir()
    (invalid_dir / "agent_manifest.json").write_text("{bad json", encoding="utf-8")

    missing_result = scan_project_manifest(missing_dir)
    invalid_result = scan_project_manifest(invalid_dir)

    assert missing_result["manifest_status"] == "missing"
    assert invalid_result["manifest_status"] == "invalid"
    assert "Invalid JSON" in invalid_result["warnings"][0]


def test_scan_ai_projects_skips_runtime_directories(tmp_path):
    (tmp_path / ".venv").mkdir()
    (tmp_path / "node_modules").mkdir()
    project_dir = tmp_path / "DemoAgent"
    project_dir.mkdir()
    (project_dir / "agent_manifest.json").write_text(
        json.dumps(_valid_manifest()),
        encoding="utf-8",
    )

    projects = discover_project_directories(tmp_path)
    scan = scan_ai_projects_manifests(tmp_path)

    assert [path.name for path in projects] == ["DemoAgent"]
    assert scan["summary"]["total_projects_scanned"] == 1
    assert scan["summary"]["valid_manifests"] == 1
