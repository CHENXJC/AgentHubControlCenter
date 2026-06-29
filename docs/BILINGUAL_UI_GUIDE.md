# Bilingual UI Guide

Checkpoint:
`HUB-V2-024-DEEP-CHINESE-UI-COVERAGE-CHECK-COMPLETE`

## Purpose

This guide covers the local Chinese / English UI toggle, stage status sync, and
HUB-V2-024 deep Chinese UI coverage for user-facing dynamic display values.

This is a UI display layer only. It does not add action execution, connector
activation, child project scripts, external API calls, OAuth, git remote changes,
or git push.

## Language Toggle

The Streamlit sidebar includes an interface language selector:

- `中文`
- `English`

The selected language is stored in `st.session_state` through
`agent_hub/ui_i18n.py`.

Default language: `zh`.

## Implementation

The UI helper module is:

`agent_hub/ui_i18n.py`

It exposes:

- `TRANSLATIONS`
- `get_language()`
- `set_language()`
- `t(key, language)`
- `display_text(value, language, domain="generic")`
- `translate_category(value, language)`
- `translate_status(value, language)`
- `translate_badge(value, language)`
- `translate_action_label(value, language)`
- `translate_connector(value, language)`
- `translate_next_step(value, language)`
- `translate_filter_option(value, language)`
- `translate_agent_display_name(value, language)`
- `translate_agent_description(value, language)`
- `translate_column_label(value, language)`

Translations use a local dictionary only. No external translation API is called.

Stage/status display is handled by:

`agent_hub/stage_status.py`

It exposes:

- `load_project_status_checkpoint(project_root)`
- `load_manifest_version(project_root)`
- `get_product_status_label(project_root)`
- `get_stage_snapshot(project_root)`

## Covered UI Scope

The bilingual layer covers the major visible navigation and product UI text:

- Sidebar labels and filters
- Header / hero copy
- Top metric cards
- Main tab labels
- Command Overview
- My Tools / Agent Registry
- My Workflows
- Useful Signals
- Action Center
- Connectors
- Future Plugin Interface
- Agent Onboarding
- Codex Prompt Generator
- Demo Workflow Report Export
- Safety and disclaimer text

HUB-V2-024 also covers dynamic values loaded from manifests, registries, and
demo metadata:

- Agent display names and descriptions
- Category labels and category filters
- Status labels and status filters
- Manifest/source badges
- Action labels and action card fields
- Connector labels, provider names, and connector card fields
- Next-step and recommendation copy
- Table column labels and common table cell values
- Useful Signal, workflow, portfolio matrix, and Future Plugin Interface copy

Internal identifiers remain unchanged. The UI display layer does not translate
`agent_id`, `action_id`, `connector_id`, file names, repository names, schema
field names, code variables, or JSON keys.

## Stage Status Source

The sidebar separates product status from checkpoint metadata:

| Field | Source | Notes |
| --- | --- | --- |
| Product Status | `get_product_status_label()` | Stable product posture, currently `Maintain / Showcase Ready` |
| Latest Checkpoint | `PROJECT_STATUS.md` line matching `Current status: ...` | Exact latest checkpoint, including cross-project sync checkpoints |
| Manifest Version | `agent_manifest.json` `manifest_version`, then first Agent `version` | Root manifest metadata version |

In HUB-V2-024 the sidebar displays:

- Product Status from `agent_hub/stage_status.py`
- Latest Checkpoint from `PROJECT_STATUS.md`
- Manifest Version from `agent_manifest.json`

The hero badge displays Product Status, not Latest Checkpoint. This avoids the
previous stale hard-coded `HUB-V2-014` display and prevents child-project sync
checkpoints from being misread as the AgentHub product stage.

## Safety Boundary

- No `.env` is read.
- No secret, token, password, API key, or credential is output.
- No OAuth flow is created.
- No Gmail, Google Sheets, Notion, Airtable, Telegram, GitHub, n8n, Make,
  Zapier, or other live connector is connected.
- No child project script is run.
- No real Agent action is executed.
- No command template is executed.
- No git remote is modified.
- No git push or force push is performed in this stage.
- Generated prompts and command templates remain display/copy text only.

## Validation Notes

Recommended validation:

```powershell
cd F:\AIProjects\AgentHubControlCenter
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall .
```

Streamlit smoke check:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8525
```

Expected UI evidence:

- Chinese mode shows `总控概览`, `我的工具 / 智能体注册表`, `有用信号`, `操作中心`,
  `连接器`, and `未来插件接口`.
- Chinese mode shows dynamic values such as `本地 Manifest`, `演示模式 / 安全模式`,
  `可公开展示`, `查看项目状态`, and `暂无立即行动`.
- English mode shows `Command Overview`, `My Tools / Agent Registry`,
  `Useful Signals`, `Action Center`, `Connectors`, and
  `Future Plugin Interface`.
- English mode still shows dynamic values such as `Local Manifest`,
  `Demo Mode / Safe Mode`, and `View project status`.
- Project Stage is not `HUB-V2-014`.
- All actions remain display/manual/template/planned metadata only.
