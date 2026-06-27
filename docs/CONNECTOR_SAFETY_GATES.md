# Connector Safety Gates

Status: HUB-V2-009-LOCAL-WORKFLOW-SIMULATION-APPROVAL-GATES-COMPLETE

## Purpose

This document defines the safety gates required before AgentHubControlCenter can
move from connector readiness simulation to any future connector implementation.

HUB-V2-009 does not implement live connectors. It displays readiness metadata,
connector-generated Useful Signals, workflow simulation records, and approval
gate planning.

## Global Gates

Before any connector can move beyond design-only review, it needs:

- Explicit user approval for the connector class.
- Clear provider permission scope.
- Read-only mode where possible.
- Local fixture or demo-mode test data.
- No credential printing.
- No `.env` reading unless the user explicitly starts a separate credentialed
  connector stage.
- Rollback plan.
- Test plan.
- Dry-run or preview mode.
- Visible audit notes.
- Manual disable path.

## Blocked Until Approved

These connector classes stay blocked until a separate approved stage:

- Gmail Send
- Gmail Draft Creation
- Google Sheets Write
- Google Drive Write
- Notion Database Write
- Airtable CRM Sync
- Telegram Alert live send
- GitHub Push / Release
- n8n Webhook POST
- Make Scenario trigger
- Zapier Zap trigger

## Safer First Candidates

Lower-risk candidates for a future demo stage:

- GitHub Status Read with public metadata only.
- Google Sheets Read through a local CSV mirror first.
- Gmail Read Review through synthetic fixtures before any mailbox access.

Even these safer candidates remain `not_connected` in HUB-V2-009.

## Provider-Specific Gates

Gmail:

- Read-only scope before compose or send.
- Synthetic mailbox fixtures first.
- No send endpoint in tests.
- Manual approval before any draft or send workflow.

Google Sheets / Drive:

- Read-only scope first.
- Local CSV or document fixtures.
- Sheet/file allowlist.
- Write preview before any write-capable connector.

Notion / Airtable:

- Database/base allowlist.
- Local Markdown or CSV export first.
- Dry-run diff before writes.
- Manual approval before create/update actions.

Telegram:

- Local alert preview first.
- Fake chat ID fixtures.
- No bot token loading in readiness stage.
- Manual approval before live send.

GitHub:

- Public metadata read only for first demo.
- No git push from AgentHub UI.
- No remote mutation.
- Releases and pushes remain blocked until a separate explicit stage.

n8n / Make / Zapier:

- Local JSON payload preview first.
- Webhook URL allowlist.
- No automatic HTTP POST in readiness stage.
- Manual trigger approval before any future live workflow.

## Never Allowed In HUB-V2-009

- OAuth creation.
- Provider API calls.
- Reading or printing secrets.
- Sending messages.
- Writing external data.
- Running child project scripts.
- Executing connector actions.
- Modifying git remotes.
- Running `git push`.

HUB-V2-009 also shows Gmail Send and GitHub Push / Release as blocked Approval
Gates in the My Workflows page.

## Completion Rule

A connector can only be considered for future implementation when the readiness
record has complete permissions, rollback plan, test plan, safety gates,
approval requirement, and a clear reason why a live connector is needed.
