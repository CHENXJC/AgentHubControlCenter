# Child Agent Manifest Summary

Status: HUB-V2-005-LOCAL-ACTION-SCHEMA-MANUAL-RUNBOOK-COMPLETE

HUB-V2-003 added manual-reviewable `agent_manifest.json` files to the existing
child Agent and Skill projects under `F:\AIProjects`. HUB-V2-005 upgrades their
`actions` fields to the unified local action schema. These manifests are
metadata only. They do not enable execution, do not connect live accounts, and
do not contain credentials.

## Discovery Result

After the manifests were created, AgentHubControlCenter discovery returned:

| Metric | Result |
| --- | --- |
| Total projects scanned | 11 |
| Manifests found | 11 |
| Valid manifests | 11 |
| Invalid manifests | 0 |
| Missing manifests | 0 |
| Imported agents | 11 |
| Duplicate agent IDs | 9 static registry overrides |

The duplicate IDs are expected because 9 existing portfolio projects already
exist in `data/agent_registry.csv`. Runtime display uses the richer local
manifest data and keeps the CSV registry as the stable baseline.

## Child Manifest Map

| agent_id | Project | Category | Manifest path | Public status | Pin status |
| --- | --- | --- | --- | --- | --- |
| `business_ops_agent` | BusinessOpsAgent | `sme_operations` | `F:\AIProjects\BusinessOpsAgent\agent_manifest.json` | GitHub Public Showcase | Pinned |
| `career_pilot_agent` | CareerPilotAgent | `career_operations` | `F:\AIProjects\CareerPilotAgent\agent_manifest.json` | GitHub Public Showcase | Pinned |
| `idea_score_agent` | IdeaScoreAgent | `idea_validation` | `F:\AIProjects\IdeaScoreAgent\agent_manifest.json` | Local Public Showcase Candidate | Not pinned |
| `market_sense_agent` | MarketSenseAgent | `market_intelligence` | `F:\AIProjects\MarketSenseAgent\agent_manifest.json` | GitHub Public Showcase | Pinned |
| `news_signal_agent` | NewsSignalAgent | `news_intelligence` | `F:\AIProjects\NewsSignalAgent\agent_manifest.json` | GitHub Public Showcase | Pin pending |
| `next_ops_agent` | NextOpsAgent | `sme_operations` | `F:\AIProjects\NextOpsAgent\agent_manifest.json` | GitHub Public Showcase | Not pinned |
| `personal_knowledge_agent` | PersonalKnowledgeAgent | `knowledge_management` | `F:\AIProjects\PersonalKnowledgeAgent\agent_manifest.json` | GitHub Public Showcase | Not pinned |
| `quant_lab_agent` | QuantLabAgent | `quant_research` | `F:\AIProjects\QuantLabAgent\agent_manifest.json` | GitHub Public Showcase | Pinned |
| `social_pain_finder_agent` | SocialPainFinderAgent | `opportunity_discovery` | `F:\AIProjects\SocialPainFinderAgent\agent_manifest.json` | GitHub Public Showcase | Pinned |
| `video_extract_skill` | VideoExtractSkill | `content_intelligence` | `F:\AIProjects\VideoExtractSkill\agent_manifest.json` | GitHub Public Showcase | Pinned |

## HUB-V2-004 Display Review

All 11 Agent cards were reviewed in the V2 UI model.

| Agent | Display category | Source badge | Safety badge | Action display | Connector display | Review result |
| --- | --- | --- | --- | --- | --- | --- |
| AgentHubControlCenter | AgentOps / PortfolioOps | Demo Manifest | Demo Mode / Safe Mode | Display-only / user-started launcher metadata | Local filesystem and GitHub link | Ready |
| BusinessOpsAgent | SME Operations | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / metadata | Local, GitHub, Streamlit, planned Sheets/Airtable | Ready |
| CareerPilotAgent | Career Operations | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, GitHub, Streamlit, optional Gmail, planned Notion | Ready |
| IdeaScoreAgent | Idea Validation | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, Streamlit, planned Notion/Sheets | Ready |
| MarketSenseAgent | Market Intelligence | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, GitHub, Streamlit, optional Telegram/market data | Ready |
| NewsSignalAgent | News Intelligence | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, GitHub, Streamlit, optional RSS/news API, planned Sheets | Ready |
| NextOpsAgent | SME Operations | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, GitHub, Streamlit, optional Airtable, planned Notion | Ready |
| PersonalKnowledgeAgent | Knowledge Management | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, GitHub, Streamlit, optional Notion, planned local vector store | Ready |
| QuantLabAgent | Quant Research | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, GitHub, Streamlit, optional market data, planned Sheets | Ready |
| SocialPainFinderAgent | Opportunity Discovery | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, GitHub, Streamlit, optional social API, planned Airtable | Ready |
| VideoExtractSkill | Content Intelligence | Local Manifest | Demo Mode / Safe Mode | Display-only / manual / demo | Local, GitHub, Streamlit, optional local OCR/ASR | Ready |

Review notes:

- Category values remain stable in manifest files and display as readable labels
  in the UI.
- Actions remain display-only, manual, demo, or metadata-only.
- Connectors remain local, link-based, planned, optional, manual, or
  not-connected.
- No Agent card claims that Gmail, Google Sheets, Notion, Airtable, Telegram,
  social APIs, market data providers, OCR, ASR, or execution connectors are
  actively connected by AgentHub.
- `demo_mode` and `safe_mode` are true for all 11 visible Agents.

## Action Policy

All child manifest actions are declared as display-only, manual-only,
template-only, or report-view actions. They are intended for the Action Center
preview layer only.

Examples include:

- `manual_run_dashboard`
- `open_project_folder`
- `view_agent_manifest`
- `view_latest_report`
- `export_summary`
- `view_project_status`
- `generate_codex_prompt`

AgentHubControlCenter does not execute these actions in HUB-V2-005.

## HUB-V2-005 Action Schema Result

| Metric | Result |
| --- | --- |
| Total actions | 55 |
| Manual-only actions | 17 |
| Display-only actions | 30 |
| Future connector actions | 0 |
| Requires approval | 0 |
| Blocked actions | 0 |
| Policy violations | 0 |

Each of the 11 visible Agents declares 5 safe actions with `action_id`,
`label`, `description`, `action_type`, `execution_mode`, `risk_level`,
`requires_approval`, `command_template`, `runbook_ref`, `expected_output`,
`safety_note`, `connector_required`, and `status`.

## Connector Policy

Connectors are declared as local, link-based, planned, optional, or manual only.

Allowed now:

- Local project file references for manifest metadata.
- GitHub showcase links when already public.
- Streamlit local dashboard launch commands as display-only commands.

Not enabled:

- Gmail
- Google Sheets
- Notion
- Airtable
- Telegram
- Social platform APIs
- Market data providers
- Any connector that requires secrets or account access

## Next Recommended Stage

HUB-V2-006 should build a Codex Prompt Generator on top of the reserved
`codex_prompt` action type while keeping output template-only.
