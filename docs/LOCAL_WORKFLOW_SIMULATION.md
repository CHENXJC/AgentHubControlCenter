# Local Workflow Simulation

Status: HUB-V2-010-DEMO-WORKFLOW-REPORT-EXPORT-COMPLETE

## Purpose

HUB-V2-009 adds local workflow simulation for AgentHubControlCenter. It shows how
existing metadata layers can be chained into a safe planning workflow:

Input signal -> Useful Signals scoring -> recommended action -> Approval Gate
decision -> Manual Runbook / Codex Prompt / Summary Report output.

This stage is simulation-only. It does not run child Agent scripts, does not
connect live accounts, does not load credentials, and does not execute real
actions.

## Workflow Schema

Each workflow includes:

- `workflow_id`
- `workflow_name`
- `workflow_type`
- `input_source`
- `source_agents`
- `signals_used`
- `recommended_actions`
- `approval_gates`
- `blocked_steps`
- `manual_steps`
- `generated_outputs`
- `risk_summary`
- `next_recommended_step`
- `execution_policy`

The execution policy is always:

`local_simulation_only_no_live_connector_no_real_action_no_credentials`

## Demo Workflows

HUB-V2-009 includes four demo workflows:

| Workflow | Purpose | Result |
| --- | --- | --- |
| Project Progress Review Workflow | Summarize next steps across 11 Agents. | Display-only project review. |
| Useful Signals Review Workflow | Review top/needs-action/watchlist signals. | Manual review only. |
| Connector Readiness Review Workflow | Evaluate connector readiness and blocked connector steps. | Blocks Gmail Send and GitHub Push / Release. |
| Codex Handoff Workflow | Generate copy-ready handoff prompt text. | Template-only manual use. |

## Readiness Score Rules

Workflow readiness score increases when a workflow has:

- declared source Agents
- useful signals
- recommended actions
- manual steps
- generated outputs
- valid approval gates

The score decreases for blocked gates, high-risk gates, and blocked workflow
steps. The score does not mean execution is enabled.

## Workflow-Generated Useful Signals

The workflow simulator emits selected Useful Signal seeds, including:

- Project review workflow can summarize next steps across 11 agents.
- Connector approval gates should block Gmail Send and GitHub Push.
- Codex handoff workflow is ready for manual use.

These signals use `source_type=workflow_simulation` and remain display-only text
recommendations.

## UI Behavior

The My Workflows page shows:

- Total demo workflows
- Workflows ready for manual review
- Blocked steps
- Manual-only steps
- Template-only outputs
- Approval gates required
- Average workflow readiness score
- Workflow simulation cards
- Approval Gates table
- Workflow-generated Useful Signals table
- Demo Workflow Report Export previews and downloads

No workflow card includes an execution button.

## HUB-V2-010 Report Export Integration

HUB-V2-010 exports workflow simulation results into public-safe Markdown, JSON,
and CSV report text. The export includes workflow summary metrics, workflow
cards, approval gate status, useful signal recommendations, connector readiness,
and a validation snapshot.

Report export does not change the workflow execution policy:

`local_simulation_only_no_live_connector_no_real_action_no_credentials`

The exporter may write local files only under `outputs/public_reports/` and must
not write `outputs/private/`.

## Safety Boundary

HUB-V2-010 does not:

- read `.env`
- print secrets, tokens, passwords, or API keys
- create OAuth flows
- call external APIs
- connect Gmail, Google Sheets, Notion, Airtable, Telegram, GitHub, n8n, Make,
  Zapier, or other live providers
- run child project scripts
- execute real actions
- modify git remote
- run `git push`
- write `outputs/private/`

All workflow simulation outputs are metadata, manual instruction, summary text,
public-safe report text, or future planning notes.
