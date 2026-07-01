from __future__ import annotations

from pathlib import Path
from typing import Any, MutableMapping

from agent_hub.stage_status import get_stage_snapshot


DEFAULT_LANGUAGE = "zh"
SUPPORTED_LANGUAGES = ("zh", "en")
SESSION_LANGUAGE_KEY = "ui_language"

LANGUAGE_LABELS = {
    "zh": "中文",
    "en": "English",
}

LANGUAGE_LABEL_TO_CODE = {
    "zh": "zh",
    "zh-cn": "zh",
    "中文": "zh",
    "chinese": "zh",
    "en": "en",
    "english": "en",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "page_title": {
        "zh": "个人 AI 总控台",
        "en": "Personal AI Command Center",
    },
    "sidebar_title": {
        "zh": "AI Command Center",
        "en": "AI Command Center",
    },
    "language_toggle_label": {
        "zh": "界面语言",
        "en": "Interface language",
    },
    "language_caption": {
        "zh": "本地双语 UI；不调用翻译 API。",
        "en": "Local bilingual UI; no translation API is called.",
    },
    "project_stage": {
        "zh": "项目阶段",
        "en": "Project Stage",
    },
    "product_status": {
        "zh": "产品状态",
        "en": "Product Status",
    },
    "latest_checkpoint": {
        "zh": "最新检查点",
        "en": "Latest Checkpoint",
    },
    "manifest_version": {
        "zh": "Manifest 版本",
        "en": "Manifest Version",
    },
    "stage_source": {
        "zh": "阶段来源",
        "en": "Stage Source",
    },
    "manifest_stage": {
        "zh": "Manifest 阶段",
        "en": "Manifest Stage",
    },
    "mode": {
        "zh": "模式",
        "en": "Mode",
    },
    "local_demo_safe_mode": {
        "zh": "本地演示 / 安全模式",
        "en": "Local Demo / Safe Mode",
    },
    "api": {
        "zh": "API",
        "en": "API",
    },
    "api_not_required": {
        "zh": "不需要",
        "en": "Not required",
    },
    "data_source": {
        "zh": "数据来源",
        "en": "Data Source",
    },
    "csv_local_manifests": {
        "zh": "CSV + 本地 manifests",
        "en": "CSV + local manifests",
    },
    "scan_root": {
        "zh": "扫描目录",
        "en": "Scan Root",
    },
    "external_actions": {
        "zh": "外部动作",
        "en": "External actions",
    },
    "external_actions_disabled": {
        "zh": "已禁用",
        "en": "Disabled",
    },
    "launcher_port": {
        "zh": "启动端口",
        "en": "Launcher Port",
    },
    "filters": {
        "zh": "筛选器",
        "en": "Filters",
    },
    "all": {
        "zh": "All",
        "en": "All",
    },
    "category": {
        "zh": "分类",
        "en": "Category",
    },
    "status": {
        "zh": "状态",
        "en": "Status",
    },
    "pin_status": {
        "zh": "置顶状态",
        "en": "Pin Status",
    },
    "health_status": {
        "zh": "健康状态",
        "en": "Health Status",
    },
    "action_priority": {
        "zh": "操作优先级",
        "en": "Action Priority",
    },
    "hero_title": {
        "zh": "Personal AI Command Center",
        "en": "Personal AI Command Center",
    },
    "hero_subtitle": {
        "zh": "AgentHubControlCenter V2 - 本地优先 AI Agent Operating System",
        "en": "AgentHubControlCenter V2 - AI Agent Operating System for a local-first portfolio",
    },
    "hero_copy": {
        "zh": "查看每个 AI Agent / Skill 能做什么、有哪些安全本地动作、哪些信号需要关注，以及未来工具如何接入统一接口标准。",
        "en": "See every AI Agent and Skill you can use, what each one does, which local actions are available, which signals need attention, and how future tools can plug into the same interface standard.",
    },
    "badge_local_first": {
        "zh": "Local-first",
        "en": "Local-first",
    },
    "badge_agent_os": {
        "zh": "Agent OS",
        "en": "Agent OS",
    },
    "badge_safe_demo": {
        "zh": "安全演示模式",
        "en": "Safe demo mode",
    },
    "badge_manifest_onboarding": {
        "zh": "Manifest 接入",
        "en": "Manifest onboarding",
    },
    "available_tools": {
        "zh": "可用工具",
        "en": "Available Tools",
    },
    "completed_tools": {
        "zh": "已完成工具",
        "en": "Completed Tools",
    },
    "public_showcase": {
        "zh": "公开展示项目",
        "en": "Public Showcase",
    },
    "pinned": {
        "zh": "已置顶",
        "en": "Pinned",
    },
    "public_not_pinned": {
        "zh": "公开未置顶",
        "en": "Public Not Pinned",
    },
    "paused_complete": {
        "zh": "暂停 / 完成",
        "en": "Paused / Complete",
    },
    "tab_command_overview": {
        "zh": "总控概览",
        "en": "Command Overview",
    },
    "tab_tools": {
        "zh": "我的工具 / 智能体注册表",
        "en": "My Tools / Agent Registry",
    },
    "tab_workflows": {
        "zh": "工作流中心",
        "en": "My Workflows",
    },
    "tab_useful_signals": {
        "zh": "有用信号",
        "en": "Useful Signals",
    },
    "tab_action_center": {
        "zh": "操作中心",
        "en": "Action Center",
    },
    "tab_connectors": {
        "zh": "连接器",
        "en": "Connectors",
    },
    "tab_future_plugin": {
        "zh": "未来插件接口",
        "en": "Future Plugin Interface",
    },
    "command_overview_title": {
        "zh": "总控概览",
        "en": "Command Overview",
    },
    "command_overview_intro": {
        "zh": "V2 总控入口：集中查看工具、工作流、有用信号、操作中心、连接器和未来插件规则。",
        "en": "A V2 entry page for the personal AI Agent and Skill operating system: tools, workflows, useful signals, actions, connectors, and future plugin rules.",
    },
    "what_you_can_use_now": {
        "zh": "当前可用工具",
        "en": "What You Can Use Now",
    },
    "command_center_summary": {
        "zh": "总控台摘要",
        "en": "Command Center Summary",
    },
    "portfolio_overview": {
        "zh": "作品集概览",
        "en": "Portfolio Overview",
    },
    "health_snapshot": {
        "zh": "健康状态快照",
        "en": "Health Snapshot",
    },
    "strategic_summary": {
        "zh": "战略摘要",
        "en": "Strategic Summary",
    },
    "showcase_status": {
        "zh": "公开展示状态",
        "en": "Showcase Status",
    },
    "priority_actions": {
        "zh": "优先操作",
        "en": "Priority Actions",
    },
    "next_best_move": {
        "zh": "下一步建议",
        "en": "Next Best Move",
    },
    "portfolio_positioning": {
        "zh": "作品集定位",
        "en": "Portfolio Positioning",
    },
    "showcase_strengths": {
        "zh": "展示优势",
        "en": "Showcase Strengths",
    },
    "portfolio_gaps": {
        "zh": "作品集缺口",
        "en": "Portfolio Gaps",
    },
    "capability_overview": {
        "zh": "能力概览",
        "en": "Capability Overview",
    },
    "next_action_snapshot": {
        "zh": "下一步快照",
        "en": "Next Action Snapshot",
    },
    "tools_title": {
        "zh": "我的工具 / 智能体注册表",
        "en": "My Tools / Agent Registry",
    },
    "tools_intro": {
        "zh": "按筛选条件查看当前 Agents / Skills、每个工具能做什么，以及可手动使用的安全本地命令。",
        "en": "A filtered view of current Agents and Skills, what each tool does, and which safe local commands are available.",
    },
    "metadata_only_caption": {
        "zh": "每张卡片都是 metadata-only。动作遵守 HUB-V2-005 local action schema，外部连接器仍保持 planned / optional，直到未来明确 opt-in 阶段。",
        "en": "Each card is metadata-only. Actions use the HUB-V2-005 local action schema, and external connectors remain planned or optional until a future opt-in stage.",
    },
    "tool_cards": {
        "zh": "工具卡片",
        "en": "Tool Cards",
    },
    "registry_table": {
        "zh": "注册表",
        "en": "Registry Table",
    },
    "agent_detail_panel": {
        "zh": "Agent 详情面板",
        "en": "Agent Detail Panel",
    },
    "select_agent": {
        "zh": "选择 Agent",
        "en": "Select agent",
    },
    "capability": {
        "zh": "能力",
        "en": "Capability",
    },
    "portfolio_value": {
        "zh": "作品集价值",
        "en": "Portfolio Value",
    },
    "notes": {
        "zh": "备注",
        "en": "Notes",
    },
    "tech_stack": {
        "zh": "技术栈",
        "en": "Tech Stack",
    },
    "local_path": {
        "zh": "本地路径",
        "en": "Local Path",
    },
    "github_url": {
        "zh": "GitHub URL",
        "en": "GitHub URL",
    },
    "command_pack_panel": {
        "zh": "命令包面板",
        "en": "Command Pack Panel",
    },
    "registry_validation_table": {
        "zh": "注册表校验表",
        "en": "Registry Validation Table",
    },
    "useful_signals_title": {
        "zh": "有用信号",
        "en": "Useful Signals",
    },
    "useful_signals_intro": {
        "zh": "本地决策面板：把 Agent metadata、项目状态、demo data 和 action references 转成排序后的有用信号。推荐动作只作为文本展示。",
        "en": "A local decision panel that turns Agent metadata, project status, demo data, and action references into ranked useful signals. Recommended actions are text-only.",
    },
    "signal_metrics": {
        "zh": "信号指标",
        "en": "Signal Metrics",
    },
    "signal_filters": {
        "zh": "信号筛选器",
        "en": "Signal Filters",
    },
    "top_useful_signals": {
        "zh": "Top 5 有用信号",
        "en": "Top 5 Useful Signals",
    },
    "needs_action": {
        "zh": "需要行动",
        "en": "Needs Action",
    },
    "watchlist": {
        "zh": "观察列表",
        "en": "Watchlist",
    },
    "low_priority_ignored": {
        "zh": "低优先级 / 已忽略",
        "en": "Low Priority / Ignored",
    },
    "signal_table": {
        "zh": "信号表",
        "en": "Signal Table",
    },
    "health_overview": {
        "zh": "健康状态概览",
        "en": "Health Overview",
    },
    "health_table": {
        "zh": "健康状态表",
        "en": "Health Table",
    },
    "health_detail": {
        "zh": "健康状态详情",
        "en": "Health Detail",
    },
    "workflows_title": {
        "zh": "工作流中心",
        "en": "My Workflows",
    },
    "workflows_intro": {
        "zh": "用于查看作品集复盘、有用信号复盘、连接器 readiness、Codex handoff 和未来 Agent integration 的工作流层。",
        "en": "Workflow-level view for portfolio review, useful signal review, connector readiness review, Codex handoff, and future Agent integration.",
    },
    "local_workflow_simulation": {
        "zh": "本地工作流模拟",
        "en": "Local Workflow Simulation",
    },
    "local_simulation_caption": {
        "zh": "仅本地模拟。不连接真实外部账号。不执行真实操作。不加载凭证。",
        "en": "Local simulation only. No live connector. No real action execution. No credentials loaded.",
    },
    "approval_gates": {
        "zh": "审批闸门",
        "en": "Approval Gates",
    },
    "workflow_generated_signals": {
        "zh": "工作流生成的有用信号",
        "en": "Workflow-Generated Useful Signals",
    },
    "workflow_catalog": {
        "zh": "工作流目录",
        "en": "Workflow Catalog",
    },
    "project_matrix_view": {
        "zh": "项目矩阵视图",
        "en": "Project Matrix View",
    },
    "capability_cluster_cards": {
        "zh": "能力集群卡片",
        "en": "Capability Cluster Cards",
    },
    "strongest_categories": {
        "zh": "最强分类",
        "en": "Strongest Categories",
    },
    "category_matrix": {
        "zh": "分类矩阵",
        "en": "Category Matrix",
    },
    "action_center_title": {
        "zh": "操作中心",
        "en": "Action Center",
    },
    "action_center_intro": {
        "zh": "用于规划和追踪注册表、健康状态、截图、置顶决策和 schema-backed 本地动作。不执行自动化。",
        "en": "Planning and tracking view for registry, health, screenshots, pin decisions, and schema-backed local actions. No automation is executed.",
    },
    "priority_summary": {
        "zh": "优先级摘要",
        "en": "Priority Summary",
    },
    "current_next_project": {
        "zh": "当前下一项目",
        "en": "Current Next Project",
    },
    "paused_projects": {
        "zh": "暂停项目",
        "en": "Paused Projects",
    },
    "github_showcase_projects": {
        "zh": "GitHub 公开展示项目",
        "en": "GitHub Showcase Projects",
    },
    "portfolio_follow_up": {
        "zh": "作品集后续",
        "en": "Portfolio Follow-up",
    },
    "future_commercial_candidates": {
        "zh": "未来商业化候选",
        "en": "Future Commercial Candidates",
    },
    "future_agenthub_integration": {
        "zh": "未来 AgentHub 接入",
        "en": "Future AgentHub Integration",
    },
    "local_action_schema_metrics": {
        "zh": "Local Action Schema 指标",
        "en": "Local Action Schema Metrics",
    },
    "total_actions": {
        "zh": "总 actions",
        "en": "Total actions",
    },
    "manual_only_actions": {
        "zh": "仅手动 actions",
        "en": "Manual-only actions",
    },
    "display_only_actions": {
        "zh": "仅展示 actions",
        "en": "Display-only actions",
    },
    "future_connector_actions": {
        "zh": "未来连接器 actions",
        "en": "Future connector actions",
    },
    "requires_approval": {
        "zh": "需要审批",
        "en": "Requires approval",
    },
    "blocked_actions": {
        "zh": "已阻断 actions",
        "en": "Blocked actions",
    },
    "local_action_schema_table": {
        "zh": "Local Action Schema 表",
        "en": "Local Action Schema Table",
    },
    "local_action_cards": {
        "zh": "Local Action 卡片",
        "en": "Local Action Cards",
    },
    "available_actions": {
        "zh": "可用 Actions",
        "en": "Available Actions",
    },
    "action_plan_table": {
        "zh": "Action Plan 表",
        "en": "Action Plan Table",
    },
    "action_cards": {
        "zh": "Action 卡片",
        "en": "Action Cards",
    },
    "codex_prompt_generator": {
        "zh": "Codex Prompt Generator",
        "en": "Codex Prompt Generator",
    },
    "codex_prompt_caption": {
        "zh": "template-only / no execution。生成的 prompt 只是可复制文本，不会自动发送给 Codex。",
        "en": "template-only / no execution. Generated prompts are copy-ready text only and are not sent to Codex automatically.",
    },
    "agent_selector": {
        "zh": "Agent 选择器",
        "en": "Agent selector",
    },
    "prompt_type_selector": {
        "zh": "Prompt 类型选择器",
        "en": "Prompt type selector",
    },
    "selected_agent": {
        "zh": "已选择 Agent",
        "en": "Selected Agent",
    },
    "next_recommended_action": {
        "zh": "下一步推荐动作",
        "en": "Next Recommended Action",
    },
    "safety_checklist": {
        "zh": "安全检查清单",
        "en": "Safety Checklist",
    },
    "validation_checklist": {
        "zh": "验证清单",
        "en": "Validation Checklist",
    },
    "generated_prompt_preview": {
        "zh": "生成 Prompt 预览",
        "en": "Generated Prompt Preview",
    },
    "copy_ready_generated_prompt": {
        "zh": "可复制 generated prompt",
        "en": "Copy-ready generated prompt",
    },
    "copy_prompt_help": {
        "zh": "手动复制此文本到 Codex。AgentHub 不执行、不发送。",
        "en": "Copy this text manually into Codex. AgentHub does not execute or send it.",
    },
    "download_prompt_text": {
        "zh": "下载 prompt 文本",
        "en": "Download prompt text",
    },
    "download_prompt_help": {
        "zh": "将生成的 prompt 下载为文本。此操作不会执行任何内容。",
        "en": "Download the generated prompt as text only. This does not execute anything.",
    },
    "connectors_title": {
        "zh": "连接器",
        "en": "Connectors",
    },
    "connectors_intro": {
        "zh": "Connector Readiness Simulator：用 design-only metadata 评估未来连接器 readiness。",
        "en": "Connector Readiness Simulator. HUB-V2-008 evaluates future connector readiness with design-only metadata.",
    },
    "connectors_caption": {
        "zh": "未连接真实外部账号。Design-only readiness simulation。不加载凭证。",
        "en": "No live connector is connected. Design-only readiness simulation. No credentials loaded.",
    },
    "connector_readiness_simulator": {
        "zh": "连接器 readiness 模拟器",
        "en": "Connector Readiness Simulator",
    },
    "readiness_filters": {
        "zh": "Readiness 筛选器",
        "en": "Readiness Filters",
    },
    "connector_cards": {
        "zh": "连接器卡片",
        "en": "Connector Cards",
    },
    "readiness_table": {
        "zh": "Readiness 表",
        "en": "Readiness Table",
    },
    "connector_generated_signals": {
        "zh": "连接器生成的有用信号",
        "en": "Connector-Generated Useful Signals",
    },
    "existing_connector_overview": {
        "zh": "现有连接器概览",
        "en": "Existing Connector Overview",
    },
    "connector_policy": {
        "zh": "连接器策略",
        "en": "Connector Policy",
    },
    "current_boundary": {
        "zh": "当前边界",
        "en": "Current Boundary",
    },
    "planned_connectors": {
        "zh": "计划中的连接器",
        "en": "Planned Connectors",
    },
    "future_plugin_title": {
        "zh": "未来插件接口",
        "en": "Future Plugin Interface",
    },
    "future_plugin_intro": {
        "zh": "面向未来 Agents / Skills 的接口标准、manifest import、Agent onboarding 和 report export surface。",
        "en": "Interface standard, manifest import, Agent onboarding, and report export surface for future Agents and Skills.",
    },
    "agent_onboarding": {
        "zh": "Agent 接入",
        "en": "Agent Onboarding",
    },
    "agent_onboarding_caption": {
        "zh": "只扫描 F:\\AIProjects 下一级子目录的 agent_manifest.json，不执行子项目脚本。",
        "en": "Scans immediate child folders under F:\\AIProjects for agent_manifest.json only. No child project scripts are executed.",
    },
    "discovery_results": {
        "zh": "发现结果",
        "en": "Discovery Results",
    },
    "imported_agents": {
        "zh": "已导入 Agents",
        "en": "Imported Agents",
    },
    "duplicate_agent_ids": {
        "zh": "重复 Agent IDs",
        "en": "Duplicate Agent IDs",
    },
    "missing_manifests": {
        "zh": "缺失 Manifests",
        "en": "Missing Manifests",
    },
    "invalid_manifests": {
        "zh": "无效 Manifests",
        "en": "Invalid Manifests",
    },
    "agent_contract": {
        "zh": "Agent Contract",
        "en": "Agent Contract",
    },
    "plugin_interface_roadmap": {
        "zh": "插件接口路线图",
        "en": "Plugin Interface Roadmap",
    },
    "export_report": {
        "zh": "报告导出",
        "en": "Export Report",
    },
    "export_report_intro": {
        "zh": "生成并预览增强版本地 Markdown 报告。",
        "en": "Generate and preview the enhanced local Markdown report.",
    },
    "command_center_export_summary": {
        "zh": "总控台导出摘要",
        "en": "Command Center Export Summary",
    },
    "showcase_asset_checklist": {
        "zh": "公开展示资产清单",
        "en": "Showcase Asset Checklist",
    },
    "markdown_report_preview": {
        "zh": "Markdown 报告预览",
        "en": "Markdown Report Preview",
    },
    "demo_workflow_report_export": {
        "zh": "Demo 工作流报告导出",
        "en": "Demo Workflow Report Export",
    },
    "report_export_caption": {
        "zh": "仅 public-safe demo export。不加载凭证，不连接真实 connector，不执行真实操作。生成文本只用于预览/下载。",
        "en": "Public-safe demo export only. No credentials. No live connector. No real execution. Generated text is preview/download content only.",
    },
    "report_sections": {
        "zh": "报告章节",
        "en": "Report sections",
    },
    "available_report_sections": {
        "zh": "可用报告章节",
        "en": "Available report sections",
    },
    "export_formats": {
        "zh": "导出格式",
        "en": "Export formats",
    },
    "public_safe_status": {
        "zh": "Public-safe 状态",
        "en": "Public-safe status",
    },
    "last_generated_report_path": {
        "zh": "最近生成报告路径",
        "en": "Last generated report path",
    },
    "report_export_note": {
        "zh": "Report Export 是 template-only / no execution。下载按钮只生成本地文本副本；保存模块只写入 outputs/public_reports/。",
        "en": "Report Export is template-only / no execution. Use download buttons for local text copies, or the exporter module to save only under outputs/public_reports/.",
    },
    "markdown_preview": {
        "zh": "Markdown 预览",
        "en": "Markdown preview",
    },
    "json_preview": {
        "zh": "JSON 预览",
        "en": "JSON preview",
    },
    "csv_summary_preview": {
        "zh": "CSV 摘要预览",
        "en": "CSV summary preview",
    },
    "copy_ready_markdown_report": {
        "zh": "可复制 Markdown 报告",
        "en": "Copy-ready Markdown report",
    },
    "download_markdown_report_text": {
        "zh": "下载 Markdown 报告文本",
        "en": "Download Markdown report text",
    },
    "download_json_report_text": {
        "zh": "下载 JSON 报告文本",
        "en": "Download JSON report text",
    },
    "download_csv_summary_text": {
        "zh": "下载 CSV 摘要文本",
        "en": "Download CSV summary text",
    },
    "report_safety_checklist": {
        "zh": "报告安全检查清单",
        "en": "Report Safety Checklist",
    },
    "download_markdown_report": {
        "zh": "下载 Markdown 报告",
        "en": "Download Markdown Report",
    },
    "save_report_local_outputs": {
        "zh": "保存报告到本地 outputs",
        "en": "Save Report to Local Outputs",
    },
    "saved_report_caption": {
        "zh": "保存的报告保留在本地 outputs/，除 outputs/.gitkeep 外会被 git 忽略。",
        "en": "Saved reports stay local in outputs/ and are ignored by git except outputs/.gitkeep.",
    },
    "disclaimer": {
        "zh": "此 dashboard 仅用于本地作品集管理和工作流规划。它不会执行外部动作，也不会访问私人凭证。",
        "en": "This dashboard is for local portfolio management and workflow planning only. It does not execute external actions or access private credentials.",
    },
    "no_live_connector": {
        "zh": "未连接真实外部账号",
        "en": "No live connector",
    },
    "no_real_action_execution": {
        "zh": "不执行真实操作",
        "en": "No real action execution",
    },
    "template_only_no_execution": {
        "zh": "仅模板 / 不执行",
        "en": "template-only / no execution",
    },
    "demo_mode": {
        "zh": "演示模式",
        "en": "Demo Mode",
    },
    "manual_review_mode": {
        "zh": "手动审阅模式",
        "en": "Manual Review Mode",
    },
    "safe_mode": {
        "zh": "安全模式",
        "en": "Safe Mode",
    },
    "review_required": {
        "zh": "需要审阅",
        "en": "Review Required",
    },
    "source_local_manifest": {
        "zh": "本地 Manifest",
        "en": "Local Manifest",
    },
    "source_demo_manifest": {
        "zh": "演示 Manifest",
        "en": "Demo Manifest",
    },
    "source_static_registry": {
        "zh": "静态注册表",
        "en": "Static Registry",
    },
    "field_status": {
        "zh": "状态",
        "en": "Status",
    },
    "field_can_do": {
        "zh": "可做",
        "en": "Can do",
    },
    "field_connectors": {
        "zh": "连接器",
        "en": "Connectors",
    },
    "field_next": {
        "zh": "下一步",
        "en": "Next",
    },
    "field_score": {
        "zh": "分数",
        "en": "Score",
    },
    "field_source": {
        "zh": "来源",
        "en": "Source",
    },
    "field_why_important": {
        "zh": "为什么重要",
        "en": "Why important",
    },
    "field_recommended_next_step": {
        "zh": "推荐下一步",
        "en": "Recommended next step",
    },
    "field_related_agent": {
        "zh": "相关 Agent",
        "en": "Related Agent",
    },
    "field_action_reference": {
        "zh": "Action 引用",
        "en": "Action reference",
    },
    "field_policy": {
        "zh": "策略",
        "en": "Policy",
    },
    "field_risk": {
        "zh": "风险",
        "en": "Risk",
    },
    "field_type": {
        "zh": "类型",
        "en": "Type",
    },
    "field_execution_mode": {
        "zh": "执行模式",
        "en": "Execution mode",
    },
    "field_risk_level": {
        "zh": "风险级别",
        "en": "Risk level",
    },
    "field_approval": {
        "zh": "审批",
        "en": "Approval",
    },
    "field_expected_output": {
        "zh": "预期输出",
        "en": "Expected output",
    },
    "field_runbook": {
        "zh": "Runbook",
        "en": "Runbook",
    },
    "field_safety": {
        "zh": "安全说明",
        "en": "Safety",
    },
    "approval_required": {
        "zh": "需要审批",
        "en": "Required",
    },
    "approval_not_required": {
        "zh": "无需审批",
        "en": "Not required",
    },
    "commands_manual_only": {
        "zh": "命令仅作为手动使用文本展示。",
        "en": "Commands are displayed for manual use only.",
    },
    "no_items_group": {
        "zh": "此分组暂无项目。",
        "en": "No items in this group.",
    },
    "no_agents_match": {
        "zh": "没有 Agent 符合当前注册表筛选器。",
        "en": "No agents match the selected registry filters.",
    },
    "no_validation_rows": {
        "zh": "没有校验行符合当前注册表筛选器。",
        "en": "No validation rows match the selected registry filters.",
    },
    "no_signals_match": {
        "zh": "没有信号符合当前筛选器。",
        "en": "No signals match the current filters.",
    },
    "no_workflows_match": {
        "zh": "没有工作流模拟符合当前视图。",
        "en": "No workflow simulations match this view.",
    },
    "no_connectors_match": {
        "zh": "没有连接器 readiness 记录符合当前视图。",
        "en": "No connector readiness records match this view.",
    },
}


AGENT_DISPLAY_NAMES = {
    "AgentHubControlCenter": "AgentHubControlCenter / AI 智能体总控台",
    "BusinessOpsAgent": "BusinessOpsAgent / 小企业运营诊断智能体",
    "CareerPilotAgent": "CareerPilotAgent / 职业申请导航智能体",
    "ClientDeliveryKitAgent": "ClientDeliveryKitAgent / 客户交付工具包智能体",
    "IdeaScoreAgent": "IdeaScoreAgent / 想法评分智能体",
    "MarketSenseAgent": "MarketSenseAgent / 市场感知智能体",
    "NewsSignalAgent": "NewsSignalAgent / 新闻信号分析智能体",
    "NextOpsAgent": "NextOpsAgent / 下一步运营建议智能体",
    "PersonalKnowledgeAgent": "PersonalKnowledgeAgent / 个人知识库智能体",
    "QuantLabAgent": "QuantLabAgent / 量化研究实验室智能体",
    "SocialPainFinderAgent": "SocialPainFinderAgent / 社媒痛点发现智能体",
    "VideoExtractSkill": "VideoExtractSkill / 视频图片内容提取技能",
    "WorkflowCommandCenterAgent": "WorkflowCommandCenterAgent / AI 工作流指令中台",
}

CATEGORY_TRANSLATIONS = {
    "AgentOps / PortfolioOps": "智能体运维 / 作品集运维",
    "agent_ops": "智能体运维",
    "Control Center / Meta Agent": "总控台 / 元智能体",
    "SME Operations": "中小企业运营",
    "sme_operations": "中小企业运营",
    "Business Operations": "商业运营",
    "Business Discovery": "商业机会发现",
    "Workflow Automation": "工作流自动化",
    "Career Operations": "职业申请运营",
    "Career Automation": "职业申请自动化",
    "career_operations": "职业申请运营",
    "Client Delivery": "客户交付",
    "client_delivery": "客户交付",
    "Client delivery / AI automation consulting": "客户交付 / AI 自动化咨询",
    "Client Delivery / AI Consulting": "客户交付 / AI 咨询",
    "Idea Validation": "想法验证",
    "idea_validation": "想法验证",
    "Market Intelligence": "市场情报",
    "market_intelligence": "市场情报",
    "Finance Automation": "金融市场自动化",
    "News Intelligence": "新闻信号",
    "news_intelligence": "新闻信号",
    "Knowledge Management": "知识管理",
    "Knowledge Base": "知识管理",
    "knowledge_management": "知识管理",
    "Quant Research": "量化研究",
    "quant_research": "量化研究",
    "Opportunity Discovery": "商业机会发现",
    "opportunity_discovery": "商业机会发现",
    "Content Intelligence": "内容智能",
    "content_intelligence": "内容智能",
    "Media Intelligence": "媒体内容智能",
    "Finance / Market": "金融 / 市场",
    "Media / OCR / Extraction": "媒体 / OCR / 提取",
    "Career": "职业",
    "News / Signal": "新闻 / 信号",
    "SME Automation": "中小企业自动化",
    "Finance & Quant Research": "金融与量化研究",
    "Workflow Orchestration / AgentOps": "工作流编排 / 智能体运维",
    "Workflow Orchestration / AgentOps / Project Command": "工作流编排 / 智能体运维 / 项目指令中台",
    "workflow-orchestration": "工作流编排",
    "workflow_orchestration": "工作流编排",
    "project-execution-command-center": "项目执行指令中台",
}

STATUS_TRANSLATIONS = {
    "All": "全部",
    "Complete": "已完成",
    "Active": "运行中",
    "Paused": "已暂停",
    "Maintain / Showcase Ready": "维护展示就绪",
    "Showcase Ready": "可公开展示",
    "Healthy": "健康",
    "Partial": "部分就绪",
    "Missing or Incomplete": "缺失或不完整",
    "Missing / Incomplete": "缺失 / 不完整",
    "Not checked": "未检查",
    "Published": "已发布",
    "Public": "公开",
    "Pinned": "已置顶",
    "Not Pinned": "未置顶",
    "Not pinned": "未置顶",
    "Pin pending": "待决定置顶",
    "recommend_pin": "建议置顶",
    "live_showcase_verified": "公开展示已验证",
    "GitHub Public Showcase": "GitHub 公开展示",
    "Local Public Showcase Candidate": "本地公开展示候选",
    "bilingual_ui_stage_sync_ready": "双语 UI 与阶段同步就绪",
    "deep_chinese_ui_coverage_ready": "深度中文 UI 覆盖就绪",
    "deep_chinese_ui_coverage_check": "深度中文 UI 覆盖检查",
    "profile_pin_maintain_showcase_decision_complete": "置顶 / 维护展示决策完成",
    "Complete-no-pin pause; future AgentHub integration candidate": "已完成但不置顶；未来可接入 AgentHub",
    "Profile pin optional, screenshots pending": "置顶可选，截图待刷新",
    "new": "新信号",
    "reviewed": "已查看",
    "needs_action": "需要处理",
    "watchlist": "观察列表",
    "ignored": "已忽略",
    "archived": "已归档",
    "ready_for_manual_review": "可手动审阅",
    "simulation_ready": "模拟已就绪",
    "blocked_until_approval": "审批前阻止",
    "needs_review": "需要审阅",
    "design_only": "仅设计",
    "ready_for_demo": "可用于演示",
    "future": "未来规划",
    "not_connected": "未连接",
    "available_local": "本地可用",
    "available_link": "链接可用",
    "manual_launch": "手动启动",
    "planned": "计划中",
    "optional_future": "未来可选",
    "optional_local": "本地可选",
    "not_configured": "未配置",
    "demo_disabled": "演示禁用",
    "display_only": "仅展示",
    "manual_ready": "可手动操作",
    "template_ready": "模板就绪",
    "blocked": "已阻止",
    "Pass": "通过",
    "Review": "需检查",
    "High": "高",
    "Medium": "中",
    "Low": "低",
    "None": "无",
}

BADGE_TRANSLATIONS = {
    "Local Manifest": "本地 Manifest",
    "Demo Manifest": "演示 Manifest",
    "Static Registry": "静态注册表",
    "Demo Mode": "演示模式",
    "Safe Mode": "安全模式",
    "Demo Mode / Safe Mode": "演示模式 / 安全模式",
    "Local-first": "本地优先",
    "Safe demo mode": "安全演示模式",
    "Manifest onboarding": "Manifest 接入",
    "Agent OS": "智能体操作系统",
}

ACTION_LABEL_TRANSLATIONS = {
    "View project status": "查看项目状态",
    "View Project Status": "查看项目状态",
    "View agent manifest": "查看智能体 Manifest",
    "View Agent Manifest": "查看智能体 Manifest",
    "Open project folder": "打开项目文件夹",
    "Open Project Folder": "打开项目文件夹",
    "Manual run dashboard": "手动运行仪表盘",
    "View Streamlit Dashboard": "查看 Streamlit 仪表盘",
    "Generate Codex prompt": "生成 Codex 提示词",
    "Generate Codex Prompt": "生成 Codex 提示词",
    "Export summary": "导出摘要",
    "Export AgentHub Summary": "导出 AgentHub 摘要",
    "View latest report": "查看最新报告",
    "Export demo workflow report": "导出演示工作流报告",
    "Generate Demo Delivery Report": "生成演示交付报告",
    "Export Public-Safe Report": "导出公开安全报告",
    "View Opportunity Scorecard": "查看机会评分卡",
    "Score Automation Opportunities": "评分自动化机会",
    "Open GitHub showcase": "打开 GitHub 展示页",
    "Launch local app": "启动本地应用",
}

CONNECTOR_TRANSLATIONS = {
    "Local Filesystem": "本地文件系统",
    "Local File": "本地文件",
    "Local project files": "本地项目文件",
    "GitHub Showcase Link": "GitHub 展示链接",
    "GitHub showcase": "GitHub 公开展示",
    "Streamlit local dashboard": "Streamlit 本地仪表盘",
    "Local JSON / CSV": "本地 JSON / CSV",
    "CSV / JSON Demo Data": "CSV / JSON 演示数据",
    "AgentHubControlCenter": "AgentHubControlCenter 元数据入口",
    "Google Docs Planned": "Google Docs 规划连接器",
    "Google Sheets Planned": "Google Sheets 规划连接器",
    "Notion Planned": "Notion 规划连接器",
    "Airtable Planned": "Airtable 规划连接器",
    "Gmail Planned": "Gmail 规划连接器",
    "PDF Export Planned": "PDF 导出规划",
    "Local vector store": "本地向量库",
    "Local OCR engine": "本地 OCR 引擎",
    "Local ASR engine": "本地语音识别引擎",
    "Market data provider": "市场数据提供方",
    "RSS or News API": "RSS 或新闻 API",
    "Social platform API": "社交平台 API",
    "Google Sheets": "Google Sheets",
    "Google Drive": "Google Drive",
    "Gmail": "Gmail",
    "Notion": "Notion",
    "Airtable": "Airtable",
    "Telegram": "Telegram",
    "GitHub": "GitHub",
    "n8n": "n8n",
    "Make": "Make",
    "Zapier": "Zapier",
}

NEXT_STEP_TRANSLATIONS = {
    "No immediate action": "暂无立即行动",
    "No urgent child-project action.": "暂无紧急子项目行动。",
    "Maintain showcase": "保持展示维护状态",
    "Maintain showcase; only refresh docs/screenshots or update UI labels when needed.": "保持展示维护状态；仅在需要时刷新文档、截图或 UI 标签。",
    "Review GitHub profile pin decision": "检查 GitHub Profile 置顶决策",
    "Review GitHub public showcase readiness before publishing or pinning.": "发布或置顶前检查 GitHub 公开展示准备度。",
    "Keep as a public showcase project; use AgentHub for metadata review only.": "保持公开展示项目状态；AgentHub 仅用于元数据审阅。",
    "Keep paused after public showcase and profile pin; review only from AgentHub.": "公开展示和置顶后保持暂停；仅从 AgentHub 审阅。",
    "Keep public showcase version paused; do not enable automated notifications from AgentHub yet.": "保持公开展示版本暂停；暂不从 AgentHub 启用自动通知。",
    "Review optional profile pin decision; keep AgentHub access metadata-only.": "检查可选 Profile 置顶决策；AgentHub 访问保持仅元数据。",
    "Refresh public-safe screenshots later; keep feature expansion paused.": "后续刷新公开安全截图；继续暂停功能扩展。",
    "Keep complete-no-pin status; use AgentHub for discovery and metadata review.": "保持完成但不置顶状态；使用 AgentHub 做发现和元数据审阅。",
    "Keep as educational research showcase; do not enable trading or automated execution.": "保持教育研究展示定位；不启用交易或自动执行。",
    "Keep paused after public showcase and profile pin; use AgentHub for portfolio-level review.": "公开展示和置顶后保持暂停；AgentHub 仅用于作品集层级审阅。",
    "Optional profile pin decision or maintain-showcase": "可选 Profile 置顶决策或保持展示维护状态",
    "CLIENTDELIVERYKIT-012-MAINTAIN-SHOWCASE-PERIODIC-REFRESH-ONLY-IF-NEEDED": "CLIENTDELIVERYKIT-012：仅在需要时做展示维护刷新",
    "Review next action after current showcase pass.": "当前展示检查后再审阅下一步。",
    "Paused after public showcase/profile pin; no immediate expansion needed.": "公开展示 / 置顶后已暂停；暂无扩展需求。",
    "No registered project yet.": "暂无已注册项目。",
}

DESCRIPTION_TRANSLATIONS = {
    "Personal AI Command Center for viewing, planning, and connecting local-first AI Agents and Skills.": "用于查看、规划和连接本地优先 AI Agent / Skill 的个人智能体总控台。",
    "Business operations analysis Agent for KPI-style dashboards, operational summaries, and improvement planning.": "面向小企业运营诊断的智能体，用于 KPI 仪表盘、运营摘要和改进计划。",
    "Career workflow assistant for structured career planning, job matching notes, and application task support.": "职业申请工作流助手，用于结构化职业规划、岗位匹配笔记和申请任务支持。",
    "Client-facing AI automation delivery kit for converting demo intake, workflow pain points, and automation opportunities into structured consulting deliverables.": "面向客户的 AI 自动化交付工具包，将演示需求、流程痛点和自动化机会转成结构化咨询交付物。",
    "Local AI skill and business opportunity scoring dashboard that evaluates project ideas with transparent rule-based dimensions.": "本地 AI 技能与商业机会评分仪表盘，用透明规则维度评估项目想法。",
    "Market intelligence Agent for multi-market watchlists, risk flags, dashboards, and scheduled-style market briefs.": "市场情报智能体，用于多市场观察列表、风险标记、仪表盘和定时风格市场简报。",
    "News signal analysis Agent for extracting structured insights, narrative shifts, and risk flags from public-safe news content.": "新闻信号分析智能体，从公开安全新闻内容中提取结构化洞察、叙事变化和风险标记。",
    "SME workflow diagnosis Agent for bottleneck detection, automation scoring, ROI estimates, and consulting-style reports.": "中小企业工作流诊断智能体，用于瓶颈检测、自动化评分、ROI 估算和咨询式报告。",
    "Local-first personal knowledge workflow for demo notes, structured retrieval planning, summaries, and source-aware knowledge views.": "本地优先个人知识工作流，用于演示笔记、结构化检索规划、摘要和来源感知知识视图。",
    "Quant research dashboard for educational backtesting, risk metrics, technical indicators, and candlestick visualization.": "量化研究仪表盘，用于教育型回测、风险指标、技术指标和 K 线可视化。",
    "Business opportunity discovery Agent for identifying social pain points, scoring opportunities, and exporting insight reports.": "商业机会发现智能体，用于识别社媒痛点、评分机会并导出洞察报告。",
    "Batch video and image content extraction Skill for transcription, OCR, structured notes, and report generation.": "批量视频和图片内容提取技能，用于转写、OCR、结构化笔记和报告生成。",
}

GENERIC_VALUE_TRANSLATIONS = {
    "display_only": "仅展示",
    "manual_instruction": "手动说明",
    "command_template": "命令模板",
    "local_link": "本地链接",
    "report_view": "报告查看",
    "codex_prompt": "Codex 提示词",
    "future_connector": "未来连接器",
    "not_executable": "不可执行",
    "manual_only": "仅手动",
    "template_only": "仅模板",
    "planned": "计划中",
    "low": "低",
    "medium": "中",
    "high": "高",
    "blocked": "已阻止",
    "none": "无",
    "true": "是",
    "false": "否",
    "read_only_health_check": "只读健康检查",
    "read_only_manifest_context": "只读 Manifest 上下文",
    "display_command_only": "仅展示命令",
    "demo_only": "仅演示",
    "metadata_only": "仅元数据",
    "future_connector": "未来连接器",
    "local_export": "本地导出",
    "read_only_metadata": "只读元数据",
    "read_only_content": "只读内容",
    "write_limited": "有限写入",
    "write_sensitive": "敏感写入",
    "local_demo": "本地演示",
    "dry_run_only": "仅 dry-run",
    "allowed": "允许",
    "rejected": "已拒绝",
    "pending": "待处理",
    "required": "需要",
    "not_required": "不需要",
    "display_only_no_execution": "仅展示，不执行",
    "deep_chinese_ui_coverage_check": "深度中文 UI 覆盖检查",
    "not_enabled_in_hub_v2_024": "HUB-V2-024 未启用真实连接器",
    "demo_safe": "演示安全模式",
    "disabled_by_default": "默认禁用",
    "metadata_instruction_template_only": "仅元数据 / 说明 / 模板",
    "display_text_only_never_auto_execute": "仅文本展示，绝不自动执行",
    "display_only_text_recommendation_no_execution": "仅展示文本建议，不执行",
    "design_only_readiness_simulation_no_live_connection": "仅设计级就绪度模拟，无真实连接",
    "approval_gate_metadata_only_no_execution": "仅审批门元数据，不执行",
    "public_safe_demo_report_metadata_only_no_execution": "仅公开安全演示报告元数据，不执行",
    "local_simulation_only_no_live_connector_no_real_action_no_credentials": "仅本地模拟，无真实连接器、无真实动作、无凭证",
}

COLUMN_LABEL_TRANSLATIONS = {
    "agent_id": "智能体 ID",
    "agent_name": "智能体",
    "source": "来源",
    "category": "分类",
    "category_label": "分类",
    "project_type": "项目类型",
    "status": "状态",
    "stage": "阶段",
    "showcase_status": "展示状态",
    "pin_status": "置顶状态",
    "next_action": "下一步",
    "next_recommended_action": "下一步建议",
    "health_status": "健康状态",
    "priority": "优先级",
    "recommended_action": "建议行动",
    "reason": "原因",
    "related_issue": "相关问题",
    "available_actions": "可用动作",
    "execution_policy": "执行策略",
    "action_id": "动作 ID",
    "label": "标签",
    "action_type": "动作类型",
    "execution_mode": "执行模式",
    "risk_level": "风险级别",
    "requires_approval": "需要审批",
    "connector_required": "所需连接器",
    "runbook_ref": "Runbook 引用",
    "title": "标题",
    "source_agent": "来源智能体",
    "source_type": "来源类型",
    "usefulness_score": "有用性",
    "relevance_score": "相关性",
    "urgency_score": "紧急度",
    "actionability_score": "可行动性",
    "value_score": "价值",
    "risk_score": "风险",
    "target_agent": "目标智能体",
    "bucket": "分组",
    "health_score": "健康分",
    "path_exists": "路径存在",
    "readme_exists": "README 存在",
    "requirements_exists": "requirements 存在",
    "app_exists": "App 存在",
    "tests_folder_exists": "tests 存在",
    "docs_folder_exists": "docs 存在",
    "project_status_exists": "PROJECT_STATUS 存在",
    "portfolio_folder_exists": "portfolio 存在",
    "missing_items": "缺失项",
    "suggested_fix": "建议修复",
    "workflow_name": "工作流",
    "gate_name": "审批门",
    "target_action_id": "目标动作",
    "target_connector_id": "目标连接器",
    "approval_status": "审批状态",
    "required_checks": "必需检查",
    "allowed_execution_mode": "允许执行模式",
    "block_reason": "阻止原因",
    "connector_name": "连接器",
    "provider": "提供方",
    "purpose": "用途",
    "data_access_level": "数据访问级别",
    "write_access": "写入权限",
    "approval_required": "需要审批",
    "demo_mode_available": "可演示模式",
    "read_only_mode_available": "可只读模式",
    "readiness_score": "就绪分",
    "readiness_status": "就绪状态",
    "live_connection_status": "真实连接状态",
    "connector_id": "连接器 ID",
    "mode": "模式",
    "agent_count": "智能体数量",
    "safe_mode": "安全模式",
    "project_name": "项目",
    "manifest_status": "Manifest 状态",
    "imported_agents": "已导入智能体",
    "invalid_agents": "无效智能体",
    "warnings": "警告",
    "recommended_fix": "建议修复",
    "is_valid": "是否有效",
    "quality_score": "质量分",
    "missing_required_fields": "缺失必填字段",
    "validation_notes": "校验说明",
}

PHRASE_TRANSLATIONS = {
    "No immediate action": "暂无立即行动",
    "Projects Scanned": "已扫描项目",
    "Manifests Found": "已发现 Manifest",
    "Valid Manifests": "有效 Manifest",
    "Static Overrides": "静态覆盖",
    "Total signals": "信号总数",
    "High-value signals": "高价值信号",
    "Needs action": "需要处理",
    "Watchlist": "观察列表",
    "Ignored / low priority": "已忽略 / 低优先级",
    "Avg usefulness": "平均有用性",
    "Signal category": "信号分类",
    "Signal status": "信号状态",
    "Source agent": "来源智能体",
    "Min usefulness": "最低有用性",
    "Total demo workflows": "演示工作流总数",
    "Ready for manual review": "可手动审阅",
    "Blocked steps": "阻止步骤",
    "Manual-only steps": "仅手动步骤",
    "Template-only outputs": "仅模板输出",
    "Approval gates required": "需要审批门",
    "Avg workflow readiness": "平均工作流就绪度",
    "Workflow type": "工作流类型",
    "Workflow status": "工作流状态",
    "Total connectors": "连接器总数",
    "Design-only connectors": "仅设计连接器",
    "Ready for demo": "可用于演示",
    "Needs review": "需要审阅",
    "Blocked until approved": "审批前阻止",
    "High-risk connectors": "高风险连接器",
    "Avg readiness": "平均就绪度",
    "Connector risk": "连接器风险",
    "Readiness status": "就绪状态",
    "Recommended Fixes": "建议修复",
    "Required Fields": "必填字段",
    "Execution Policy": "执行策略",
    "Connector Policy": "连接器策略",
    "Manifest Files": "Manifest 文件",
    "Local path details for manual review": "手动审阅的本地路径详情",
    "Path details are intentionally collapsed for public-safe screenshots.": "路径详情默认折叠，避免公开安全截图暴露过多本地路径。",
    "Tracked Agents": "追踪智能体",
    "Agents": "智能体",
    "Actions": "动作",
    "Useful Signals": "有用信号",
    "Connectors": "连接器",
    "Workflows": "工作流",
    "Approval Gates": "审批门",
    "Safety Snapshot": "安全快照",
    "High Priority": "高优先级",
    "Medium Priority": "中优先级",
    "Low Priority": "低优先级",
    "Report Summary": "报告摘要",
    "Saved local report": "已保存本地报告",
    "Could not save local report": "无法保存本地报告",
    "Demo/local metadata only": "仅演示 / 本地元数据",
    "No live connector connected": "未连接真实连接器",
    "No credentials loaded": "未加载凭证",
    "No real action executed": "未执行真实动作",
    "No external API called": "未调用外部 API",
    "It points to a decision or build step that can move the current checkpoint forward.": "它指向一个能推进当前 checkpoint 的决策或构建步骤。",
    "Complete HUB-V2-007 with schema, scoring, filters, recommendations, and UI cards.": "完成 HUB-V2-007 的 schema、评分、筛选器、推荐和 UI 卡片。",
    "This Agent has no declared action rows.": "此智能体暂无已声明动作行。",
    "No Agent manifests are available for prompt generation.": "暂无可用于生成提示词的智能体 Manifest。",
    "Connector readiness": "连接器就绪度",
    "Priority": "优先级",
    "Reason": "原因",
    "Issue": "问题",
    "Showcase": "展示",
    "Agent is complete and showcase-ready.": "智能体已完成并可公开展示。",
    "Project is complete and showcase-ready.": "项目已完成并可公开展示。",
    "Registry validation failed.": "注册表校验失败。",
    "Pin status is not finalized.": "置顶状态尚未最终确定。",
    "Health check found missing local project structure.": "健康检查发现本地项目结构缺失。",
    "Health check is partial.": "健康检查部分通过。",
    "Next action indicates screenshot work is pending.": "下一步显示截图工作待完成。",
    "Fix registry metadata": "修复注册表元数据",
    "Fix local project path or missing core files": "修复本地项目路径或缺失核心文件",
    "Complete missing project structure files": "补齐缺失的项目结构文件",
    "Capture showcase screenshots": "采集展示截图",
    "Continue HUB-V2-002 Manifest Import + Agent Onboarding Flow.": "继续 HUB-V2-002 Manifest 导入与智能体接入流程。",
    "Local filesystem presence check only.": "仅检查本地文件是否存在。",
    "Project looks showcase-ready.": "项目看起来已具备展示条件。",
    "Local path not found. Confirm project location or update registry.": "未找到本地路径。请确认项目位置或更新注册表。",
    "Complete missing project structure files before public showcase.": "公开展示前补齐缺失的项目结构文件。",
    "Add README.md and requirements.txt before public showcase.": "公开展示前补齐 README.md 和 requirements.txt。",
    "HUB-V2-007 signals are local/demo/template-only recommendations. They do not execute actions or connect external services.": "HUB-V2-007 信号仅为本地 / 演示 / 模板建议，不执行动作，也不连接外部服务。",
    "HUB-V2-005 actions are metadata, instructions, command templates, links, report views, Codex prompts, or future connector placeholders only.": "HUB-V2-005 动作仅为元数据、说明、命令模板、链接、报告视图、Codex 提示词或未来连接器占位。",
    "Approval gates are metadata only.": "审批门仅为元数据。",
    "Total gates": "审批门总数",
    "Blocked gates": "已阻止审批门",
    "Allowed modes are": "允许模式为",
    "Manifest-declared connector surfaces remain local, link-based, planned, optional, or not connected.": "Manifest 声明的连接器入口仍保持本地、链接型、计划中、可选或未连接状态。",
    "Local filesystem checks, GitHub links, and Streamlit launch commands are available as safe display-only surfaces. Live account connectors remain disabled until a future explicit integration stage.": "本地文件系统检查、GitHub 链接和 Streamlit 启动命令仅作为安全展示入口。真实账号连接器在未来明确集成阶段前保持禁用。",
    "Gmail, Google Sheets, Google Drive, Notion, Airtable, Telegram, GitHub, n8n, Make, and Zapier are reserved for future opt-in connector work.": "Gmail、Google Sheets、Google Drive、Notion、Airtable、Telegram、GitHub、n8n、Make 和 Zapier 保留给未来明确选择的连接器阶段。",
    "Static registry overrides are expected while AgentHub keeps CSV data as a baseline and local manifests as the richer runtime source.": "静态注册表覆盖是预期行为；AgentHub 保留 CSV 作为基线，同时使用本地 Manifest 作为更丰富的运行时来源。",
    "tracked projects": "个追踪项目",
    "paused or complete": "已暂停或已完成",
    "public showcase projects": "个公开展示项目",
    "public but not pinned": "公开但未置顶",
    "showcase-ready projects": "个可公开展示项目",
    "missing/incomplete health checks": "项健康检查缺失或不完整",
    "registry metadata issue(s)": "项注册表元数据问题",
    "high-priority action(s)": "项高优先级行动",
    "Next best move": "下一步最佳行动",
    "The portfolio is strongest where local-first AI workflows, business analysis, media extraction, finance research, and operations dashboards are already visible. The main gaps are dedicated knowledge-base workflows, deeper orchestration, and public showcase packaging for the hub itself.": "当前作品集优势集中在本地优先 AI 工作流、商业分析、媒体提取、金融研究和运营仪表盘。主要缺口是专门的知识库工作流、更深的编排能力，以及 Hub 自身的公开展示包装。",
    "AgentHubControlCenter frames the portfolio as a local-first AI Agent and Skill ecosystem spanning media intelligence, finance research, business discovery, workflow automation, news analysis, career workflows, and AgentOps / PortfolioOps management.": "AgentHubControlCenter 将作品集呈现为本地优先 AI Agent / Skill 生态，覆盖媒体智能、金融研究、商业发现、工作流自动化、新闻分析、职业流程和 AgentOps / PortfolioOps 管理。",
    "Local-first AI workflows": "本地优先 AI 工作流",
    "Streamlit dashboards": "Streamlit 仪表盘",
    "Business-oriented automation": "面向商业的自动化",
    "Report generation": "报告生成",
    "Finance and market analysis": "金融与市场分析",
    "Workflow diagnosis": "工作流诊断",
    "Knowledge base workflow not yet represented as a dedicated project": "知识库工作流尚未作为独立项目充分展示",
    "AI persona / avatar content workflow pending": "AI 人设 / 数字形象内容工作流待补齐",
    "Multi-agent orchestration still early-stage": "多智能体编排仍处于早期阶段",
    "Production deployment not yet included": "尚未包含生产部署案例",
    "Real client case studies not included": "尚未包含真实客户案例",
    "No action rows match the selected filters.": "没有行动行符合当前筛选器。",
    "No health rows match the selected filters.": "没有健康检查行符合当前筛选器。",
    "No top signals match the current filters.": "没有高优先级信号符合当前筛选器。",
    "No needs-action signals match the current filters.": "没有需要处理的信号符合当前筛选器。",
    "No watchlist signals match the current filters.": "没有观察列表信号符合当前筛选器。",
    "No low-priority signals match the current filters.": "没有低优先级信号符合当前筛选器。",
    "No connector readiness rows match the selected filters.": "没有连接器就绪记录符合当前筛选器。",
    "No connector-generated signals are available.": "暂无连接器生成信号。",
    "No workflow-generated signals are available.": "暂无工作流生成信号。",
    "No approval gates are available.": "暂无审批门。",
    "No project folders were found under the scan root.": "扫描根目录下未发现项目文件夹。",
    "No valid local manifests were imported yet.": "尚未导入有效的本地 Manifest。",
    "No duplicate agent_id conflicts found.": "未发现重复 agent_id 冲突。",
    "No missing manifests.": "没有缺失 Manifest。",
    "No invalid manifests.": "没有无效 Manifest。",
    "Missing items": "缺失项",
    "Warnings": "警告",
    "Suggested fix": "建议修复",
    "Last checked": "上次检查",
    "Scope": "范围",
    "Input source": "输入来源",
    "Connected agents": "连接的智能体",
    "Signals used": "使用的信号",
    "Recommended actions": "建议行动",
    "Approval gate result": "审批门结果",
    "Blocked steps": "阻止步骤",
    "Generated outputs": "生成输出",
    "Readiness": "就绪度",
    "Purpose": "用途",
    "Provider": "提供方",
    "Data access": "数据访问",
    "Approval required": "需要审批",
    "Live status": "真实连接状态",
    "Permissions": "权限",
    "Safety gates": "安全门",
    "Rollback plan": "回滚计划",
    "Test plan": "测试计划",
    "Project path": "项目路径",
    "Checkpoint": "检查点",
    "Codex prompt actions": "Codex 提示词动作",
    "Execution": "执行方式",
    "template-only / no execution": "仅模板 / 不执行",
    "Projects": "项目",
    "Status": "状态",
    "Next": "下一步",
    "Role": "角色",
    "Agents": "智能体",
    "Capabilities": "能力",
    "Showcase count": "展示数量",
    "Pinned count": "置顶数量",
    "Tracked Agents": "追踪智能体",
    "Public Showcase": "公开展示",
    "Showcase Ready": "可公开展示",
    "High Priority": "高优先级",
    "Report Summary": "报告摘要",
    "Default mode": "默认模式",
    "External API calls": "外部 API 调用",
    "Actions": "动作",
    "Current stage": "当前阶段",
    "Live connectors": "真实连接器",
    "Planned": "计划中",
    "Use agent_manifest.json, agent_contract.json, docs/AGENT_INTERFACE_STANDARD.md, and docs/FUTURE_PLUGIN_INTERFACE.md as the onboarding baseline.": "使用 agent_manifest.json、agent_contract.json、docs/AGENT_INTERFACE_STANDARD.md 和 docs/FUTURE_PLUGIN_INTERFACE.md 作为接入基线。",
}


def _text_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value).strip()


def _lookup(mapping: dict[str, str], value: Any) -> str | None:
    text = _text_value(value)
    if not text:
        return None
    if text in mapping:
        return mapping[text]
    lowered = text.lower()
    for key, translated in mapping.items():
        if key.lower() == lowered:
            return translated
    return None


def _phrase_translate(value: str) -> str:
    translated = value
    for source, target in sorted(PHRASE_TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True):
        translated = translated.replace(source, target)
    dynamic_phrase_maps = (
        DESCRIPTION_TRANSLATIONS,
        NEXT_STEP_TRANSLATIONS,
        ACTION_LABEL_TRANSLATIONS,
        CONNECTOR_TRANSLATIONS,
        BADGE_TRANSLATIONS,
        CATEGORY_TRANSLATIONS,
        AGENT_DISPLAY_NAMES,
    )
    for mapping in dynamic_phrase_maps:
        for source, target in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
            if source and source != target:
                translated = translated.replace(source, target)
    return translated


DOMAIN_TRANSLATIONS = {
    "agent": AGENT_DISPLAY_NAMES,
    "agent_name": AGENT_DISPLAY_NAMES,
    "category": CATEGORY_TRANSLATIONS,
    "status": STATUS_TRANSLATIONS,
    "health": STATUS_TRANSLATIONS,
    "pin": STATUS_TRANSLATIONS,
    "showcase": STATUS_TRANSLATIONS,
    "badge": BADGE_TRANSLATIONS,
    "action": ACTION_LABEL_TRANSLATIONS,
    "action_label": ACTION_LABEL_TRANSLATIONS,
    "connector": CONNECTOR_TRANSLATIONS,
    "next_step": NEXT_STEP_TRANSLATIONS,
    "description": DESCRIPTION_TRANSLATIONS,
    "filter": STATUS_TRANSLATIONS,
    "priority": STATUS_TRANSLATIONS,
    "source": {
        "local_manifest": "本地 Manifest",
        "demo_manifest": "演示 Manifest",
        "static_registry": "静态注册表",
        "local_json": "本地 JSON",
        "local_csv": "本地 CSV",
        "agent_manifest": "Agent Manifest",
        "project_status": "项目状态",
        "report": "报告",
        "manual_demo_data": "手动演示数据",
        "action_registry": "动作注册表",
        "codex_prompt_generator": "Codex 提示词生成器",
        "connector_readiness": "连接器就绪度",
        "workflow_simulation": "工作流模拟",
    },
    "column": COLUMN_LABEL_TRANSLATIONS,
    "generic": GENERIC_VALUE_TRANSLATIONS,
}


def normalize_language(language: str | None) -> str:
    """Return a supported UI language code."""
    if not language:
        return DEFAULT_LANGUAGE
    normalized = str(language).strip().lower()
    return LANGUAGE_LABEL_TO_CODE.get(normalized, DEFAULT_LANGUAGE)


def _default_session_state() -> MutableMapping[str, Any] | None:
    try:
        import streamlit as st
    except Exception:
        return None
    return st.session_state


def get_language(session_state: MutableMapping[str, Any] | None = None) -> str:
    """Read the current UI language from session state."""
    state = session_state if session_state is not None else _default_session_state()
    if state is None:
        return DEFAULT_LANGUAGE
    return normalize_language(state.get(SESSION_LANGUAGE_KEY, DEFAULT_LANGUAGE))


def set_language(
    language: str,
    session_state: MutableMapping[str, Any] | None = None,
) -> str:
    """Store and return the current UI language code."""
    code = normalize_language(language)
    state = session_state if session_state is not None else _default_session_state()
    if state is not None:
        state[SESSION_LANGUAGE_KEY] = code
    return code


def t(key: str, language: str | None = None, **kwargs: Any) -> str:
    """Translate a UI label with English/key fallback."""
    code = normalize_language(language) if language else get_language()
    value = TRANSLATIONS.get(key, {}).get(code)
    if value is None:
        value = TRANSLATIONS.get(key, {}).get("en", key)
    if kwargs:
        try:
            return value.format(**kwargs)
        except (KeyError, ValueError):
            return value
    return value


def display_text(value: Any, language: str | None = None, domain: str = "generic") -> str:
    """Translate a dynamic UI value for display without changing source data."""
    text = _text_value(value)
    if not text:
        return text
    code = normalize_language(language) if language else get_language()
    if code != "zh":
        return text

    mapping = DOMAIN_TRANSLATIONS.get(domain, {})
    translated = _lookup(mapping, text)
    if translated is not None:
        return translated

    generic = _lookup(GENERIC_VALUE_TRANSLATIONS, text)
    if generic is not None:
        return generic

    status = _lookup(STATUS_TRANSLATIONS, text)
    if status is not None:
        return status

    category = _lookup(CATEGORY_TRANSLATIONS, text)
    if category is not None:
        return category

    return _phrase_translate(text)


def translate_list_values(
    values: list[Any] | tuple[Any, ...] | set[Any],
    language: str | None = None,
    domain: str = "generic",
) -> list[str]:
    """Translate a list of dynamic values for display."""
    if not isinstance(values, (list, tuple, set)):
        return []
    return [display_text(value, language, domain=domain) for value in values if _text_value(value)]


def translate_category(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="category")


def translate_status(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="status")


def translate_badge(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="badge")


def translate_action_label(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="action_label")


def translate_connector(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="connector")


def translate_next_step(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="next_step")


def translate_filter_option(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="filter")


def translate_agent_display_name(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="agent")


def translate_agent_description(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="description")


def translate_column_label(value: Any, language: str | None = None) -> str:
    return display_text(value, language, domain="column")


def resolve_project_stage(project_root: str | Path) -> dict[str, str]:
    """Backward-compatible wrapper around the stage status snapshot."""
    snapshot = get_stage_snapshot(project_root)
    if snapshot["latest_checkpoint"] == "Unknown" and snapshot["manifest_version"] != "Unknown":
        return {
            "stage": snapshot["manifest_version"],
            "source": snapshot["manifest_version_source"],
            "manifest_stage": snapshot["manifest_version"],
        }
    return {
        "stage": snapshot["latest_checkpoint"],
        "source": snapshot["latest_checkpoint_source"],
        "manifest_stage": snapshot["manifest_version"],
    }
