from pathlib import Path

from agent_hub.ui_i18n import get_language, resolve_project_stage, set_language, t


def test_language_defaults_to_chinese():
    state = {}

    assert get_language(state) == "zh"
    assert t("tab_command_overview", get_language(state)) == "总控概览"


def test_set_language_accepts_labels_and_codes():
    state = {}

    assert set_language("English", state) == "en"
    assert get_language(state) == "en"
    assert t("tab_action_center", get_language(state)) == "Action Center"

    assert set_language("中文", state) == "zh"
    assert t("tab_action_center", get_language(state)) == "操作中心"


def test_translation_falls_back_to_key_for_unknown_label():
    assert t("missing.translation.key", "zh") == "missing.translation.key"


def test_resolve_project_stage_prefers_project_status(tmp_path):
    (tmp_path / "PROJECT_STATUS.md").write_text(
        "# Project Status\n\nCurrent status: DEMO-STAGE-COMPLETE\n",
        encoding="utf-8",
    )
    (tmp_path / "agent_manifest.json").write_text(
        '{"manifest_version": "MANIFEST-STAGE"}',
        encoding="utf-8",
    )

    result = resolve_project_stage(tmp_path)

    assert result["stage"] == "DEMO-STAGE-COMPLETE"
    assert result["source"] == "PROJECT_STATUS.md"
    assert result["manifest_stage"] == "MANIFEST-STAGE"


def test_resolve_project_stage_falls_back_to_manifest(tmp_path):
    (tmp_path / "agent_manifest.json").write_text(
        '{"agents": [{"version": "AGENT-VERSION"}]}',
        encoding="utf-8",
    )

    result = resolve_project_stage(tmp_path)

    assert result["stage"] == "AGENT-VERSION"
    assert result["source"] == "agent_manifest.json"


def test_current_project_stage_is_not_stale_hub_v2_014():
    root = Path(__file__).resolve().parents[1]
    result = resolve_project_stage(root)

    assert result["stage"] != "HUB-V2-014"
    assert result["source"] in {"PROJECT_STATUS.md", "agent_manifest.json"}
