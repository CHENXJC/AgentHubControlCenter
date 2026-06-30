import json
from pathlib import Path

from agent_hub.external_agent_summary import (
    build_agent_summary_metrics,
    build_external_summary_index,
    build_summary_display_rows,
    read_agenthub_summary,
    resolve_agent_artifact_path,
)
from agent_hub.manifest_loader import scan_project_manifest


def _agent(project_dir: Path) -> dict:
    return {
        "agent_id": "data_to_insight_workflow_agent",
        "agent_name": "DataToInsightWorkflowAgent",
        "local_path": str(project_dir),
        "agenthub_summary_path": "outputs/agenthub_summary.json",
    }


def test_resolve_agent_artifact_path_stays_inside_project(tmp_path):
    agent = _agent(tmp_path)

    assert resolve_agent_artifact_path(agent, "agenthub_summary_path") == (
        tmp_path / "outputs" / "agenthub_summary.json"
    ).resolve()

    escaped = dict(agent)
    escaped["agenthub_summary_path"] = "..\\outside.json"
    assert resolve_agent_artifact_path(escaped, "agenthub_summary_path") is None


def test_read_agenthub_summary_and_metrics(tmp_path):
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    payload = {
        "agent_id": "data_to_insight_workflow_agent",
        "agent_name": "DataToInsightWorkflowAgent",
        "status": "D2I-004-AGENTHUB-CONTROLCENTER-INTEGRATION-COMPLETE",
        "demo_mode": True,
        "public_safe": True,
        "total_items_processed": 14,
        "high_value_signals": 4,
        "medium_value_items": 5,
        "low_value_or_noise_items": 5,
        "recommended_actions_count": 23,
        "top_routes": {"DataToInsightWorkflowAgent": 9, "AgentHubControlCenter": 2},
        "latest_report_path": "outputs/demo_insight_report.md",
        "generated_at": "2026-06-30T00:00:00+00:00",
    }
    (output_dir / "agenthub_summary.json").write_text(json.dumps(payload), encoding="utf-8")

    summary = read_agenthub_summary(_agent(tmp_path))
    metrics = build_agent_summary_metrics(summary["data"])
    rows = build_summary_display_rows(summary["data"])

    assert summary["available"] is True
    assert metrics["total_items_processed"] == 14
    assert metrics["top_route"] == "DataToInsightWorkflowAgent"
    assert any(row["field"] == "high_value_signals" for row in rows)


def test_build_external_summary_index_reads_declared_summary(tmp_path):
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    (output_dir / "agenthub_summary.json").write_text(
        json.dumps(
            {
                "agent_id": "data_to_insight_workflow_agent",
                "agent_name": "DataToInsightWorkflowAgent",
                "total_items_processed": 14,
            }
        ),
        encoding="utf-8",
    )

    index = build_external_summary_index([_agent(tmp_path)])

    assert "data_to_insight_workflow_agent" in index
    assert index["data_to_insight_workflow_agent"]["data"]["total_items_processed"] == 14


def test_d2i_manifest_is_agenthub_valid_when_project_exists():
    d2i_project = Path("F:/AIProjects/DataToInsightWorkflowAgent")
    if not d2i_project.exists():
        return

    result = scan_project_manifest(d2i_project)

    assert result["manifest_status"] == "valid"
    d2i_record = result["valid_agent_records"][0]
    assert d2i_record["agent_id"] == "data_to_insight_workflow_agent"
    assert d2i_record["agent_name"] == "DataToInsightWorkflowAgent"
    assert d2i_record["display_name_zh"] == "数据洞察工作流智能体"
    assert d2i_record["agenthub_summary_path"] == "outputs/agenthub_summary.json"
    assert "streamlit_dashboard" in d2i_record["capabilities"]
