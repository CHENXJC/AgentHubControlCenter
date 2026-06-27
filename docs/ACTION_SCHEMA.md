# Action Schema

Status: HUB-V2-009-LOCAL-WORKFLOW-SIMULATION-APPROVAL-GATES-COMPLETE

AgentHubControlCenter V2 uses a local action schema to describe what each Agent
can safely show, explain, copy, or reserve for a future connector stage. The
schema remains metadata-only in HUB-V2-009. It does not execute actions, does
not run child project scripts, and does not connect live accounts.

## Required Action Fields

Every action must include:

| Field | Meaning |
| --- | --- |
| `action_id` | Stable lowercase action identifier. |
| `label` | Human-readable action label. |
| `description` | What the action helps the user understand or do manually. |
| `action_type` | One of the approved action type enum values. |
| `execution_mode` | One of the approved execution mode enum values. |
| `risk_level` | One of the approved risk level enum values. |
| `requires_approval` | Boolean approval flag. |
| `command_template` | Text-only command or instruction template. Never auto-executed. |
| `runbook_ref` | Manual runbook reference for safe human operation. |
| `expected_output` | What the user should expect after manual review or manual use. |
| `safety_note` | Short safety boundary shown in the Action Center. |
| `connector_required` | Connector dependency, or `none`. |
| `status` | Display status such as `display_only`, `manual_ready`, `template_ready`, `planned`, or `blocked`. |

## Action Type Enum

- `display_only`
- `manual_instruction`
- `command_template`
- `local_link`
- `report_view`
- `codex_prompt`
- `future_connector`

## Execution Mode Enum

- `not_executable`
- `manual_only`
- `template_only`
- `planned`

No action in HUB-V2-009 may use a real execution mode such as `auto_execute`,
`run_now`, `background_job`, or `live_connector`.

## Risk Level Enum

- `low`
- `medium`
- `high`
- `blocked`

High or blocked actions must set `requires_approval=true`. Blocked actions must
not provide an executable workflow inside AgentHub.

## Blocked Action Examples

These action IDs are reserved as blocked or explicit-approval-only examples:

- `send_email`
- `delete_files`
- `modify_git_remote`
- `git_push`
- `connect_real_gmail`
- `connect_real_sheets`
- `run_external_script`

## HUB-V2-005 Safety Contract

- AgentHub displays actions, instructions, command templates, links, report
  views, Codex prompts, and future connector placeholders only.
- `command_template` is text. The Streamlit app must not call `subprocess`,
  launch child scripts, delete files, modify git remotes, or push to GitHub.
- Connectors remain local, link-based, planned, optional, or not connected.
- Live Gmail, Google Sheets, Notion, Airtable, Telegram, market-data, social,
  OCR, ASR, or account automation is not enabled by this schema.

## HUB-V2-006 Codex Prompt Generator

`action_type=codex_prompt` and `execution_mode=template_only` are now linked to
the Action Center Codex Prompt Generator. The generator creates copy-ready text
from Agent metadata, action rows, checkpoint context, safety rules, validation
requirements, and `next_recommended_action`.

Codex prompt actions still do not call Codex, write tasks to other threads, run
project code, or modify projects automatically.

## HUB-V2-007 Useful Signals Engine

HUB-V2-007 adds `docs/USEFUL_SIGNALS_ENGINE.md` as a separate recommendation
schema. Useful Signals can reference action IDs and suggest manual next steps,
but they do not change action execution mode. Action cards and signal cards both
remain display/manual/template/planned metadata only.

## HUB-V2-008 Connector Readiness Simulator

HUB-V2-008 adds `docs/CONNECTOR_READINESS_SIMULATOR.md` as a separate
design-only connector schema. Connector readiness cards can reference future
connector action classes, but they do not change the HUB-V2-005 action schema
and do not enable live execution.

## HUB-V2-009 Local Workflow Simulation + Approval Gates

HUB-V2-009 adds `docs/LOCAL_WORKFLOW_SIMULATION.md` and
`docs/APPROVAL_GATE_PLANNER.md` as separate simulation-only metadata layers.
Workflow cards and Approval Gates can reference action IDs or connector IDs,
but they do not change the HUB-V2-005 action schema and do not enable real
execution.
