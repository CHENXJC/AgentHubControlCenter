# Future Plugin Interface

Status: HUB-V2-009

The future plugin interface is the path for turning AgentHubControlCenter from a
portfolio dashboard into a local-first AI Agent Operating System. HUB-V2-009
adds Local Workflow Simulation + Approval Gates before any future live
connector or execution stage.

## Interface Flow

```text
Declare -> Validate -> Preview -> Execute
```

## Stage 1: Declare

Each Agent declares:

- Identity: `agent_id`, `agent_name`, `category`, `description`
- Local project metadata: `project_path`, `status`, `last_run`
- IO: `inputs`, `outputs`
- Actions: schema-backed display, manual instruction, command template, local
  link, report view, Codex prompt, or future connector placeholder
- Connectors: local filesystem, GitHub link, future account connectors
- Safety flags: `demo_mode`, `safe_mode`
- Next recommendation: `next_recommended_action`

Current status: ready as a standard through `agent_contract.json`,
`docs/AGENT_INTERFACE_STANDARD.md`, `docs/ACTION_SCHEMA.md`, and
`docs/MANIFEST_IMPORT_GUIDE.md`.

## Stage 2: Validate

AgentHub should validate required fields before showing a project as a usable
tool.

Validation should check:

- Required field presence.
- Safe mode is true by default.
- Demo mode is clear.
- Local path exists if the tool is marked active.
- Connector declarations do not include secrets.
- External connector status is planned/demo unless explicitly enabled later.
- Action declarations use approved `action_type`, `execution_mode`, and
  `risk_level` enum values.
- High-risk and blocked actions require explicit approval and remain blocked in
  this stage.

Current status: implemented through `agent_hub/manifest_loader.py` and
`agent_hub/agent_onboarding.py`, with action validation support in
`agent_hub/action_schema.py` and `agent_hub/action_registry.py`.

## Stage 3: Preview

The user should see exactly what an Agent can do before anything is executed.

Preview surfaces:

- Command Overview
- My Tools / Agent Registry
- My Workflows
- Useful Signals
- Action Center
- Connectors
- Future Plugin Interface

Current status: implemented as schema-backed display/manual/template UI in
HUB-V2-009, including Local Action Schema metrics, Agent-grouped action cards,
Codex Prompt Generator, Useful Signals ranking, Connector Readiness Simulator,
Local Workflow Simulation, and Approval Gates.

## Stage 4: Execute

Execution is a future opt-in stage. It should not be added casually.

Before execution is enabled, the project needs:

- Explicit user approval for each action class.
- Separate connector configuration docs.
- Secret-safe handling that never prints tokens or credentials.
- Tests for action routing and failure handling.
- Clear action logs.
- A rollback or disable path.

Current status: not enabled in HUB-V2-009.

## Connector Roadmap

| Connector | HUB-V2-009 Status | Notes |
| --- | --- | --- |
| Local filesystem | Available local | Health checks and paths only. |
| GitHub showcase | Available as link | User-click navigation only. |
| Streamlit local app | Manual launch | Commands are shown, not executed inside the UI. |
| Gmail | Simulated readiness | No live mailbox access in this stage. |
| Google Sheets | Simulated readiness | Read/write readiness is scored, but no live sheet is connected. |
| Google Drive | Simulated readiness | No Drive file access in this stage. |
| Notion | Simulated readiness | No live workspace access in this stage. |
| Airtable | Simulated readiness | No live base access in this stage. |
| Telegram | Simulated readiness | No bot token is read and no message is sent. |
| GitHub | Simulated readiness | Public status read can be demo-planned; push/release stays blocked. |
| n8n / Make / Zapier | Future readiness | Payload/webhook plans are local metadata only. |

## HUB-V2-005 Completed Scope

HUB-V2-005 stays practical:

1. Keeps optional manifest import from child project folders.
2. Keeps manifest templates for the existing 10 child projects.
3. Preserves manifest-declared inputs, outputs, actions, and connectors in the runtime UI.
4. Normalizes 55 actions across 11 Agents into the HUB-V2-005 action schema.
5. Adds Action Center metrics and Agent-grouped action cards.
6. Adds manual runbook and action safety policy docs.
7. Keeps all actions display/manual/template/planned only.

## HUB-V2-006 Completed Scope

HUB-V2-006 builds a Codex Prompt Generator on top of the `codex_prompt` action
type. It remains template-only and does not send messages, run project code, or
trigger child Agent actions automatically.

## HUB-V2-007 Completed Scope

HUB-V2-007 adds a Useful Signals Engine on top of local manifest, status,
report, action registry, local JSON/CSV-style demo, and manual demo metadata.
It ranks recommendations with usefulness, relevance, urgency, actionability,
value, and risk scores while keeping every recommendation display-only.

## HUB-V2-008 Completed Scope

HUB-V2-008 adds a Connector Readiness Simulator: a design-only view that shows
required permissions, safety gates, approval requirements, risk levels, test
plans, rollback plans, readiness scores, and recommended next steps before any
future Gmail, Google Sheets, Google Drive, Notion, Airtable, Telegram, GitHub,
n8n, Make, Zapier, or other live connector stage.

## HUB-V2-009 Completed Scope

HUB-V2-009 adds Local Workflow Simulation + Approval Gates: a simulation-only
model for chaining local input signals, Useful Signals scoring, recommended
actions, approval gates, blocked steps, manual steps, Codex handoff prompts,
Manual Runbook references, and summary outputs.

It still avoids live provider calls, OAuth, credentials, child scripts, real
actions, remote mutations, and git push.

## Recommended HUB-V2-010 Scope

HUB-V2-010 can add a demo workflow report/export layer for the workflow
simulation results. It should remain metadata-only unless the user explicitly
starts a separate live connector or execution implementation stage.
