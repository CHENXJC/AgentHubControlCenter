# Codex Prompt Generator

## Purpose

HUB-V2-006 adds a copy-ready Codex Prompt Generator to AgentHubControlCenter V2.
It turns each Agent manifest, local action schema, checkpoint metadata, README
availability, runbook references, and `next_recommended_action` into a Chinese
first task prompt that can be copied manually into Codex.

This feature is text-only. It does not send prompts to Codex, does not execute
commands, does not run child project scripts, and does not connect live
connectors.

## Inputs

The generator uses only safe metadata already loaded by AgentHubControlCenter:

- `agent_manifest.json` metadata
- normalized Action Center rows
- `project_path`
- current checkpoint from `PROJECT_STATUS.md` when available
- `README.md` / `agent_manifest.json` existence checks
- runbook and action safety references
- `next_recommended_action`

It only checks fixed safe context files:

- `PROJECT_STATUS.md`
- `README.md`
- `agent_manifest.json`
- `docs/MANUAL_RUNBOOK.md`
- `docs/ACTION_SAFETY_POLICY.md`

If a child project is missing `PROJECT_STATUS.md` or `README.md`, the generator
adds a warning to the prompt package and continues.

## Supported Prompt Types

| Prompt type | Status | Use |
| --- | --- | --- |
| `continue_next_stage` | Supported | Continue the next safe project stage based on manifest and checkpoint context. |
| `fix_or_polish` | Supported | Fix a bug or polish a small UI/docs/test issue without expanding scope. |
| `github_showcase_update` | Supported | Prepare public-safe README/docs/screenshot/status updates. |

## Reserved Prompt Types

These prompt types are reserved for future stages and are still text-only:

- `add_manifest`
- `refresh_screenshots`
- `run_tests_only`
- `create_connector_plan`
- `generate_report`

## Generated Prompt Sections

Each prompt includes:

- `project_path`
- current checkpoint
- project positioning
- current capabilities
- next recommended action
- files to read first
- task goals
- safety requirements
- validation requirements
- expected completion report format

## Safety Requirements Embedded In Every Prompt

- Do not read `.env`.
- Do not output secret/token/password/API key.
- Do not modify git remote.
- Do not execute git push.
- Do not delete user files.
- Do not run unauthorized external scripts or child project scripts.
- Do not connect real Gmail, Google Sheets, Notion, Airtable, Telegram, or other
  connectors unless the user explicitly asks.
- Treat command templates and generated prompts as display text only.

## UI Behavior

The Action Center includes a `Codex Prompt Generator` section with:

- Agent selector
- prompt type selector
- selected Agent metadata
- available action table
- safety checklist
- validation checklist
- generated prompt preview
- copy-ready text area
- download text button

There is no execute button and no connector trigger.

## Validation Expectations

For HUB-V2-006 verification:

- 11 agents remain visible.
- Codex Prompt Generator is visible.
- At least 3 different Agents can generate prompts.
- Generated prompts include safety and validation requirements.
- `codex_prompt` actions remain `template_only` and not executable.
- Valid manifests remain 11.
- Invalid manifests remain 0.
- Missing manifests remain 0.
