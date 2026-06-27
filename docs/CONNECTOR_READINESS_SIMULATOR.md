# Connector Readiness Simulator

Status: HUB-V2-010-DEMO-WORKFLOW-REPORT-EXPORT-COMPLETE

## Purpose

The Connector Readiness Simulator evaluates future connector ideas before any
real integration work starts. It shows required permissions, risk level,
approval gates, rollback plan, test plan, readiness score, and recommended next
step for each candidate connector.

This is design-only metadata. It does not create OAuth flows, read credentials,
call provider APIs, send messages, write files, modify remotes, or run child
project scripts.

## Required Fields

Each connector readiness record includes:

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

Each evaluated connector also includes:

- `live_connection_status = not_connected`
- `execution_policy = design_only_readiness_simulation_no_live_connection`

## Readiness Status

- `design_only`
- `not_connected`
- `ready_for_demo`
- `needs_review`
- `blocked_until_approved`
- `future`

## Data Access Level

- `none`
- `local_demo`
- `read_only_metadata`
- `read_only_content`
- `write_limited`
- `write_sensitive`

## Risk Level

- `low`
- `medium`
- `high`
- `blocked`

High-risk and blocked connectors must set `approval_required=true`.
Write-capable connectors must also require approval.

## Readiness Score

Readiness score is explainable and metadata-only:

- Demo-mode availability increases readiness.
- Read-only mode increases readiness.
- A rollback plan increases readiness.
- A test plan increases readiness.
- Safety gates increase readiness.
- Medium, high, and blocked risk reduce readiness.
- Write access reduces readiness.
- Sensitive data access reduces readiness.

The score does not imply that the connector is connected. It only indicates
how ready the design is for a future approved stage.

## Demo Connectors

HUB-V2-008 includes 14 demo connector readiness records:

- Gmail Read Review
- Gmail Draft Creation
- Gmail Send
- Google Sheets Read
- Google Sheets Write
- Google Drive Read
- Notion Database Write
- Airtable CRM Sync
- Telegram Alert
- GitHub Status Read
- GitHub Push / Release
- n8n Webhook
- Make Scenario
- Zapier Zap

## Connector-Generated Useful Signals

The simulator converts selected readiness results into Useful Signals, such as:

- Gmail Send should stay blocked until approval workflow exists.
- Google Sheets Read is a safer first connector candidate.
- Telegram Alert can be demoed as preview text before any live send.

These signals are still display-only recommendations.

## HUB-V2-009 Workflow Integration

HUB-V2-009 connects connector readiness results into Local Workflow Simulation
and Approval Gates. The Connector Readiness Review Workflow blocks Gmail Send
and GitHub Push / Release, and only allows dry-run planning for safer read-only
connector candidates.

This integration is still metadata-only. It does not connect live providers or
execute connector actions.

## HUB-V2-010 Report Export Integration

Demo Workflow Report Export includes Connector Readiness summary metrics and a
connector table in Markdown, JSON, and CSV outputs. Connector rows remain
`not_connected`, and exporting readiness metadata does not create OAuth flows,
load credentials, call provider APIs, or execute connector actions.

## UI Behavior

The Connectors page shows:

- Total connectors.
- Design-only connectors.
- Ready-for-demo connectors.
- Needs-review connectors.
- Blocked-until-approved connectors.
- High-risk connectors.
- Average readiness score.
- Risk, status, and provider filters.
- Connector cards.
- Readiness table.
- Connector-generated Useful Signals table.

No live connector button is provided. The page explicitly displays:

- No live connector is connected.
- Design-only readiness simulation.
- No credentials loaded.

## Safety Boundary

HUB-V2-010 does not:

- Read `.env`, tokens, credentials, passwords, API keys, or private outputs.
- Create OAuth flows.
- Call Gmail, Google Sheets, Google Drive, Notion, Airtable, Telegram, GitHub,
  n8n, Make, Zapier, or other provider APIs.
- Send email or Telegram messages.
- Write to Sheets, Drive, Notion, Airtable, GitHub, or automation platforms.
- Run child project scripts.
- Execute real actions.
- Delete files.
- Modify git remotes.
- Run `git push`.
- Write report files to `outputs/private/`.

## Next Stage

Recommended next stage: HUB-V2-011 Report Showcase / Screenshot Refresh.

That stage should still avoid real provider calls unless the user explicitly
requests a separate live connector implementation with credentials, approval
workflow, tests, and rollback controls.
