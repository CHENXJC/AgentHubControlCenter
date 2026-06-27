import json

from agent_hub.agent_onboarding import (
    build_agent_onboarding,
    build_onboarding_summary,
    merge_registry_with_manifest_records,
)


def _manifest(agent_id="demo_agent", name="DemoAgent"):
    return {
        "agent_id": agent_id,
        "agent_name": name,
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
    }


def test_merge_registry_with_manifest_records_prefers_manifest_over_static():
    static_agents = [
        {
            "agent_id": "demo_agent",
            "agent_name": "StaticDemo",
            "category": "Static",
            "source": "static_registry",
        }
    ]
    manifest_records = [
        {
            "agent_id": "demo_agent",
            "agent_name": "ManifestDemo",
            "category": "Workflow Automation",
            "source": "local_manifest",
        }
    ]

    result = merge_registry_with_manifest_records(static_agents, manifest_records)

    assert result["merged_agents"][0]["agent_name"] == "ManifestDemo"
    assert result["duplicate_agent_ids"][0]["resolution"] == "manifest_overrides_static_registry"
    assert result["imported_agents"][0]["source"] == "local_manifest"


def test_merge_registry_with_manifest_records_keeps_first_manifest_duplicate():
    manifest_records = [
        {"agent_id": "demo_agent", "agent_name": "First", "source": "local_manifest"},
        {"agent_id": "demo_agent", "agent_name": "Second", "source": "local_manifest"},
    ]

    result = merge_registry_with_manifest_records([], manifest_records)

    assert result["merged_agents"][0]["agent_name"] == "First"
    assert result["duplicate_agent_ids"][0]["resolution"] == "first_manifest_kept"


def test_build_onboarding_summary_returns_recommended_fixes():
    summary = build_onboarding_summary(
        {
            "total_projects_scanned": 3,
            "manifests_found": 2,
            "valid_manifests": 1,
            "invalid_manifests": 1,
            "missing_manifests": 1,
        },
        imported_agents=[{"agent_id": "demo"}],
        duplicate_agent_ids=[{"agent_id": "demo"}],
        project_rows=[
            {"manifest_status": "valid"},
            {"manifest_status": "invalid"},
            {"manifest_status": "missing"},
        ],
    )

    assert summary["total_projects_scanned"] == 3
    assert summary["imported_agents"] == 1
    assert summary["duplicate_agent_ids"] == 1
    assert len(summary["recommended_fixes"]) == 3


def test_build_agent_onboarding_scans_and_merges(tmp_path):
    project_dir = tmp_path / "DemoAgent"
    project_dir.mkdir()
    (project_dir / "agent_manifest.json").write_text(
        json.dumps(_manifest()),
        encoding="utf-8",
    )
    missing_dir = tmp_path / "MissingAgent"
    missing_dir.mkdir()

    result = build_agent_onboarding(
        tmp_path,
        static_agents=[{"agent_id": "static_agent", "agent_name": "StaticAgent"}],
    )

    assert result["summary"]["total_projects_scanned"] == 2
    assert result["summary"]["valid_manifests"] == 1
    assert result["summary"]["missing_manifests"] == 1
    assert any(agent["agent_id"] == "demo_agent" for agent in result["merged_agents"])
    assert result["missing_manifest_projects"][0]["project_name"] == "MissingAgent"
