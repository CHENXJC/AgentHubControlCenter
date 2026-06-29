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
        "zh": "template-only / no execution",
        "en": "template-only / no execution",
    },
    "demo_mode": {
        "zh": "Demo Mode",
        "en": "Demo Mode",
    },
    "manual_review_mode": {
        "zh": "Manual Review Mode",
        "en": "Manual Review Mode",
    },
    "safe_mode": {
        "zh": "Safe Mode",
        "en": "Safe Mode",
    },
    "review_required": {
        "zh": "Review Required",
        "en": "Review Required",
    },
    "source_local_manifest": {
        "zh": "Local Manifest",
        "en": "Local Manifest",
    },
    "source_demo_manifest": {
        "zh": "Demo Manifest",
        "en": "Demo Manifest",
    },
    "source_static_registry": {
        "zh": "Static Registry",
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
        "zh": "Required",
        "en": "Required",
    },
    "approval_not_required": {
        "zh": "Not required",
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
