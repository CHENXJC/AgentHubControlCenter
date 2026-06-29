from pathlib import Path

from agent_hub.ui_i18n import (
    display_text,
    get_language,
    resolve_project_stage,
    set_language,
    t,
    translate_action_label,
    translate_agent_description,
    translate_agent_display_name,
    translate_category,
    translate_connector,
    translate_filter_option,
    translate_next_step,
    translate_status,
)


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


def test_dynamic_agent_category_status_and_filter_translations():
    assert translate_agent_display_name("BusinessOpsAgent", "zh") == "BusinessOpsAgent / 小企业运营诊断智能体"
    assert translate_category("AgentOps / PortfolioOps", "zh") == "智能体运维 / 作品集运维"
    assert translate_category("sme_operations", "zh") == "中小企业运营"
    assert translate_status("Complete", "zh") == "已完成"
    assert translate_status("Showcase Ready", "zh") == "可公开展示"
    assert translate_status("Maintain / Showcase Ready", "zh") == "维护展示就绪"
    assert translate_status("deep_chinese_ui_coverage_ready", "zh") == "深度中文 UI 覆盖就绪"
    assert translate_filter_option("All", "zh") == "全部"
    assert translate_filter_option("High", "zh") == "高"


def test_dynamic_action_connector_next_step_and_description_translations():
    assert translate_action_label("View project status", "zh") == "查看项目状态"
    assert translate_action_label("Manual run dashboard", "zh") == "手动运行仪表盘"
    assert translate_connector("Local Filesystem", "zh") == "本地文件系统"
    assert translate_connector("Streamlit local dashboard", "zh") == "Streamlit 本地仪表盘"
    assert translate_next_step("No immediate action", "zh") == "暂无立即行动"
    assert translate_next_step("Maintain showcase", "zh") == "保持展示维护状态"
    assert translate_agent_description(
        "Business operations analysis Agent for KPI-style dashboards, operational summaries, and improvement planning.",
        "zh",
    ) == "面向小企业运营诊断的智能体，用于 KPI 仪表盘、运营摘要和改进计划。"


def test_dynamic_translation_keeps_english_mode_unchanged():
    assert translate_action_label("View project status", "en") == "View project status"
    assert translate_connector("Local Filesystem", "en") == "Local Filesystem"
    assert display_text("No immediate action", "en") == "No immediate action"


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
