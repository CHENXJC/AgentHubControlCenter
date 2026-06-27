# Manifest Import Guide

Status: HUB-V2-004

HUB-V2-004 lets AgentHubControlCenter discover local Agents and Skills by
scanning immediate child folders under:

```text
F:\AIProjects
```

The scanner only checks whether each project folder contains:

```text
agent_manifest.json
```

It does not run child project code, does not read `.env`, and does not scan
credentials, tokens, database files, logs, or private outputs.

## Import Flow

```text
Scan project folders -> Find agent_manifest.json -> Validate required fields -> Convert to registry record -> Merge with static CSV registry -> Display in UI
```

## Required Fields

Each importable manifest Agent record must include:

- `agent_id`
- `agent_name`
- `category`
- `description`
- `project_path`
- `status`
- `inputs`
- `outputs`
- `actions`
- `connectors`
- `demo_mode`
- `safe_mode`

`safe_mode` must be `true` for HUB-V2-004 import.

## Optional Fields

- `version`
- `last_run`
- `next_recommended_action`
- `github_repo`
- `dashboard_url`
- `tags`
- `owner`
- `public_showcase_status`
- `pin_status`

## Supported Manifest Shapes

Single Agent:

```json
{
  "agent_id": "demo_agent",
  "agent_name": "DemoAgent",
  "category": "Workflow Automation",
  "description": "Demo workflow automation assistant.",
  "project_path": "F:\\AIProjects\\DemoAgent",
  "status": "Active",
  "inputs": ["workflow_notes"],
  "outputs": ["dashboard"],
  "actions": [{"action_id": "launch", "label": "Launch local app"}],
  "connectors": [{"connector_id": "local_filesystem", "label": "Local Filesystem"}],
  "demo_mode": true,
  "safe_mode": true
}
```

Multiple Agents in one project:

```json
{
  "agents": [
    {
      "agent_id": "demo_agent",
      "agent_name": "DemoAgent",
      "category": "Workflow Automation",
      "description": "Demo workflow automation assistant.",
      "project_path": "F:\\AIProjects\\DemoAgent",
      "status": "Active",
      "inputs": ["workflow_notes"],
      "outputs": ["dashboard"],
      "actions": [{"action_id": "launch", "label": "Launch local app"}],
      "connectors": [{"connector_id": "local_filesystem", "label": "Local Filesystem"}],
      "demo_mode": true,
      "safe_mode": true
    }
  ]
}
```

## Merge Rules

- Static CSV records get source `static_registry`.
- Valid local manifests get source `local_manifest`.
- Demo/example manifests get source `demo_manifest`.
- If a manifest and static registry record share the same `agent_id`, manifest
  data is displayed in the merged runtime registry.
- Duplicate manifest IDs are not imported twice; the first manifest record is
  kept and a duplicate warning is shown.

## Skipped Directories

The scanner ignores runtime and private-style folders such as:

- `.git`
- `.venv`
- `venv`
- `node_modules`
- `__pycache__`
- `.pytest_cache`
- `outputs`
- `private_outputs`
- `secrets`

## Current Scan Result

At HUB-V2-004 completion, the local scan found:

- Total projects scanned: 11
- Manifests found: 11
- Valid manifests: 11
- Invalid manifests: 0
- Missing manifests: 0
- Imported agents: 11
- Duplicate agent IDs: 9 static registry overrides

Imported manifests:

- `AgentHubControlCenter` from `F:\AIProjects\AgentHubControlCenter\agent_manifest.json`
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

The duplicate agent IDs are expected for the 9 projects that already existed in
`data/agent_registry.csv`. Runtime display uses the richer local manifest data
and keeps the CSV registry as the baseline source.
