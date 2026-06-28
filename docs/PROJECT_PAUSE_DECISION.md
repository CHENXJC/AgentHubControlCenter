# Project Pause Decision

Checkpoint:
`HUB-V2-020-PROJECT-PAUSE-AND-NEXT-PORTFOLIO-GAP-DECISION-COMPLETE`

## Pause Decision

Decision: `pause_feature_expansion`

AgentHubControlCenter should pause feature expansion now.

The project has reached the intended portfolio-hub milestone:

- Public GitHub showcase is complete.
- Profile pin and portfolio positioning are documented.
- Cross-project backlinks are live for pushed child repos.
- Portfolio Matrix covers 12/12 projects after the ClientDeliveryKitAgent import.
- Hub-and-spoke navigation has been reviewed.
- V2 command surfaces are complete enough for public demonstration.
- Safety gates remain clear: metadata only, no live connector, no real action
  execution.

## Why AgentHub Should Pause

AgentHubControlCenter is now doing its main job: it explains the portfolio,
organizes the Agent matrix, shows safe metadata, and gives future integration
surfaces without overclaiming automation.

Continuing to add features inside AgentHub would create diminishing returns:

- It would make the hub heavier without adding a new portfolio category.
- It would risk turning a strong showcase hub into an unfinished platform.
- It would delay a new standalone project that can demonstrate a fresh business
  use case.
- It would blur the current public-safe boundary between metadata planning and
  real automation.

The better move is to use AgentHub as the control center for a new spoke
project.

## What Maintenance Still Matters

Maintenance should stay narrow:

- Keep README status and screenshots accurate after any later approved changes.
- Keep child `agent_manifest.json` files valid when new projects are created.
- Keep public-safe docs aligned with the real implementation.
- Fix broken links, stale project status text, or failed tests if discovered.
- Add new projects to the registry only when a separate project reaches a stable
  local demo stage.
- Maintain-only spoke imports are allowed when they update registry,
  documentation, portfolio matrix, and public-safe metadata without adding new
  AgentHub execution features.

## What Not To Build Next In AgentHub

Do not start these as the next AgentHub stage by default:

- Real Gmail, Google Sheets, Notion, Airtable, Telegram, or GitHub connector
  execution.
- Real workflow execution from Action Center.
- Background automation daemons.
- Multi-agent autonomous control.
- Client data ingestion inside AgentHub itself.
- Another broad dashboard page unless a real maintenance gap appears.
- More portfolio polish that does not change the user's capability matrix.

## Deferred AgentHub Enhancements

These ideas can remain deferred until a new spoke project creates a clear need:

- Read-only connector pilot.
- Safer command dry-run console.
- Plugin install package format.
- Cross-project report aggregation.
- Agent score history.
- Portfolio export refresh for a new project cohort.
- Controlled connector approval workflow.

## When To Resume AgentHub Development

Resume AgentHub only when one of these conditions is met:

- A new standalone Agent needs onboarding into the hub.
- A manifest or contract field is missing for a real new use case.
- A public README or screenshot becomes inaccurate.
- Tests fail after environment or dependency drift.
- The user explicitly asks for an AgentHub maintenance or integration stage.

Until then, AgentHub should be treated as showcase-ready and maintain-only.

## Safety Boundary

This decision is planning-only. It does not create new project code, connect
external providers, run child scripts, execute real actions, modify git remotes,
stage files, commit, or push.
