# Profile Pin / Portfolio Placement Decision

Checkpoint:
`HUB-V2-015-PROFILE-PIN-PORTFOLIO-PLACEMENT-DECISION-COMPLETE`

## Decision

Pin decision: `strongly recommend pin`

AgentHubControlCenter should be treated as a primary GitHub profile pinned
project because it represents the user's current AI Agent portfolio as a system,
not just as one isolated tool.

## Why This Should Be Pinned

| Evaluation Area | Decision | Reason |
| --- | --- | --- |
| Represents the current AI project matrix | Strong | It connects 11 Agent and Skill manifests into one command center. |
| Shows system architecture ability | Strong | It includes manifest loading, registry merge, schemas, reports, simulations, and tests. |
| Shows workflow automation thinking | Strong | It models actions, useful signals, connector readiness, workflows, approval gates, and runbooks. |
| Shows safety and governance | Strong | It keeps real execution disabled, blocks unsafe actions, and makes approval gates visible. |
| Fits business / AI automation consultant positioning | Strong | It demonstrates how business workflows can be mapped, evaluated, and packaged safely. |
| Stronger than a single small tool as a main showcase | Strong | It acts as the portfolio hub that explains the rest of the project ecosystem. |

## Pin Placement Recommendation

Recommended GitHub profile placement:

1. Pin AgentHubControlCenter as the main portfolio hub.
2. Keep 3-5 vertical Agent projects pinned to show applied use cases.
3. If the profile already has six pinned repos, replace one narrower or
   overlapping single-purpose project rather than removing a strategically
   important vertical demo.

Suggested replacement logic if six pins are full:

- Prefer keeping projects that prove distinct marketable capabilities:
  business workflow, opportunity discovery, quant research, content extraction,
  career workflow, and the AgentHub meta-system.
- If finance/market coverage is duplicated, consider replacing the narrower
  market-dashboard style pin with AgentHubControlCenter, because QuantLabAgent
  already demonstrates finance/analysis and AgentHub adds system-level value.
- Do not change pins automatically. The final GitHub profile replacement choice
  should remain a manual user decision.

## Repo About Suggestions

### Concise Technical

Local-first AgentOps command center for managing AI Agent manifests, safe
actions, useful signals, connector readiness, workflows, approval gates, and
public showcase reports.

### Portfolio-Focused

Portfolio command center that organizes 11 local AI Agents and Skills into a
safe, documented, test-backed AgentOps dashboard with screenshots and runbooks.

### Business / Automation Consultant Focused

AI automation command center for mapping business workflows, Agent capabilities,
connector readiness, safety gates, and next-step recommendations across a
local-first project portfolio.

Recommended About version for GitHub:

`AI automation command center for managing 11 local-first Agent projects, safe actions, useful signals, workflows, connector readiness, and approval gates.`

## Topic Suggestions

Recommended topic set:

- `ai-agents`
- `ai-automation`
- `workflow-automation`
- `streamlit`
- `command-center`
- `agent-dashboard`
- `agentops`
- `useful-signals`
- `approval-gates`
- `connector-readiness`
- `local-first`
- `portfolio-dashboard`

Optional alternates if GitHub topic slots need to stay tighter:

- `python`
- `public-showcase`
- `business-automation`
- `workflow-simulation`

## README First-Screen Check

Result: pass with small wording improvement.

Current strengths:

- The project name is clear.
- The first paragraph explains Personal AI Command Center and AI Agent OS.
- The current checkpoint is visible near the top.
- The README immediately lists what the tool does.
- The screenshot section uses the current 10 canonical public-safe images.

Small improvement applied in this checkpoint:

- Added a compact portfolio positioning line near the top so a GitHub visitor
  understands that this repo is the user's portfolio hub, not only a standalone
  Streamlit dashboard.

No major README rewrite is recommended in this stage. Moving screenshots higher
could make the first viewport more visual, but the current README is already
clear enough for a technical GitHub visitor.

## Cross-Project Backlink Recommendation

Recommendation: yes, but only as a separate explicit stage.

Backlinks would help visitors understand that AgentHubControlCenter is the
hub that organizes the portfolio matrix. This should not be done in V2-015
because this stage is a placement decision only and must not modify sibling
projects.

Recommended projects for future backlinks:

| Project | Backlink Reason |
| --- | --- |
| BusinessOpsAgent | Strong fit for AI automation consultant positioning and workflow operations. |
| SocialPainFinderAgent | Shows opportunity discovery and business pain-point analysis feeding the hub. |
| QuantLabAgent | Shows analysis-heavy vertical capability that can be tracked by AgentHub. |
| VideoExtractSkill | Shows content intelligence capability as one node in the skill ecosystem. |
| CareerPilotAgent | Shows career workflow automation as a practical user-facing Agent. |
| NewsSignalAgent | Shows signal analysis that can feed Useful Signals / workflow review. |
| PersonalKnowledgeAgent | Shows knowledge workflow positioning, even if it remains not pinned. |

Suggested backlink sentence for future README use:

`This project is also tracked in AgentHubControlCenter, a local-first command center for managing my AI Agent portfolio, safe actions, workflows, connector readiness, and public showcase status.`

## Safety Boundary

This checkpoint is documentation and placement decision only.

- No `.env` is read.
- No secret, token, password, credential, or API key is output.
- No OAuth flow is created.
- No external connector is called.
- No child project script is run.
- No real action is executed.
- No git remote is modified.
- No git push is executed.
- No force push is used.
- No `outputs/private/` folder is written.

