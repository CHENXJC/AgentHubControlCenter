# Screenshots Guide

HUB-V2-011 screenshot status: refreshed for Report Showcase / Screenshot
Refresh.

HUB-V2-012 release-check status: screenshot inventory verified against README,
the screenshot guide, and the public release checklist. No new screenshot set is
required for V2-012.

HUB-V2-013 GitHub showcase update decision: the 10 canonical screenshot files
listed below are recommended for the future public commit. No new screenshot set
is required for V2-013.

HUB-V2-014 live showcase verification: the same 10 canonical screenshot files
are committed and verified from GitHub after push. No new screenshot set is
required for V2-014.

The public showcase screenshots are saved under `docs/images/` and are intended
for the GitHub README screenshot section. The V2-011 set was captured from the
local Streamlit demo app on port `8525` using manifest-onboarded Agent metadata.

## Public-Safe Screenshot Rules

- Do not include `.env`, API keys, tokens, passwords, credentials, customer
  data, private documents, private reports, or live connector data.
- Use local demo portfolio metadata only.
- Keep screenshot areas focused on product UI, metrics, planning, readiness,
  report preview, and safety gates.
- Do not run child Agent scripts during screenshot preparation.
- Do not connect Gmail, Google Sheets, Notion, Airtable, Telegram, GitHub, n8n,
  Make, Zapier, or other live providers.
- Avoid exposing detailed local command output in public README screenshots.

## V2-011 Canonical Screenshots

### 1. `docs/images/01_command_overview.png`

UI area: Command Overview.

Shows the Personal AI Command Center hero, current stage label, 11 available
tools, portfolio metrics, and first-row Agent cards.

### 2. `docs/images/02_agent_registry.png`

UI area: My Tools / Agent Registry.

Shows 11 manifest-onboarded local Agents and Skills with source, demo-mode,
safe-mode, action, and connector badges.

### 3. `docs/images/03_action_center.png`

UI area: Action Center.

Shows Local Action Schema metrics and action policy tables. All actions are
display/manual/template/planned metadata only.

### 4. `docs/images/04_codex_prompt_generator.png`

UI area: Action Center / Codex Prompt Generator.

Shows the template-only prompt generator with Agent selector, prompt type
selector, selected Agent context, safety checklist, validation checklist,
preview, and copy-ready text area.

### 5. `docs/images/05_useful_signals.png`

UI area: Useful Signals.

Shows Signal Metrics, filters, and local/demo recommendation context. Useful
Signals are display-only text recommendations.

### 6. `docs/images/06_workflow_simulation.png`

UI area: My Workflows / Local Workflow Simulation.

Shows local workflow simulation metrics and filters. Workflows remain
simulation-only with no live connector and no real action execution.

### 7. `docs/images/07_connectors.png`

UI area: Connectors.

Shows Connector Readiness Simulator metrics and filters. All connectors remain
`not_connected`; this page does not create OAuth flows or call provider APIs.

### 8. `docs/images/08_agent_onboarding_metrics.png`

UI area: Future Plugin Interface / Agent Onboarding.

Shows Agent Onboarding metrics:

- Projects scanned: 11
- Manifests found: 11
- Valid manifests: 11
- Invalid manifests: 0
- Missing manifests: 0
- Imported agents: 11

### 9. `docs/images/09_report_export.png`

UI area: My Workflows / Demo Workflow Report Export.

Shows the public-safe report export surface for Markdown, JSON, and CSV text
reports under `outputs/public_reports/`.

### 10. `docs/images/10_approval_gates.png`

UI area: My Workflows / Approval Gates.

Shows approval gate metadata for manual/template/blocked workflow steps,
including blocked Gmail Send and GitHub Push / Release examples.

## Historical Screenshot Assets

Older HUB-006 and HUB-V2-004 screenshot files may remain in `docs/images/` for
history, but the README should use the V2-011 canonical 10-image set above.

## Capture Notes

- Recommended browser width: 1440px.
- Current V2-011 images were captured at 1440x1000.
- Streamlit URL used for capture: `http://localhost:8525/`.
- Screenshot review confirmed no `.env`, token, API key, password, credential,
  private customer data, private output, or live connector data is visible.
- The Report Export screenshot shows public-safe preview/download surfaces only.
- The visible export path remains `outputs/public_reports/`; do not use
  `outputs/private/`.

## Manual Refresh Procedure

If automatic capture is unavailable:

1. Start the app with `launch_command_center.cmd` or
   `.venv\Scripts\streamlit.exe run app.py --server.port 8525`.
2. Open `http://localhost:8525/` in a browser sized around 1440x1000.
3. Capture the 10 canonical UI areas listed above.
4. Save files with the exact filenames in this guide under `docs/images/`.
5. Re-check that no credential, private output, live connector, or real
   execution result is visible.
6. Run pytest, compileall, Streamlit smoke check, and launcher smoke check.
