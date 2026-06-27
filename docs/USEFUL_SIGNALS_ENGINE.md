# Useful Signals Engine

Status: HUB-V2-010-DEMO-WORKFLOW-REPORT-EXPORT-COMPLETE

## Purpose

The Useful Signals Engine turns local AgentHub metadata into ranked decision
signals. It helps the command center answer: what matters now, why it matters,
which Agent it relates to, and what the user can do manually next.

This stage is display-only. It does not execute actions, run child project
scripts, call external connectors, read credentials, or send prompts anywhere.

## Signal Schema

Each signal contains:

- `signal_id`
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
- `why_important`
- `suggested_next_step`
- `score_explanation`
- `execution_policy`

All generated records use
`display_only_text_recommendation_no_execution`.

## Categories

- `project_progress`
- `action_required`
- `business_opportunity`
- `learning_value`
- `portfolio_improvement`
- `connector_readiness`
- `workflow_automation`
- `risk_warning`

## Status Values

- `new`
- `reviewed`
- `needs_action`
- `watchlist`
- `ignored`
- `archived`

## Source Types

- `agent_manifest`
- `project_status`
- `report`
- `manual_demo_data`
- `local_json`
- `local_csv`
- `action_registry`
- `codex_prompt_generator`
- `connector_readiness`
- `workflow_simulation`

## Scoring Rules

`usefulness_score` is calculated as:

`28% relevance + 24% urgency + 24% actionability + 24% value`

Then a visible risk adjustment is applied:

- `risk_warning` signals receive a small risk-awareness bonus.
- High non-warning risk slightly lowers the final score.
- Low or medium risk is tracked without changing the final score.

Display buckets:

- `high_value`: score >= 75 unless classified as needs-action first.
- `needs_action`: status is `needs_action`, or urgency and actionability are
  both high.
- `watchlist`: score >= 55 but not high-value or needs-action.
- `low_priority`: ignored signals or score < 55.

## Demo Signal Set

The local demo dataset includes signals for:

- 11 valid Agent manifests in AgentHubControlCenter V2.
- Codex Prompt Generator handoff speed.
- Useful Signals Engine as the next decision layer.
- Connector readiness staying disconnected.
- VideoExtractSkill as a content extraction input source.
- PersonalKnowledgeAgent as a long-term learning target.
- SocialPainFinderAgent as a business opportunity source.
- BusinessOpsAgent and NextOpsAgent as SME recommendation inputs.
- MarketSenseAgent and NewsSignalAgent as market/news signal sources.
- CareerPilotAgent as a metadata-only career workflow source.
- GitHub screenshot refresh after V2 stabilizes.
- High-risk connector execution requiring explicit approval.
- IdeaScoreAgent as a future project ranking input.
- Social packaging staying low priority unless explicitly requested.
- Connector Readiness Simulator signals for Gmail Send, Google Sheets Read, and
  Telegram Alert.
- Workflow Simulation signals for project review, connector approval gates, and
  Codex handoff.

## UI Behavior

The Useful Signals page shows:

- Total signals.
- High-value signals.
- Needs-action signals.
- Watchlist signals.
- Ignored or low-priority signals.
- Average usefulness score.
- Category, status, source Agent, and minimum-score filters.
- Top 5 Useful Signals.
- Needs Action.
- Watchlist.
- Low Priority / Ignored expander.
- Signal table for scanning.

There are no execution buttons. Recommendations remain copy/read/manual
planning text.

## HUB-V2-008 Connector Signals

HUB-V2-008 adds selected Connector Readiness Simulator outputs as Useful Signal
seeds with `source_type=connector_readiness`.

Examples:

- Gmail Send readiness needs review.
- Google Sheets Read readiness needs review.
- Telegram Alert readiness needs review.

These signals inherit the same display-only policy:
`display_only_text_recommendation_no_execution`.

## HUB-V2-009 Workflow Simulation Signals

HUB-V2-009 adds selected Local Workflow Simulation outputs as Useful Signal
seeds with `source_type=workflow_simulation`.

Examples:

- Project review workflow can summarize next steps across 11 agents.
- Connector approval gates should block Gmail Send and GitHub Push.
- Codex handoff workflow is ready for manual use.

The current local/demo Useful Signal registry contains 20 signals: 14 base demo
signals, 3 connector-generated signals, and 3 workflow-generated signals.

These signals inherit the same display-only policy:
`display_only_text_recommendation_no_execution`.

## HUB-V2-010 Report Export Integration

Demo Workflow Report Export includes Useful Signals summary metrics and the Top
Useful Signals table in Markdown, JSON, and CSV outputs. Signal recommendations
remain display-only text; exporting a signal does not execute the recommended
action or call any connector.

## Safety Boundary

HUB-V2-010 does not:

- Read `.env`, credentials, tokens, passwords, API keys, or private outputs.
- Run child Agent scripts.
- Connect Gmail, Google Sheets, Google Drive, Notion, Airtable, Telegram,
  GitHub, n8n, Make, Zapier, OpenAI, market data, OCR, ASR, or account
  automation.
- Create OAuth flows or call connector provider APIs.
- Execute command templates.
- Execute workflow simulations.
- Treat approval gates as permission to run real actions.
- Delete files.
- Modify git remotes.
- Run `git push`.
- Send prompts or recommendations automatically.
- Write report files to `outputs/private/`.

## Next Stage

Recommended next stage: HUB-V2-011 Report Showcase / Screenshot Refresh.

That stage should remain local/demo metadata-only unless the user explicitly
requests a separate live connector or execution implementation stage.
