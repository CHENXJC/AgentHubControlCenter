from __future__ import annotations

from agent_hub.action_registry import build_action_registry, get_actions_for_agent, get_codex_prompt_actions
from agent_hub.codex_prompt_generator import (
    PROMPT_TYPES,
    RESERVED_PROMPT_TYPES,
    build_codex_prompt_package,
    extract_checkpoint_from_text,
)


def _manifest(project_path: str) -> dict:
    return {
        "agent_id": "demo_agent",
        "agent_name": "DemoAgent",
        "category": "Workflow Automation",
        "category_label": "Workflow Automation",
        "description": "Demo Agent for safe local workflow planning.",
        "project_path": project_path,
        "status": "Active",
        "stage": "DEMO-001",
        "inputs": ["local_file", "manual_notes"],
        "outputs": ["dashboard", "summary"],
        "actions": [
            {
                "action_id": "view_project_status",
                "label": "View project status",
            },
            {
                "action_id": "generate_codex_prompt",
                "label": "Generate Codex prompt",
            },
        ],
        "next_recommended_action": "Continue the next safe local stage.",
    }


def _write_safe_project_files(project_dir) -> None:
    project_dir.mkdir(exist_ok=True)
    (project_dir / "PROJECT_STATUS.md").write_text(
        "Current status: DEMO-002-CODEX-PROMPT\n",
        encoding="utf-8",
    )
    (project_dir / "README.md").write_text("# DemoAgent\n", encoding="utf-8")
    (project_dir / "agent_manifest.json").write_text("{}", encoding="utf-8")


def test_extract_checkpoint_from_status_text():
    checkpoint = extract_checkpoint_from_text(
        "# Project Status\n\nCurrent status: HUB-V2-006-CODEX-PROMPT-GENERATOR\n",
        fallback="fallback",
    )

    assert checkpoint == "HUB-V2-006-CODEX-PROMPT-GENERATOR"


def test_build_codex_prompt_supports_required_prompt_types(tmp_path):
    _write_safe_project_files(tmp_path)
    manifest = _manifest(str(tmp_path))
    rows = build_action_registry([manifest])
    action_rows = get_actions_for_agent(rows, agent_id="demo_agent")

    for prompt_type in PROMPT_TYPES:
        package = build_codex_prompt_package(
            manifest,
            action_rows=action_rows,
            prompt_type=prompt_type,
        )
        prompt = package["generated_prompt"]

        assert package["prompt_type"] == prompt_type
        assert package["current_checkpoint"] == "DEMO-002-CODEX-PROMPT"
        assert "project_path:" in prompt
        assert "current checkpoint:" in prompt
        assert "项目定位" in prompt
        assert "next recommended action" in prompt
        assert "请先读取" in prompt
        assert "安全要求" in prompt
        assert "验证要求" in prompt
        assert "完成后请按下面格式汇报" in prompt
        assert "不读取 .env" in prompt
        assert "不执行 git push" in prompt
        assert "不连接真实 Gmail" in prompt


def test_build_codex_prompt_warns_for_missing_safe_docs(tmp_path):
    tmp_path.mkdir(exist_ok=True)
    (tmp_path / "agent_manifest.json").write_text("{}", encoding="utf-8")
    manifest = _manifest(str(tmp_path))

    package = build_codex_prompt_package(manifest, action_rows=[], prompt_type="continue_next_stage")

    assert package["warnings"]
    assert any("PROJECT_STATUS.md" in warning for warning in package["warnings"])
    assert any("README.md" in warning for warning in package["warnings"])
    assert "Warning:" in package["generated_prompt"]


def test_reserved_prompt_types_are_text_only(tmp_path):
    _write_safe_project_files(tmp_path)
    manifest = _manifest(str(tmp_path))

    for prompt_type in RESERVED_PROMPT_TYPES:
        package = build_codex_prompt_package(manifest, action_rows=[], prompt_type=prompt_type)

        assert package["prompt_type"] == prompt_type
        assert package["prompt_type_status"] == "reserved"
        assert "预留模板" in package["generated_prompt"]
        assert "不要执行真实 action" in package["generated_prompt"]


def test_codex_prompt_actions_remain_template_only(tmp_path):
    manifest = _manifest(str(tmp_path))
    rows = build_action_registry([manifest])
    codex_actions = get_codex_prompt_actions(rows)

    assert len(codex_actions) == 1
    assert codex_actions[0]["action_type"] == "codex_prompt"
    assert codex_actions[0]["execution_mode"] == "template_only"
    assert codex_actions[0]["risk_level"] == "low"
