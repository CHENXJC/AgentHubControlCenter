# Chinese UI Coverage Checklist

Checkpoint:
`HUB-V2-024-DEEP-CHINESE-UI-COVERAGE-CHECK-COMPLETE`

## Purpose

This checklist records the deep Chinese UI coverage rules for
AgentHubControlCenter. The goal is to make Chinese mode usable as the default
local working interface without changing internal metadata, action schemas,
connector IDs, repository names, or public GitHub traceability.

This stage is display-only. It does not execute actions, run command
templates, connect live providers, create OAuth flows, call external APIs, run
child project scripts, modify git remotes, commit, or push.

## Display Translation Helpers

`agent_hub/ui_i18n.py` provides display-layer helpers for:

| Helper | UI responsibility |
| --- | --- |
| `translate_category` | Category badges, filters, matrix cards, and registry rows |
| `translate_status` | Product status, health status, readiness status, action status, and connector status |
| `translate_badge` | Manifest/source/safe-mode badges |
| `translate_action_label` | Action card titles, command labels, and action tables |
| `translate_connector` | Connector labels, provider names, and connector lists |
| `translate_next_step` | Next recommended actions and safe next-step text |
| `translate_filter_option` | Sidebar and page filter option labels |
| `translate_agent_display_name` | User-facing Agent names in Chinese mode |
| `translate_agent_description` | Agent card descriptions and registry detail descriptions |
| `translate_column_label` | Dataframe/table column headers |
| `display_text` | Generic display copy and phrase translation fallback |

## Chinese-Mode Coverage

| UI area | Required Chinese coverage | Status |
| --- | --- | --- |
| Sidebar | Language, product status, checkpoint labels, registry filters | Complete |
| Hero / Command Overview | Product posture, metrics, portfolio summary, capability summaries | Complete |
| Agent cards | Agent display name, description, category, status, source, actions, connectors, next step | Complete |
| My Tools / Registry | Table column labels, filter options, status values, health details, validation messages | Complete |
| Useful Signals | Signal category, status, source type, why-important copy, next action, policy text | Complete |
| My Workflows | Workflow cards, approval gate labels, workflow statuses, generated outputs, next steps | Complete |
| Action Center | Action labels, type, execution mode, risk, approval, status, expected output, safety note | Complete |
| Codex Prompt Generator | Agent selector labels, prompt action table, safety checklist, validation checklist | Complete |
| Connectors | Connector label, purpose, provider, status, permissions, safety gates, rollback/test plan | Complete |
| Future Plugin Interface | Onboarding metrics, manifest tables, policy cards, roadmap rows, report preview text | Complete |
| Portfolio Matrix | Category labels, Agent display names, status summary, next notes, roles | Complete |
| Local report preview | Visible preview text in the app display layer | Complete |

## Proper Nouns And Internal Values To Preserve

These values should remain English or internal-form in both languages:

- Repository names, such as `AgentHubControlCenter` and `ClientDeliveryKitAgent`
- GitHub URLs and repo owner/name strings
- Local paths, such as `F:\AIProjects\AgentHubControlCenter`
- `agent_id`, `action_id`, `connector_id`, and schema enum names where shown as
  technical fields
- JSON keys, Python variable names, module names, and file names
- Command templates, because they are copy/display text and must remain exact
- Checkpoint names, because they are audit identifiers

## Residual English Checks

Chinese mode should not show these English dynamic labels in primary UI cards or
filters:

- `Local Manifest`
- `Demo Mode / Safe Mode`
- `No immediate action`
- `View project status`
- `Showcase Ready`
- `AgentOps / PortfolioOps`
- `Business Ops Agent`

English mode should still show the English equivalents for public review.

## Safety Checklist

- `.env` is not read.
- No secret, token, password, API key, or credential is output.
- No OAuth or external connector is created.
- No Gmail, Google Sheets, Notion, Airtable, Telegram, GitHub connector, n8n,
  Make, or Zapier account is connected.
- No child project script is run.
- No real Agent action is executed.
- No command template is executed.
- No generated prompt is sent automatically to Codex.
- No git remote is modified.
- No git push or force push is performed.
- No generated private report is written.
