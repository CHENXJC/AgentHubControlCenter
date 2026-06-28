# Next Portfolio Gap Analysis

Checkpoint:
`HUB-V2-020-PROJECT-PAUSE-AND-NEXT-PORTFOLIO-GAP-DECISION-COMPLETE`

## Current Portfolio Map

| Project | Capability covered | Current portfolio role | Status |
| --- | --- | --- | --- |
| AgentHubControlCenter | AgentHub / AgentOps | Main hub, registry, signals, actions, workflows, connector readiness | Showcase hub complete |
| BusinessOpsAgent | Business operations | SME workflow and operational analysis example | Complete |
| CareerPilotAgent | Career operations | Job and career planning workflow example | Complete |
| IdeaScoreAgent | Idea validation | Business idea scoring and validation example | Complete |
| MarketSenseAgent | Market intelligence | Market monitoring and local automation example | Complete, local-only folder |
| NewsSignalAgent | News intelligence | News signal analysis example | Complete |
| NextOpsAgent | SME next actions | Operational next-step recommendation example | Complete |
| PersonalKnowledgeAgent | Knowledge management | Personal knowledge workflow example | Complete |
| QuantLabAgent | Quant research | Research, backtesting, and risk-analysis example | Complete |
| SocialPainFinderAgent | Opportunity discovery | Pain-point and opportunity discovery example | Complete |
| VideoExtractSkill | Content extraction | Video/image content extraction example | Complete, local-only folder |

## Covered Capabilities

The current matrix already covers a broad local-first AI Agent portfolio:

- AgentHub / AgentOps command center.
- Business operations and SME workflow reasoning.
- Career operations.
- Idea validation.
- Market intelligence.
- News intelligence.
- Knowledge management.
- Quant research.
- Opportunity discovery.
- Content extraction.

This is enough to show breadth. The next gap is not another hub page. The next
gap is a stronger end-to-end business delivery spoke.

## Missing Capabilities

Current gaps:

- Client-facing delivery workflow: discovery, diagnosis, recommendation,
  proposal, and implementation plan in one package.
- Before/after automation case study format that a consultant can show to a
  small business.
- Structured business intake to workflow map conversion.
- Public-safe client demo mode with synthetic example briefs.
- Practical recommendation output that feels close to a real paid service.
- A standalone spoke that proves AgentHub can govern future workflow projects
  instead of only cataloging older ones.

## Gap Scoring Table

Scoring uses 1-10 where higher is better. For `risk / complexity`, 10 means
lower and more manageable risk.

| Candidate | Portfolio value | Business/commercial value | Job-search value | Technical depth | AgentHub connection | Risk / complexity | Time-to-demo | Differentiation | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Live Connector Pilot | 7 | 8 | 7 | 8 | 10 | 3 | 4 | 7 | 54 |
| Client Delivery Kit Agent | 10 | 10 | 9 | 7 | 9 | 8 | 8 | 9 | 70 |
| StudyOps / Monash Business Learning Agent | 7 | 6 | 8 | 6 | 7 | 8 | 8 | 7 | 57 |
| Career Application Ops Agent V2 | 6 | 5 | 10 | 6 | 7 | 8 | 8 | 5 | 55 |
| SME Automation Demo Kit | 9 | 9 | 8 | 7 | 10 | 7 | 8 | 8 | 66 |
| Data-to-Insight Workflow Agent | 9 | 8 | 8 | 9 | 8 | 7 | 7 | 8 | 64 |

## Candidate Notes

### Live Connector Pilot

Strong connection to AgentHub, but it introduces provider accounts, OAuth,
permission design, and higher safety overhead. It should wait until a new spoke
project proves a specific connector need.

### Client Delivery Kit Agent

Best next step for an AI automation consultant positioning. It turns a business
problem intake into a structured workflow audit, opportunity score, automation
recommendation, proposal outline, and client-ready report.

### StudyOps / Monash Business Learning Agent

Useful for the user's personal background and study workflow, but less directly
commercial than a client-delivery project. It is a good later project if the
portfolio needs a student productivity angle.

### Career Application Ops Agent V2

High job-search relevance, but it overlaps with CareerPilotAgent. It should be
deferred unless the user's immediate priority becomes job applications.

### SME Automation Demo Kit

Strong portfolio value and strong AgentHub connection. It is a good second
choice, but it is broader than Client Delivery Kit Agent and could become a
collection of demos without a clear deliverable.

### Data-to-Insight Workflow Agent

Strong technical depth and broadly useful. It is a good third choice, especially
if the next goal is to show data processing, scoring, analysis, and reporting.
It is less directly tied to consultant delivery than Client Delivery Kit Agent.

## Top 3 Next Project Candidates

1. Client Delivery Kit Agent.
2. SME Automation Demo Kit.
3. Data-to-Insight Workflow Agent.

## Recommended Next Project

Recommended next project: `ClientDeliveryKitAgent`

One-line positioning:

`ClientDeliveryKitAgent is a local-first AI automation consultant kit that turns
an SME workflow intake into a public-safe automation diagnosis, useful signals,
recommended next actions, and a client-ready delivery report.`

## Why This Beats More AgentHub Work

AgentHub already proves command center thinking. The portfolio now needs a
client-facing spoke that proves the user can package AI automation into a
business deliverable.

ClientDeliveryKitAgent adds a new capability layer:

- Consultant-style intake.
- Workflow diagnosis.
- Opportunity scoring.
- Recommended automation roadmap.
- Report export.
- Future connector planning.

That is more useful than another AgentHub surface because it creates a new
public project with commercial framing.

## How It Connects To AgentHubControlCenter

ClientDeliveryKitAgent should connect to AgentHub through:

- A standard `agent_manifest.json`.
- Safe actions such as `view_project_status`, `view_agent_manifest`,
  `manual_run_dashboard`, `generate_codex_prompt`, and `export_summary`.
- Useful Signals such as high-ROI automation opportunity, missing stakeholder
  inputs, approval needed, and report-ready status.
- Connector readiness records for Google Sheets, Gmail, Notion, and Airtable as
  future planned connectors only.
- Local workflow simulation records for intake, scoring, recommendation, and
  report export.

## Risks And Trade-Offs

- Avoid using real client data in the showcase version.
- Avoid building live connector execution in the MVP.
- Keep the first version synthetic/demo-only.
- Keep the workflow concrete enough to show value without becoming a full CRM.
- Use AgentHub for visibility, not execution.

## Safety Boundary

This analysis is planning-only. It does not create a new project, read private
files, connect providers, run child scripts, execute real actions, commit, or
push.
