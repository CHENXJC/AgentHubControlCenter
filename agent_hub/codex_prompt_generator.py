from __future__ import annotations

from pathlib import Path
from typing import Any


PROMPT_TYPE_DETAILS = {
    "continue_next_stage": {
        "label": "Continue next stage",
        "status": "supported",
        "goal": "继续推进该 Agent 的下一阶段任务，保持小范围、可验证、可展示。",
        "task_focus": [
            "读取当前项目状态和 manifest 后再判断下一步。",
            "优先完成 next_recommended_action 指向的安全任务。",
            "同步更新 README、PROJECT_STATUS、相关 docs 和测试。",
        ],
    },
    "fix_or_polish": {
        "label": "Fix or polish",
        "status": "supported",
        "goal": "修复明确问题或做小范围产品化打磨，不扩大到新阶段大功能。",
        "task_focus": [
            "先复现或定位问题，再做最小必要修改。",
            "保持现有功能边界，不重构整个项目。",
            "补充或更新能覆盖本次修改的测试。",
        ],
    },
    "github_showcase_update": {
        "label": "GitHub showcase update",
        "status": "supported",
        "goal": "更新公开展示所需的 README、截图说明、manifest、状态文档和安全边界。",
        "task_focus": [
            "只准备 public-safe showcase 内容。",
            "检查 README、截图引用、docs、manifest 和公开安全说明是否一致。",
            "不执行 git push，不修改 remote，除非用户另行明确授权。",
        ],
    },
}

RESERVED_PROMPT_TYPE_DETAILS = {
    "add_manifest": {
        "label": "Add manifest",
        "status": "reserved",
        "goal": "为新 Agent 规划或补齐 agent_manifest.json。",
        "task_focus": ["预留模板；本阶段只生成文本提示词。"],
    },
    "refresh_screenshots": {
        "label": "Refresh screenshots",
        "status": "reserved",
        "goal": "刷新公开安全截图和截图指南。",
        "task_focus": ["预留模板；截图刷新仍需人工确认范围。"],
    },
    "run_tests_only": {
        "label": "Run tests only",
        "status": "reserved",
        "goal": "只做测试和验证，不改业务代码。",
        "task_focus": ["预留模板；由用户复制给 Codex 后再执行。"],
    },
    "create_connector_plan": {
        "label": "Create connector plan",
        "status": "reserved",
        "goal": "规划未来 connector 接入，不连接真实账号。",
        "task_focus": ["预留模板；真实 connector 不在本阶段启用。"],
    },
    "generate_report": {
        "label": "Generate report",
        "status": "reserved",
        "goal": "生成项目报告或阶段总结。",
        "task_focus": ["预留模板；报告生成由后续阶段扩展。"],
    },
}

PROMPT_TYPES = tuple(PROMPT_TYPE_DETAILS)
RESERVED_PROMPT_TYPES = tuple(RESERVED_PROMPT_TYPE_DETAILS)
ALL_PROMPT_TYPES = PROMPT_TYPES + RESERVED_PROMPT_TYPES

SAFE_CONTEXT_FILES = (
    "PROJECT_STATUS.md",
    "README.md",
    "agent_manifest.json",
    "docs/MANUAL_RUNBOOK.md",
    "docs/ACTION_SAFETY_POLICY.md",
)

SAFETY_REQUIREMENTS = [
    "不读取 .env。",
    "不输出 secret/token/password/API key。",
    "不修改 git remote。",
    "不执行 git push。",
    "不删除用户文件。",
    "不运行未授权外部脚本或子项目脚本。",
    "不连接真实 Gmail / Google Sheets / Notion / Airtable / Telegram 等 connector，除非用户明确要求。",
    "command_template 和 generated prompt 只能作为文本展示，不得自动执行。",
]

VALIDATION_REQUIREMENTS = [
    r".\.venv\Scripts\python.exe -m pytest（如项目没有 .venv，先按项目 README 判断可用 Python 环境）。",
    r".\.venv\Scripts\python.exe -m compileall .（如项目没有 .venv，先按项目 README 判断可用 Python 环境）。",
    "Streamlit 项目需要做本地 smoke check，确认页面 HTTP 200 且 UI 不报错。",
    "如涉及 manifest / Action Center，确认 Valid Manifests、Invalid Manifests、Missing Manifests 指标符合预期。",
    "确认没有 executable real action，所有 action 仍为 display/manual/template/planned metadata。",
]

COMPLETION_REPORT_SECTIONS = [
    "本次完成",
    "修改文件清单",
    "新增文件清单",
    "验证结果",
    "安全检查",
    "当前项目状态",
    "下一阶段建议",
]


def _safe_string(value: Any, default: str = "") -> str:
    return value.strip() if isinstance(value, str) and value.strip() else default


def _safe_list(values: Any, limit: int = 8) -> list[str]:
    if not isinstance(values, list):
        return []
    items = [value.strip() for value in values if isinstance(value, str) and value.strip()]
    return items[:limit]


def _read_safe_text(path: Path, max_chars: int = 60000) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")[:max_chars]
    except OSError:
        return ""


def extract_checkpoint_from_text(text: str, fallback: str = "") -> str:
    """Extract a likely checkpoint line from safe project docs."""
    for line in text.splitlines()[:120]:
        compact = line.strip().strip("#").strip()
        if not compact:
            continue
        lower = compact.lower()
        if any(
            marker in lower
            for marker in (
                "current status",
                "current checkpoint",
                "checkpoint name",
                "current stage",
            )
        ):
            if ":" in compact:
                value = compact.split(":", 1)[1].strip()
                if value:
                    return value.strip("` *")
            return compact.strip("` *")
    return fallback


def load_safe_prompt_context(project_path: str, fallback_checkpoint: str = "") -> dict[str, Any]:
    """Inspect only safe, named context files for prompt generation."""
    project_dir = Path(project_path) if project_path else Path()
    warnings: list[str] = []
    file_status: list[dict[str, Any]] = []
    checkpoint = fallback_checkpoint

    if not project_path:
        warnings.append("WARNING: project_path is empty; prompt uses manifest metadata only.")
        return {
            "project_path": "",
            "project_exists": False,
            "files": file_status,
            "warnings": warnings,
            "current_checkpoint": checkpoint or "Unknown checkpoint",
        }

    if not project_dir.exists():
        warnings.append(f"WARNING: project_path does not exist: {project_path}")
        return {
            "project_path": project_path,
            "project_exists": False,
            "files": file_status,
            "warnings": warnings,
            "current_checkpoint": checkpoint or "Unknown checkpoint",
        }

    for relative_name in SAFE_CONTEXT_FILES:
        path = project_dir / relative_name
        exists = path.is_file()
        file_status.append({"path": relative_name, "exists": exists})
        if not exists and relative_name in {"PROJECT_STATUS.md", "README.md", "agent_manifest.json"}:
            warnings.append(f"WARNING: {relative_name} is missing in {project_path}.")

        if exists and relative_name == "PROJECT_STATUS.md":
            status_text = _read_safe_text(path)
            checkpoint = extract_checkpoint_from_text(status_text, fallback=checkpoint)

    return {
        "project_path": project_path,
        "project_exists": True,
        "files": file_status,
        "warnings": warnings,
        "current_checkpoint": checkpoint or "Unknown checkpoint",
    }


def _prompt_type_detail(prompt_type: str) -> dict[str, Any]:
    if prompt_type in PROMPT_TYPE_DETAILS:
        return PROMPT_TYPE_DETAILS[prompt_type]
    if prompt_type in RESERVED_PROMPT_TYPE_DETAILS:
        return RESERVED_PROMPT_TYPE_DETAILS[prompt_type]
    return PROMPT_TYPE_DETAILS["continue_next_stage"]


def _format_bullets(values: list[str], fallback: str = "未声明") -> str:
    if not values:
        return f"- {fallback}"
    return "\n".join(f"- {value}" for value in values)


def _format_actions(action_rows: list[dict], limit: int = 8) -> str:
    if not action_rows:
        return "- 未声明可用 action。"
    rows = []
    for action in action_rows[:limit]:
        rows.append(
            "- "
            f"{_safe_string(action.get('action_id'), 'unknown_action')}: "
            f"{_safe_string(action.get('label'), 'Action')} "
            f"[{_safe_string(action.get('action_type'), 'unknown')} / "
            f"{_safe_string(action.get('execution_mode'), 'unknown')} / "
            f"risk={_safe_string(action.get('risk_level'), 'unknown')}]"
        )
    return "\n".join(rows)


def _format_files_to_read(context: dict[str, Any]) -> str:
    base_files = ["PROJECT_STATUS.md", "README.md", "agent_manifest.json"]
    optional_files = [
        "docs/MANUAL_RUNBOOK.md",
        "docs/ACTION_SAFETY_POLICY.md",
        "docs/AGENT_INTERFACE_STANDARD.md",
    ]
    lines = [f"{index}. {name}" for index, name in enumerate(base_files + optional_files, start=1)]
    missing = [
        file_info["path"]
        for file_info in context.get("files", [])
        if file_info.get("exists") is False and file_info.get("path") in set(base_files)
    ]
    if missing:
        lines.append("")
        lines.append("Warning: 如果上述文件缺失，只记录 warning，不要崩溃。当前缺失：" + ", ".join(missing))
    return "\n".join(lines)


def build_codex_prompt_package(
    manifest: dict[str, Any],
    action_rows: list[dict] | None = None,
    prompt_type: str = "continue_next_stage",
) -> dict[str, Any]:
    """Build a copy-ready Codex prompt package without executing anything."""
    action_rows = action_rows or []
    details = _prompt_type_detail(prompt_type)
    project_path = _safe_string(manifest.get("project_path"))
    fallback_checkpoint = (
        _safe_string(manifest.get("stage"))
        or _safe_string(manifest.get("version"))
        or _safe_string(manifest.get("status"))
    )
    context = load_safe_prompt_context(project_path, fallback_checkpoint=fallback_checkpoint)
    current_checkpoint = context["current_checkpoint"]
    prompt = build_codex_prompt(
        manifest=manifest,
        action_rows=action_rows,
        prompt_type=prompt_type,
        context=context,
    )
    return {
        "prompt_type": prompt_type if prompt_type in ALL_PROMPT_TYPES else "continue_next_stage",
        "prompt_type_label": details["label"],
        "prompt_type_status": details["status"],
        "project_path": project_path,
        "current_checkpoint": current_checkpoint,
        "warnings": context["warnings"],
        "files": context["files"],
        "safety_checklist": SAFETY_REQUIREMENTS,
        "validation_requirements": VALIDATION_REQUIREMENTS,
        "available_actions": action_rows,
        "generated_prompt": prompt,
    }


def build_codex_prompt(
    *,
    manifest: dict[str, Any],
    action_rows: list[dict],
    prompt_type: str,
    context: dict[str, Any],
) -> str:
    """Build the final Chinese-first prompt text for manual copy into Codex."""
    details = _prompt_type_detail(prompt_type)
    agent_name = _safe_string(manifest.get("agent_name"), "Unknown Agent")
    agent_id = _safe_string(manifest.get("agent_id"), "unknown_agent")
    project_path = _safe_string(manifest.get("project_path"), context.get("project_path", ""))
    category = _safe_string(manifest.get("category_label")) or _safe_string(manifest.get("category"), "Uncategorized")
    status = _safe_string(manifest.get("status"), "Unknown")
    positioning = _safe_string(manifest.get("description"), "未声明项目定位。")
    next_action = _safe_string(manifest.get("next_recommended_action"), "Review next action")
    current_checkpoint = _safe_string(context.get("current_checkpoint"), "Unknown checkpoint")
    prompt_status_note = ""
    if details["status"] == "reserved":
        prompt_status_note = "\n\n注意：该 prompt type 当前是预留模板，只生成规划/说明文本，不代表已启用真实执行能力。"

    warnings = context.get("warnings", [])
    warning_text = _format_bullets(warnings, fallback="当前未发现 PROJECT_STATUS / README / manifest 缺失 warning。")

    return f"""继续在 {project_path} 开发/处理 Agent 项目：

Agent: {agent_name}
agent_id: {agent_id}
project_path: {project_path}
category: {category}
status: {status}
current checkpoint: {current_checkpoint}
prompt type: {prompt_type} ({details["label"]}, {details["status"]}){prompt_status_note}

项目定位：
{positioning}

当前能力：
Inputs:
{_format_bullets(_safe_list(manifest.get("inputs")))}

Outputs:
{_format_bullets(_safe_list(manifest.get("outputs")))}

Available safe actions:
{_format_actions(action_rows)}

next recommended action:
{next_action}

请先读取：
{_format_files_to_read(context)}

上下文 warning：
{warning_text}

任务目标：
{details["goal"]}
{_format_bullets(details["task_focus"])}

安全要求：
{_format_bullets(SAFETY_REQUIREMENTS)}

验证要求：
{_format_bullets(VALIDATION_REQUIREMENTS)}

完成后请按下面格式汇报：
{_format_bullets(COMPLETION_REPORT_SECTIONS)}

特别说明：
- 本 prompt 只用于复制给 Codex 作为任务说明。
- 不要自动发送 prompt，不要执行真实 action，不要触发外部 connector。
- 如果需要执行任何高风险动作，必须先停止并等待用户明确确认。
"""
