import json
from pathlib import Path

from agent_hub.stage_status import (
    get_product_status_label,
    get_stage_snapshot,
    load_manifest_version,
    load_project_status_checkpoint,
)


def test_load_project_status_checkpoint_reads_top_current_status(tmp_path):
    (tmp_path / "PROJECT_STATUS.md").write_text(
        "# Project Status\n\nCurrent status: DEMO-CHECKPOINT-COMPLETE\n",
        encoding="utf-8",
    )

    assert load_project_status_checkpoint(tmp_path) == "DEMO-CHECKPOINT-COMPLETE"


def test_stage_snapshot_separates_cross_project_checkpoint_from_product_status(tmp_path):
    (tmp_path / "PROJECT_STATUS.md").write_text(
        "# Project Status\n\n"
        "Current status: CLIENTDELIVERYKIT-010-GITHUB-LIVE-SHOWCASE-VERIFICATION-AND-AGENTHUB-PUBLISHED-STATUS-SYNC-COMPLETE\n",
        encoding="utf-8",
    )
    (tmp_path / "agent_manifest.json").write_text(
        json.dumps(
            {
                "manifest_version": "HUB-V2-022",
                "agents": [
                    {
                        "agent_id": "agent_hub_control_center",
                        "status": "bilingual_ui_stage_sync_ready",
                        "version": "HUB-V2-022",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    snapshot = get_stage_snapshot(tmp_path)

    assert snapshot["product_status"] == "Maintain / Showcase Ready"
    assert snapshot["latest_checkpoint"].startswith("CLIENTDELIVERYKIT-010")
    assert snapshot["manifest_version"] == "HUB-V2-022"


def test_manifest_version_falls_back_to_first_agent_version(tmp_path):
    (tmp_path / "agent_manifest.json").write_text(
        json.dumps({"agents": [{"agent_id": "demo", "version": "AGENT-STAGE"}]}),
        encoding="utf-8",
    )

    assert load_manifest_version(tmp_path) == "AGENT-STAGE"


def test_current_project_stage_snapshot_is_not_stale_hub_v2_014():
    root = Path(__file__).resolve().parents[1]
    snapshot = get_stage_snapshot(root)

    assert snapshot["product_status"] == "Maintain / Showcase Ready"
    assert snapshot["latest_checkpoint"] != "HUB-V2-014"
    assert snapshot["manifest_version"] != "HUB-V2-014"
    assert get_product_status_label(root) == "Maintain / Showcase Ready"
