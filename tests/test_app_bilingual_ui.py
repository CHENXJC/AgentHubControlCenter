from streamlit.testing.v1 import AppTest

from agent_hub.stage_status import get_stage_snapshot
from agent_hub.ui_i18n import t


def _tab_labels(app: AppTest) -> set[str]:
    return {tab.label for tab in app.tabs}


def test_app_bilingual_tabs_render_without_exceptions():
    app = AppTest.from_file("app.py", default_timeout=120)

    app.run(timeout=120)

    assert len(app.exception) == 0
    assert {
        "总控概览",
        "我的工具 / 智能体注册表",
        "有用信号",
        "操作中心",
        "连接器",
        "未来插件接口",
    }.issubset(_tab_labels(app))
    assert app.radio[0].label == "界面语言"
    assert app.radio[0].value == "中文"
    assert t("product_status", "zh") == "产品状态"
    assert t("latest_checkpoint", "zh") == "最新检查点"
    assert t("manifest_version", "zh") == "Manifest 版本"
    zh_markdown = "\n".join(str(item.value) for item in app.markdown)
    for expected in [
        "本地 Manifest",
        "演示模式 / 安全模式",
        "已完成",
        "可公开展示",
        "查看项目状态",
        "暂无立即行动",
        "小企业运营诊断智能体",
        "智能体运维 / 作品集运维",
    ]:
        assert expected in zh_markdown
    for forbidden in [
        "Local Manifest",
        "Demo Mode / Safe Mode",
        "No immediate action",
        "View project status",
        "Showcase Ready",
        "AgentOps / PortfolioOps",
    ]:
        assert forbidden not in zh_markdown

    app.radio[0].set_value("English").run(timeout=120)

    assert len(app.exception) == 0
    assert {
        "Command Overview",
        "My Tools / Agent Registry",
        "Useful Signals",
        "Action Center",
        "Connectors",
        "Future Plugin Interface",
    }.issubset(_tab_labels(app))
    assert app.radio[0].value == "English"
    markdown_values = [item.value for item in app.markdown]
    assert any("Product Status: Maintain / Showcase Ready" in value for value in markdown_values)
    assert any("Latest Checkpoint:" in value for value in markdown_values)
    assert any("Manifest Version:" in value for value in markdown_values)
    en_markdown = "\n".join(str(item.value) for item in app.markdown)
    assert "Local Manifest" in en_markdown
    assert "Demo Mode / Safe Mode" in en_markdown
    assert "View project status" in en_markdown

    snapshot = get_stage_snapshot("F:\\AIProjects\\AgentHubControlCenter")
    assert snapshot["product_status"] == "Maintain / Showcase Ready"
