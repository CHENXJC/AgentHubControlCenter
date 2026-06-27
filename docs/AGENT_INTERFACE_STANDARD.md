# Agent Interface Standard

Status: HUB-V2-009

AgentHubControlCenter V2 treats each project as a tool that can declare what it
does, what it needs, what it produces, which safe local actions are visible, and
which connectors are available or planned.

This is a local-first interface standard. It does not enable live account
connectors, does not read credentials, and does not execute external actions by
default.

## Required Fields

Each future Agent or Skill should declare at least:

| Field | Meaning |
| --- | --- |
| `agent_id` | Stable lowercase identifier. |
| `agent_name` | Human-readable project name. |
| `category` | Portfolio category such as Media Intelligence or Workflow Automation. |
| `description` | One-sentence capability description. |
| `project_path` | Local Windows project path. |
| `status` | Planned, Active, Complete, or Paused. |
| `inputs` | Expected local inputs or manual context. |
| `outputs` | Files, dashboard views, summaries, or reports the Agent can produce. |
| `actions` | Safe actions to show in the Action Center. |
| `connectors` | Local, link-based, demo, or future connectors. |
| `demo_mode` | Whether the Agent uses demo/static/local data. |
| `safe_mode` | Whether external actions and credential reads are disabled. |

Optional fields include:

| Field | Meaning |
| --- | --- |
| `version` | Manifest or project stage label. |
| `action_schema_version` | Action schema version, currently `HUB-V2-005`. |
| `last_run` | Last tracked run time, or `Not tracked yet`. |
| `next_recommended_action` | Next safe action shown in the command center. |
| `github_repo` | GitHub showcase URL. |
| `dashboard_url` | Optional local or public dashboard URL. |
| `tags` | Labels such as Python, Streamlit, OCR, or Workflow Automation. |
| `owner` | Owner or maintainer label. |
| `public_showcase_status` | GitHub/public showcase status. |
| `pin_status` | GitHub profile pin status. |

## Current Source Of Truth

HUB-V2-009 keeps `data/agent_registry.csv` as the stable baseline for existing
portfolio projects, then scans immediate child folders under `F:\AIProjects`
for optional `agent_manifest.json` files.

Valid manifest records are converted into runtime registry records and merged
with the static CSV registry. Manifest records can override static records with
the same `agent_id` in the runtime view. The CSV file is not rewritten by this
stage.

The root-level files are interface examples:

- `agent_manifest.json`
- `agent_contract.json`
- `agent_hub/manifest_loader.py`
- `agent_hub/agent_onboarding.py`
- `agent_hub/action_schema.py`
- `agent_hub/action_registry.py`
- `agent_hub/codex_prompt_generator.py`
- `agent_hub/useful_signal_schema.py`
- `agent_hub/useful_signal_engine.py`
- `agent_hub/connector_readiness_schema.py`
- `agent_hub/connector_readiness_engine.py`
- `agent_hub/workflow_simulation_schema.py`
- `agent_hub/workflow_simulation_engine.py`
- `agent_hub/approval_gate_schema.py`
- `agent_hub/approval_gate_engine.py`

## Action Rules

Actions are visible before they are executable. HUB-V2-009 requires each action
to use the local action schema documented in `docs/ACTION_SCHEMA.md`.

Allowed in HUB-V2-009:

- Show local launch commands.
- Show project folder commands.
- Show GitHub links.
- Show local test commands.
- Show recommended next actions.
- Scan `F:\AIProjects` immediate child folders for `agent_manifest.json`.
- Read and validate `agent_manifest.json` only.
- Display action type, execution mode, risk level, approval flag, expected
  output, safety note, and manual runbook reference.
- Display command templates as text only.
- Generate Codex prompt text for manual copy only.
- Generate scored Useful Signals as display-only recommendations.
- Display Connector Readiness Simulator metadata for future connectors.
- Display Local Workflow Simulation metadata for demo workflows.
- Display Approval Gates for recommended action and connector classes.

Not enabled in HUB-V2-009:

- Sending email.
- Posting to Telegram.
- Writing to Google Sheets, Notion, or Airtable.
- Auto-sending generated prompts to Codex.
- Reading `.env`, tokens, passwords, or credentials.
- Running external account automation.
- Running child project scripts during discovery.
- Creating OAuth flows.
- Calling provider APIs.
- Triggering webhooks.
- Executing workflow simulations.
- Treating Approval Gates as real execution approval.

## Useful Signal Rules

Useful Signals are recommendations, not executable tasks. Each signal must use
the schema documented in `docs/USEFUL_SIGNALS_ENGINE.md`, including:

- `title`
- `source_agent`
- `source_type`
- `category`
- `summary`
- `usefulness_score`
- `relevance_score`
- `urgency_score`
- `actionability_score`
- `value_score`
- `risk_score`
- `recommended_action`
- `target_agent`
- `status`

Allowed categories are `project_progress`, `action_required`,
`business_opportunity`, `learning_value`, `portfolio_improvement`,
`connector_readiness`, `workflow_automation`, and `risk_warning`.

Allowed statuses are `new`, `reviewed`, `needs_action`, `watchlist`,
`ignored`, and `archived`.

Every signal uses `display_only_text_recommendation_no_execution`.

## Connector Readiness Rules

Connector readiness records are simulations, not integrations. Each connector
must use the schema documented in `docs/CONNECTOR_READINESS_SIMULATOR.md`,
including:

- `connector_id`
- `connector_name`
- `provider`
- `purpose`
- `required_permissions`
- `data_access_level`
- `write_access`
- `risk_level`
- `approval_required`
- `demo_mode_available`
- `read_only_mode_available`
- `rollback_plan`
- `test_plan`
- `safety_gates`
- `readiness_score`
- `readiness_status`
- `recommended_next_step`

Allowed readiness statuses are `design_only`, `not_connected`,
`ready_for_demo`, `needs_review`, `blocked_until_approved`, and `future`.

Allowed data access levels are `none`, `local_demo`, `read_only_metadata`,
`read_only_content`, `write_limited`, and `write_sensitive`.

Every connector readiness record uses
`design_only_readiness_simulation_no_live_connection`, and every evaluated
record must show `live_connection_status=not_connected`.

High-risk, blocked, and write-capable connectors must require approval.

## Workflow Simulation And Approval Gate Rules

Workflow simulations are local planning records, not executable workflows. Each
workflow must use the schema documented in `docs/LOCAL_WORKFLOW_SIMULATION.md`
and the execution policy:

`local_simulation_only_no_live_connector_no_real_action_no_credentials`

Approval gates are metadata controls, not real execution approvals. Each gate
must use the schema documented in `docs/APPROVAL_GATE_PLANNER.md` and the
execution policy:

`approval_gate_metadata_only_no_execution`

Allowed approval gate execution modes are `display_only`, `manual_only`,
`template_only`, `dry_run_only`, and `blocked`.

Blocked gates must remain blocked. HUB-V2-009 explicitly blocks Gmail Send and
GitHub Push / Release.

## Minimal Future Agent Example

```json
{
  "agent_id": "demo_agent",
  "agent_name": "DemoAgent",
  "category": "Workflow Automation",
  "description": "Demo workflow automation assistant.",
  "project_path": "F:\\AIProjects\\DemoAgent",
  "status": "Active",
  "inputs": ["workflow_notes", "manual_config"],
  "outputs": ["dashboard", "summary", "export"],
  "actions": [
    {
      "action_id": "manual_run_dashboard",
      "label": "Manual run dashboard",
      "description": "Show the manual dashboard launch runbook for the Agent.",
      "action_type": "manual_instruction",
      "execution_mode": "manual_only",
      "risk_level": "low",
      "requires_approval": false,
      "command_template": "cd /d \"F:\\AIProjects\\DemoAgent\" && streamlit run app.py",
      "runbook_ref": "docs/MANUAL_RUNBOOK.md#demo-agent-manual-run-dashboard",
      "expected_output": "User manually opens the local Streamlit dashboard outside automated execution.",
      "safety_note": "Display/manual metadata only; AgentHub does not execute this action.",
      "connector_required": "none",
      "status": "manual_ready"
    }
  ],
  "connectors": [
    {
      "connector_id": "local_filesystem",
      "label": "Local Filesystem",
      "status": "available_local",
      "mode": "read_only_health_check",
      "safe_mode": true
    }
  ],
  "demo_mode": true,
  "safe_mode": true,
  "last_run": "Not tracked yet",
  "next_recommended_action": "Review manifest before enabling execution."
}
```

## HUB-V2-009 Import, Prompt, Signal, Connector, And Workflow Flow

The current import flow is:

1. Read optional per-project `agent_manifest.json` files.
2. Validate required fields.
3. Normalize action metadata into the HUB-V2-005 action schema.
4. Merge valid manifests into the current registry-derived command center view.
5. Keep invalid or unsafe manifests visible as review items instead of executing
   anything automatically.
6. Generate copy-ready Codex prompt text from selected Agent context when the
   user opens the Codex Prompt Generator section.
7. Generate scored Useful Signals from local/demo metadata and show the results
   as display-only recommendation cards.
8. Generate Connector Readiness Simulator records from local/demo metadata and
   show the results as design-only connector cards.
9. Generate Local Workflow Simulation records and Approval Gates from local/demo
   metadata and show the results as simulation-only workflow cards.

See:

- `docs/ACTION_SCHEMA.md`
- `docs/MANUAL_RUNBOOK.md`
- `docs/ACTION_SAFETY_POLICY.md`
- `docs/MANIFEST_IMPORT_GUIDE.md`
- `docs/AGENT_ONBOARDING_FLOW.md`
- `docs/CHILD_AGENT_MANIFEST_SUMMARY.md`
- `docs/CODEX_PROMPT_GENERATOR.md`
- `docs/USEFUL_SIGNALS_ENGINE.md`
- `docs/CONNECTOR_READINESS_SIMULATOR.md`
- `docs/CONNECTOR_SAFETY_GATES.md`
- `docs/LOCAL_WORKFLOW_SIMULATION.md`
- `docs/APPROVAL_GATE_PLANNER.md`
