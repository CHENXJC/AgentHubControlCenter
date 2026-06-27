# Action Safety Policy

Status: HUB-V2-010-DEMO-WORKFLOW-REPORT-EXPORT-COMPLETE

This policy defines what AgentHubControlCenter may and may not do with local
actions, useful signal recommendations, connector readiness metadata, workflow
simulation metadata, approval gates, and demo workflow report exports in
HUB-V2-010.

## Allowed In HUB-V2-010

- Display Agent action metadata.
- Display manual runbook instructions.
- Display local command templates as text.
- Display local folder or GitHub link guidance.
- Display report-view references.
- Generate and display copy-ready Codex prompt text.
- Display future connector placeholders.
- Validate action schema fields and show safety metrics.
- Generate and display Useful Signals as scored recommendation text.
- Generate and display connector readiness metadata as design-only simulation.
- Generate and display local workflow simulation metadata.
- Generate and display approval gates with display/manual/template/dry-run or
  blocked modes.
- Generate public-safe Markdown, JSON, and CSV report text from local/demo
  metadata.
- Download generated prompt text as a local text file if the user clicks the
  download control.
- Download generated report text if the user clicks the report download
  controls.
- Write report files only under `outputs/public_reports/` when local file export
  is explicitly used.

## Not Allowed In HUB-V2-010

- Execute child project scripts.
- Execute command templates from Streamlit.
- Auto-send generated prompts to Codex or any other tool.
- Auto-run Useful Signals recommendations.
- Auto-run connector recommendations.
- Auto-run workflow recommendations.
- Treat Approval Gates as permission to execute real actions.
- Read `.env`, tokens, passwords, API keys, credentials, or private databases.
- Create OAuth flows.
- Call provider APIs.
- Trigger webhooks.
- Send email, Telegram messages, social posts, or account messages.
- Connect real Gmail, Google Sheets, Google Drive, Notion, Airtable, Telegram,
  GitHub, n8n, Make, Zapier, market-data, social, OCR, ASR, or other live
  account connectors.
- Delete user files.
- Modify git remotes.
- Run `git push` or force push.
- Add `.venv` to git.
- Publish private outputs or generated reports.
- Write report files to `outputs/private/`.

## Approval Policy

Low-risk display, report, local-link, manual-instruction, command-template, and
Codex-prompt actions can be shown without approval because they are not
executed by AgentHub.

Medium-risk future connector placeholders and readiness records should be
treated as design-only until a later connector stage adds separate approval,
configuration, and tests.

High-risk or blocked actions must set `requires_approval=true` and must not be
executable from AgentHub.

## Blocked Action Classes

The following classes are blocked in HUB-V2-010:

- `send_email`
- `delete_files`
- `modify_git_remote`
- `git_push`
- `connect_real_gmail`
- `connect_real_sheets`
- `run_external_script`
- `create_oauth_flow`
- `trigger_webhook`
- `connect_real_drive`
- `connect_real_notion`
- `connect_real_airtable`
- `connect_real_telegram`
- `live_execute`
- `auto_execute`

## Future Execution Gate

Before any future execution stage, AgentHubControlCenter would need a separate
checkpoint with explicit user approval, action routing tests, connector
configuration docs, secret-safe handling, clear logs, and a disable/rollback
path. HUB-V2-010 does not implement that execution gate; it only adds text
prompt generation, display-only signal recommendations, design-only connector
readiness simulation, local workflow simulation, approval gate planning, and
public-safe demo report export.
