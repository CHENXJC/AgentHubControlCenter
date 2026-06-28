# Cross-Project Backlink Plan

Checkpoint:
`HUB-V2-016-CROSS-PROJECT-BACKLINK-PLAN-COMPLETE`

## Goal

Connect the completed AI Agent and Skill projects back to
AgentHubControlCenter with lightweight README backlinks. The goal is portfolio
navigation and positioning only: each vertical project keeps its original
scope, while AgentHubControlCenter becomes the visible command center for the
overall local-first AI Agent matrix.

## Target Projects

| Project | Role In AgentHubControlCenter |
| --- | --- |
| BusinessOpsAgent | SME operations module |
| CareerPilotAgent | Career operations module |
| IdeaScoreAgent | Idea validation module |
| MarketSenseAgent | Market intelligence module |
| NewsSignalAgent | News intelligence module |
| NextOpsAgent | SME next-action recommendation module |
| PersonalKnowledgeAgent | Knowledge management module |
| QuantLabAgent | Quant research module |
| SocialPainFinderAgent | Opportunity discovery module |
| VideoExtractSkill | Content intelligence module |

## Standard Backlink Template

```markdown
## Managed through AgentHubControlCenter

This project is part of my local-first AI Agent portfolio and can be managed through [AgentHubControlCenter](https://github.com/CHENXJC/AgentHubControlCenter), the central command center for agent manifests, safe actions, useful signals, workflow simulations, connector readiness, approval gates, and public-safe reporting.

<ProjectName> is registered as a <module role> module in AgentHubControlCenter.
```

If a README already has an AgentHub / portfolio / related-projects section, the
backlink should be merged into that existing section instead of creating a
duplicate heading.

## Per-Project Wording

| Project | Wording |
| --- | --- |
| BusinessOpsAgent | BusinessOpsAgent is registered as an SME operations module in AgentHubControlCenter. |
| CareerPilotAgent | CareerPilotAgent is registered as a career operations module in AgentHubControlCenter. |
| IdeaScoreAgent | IdeaScoreAgent is registered as an idea validation module in AgentHubControlCenter. |
| MarketSenseAgent | MarketSenseAgent is registered as a market intelligence module in AgentHubControlCenter. |
| NewsSignalAgent | NewsSignalAgent is registered as a news intelligence module in AgentHubControlCenter. |
| NextOpsAgent | NextOpsAgent is registered as an SME next-action recommendation module in AgentHubControlCenter. |
| PersonalKnowledgeAgent | PersonalKnowledgeAgent is registered as a knowledge management module in AgentHubControlCenter. |
| QuantLabAgent | QuantLabAgent is registered as a quant research module in AgentHubControlCenter. |
| SocialPainFinderAgent | SocialPainFinderAgent is registered as an opportunity discovery module in AgentHubControlCenter. |
| VideoExtractSkill | VideoExtractSkill is registered as a content intelligence module in AgentHubControlCenter. |

## Safety Boundary

- Do not read `.env`, credentials, tokens, passwords, API keys, private exports,
  databases, or `outputs/private/`.
- Do not modify child project code.
- Do not run child project scripts.
- Do not connect Gmail, Google Sheets, Notion, Airtable, Telegram, GitHub
  connector, n8n, Make, Zapier, or any other live provider.
- Do not execute real actions.
- Do not modify git remotes.
- Do not run `git add`, commit, push, or force push in this stage.
- Do not stage generated reports or local private outputs.

## Non-Feature Scope

This stage does not change any Agent capability. The backlinks are navigation
and portfolio-positioning metadata only. They do not imply live integration,
automatic execution, connector authorization, account access, or child project
orchestration.

## Follow-Up Commit / Push Recommendation

Recommended follow-up stage:
`HUB-V2-017-CROSS-PROJECT-BACKLINK-COMMIT-DECISION`

If the user approves, commit the README backlink changes separately per git
repository using explicit file paths only. Do not use `git add .`. Do not push
non-git folders. Do not modify remotes or force push.
