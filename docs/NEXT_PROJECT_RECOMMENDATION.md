# Next Project Recommendation

Checkpoint:
`HUB-V2-020-PROJECT-PAUSE-AND-NEXT-PORTFOLIO-GAP-DECISION-COMPLETE`

## Recommended Project Name

Recommended project: `ClientDeliveryKitAgent`

## Project Positioning

ClientDeliveryKitAgent is a local-first AI automation consultant kit for turning
an SME workflow intake into a structured automation diagnosis, useful signals,
recommended next actions, and a client-ready report.

It should demonstrate the user's positioning as a business-aware AI automation
builder rather than only a tool maker.

## Target User

Primary target:

- Solo operators, small business owners, and service businesses that have messy
  repeatable workflows but do not know what to automate first.

Portfolio target:

- Recruiters, collaborators, and potential clients who need to see that the
  user can translate business problems into AI workflow deliverables.

## MVP Scope

The MVP should include:

- Public-safe synthetic client intake examples.
- Workflow pain-point capture.
- Automation opportunity scoring.
- Useful signal filtering.
- Recommended next-action output.
- Risk and approval notes.
- Public-safe Markdown report export.
- Streamlit dashboard with intake, scoring, recommendation, and report views.
- `agent_manifest.json` compatible with AgentHubControlCenter.

The MVP should not include:

- Real client data.
- Live Gmail, Google Sheets, Notion, Airtable, or CRM connection.
- OAuth.
- Automatic sending, writing, deleting, or external workflow execution.
- Paid API dependency.
- Full CRM or project management system scope.

## Integration With AgentHubControlCenter

AgentHub integration should be metadata-first:

- Add a standard manifest after the MVP exists.
- Register safe local actions only.
- Add Useful Signals for report readiness, high-ROI workflow gaps, blocked
  approvals, and missing inputs.
- Add Connector Readiness records for future Gmail, Google Sheets, Notion,
  Airtable, and CRM connectors.
- Add Local Workflow Simulation records for intake-to-report flow.
- Add report export metadata so AgentHub can show the project as a governed
  spoke.

AgentHub should not execute the project automatically.

## Suggested Folder Path

Suggested local folder:

`F:\AIProjects\ClientDeliveryKitAgent`

## Suggested Interfaces

### Connector Interfaces

Keep these as future planned connectors:

- Google Sheets: intake table import.
- Gmail: client intake email review.
- Notion: delivery workspace export.
- Airtable: workflow opportunity database.
- CRM: future contact and deal context.

### Workflow Interfaces

Recommended workflow stages:

1. Intake review.
2. Pain-point extraction.
3. Automation opportunity scoring.
4. Useful signal filtering.
5. Recommendation generation.
6. Approval and risk review.
7. Client-ready report export.

### Useful Signals

Suggested signal types:

- High ROI automation opportunity.
- Repeated manual work.
- Missing input or stakeholder context.
- Approval required before connector use.
- Report ready for client review.
- Scope too broad for MVP.

### Report Export

The MVP report should include:

- Client profile summary.
- Workflow pain points.
- Automation opportunity table.
- Priority recommendations.
- Risks and approval gates.
- Suggested implementation roadmap.
- Public-safe disclaimer.

## Suggested Milestones

1. `CDK-001-PLANNING`: define positioning, scope, data model, and public-safe
   demo boundary.
2. `CDK-002-CORE-SCORING`: build synthetic intake parser and scoring engine.
3. `CDK-003-STREAMLIT-MVP`: create dashboard views for intake, scoring,
   recommendations, and report preview.
4. `CDK-004-REPORT-EXPORT`: add Markdown report export and sample demo report.
5. `CDK-005-AGENTHUB-MANIFEST`: add standard manifest and safe actions.
6. `CDK-006-DOCS-TESTS-SAFETY`: add tests, README, screenshots guide, and
   safety docs.
7. `CDK-007-GITHUB-SHOWCASE`: prepare public showcase and optional AgentHub
   backlink.

## Suggested Codex Starting Prompt Outline

Use this when starting the new project in a separate stage:

```text
Create a new local-first project at F:\AIProjects\ClientDeliveryKitAgent.

Project goal:
Build a public-safe AI automation consultant kit that turns synthetic SME
workflow intake data into pain-point analysis, automation opportunity scoring,
useful signals, recommendations, and a client-ready Markdown report.

Read first:
- PROJECT_STATUS.md if it exists
- README.md if it exists
- AgentHubControlCenter docs/NEXT_PROJECT_RECOMMENDATION.md
- AgentHubControlCenter docs/NEXT_PORTFOLIO_GAP_ANALYSIS.md

Safety requirements:
- Do not read .env
- Do not output secrets, tokens, passwords, API keys, or credentials
- Do not connect live Gmail, Google Sheets, Notion, Airtable, CRM, or other
  connectors
- Do not run external scripts
- Do not delete user files
- Do not modify git remotes
- Do not git push unless explicitly requested later
- Use synthetic demo data only

MVP goals:
- Define intake data schema
- Build opportunity scoring
- Build useful signal filtering
- Build recommendation output
- Build Streamlit dashboard
- Build Markdown report export
- Add tests and public-safe docs

Validation:
- python -m pytest
- python -m compileall .
- Streamlit smoke check when UI exists
- public-safe scan for generated docs and demo data
```

## Final Recommendation

Start `ClientDeliveryKitAgent` next, not another AgentHub feature stage.

AgentHub should remain the portfolio command center. ClientDeliveryKitAgent
should become the next spoke that demonstrates client-facing AI automation
delivery.
