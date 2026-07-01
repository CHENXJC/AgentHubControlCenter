import json
from pathlib import Path

from agent_hub.workflow_pack_integration import (
    build_workflow_pack_integration_card,
    get_workflow_pack_integration_status,
    load_workflow_pack_agent_summary,
    load_workflow_pack_summary,
)


def test_missing_summary_file_returns_missing(tmp_path: Path):
    result = load_workflow_pack_agent_summary(tmp_path / "agenthub_summary.json")

    assert result["integration_status"] == "missing"


def test_invalid_json_returns_invalid(tmp_path: Path):
    path = tmp_path / "agenthub_summary.json"
    path.write_text("{bad-json", encoding="utf-8")

    result = load_workflow_pack_agent_summary(path)

    assert result["integration_status"] == "invalid"


def test_valid_workflow_pack_agent_summary_reads_total_packs(tmp_path: Path):
    path = tmp_path / "agenthub_summary.json"
    path.write_text(
        json.dumps(
            {
                "agent_name": "WorkflowPackAgent",
                "project_code": "WPA-004",
                "total_workflow_packs": 23,
                "metadata_enriched_agents": ["AgentA", "AgentB"],
                "safe_metadata_integration": True,
                "top_workflow_packs": [{"pack_name": "Top Pack"}],
            }
        ),
        encoding="utf-8",
    )

    result = load_workflow_pack_agent_summary(path)
    card = build_workflow_pack_integration_card(result, {"integration_status": "missing", "data": {}})

    assert result["integration_status"] == "available"
    assert card["total_workflow_packs"] == 23
    assert card["metadata_enriched_agents"] == 2


def test_valid_workflow_pack_summary_reads_top_packs(tmp_path: Path):
    path = tmp_path / "workflow_pack_summary.json"
    path.write_text(
        json.dumps(
            {
                "total_packs": 23,
                "safe_metadata_integration": True,
                "top_workflow_packs": [
                    {"pack_name": "Pack A", "total_score": 95},
                    {"pack_name": "Pack B", "total_score": 90},
                ],
            }
        ),
        encoding="utf-8",
    )

    result = load_workflow_pack_summary(path)

    assert result["integration_status"] == "available"
    assert result["data"]["top_workflow_packs"][0]["pack_name"] == "Pack A"


def test_integration_card_returns_stable_structure():
    card = build_workflow_pack_integration_card(
        {
            "integration_status": "available",
            "summary_path": "agenthub_summary.json",
            "details": "ok",
            "data": {
                "agent_name": "WorkflowPackAgent",
                "total_workflow_packs": 23,
                "metadata_enriched_agents": ["A"],
                "safe_metadata_integration": True,
                "source_metadata_stats": {"loaded_metadata_files": 35},
                "recommended_next_actions": ["Next"],
                "top_workflow_packs": [{"pack_name": "Top"}],
            },
        },
        {
            "integration_status": "available",
            "summary_path": "workflow_pack_summary.json",
            "details": "ok",
            "data": {"total_packs": 23},
        },
    )

    assert card["integration_status"] == "available"
    assert card["agent_name"] == "WorkflowPackAgent"
    assert card["safe_metadata_integration"] is True
    assert card["top_workflow_packs"][0]["pack_name"] == "Top"


def test_default_workflow_pack_integration_status_is_stable():
    result = get_workflow_pack_integration_status()

    assert result["integration_status"] in {"available", "missing", "invalid"}
    assert result["agent_name"] == "WorkflowPackAgent"
