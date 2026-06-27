# Manual Runbook

Status: HUB-V2-009-LOCAL-WORKFLOW-SIMULATION-APPROVAL-GATES-COMPLETE

This runbook explains how to use AgentHubControlCenter actions safely by hand.
HUB-V2-009 actions are not executable buttons. They are metadata cards,
instructions, command templates, local links, report views, Codex prompt text
templates, useful signal recommendations, connector readiness simulations,
local workflow simulations, approval gates, or future connector placeholders.

## Global Manual Use Rules

1. Open AgentHubControlCenter locally from `F:\AIProjects\AgentHubControlCenter`.
2. Review the Action Center card for the target Agent.
3. Read the action type, execution mode, risk level, approval flag, expected
   output, and safety note.
4. Copy command templates only if you intentionally want to run them yourself in
   PowerShell or CMD.
5. Do not paste or run any command that would read credentials, delete files,
   push to GitHub, change git remotes, send messages, send emails, or connect
   live accounts.

## Common Safe Actions

| Action | Manual meaning | Safety boundary |
| --- | --- | --- |
| `view_project_status` | Read the project checkpoint and validation history. | Display/report view only. |
| `view_agent_manifest` | Inspect the Agent manifest metadata. | Reads manifest metadata only. |
| `open_project_folder` | Open the local project folder manually. | AgentHub only shows the instruction/template. |
| `manual_run_dashboard` | Start the Agent dashboard by hand if needed. | Command template only; AgentHub does not launch it. |
| `view_latest_report` | Review a public-safe demo/sample report manually. | No private output is opened by AgentHub. |
| `export_summary` | Use the Agent UI or copied command template to export manually. | Template only; user decides whether to run it. |
| `generate_codex_prompt` | Generate copy-ready Codex task prompt text. | Template only; no prompt is auto-sent and no project code runs. |

## Codex Prompt Generator Manual Use

1. Open the Action Center.
2. Find the `Codex Prompt Generator` section.
3. Select the target Agent.
4. Select a prompt type such as `continue_next_stage`, `fix_or_polish`, or
   `github_showcase_update`.
5. Review the selected Agent context, available actions, safety checklist, and
   validation checklist.
6. Copy the generated prompt manually if you want to use it in Codex.
7. Do not treat the generated prompt as an execution button. AgentHub does not
   send it anywhere automatically.

## Useful Signals Manual Use

1. Open the Useful Signals tab.
2. Review Signal Metrics, Top 5 Useful Signals, Needs Action, Watchlist, and Low
   Priority / Ignored sections.
3. Use category, status, source Agent, and minimum-score filters to narrow the
   view.
4. Read the score components, why-important text, recommended action, related
   Agent, and execution policy.
5. Treat every recommendation as planning text only. Do not assume AgentHub has
   performed the suggested action.

## Connector Readiness Simulator Manual Use

1. Open the Connectors tab.
2. Review the Connector Readiness Simulator metrics.
3. Use risk, readiness status, and provider filters to inspect future connector
   candidates.
4. Read required permissions, approval requirement, safety gates, rollback plan,
   test plan, readiness score, and recommended next step.
5. Treat every connector card as design-only metadata. AgentHub does not create
   OAuth, load credentials, call provider APIs, trigger webhooks, send messages,
   write external records, or connect live accounts.

## Local Workflow Simulation Manual Use

1. Open the My Workflows tab.
2. Review the Local Workflow Simulation metrics.
3. Confirm the page states: Local simulation only, No live connector, No real
   action execution, No credentials loaded.
4. Review each workflow card: input source, connected Agents, signals used,
   recommended actions, approval gate result, blocked steps, generated outputs,
   and next recommended step.
5. Review the Approval Gates table before treating any recommendation as a
   manual next step.
6. Keep blocked gates blocked. In HUB-V2-009, Gmail Send and GitHub Push /
   Release are not executable.
7. Use workflow-generated Useful Signals as planning notes only.

## Agent Action Overview

| Agent | HUB-V2-005 actions |
| --- | --- |
| AgentHubControlCenter | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `manual_run_dashboard`, `generate_codex_prompt` |
| BusinessOpsAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `manual_run_dashboard`, `export_summary` |
| CareerPilotAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `manual_run_dashboard`, `generate_codex_prompt` |
| IdeaScoreAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `view_latest_report`, `export_summary` |
| MarketSenseAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `view_latest_report`, `manual_run_dashboard` |
| NewsSignalAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `view_latest_report`, `generate_codex_prompt` |
| NextOpsAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `view_latest_report`, `generate_codex_prompt` |
| PersonalKnowledgeAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `view_latest_report`, `export_summary` |
| QuantLabAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `view_latest_report`, `manual_run_dashboard` |
| SocialPainFinderAgent | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `view_latest_report`, `export_summary` |
| VideoExtractSkill | `view_project_status`, `view_agent_manifest`, `open_project_folder`, `view_latest_report`, `manual_run_dashboard` |

## Agent-Specific Notes

- AgentHubControlCenter: use the local launcher on fixed port `8525`; do not use
  AgentHub to execute child project actions.
- MarketSenseAgent and QuantLabAgent: keep all market and backtesting workflows
  educational, local, and non-trading.
- CareerPilotAgent: Gmail or job-platform integrations remain optional future
  connectors only.
- BusinessOpsAgent, NextOpsAgent, SocialPainFinderAgent, and IdeaScoreAgent:
  use demo/public-safe business data only.
- PersonalKnowledgeAgent: do not ingest private notes or documents into a public
  showcase flow.
- NewsSignalAgent: use public-safe news samples and do not connect paid or live
  news APIs from AgentHub.
- VideoExtractSkill: local OCR/ASR remains manual or optional local tooling; no
  private media should be exposed in public screenshots.

## Runbook Reference Format

Action cards use references like:

```text
docs/MANUAL_RUNBOOK.md#agent-id-action-id
```

The reference identifies the Agent and action in this runbook. It is a human
review pointer, not a runtime route.
