# Agent Onboarding Flow

Status: HUB-V2-004

Agent onboarding is the first step toward making AgentHubControlCenter a
scalable local AI Agent Operating System. A future project should not need code
changes inside AgentHub just to appear in the command center. It should declare
a standard `agent_manifest.json`.

## UI Surfaces

The onboarding flow appears in the `Future Plugin Interface` page.

The UI shows:

- Total projects scanned
- Manifests found
- Valid manifests
- Invalid manifests
- Missing manifests
- Imported agents
- Duplicate agent IDs
- Recommended fixes
- Discovery results table
- Imported agents table
- Duplicate agent ID table
- Missing manifest table
- Invalid manifest table

## Source Types

Each runtime Agent record has a source:

| Source | Meaning |
| --- | --- |
| `static_registry` | Loaded from `data/agent_registry.csv`. |
| `local_manifest` | Loaded from a local project `agent_manifest.json`. |
| `demo_manifest` | Loaded from a demo/example manifest contract. |

## Onboarding Rules

HUB-V2-004 only imports metadata.

Allowed:

- Scan immediate child folders under `F:\AIProjects`.
- Read `agent_manifest.json`.
- Validate required manifest fields.
- Show warnings for missing or invalid fields.
- Convert valid manifests into runtime registry records.
- Merge manifest records with CSV registry records.
- Display source and duplicate status in the UI.

Not allowed:

- Running child Agent code.
- Calling external APIs.
- Reading `.env`, token, password, credential, database, or private output files.
- Sending email, Telegram messages, or account actions.
- Writing back to child projects automatically.

## Recommended Fix Workflow

For each missing manifest project:

1. Create `agent_manifest.json` in the project root.
2. Copy the minimal manifest shape from `docs/MANIFEST_IMPORT_GUIDE.md`.
3. Fill the required fields.
4. Keep `demo_mode` and `safe_mode` set to `true`.
5. Reopen or refresh AgentHubControlCenter.

For invalid manifests:

1. Check the `Invalid Manifests` table.
2. Add missing required fields.
3. Make `inputs`, `outputs`, `actions`, and `connectors` arrays.
4. Set `safe_mode` to `true`.
5. Confirm the manifest is valid JSON.

For duplicate `agent_id` values:

1. Prefer stable lowercase IDs.
2. Keep one ID per logical Agent.
3. Rename duplicates before enabling future action execution.

## HUB-V2-003 Completed

HUB-V2-003 generated reviewed `agent_manifest.json` templates for the existing
child Agent and Skill projects:

- `BusinessOpsAgent`
- `CareerPilotAgent`
- `IdeaScoreAgent`
- `MarketSenseAgent`
- `NewsSignalAgent`
- `NextOpsAgent`
- `PersonalKnowledgeAgent`
- `QuantLabAgent`
- `SocialPainFinderAgent`
- `VideoExtractSkill`

Discovery now shows:

- Total projects scanned: 11
- Manifests found: 11
- Valid manifests: 11
- Invalid manifests: 0
- Missing manifests: 0

## HUB-V2-004 Completed

HUB-V2-004 reviewed the V2 onboarding UI and refreshed the screenshot set:

- Agent cards now show readable category labels.
- Agent cards now show source, demo-mode, and safe-mode badges.
- Onboarding metrics are split across two rows so 11 valid / 0 invalid / 0
  missing is visible without truncated labels.
- Default onboarding tables avoid local path columns for public-safe screenshots.
- Local path details remain available in a collapsed manual-review expander.
- V2 screenshots now cover Command Overview, My Tools / Agent Registry, My
  Workflows, Useful Signals, Action Center, Connectors, Future Plugin
  Interface, and Agent Onboarding metrics.

## Recommended HUB-V2-005 Scope

- Define a stricter local action schema and manual runbook for display-only
  commands.
- Keep all actions display-only until a separate execution stage is requested.
- Add tests around action metadata safety before any future execution work.
