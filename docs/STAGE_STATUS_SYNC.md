# Stage Status Sync

Checkpoint:
`HUB-V2-024-DEEP-CHINESE-UI-COVERAGE-CHECK-COMPLETE`

## Purpose

AgentHubControlCenter now separates product status from checkpoint history and
manifest version. This prevents a cross-project checkpoint or older hard-coded
label from being shown as the current product stage.

## UI Fields

The sidebar displays three separate fields:

| UI field | Source | Meaning |
| --- | --- | --- |
| Product Status | `agent_hub/stage_status.py` policy label | Stable product posture, currently `Maintain / Showcase Ready` |
| Latest Checkpoint | `PROJECT_STATUS.md` top `Current status:` line | Most recent local checkpoint record |
| Manifest Version | `agent_manifest.json` `manifest_version` fallback to first Agent `version` | Root manifest metadata version |

The hero badge uses Product Status, not Latest Checkpoint.

## Helper Module

`agent_hub/stage_status.py` provides:

- `load_project_status_checkpoint(project_root)`
- `load_manifest_version(project_root)`
- `get_product_status_label(project_root)`
- `get_stage_snapshot(project_root)`

## Current Snapshot

| Field | Current value |
| --- | --- |
| Product Status | `Maintain / Showcase Ready` |
| Latest Checkpoint | `HUB-V2-024-DEEP-CHINESE-UI-COVERAGE-CHECK-COMPLETE` |
| Manifest Version | `HUB-V2-024-DEEP-CHINESE-UI-COVERAGE-CHECK-COMPLETE` |

The latest checkpoint is allowed to move forward during commit-only closeout
stages. In HUB-V2-024 the manifest version moves forward because the root
manifest now declares the deep Chinese UI coverage metadata.

## Cross-Project Checkpoint Rule

If `PROJECT_STATUS.md` contains a cross-project sync checkpoint such as
`CLIENTDELIVERYKIT-010-...`, the UI should still show:

- Product Status: `Maintain / Showcase Ready`
- Latest Checkpoint: the exact cross-project checkpoint
- Manifest Version: the current root manifest version

This keeps status history accurate without implying that a child project sync is
the AgentHub product stage.

## Safety Boundary

- This helper reads only `PROJECT_STATUS.md` and `agent_manifest.json`.
- It does not read `.env`, token files, credentials, private outputs, local
  databases, or generated private reports.
- It does not execute actions, command templates, child project scripts, git
  commands, or connector calls.
- It does not connect Gmail, Google Sheets, Notion, Airtable, Telegram, GitHub,
  n8n, Make, Zapier, or any external provider.
