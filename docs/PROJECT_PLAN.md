# Project Plan

## Project Goal

AgentHubControlCenter is a local-first AI Agent / Skill control center for
managing a personal AI workflow ecosystem. It centralizes registry metadata,
local project health checks, portfolio positioning, GitHub showcase links,
launch command visibility, and next actions.

## HUB-002 MVP

- Created the local project skeleton.
- Registered existing AI Agent and Skill projects in `data/agent_registry.csv`.
- Built a Streamlit dashboard with overview, registry, health check, portfolio
  matrix, and report export tabs.
- Added core Python modules with focused tests.
- Kept all behavior local and credential-free.

## HUB-003 Registry Engine + Health Check Upgrade

- Added registry metadata validation and quality scores.
- Upgraded health scoring for tests, docs, project status, portfolio folder,
  GitHub URL presence, and suggested fixes.
- Added next action planning with High, Medium, Low, and None priority levels.
- Added portfolio positioning analysis with capability clusters, strengths, and
  gaps.
- Added command pack builder for local project workflow commands.
- Enhanced the Markdown portfolio report.
- Upgraded the Streamlit dashboard to six tabs.

## HUB-004 Streamlit Product UI Polish

- Added product-style command center hero.
- Added six metric cards and sidebar filters.
- Added registry detail and command pack panels.
- Added health overview cards and health detail expanders.
- Added capability cluster cards and category matrix cards.
- Added priority summary and grouped action cards.
- Added screenshot-ready spacing and visual hierarchy.
- Updated the screenshot guide for six public-showcase views.

## HUB-005 Report Export & Showcase Assets

- Added saved local Markdown report export flow for `outputs/`.
- Added a stable Windows-safe report filename builder.
- Added enhanced Command Center Summary to the report, Overview tab, and Export
  Report tab.
- Added fixed project matrix view for the core portfolio categories.
- Added Priority Action Summary for paused projects, future commercial
  candidates, GitHub showcase projects, and future AgentHub integration.
- Added public showcase readiness and public-safe showcase asset checklist to
  the report and UI.
- Improved report preview and output organization for screenshot readiness.

## HUB-006 Public Showcase Packaging / Screenshots / GitHub Release Polish

- Captured six public-safe Streamlit screenshots under `docs/images/`.
- Added a GitHub-ready README screenshot section with relative image paths.
- Updated the screenshot guide with UI-area mapping and safety notes.
- Updated the public showcase manifest with packaging status, asset status, and
  safety boundaries.
- Updated the showcase asset checklist for README, screenshot, docs, status, and
  validation readiness.
- Kept the app feature scope stable; no new app logic or core workflow expansion
  was added in this stage.

## HUB-007 GitHub Public Release

- Published the public-safe AgentHubControlCenter showcase repository to GitHub:
  <https://github.com/CHENXJC/AgentHubControlCenter>.
- Confirmed the repository is public and the `main` branch is available.
- Confirmed README rendering, screenshot display, repository About description,
  topics, and project file visibility.
- Kept Profile Pin as pending user decision.

## HUB-V2-001 Unified Command Center Entry + Desktop Launcher

- Upgraded positioning to Personal AI Command Center / AI Agent Operating
  System.
- Reorganized the Streamlit app into Command Overview, My Tools / Agent
  Registry, My Workflows, Useful Signals, Action Center, Connectors, and Future
  Plugin Interface pages.
- Added a V2 Agent interface layer that derives standard manifests from the
  existing CSV registry without forcing a disruptive data migration.
- Added `agent_manifest.json`, `agent_contract.json`,
  `docs/AGENT_INTERFACE_STANDARD.md`, and
  `docs/FUTURE_PLUGIN_INTERFACE.md`.
- Added a Windows launcher and desktop shortcut script for local startup on
  port `8525`.
- Kept all connectors demo/planned/display-only in this stage.

## HUB-V2-001A Desktop Launcher Runtime Fix

- Created the project-owned `.venv`.
- Installed the minimal runtime dependencies from `requirements.txt`.
- Verified `.venv\Scripts\python.exe`, `.venv\Scripts\streamlit.exe`, pytest,
  compileall, Streamlit smoke check, launcher smoke check, and desktop shortcut
  target.

## HUB-V2-002 Manifest Import + Agent Onboarding Flow

- Added safe local manifest discovery under `F:\AIProjects`.
- Added `agent_hub/manifest_loader.py` for immediate child directory scanning,
  JSON reading, required field validation, source classification, and registry
  conversion.
- Added `agent_hub/agent_onboarding.py` for CSV + manifest merge, duplicate
  `agent_id` handling, source tracking, and onboarding UI summaries.
- Added unit tests for manifest loading and onboarding merge behavior.
- Added onboarding UI under the Future Plugin Interface page.
- Added `docs/MANIFEST_IMPORT_GUIDE.md` and
  `docs/AGENT_ONBOARDING_FLOW.md`.
- Kept discovery metadata-only: no child project scripts are executed, no
  external connectors are called, and no credentials are read.

## HUB-V2-003 Child Agent Manifest Templates

- Added reviewed `agent_manifest.json` templates to 10 existing child projects:
  BusinessOpsAgent, CareerPilotAgent, IdeaScoreAgent, MarketSenseAgent,
  NewsSignalAgent, NextOpsAgent, PersonalKnowledgeAgent, QuantLabAgent,
  SocialPainFinderAgent, and VideoExtractSkill.
- Kept all actions display-only/manual/demo in the manifests.
- Declared connectors as local, link-based, planned, or optional only.
- Preserved manifest-declared inputs, outputs, actions, and connectors in the
  runtime AgentHub UI.
- Updated category mapping so the standard V2 manifest categories appear in the
  portfolio matrix.
- Confirmed local discovery now finds 11 valid manifests, 0 invalid manifests,
  and 0 missing manifests.

## HUB-V2-004 V2 Onboarding Screenshot Refresh + Registry Review

- Reviewed 11 manifest-onboarded Agent cards for wording, categories, actions,
  connectors, status, demo mode, and safe mode.
- Added readable category labels for standard manifest categories.
- Added source and safety badges to V2 Agent cards.
- Split Agent Onboarding metrics into two rows so 11 valid / 0 invalid / 0
  missing is clear.
- Collapsed local path details in the Future Plugin Interface for public-safe
  screenshots while keeping manual review access.
- Refreshed 8 V2 screenshots under `docs/images/`.
- Updated README and showcase docs for the V2 screenshot set.

## HUB-V2-005 Local Action Schema + Manual Runbook

- Added `agent_hub/action_schema.py` for action fields, enums, normalization,
  validation, blocked action rules, and summary metrics.
- Added `agent_hub/action_registry.py` for flattening manifest actions into the
  Action Center model, grouping actions by Agent, and detecting policy
  violations.
- Updated 11 onboarded manifests with 55 schema-backed actions.
- Added Action Center metrics for total actions, manual-only actions,
  display-only actions, future connector actions, required approval, and blocked
  actions.
- Added Action Center schema table and Agent-grouped action cards.
- Added `docs/ACTION_SCHEMA.md`, `docs/MANUAL_RUNBOOK.md`, and
  `docs/ACTION_SAFETY_POLICY.md`.
- Reserved `codex_prompt` as a template-only structure for the next stage.
- Kept all actions metadata/instruction/template/display only.

## HUB-V2-006 Codex Prompt Generator

- Added `agent_hub/codex_prompt_generator.py` for copy-ready Codex task prompt
  generation.
- Added supported prompt types: `continue_next_stage`, `fix_or_polish`, and
  `github_showcase_update`.
- Reserved prompt types for later stages: `add_manifest`, `refresh_screenshots`,
  `run_tests_only`, `create_connector_plan`, and `generate_report`.
- Added a Codex Prompt Generator section to the Action Center with Agent
  selector, prompt type selector, selected Agent context, available actions,
  safety checklist, validation checklist, generated prompt preview, text area,
  and text download.
- Kept prompts template-only: no auto-send to Codex, no command execution, no
  child script execution, and no live connector access.
- Added `docs/CODEX_PROMPT_GENERATOR.md` and tests for prompt generation,
  missing safe-doc warnings, reserved prompt types, and codex prompt action
  policy.

## HUB-V2-007 Useful Signals Engine

- Added `agent_hub/useful_signal_schema.py` for signal fields, enums,
  normalization, validation, and display-only execution policy.
- Added `agent_hub/useful_signal_data.py` with 14 local/demo signals across the
  AgentHub portfolio.
- Added `agent_hub/useful_signal_engine.py` for usefulness scoring, risk-aware
  score explanations, buckets, filters, and summary metrics.
- Enhanced the Useful Signals page with Signal Metrics, filters, Top 5 Useful
  Signals, Needs Action, Watchlist, Low Priority / Ignored, and a signal table.
- Kept every recommendation text-only: no child scripts, no external connector,
  no command execution, and no auto-send behavior.
- Added `docs/USEFUL_SIGNALS_ENGINE.md` and tests for schema and scoring.

## HUB-V2-008 Connector Readiness Simulator

- Added `agent_hub/connector_readiness_schema.py` for connector fields,
  readiness statuses, data access levels, normalization, validation, and
  design-only execution policy.
- Added `agent_hub/connector_readiness_data.py` with 14 demo connector
  readiness records across Gmail, Google Sheets, Google Drive, Notion,
  Airtable, Telegram, GitHub, n8n, Make, and Zapier.
- Added `agent_hub/connector_readiness_engine.py` for readiness scoring,
  summary metrics, filters, policy checks, and connector-generated Useful
  Signals.
- Enhanced the Connectors page with readiness metrics, risk/status/provider
  filters, connector cards, readiness table, and connector-generated Useful
  Signals.
- Kept every connector `not_connected`: no OAuth, no credentials, no provider
  API calls, no webhooks, no sends, no writes, and no git push.
- Added `docs/CONNECTOR_READINESS_SIMULATOR.md` and
  `docs/CONNECTOR_SAFETY_GATES.md`.

## HUB-V2-009 Local Workflow Simulation + Approval Gates

- Added `agent_hub/workflow_simulation_schema.py` for workflow simulation
  fields, enums, normalization, validation, and simulation-only execution
  policy.
- Added `agent_hub/workflow_simulation_data.py` with 4 demo workflows:
  Project Progress Review, Useful Signals Review, Connector Readiness Review,
  and Codex Handoff.
- Added `agent_hub/workflow_simulation_engine.py` for readiness scoring,
  workflow status, filters, summary metrics, policy checks, and
  workflow-generated Useful Signals.
- Added `agent_hub/approval_gate_schema.py` and
  `agent_hub/approval_gate_engine.py` for approval status, allowed execution
  modes, required checks, dry-run requirements, rollback requirements, human
  review requirements, and blocked-step handling.
- Enhanced the My Workflows page with workflow metrics, workflow cards,
  Approval Gates table, and workflow-generated Useful Signals.
- Kept every workflow simulation-only: no live connector, no credentials, no
  OAuth, no external API, no child scripts, no real actions, and no git push.
- Added `docs/LOCAL_WORKFLOW_SIMULATION.md` and
  `docs/APPROVAL_GATE_PLANNER.md`.

## HUB-V2-010 Demo Workflow Report Export

- Added `agent_hub/report_export_schema.py` for report package fields,
  allowed formats, section selection, output directory policy, and public-safe
  validation.
- Added `agent_hub/demo_report_builder.py` for Markdown, JSON, and CSV report
  text generation from existing Agent Registry, Action Center, Useful Signals,
  Connector Readiness, Workflow Simulation, and Approval Gates metadata.
- Added `agent_hub/demo_report_exporter.py` for writing report bundles only to
  `outputs/public_reports/`.
- Enhanced the My Workflows page with a Demo Workflow Report Export section,
  section selector, report metrics, Markdown preview, JSON preview, CSV preview,
  and text download controls.
- Kept report export metadata-only and public-safe: no credentials, no live
  connectors, no external APIs, no child scripts, no real actions, and no
  `outputs/private/`.
- Added `docs/DEMO_WORKFLOW_REPORT_EXPORT.md`.

## HUB-V2-011 Report Showcase / Screenshot Refresh

- Refreshed the README screenshot section to use a canonical 10-image V2-011
  showcase set.
- Captured screenshots for Command Overview, Agent Registry, Action Center,
  Codex Prompt Generator, Useful Signals, Workflow Simulation, Connectors,
  Agent Onboarding, Report Export, and Approval Gates.
- Updated `docs/SCREENSHOTS_GUIDE.md` with exact filenames, UI-area mapping,
  manual refresh steps, and public-safe capture rules.
- Updated `docs/SHOWCASE_ASSET_CHECKLIST.md` and
  `docs/PUBLIC_SHOWCASE_MANIFEST.md` for the V2-011 showcase assets.
- Added `docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md` as a compact
  public-safe summary of the latest generated report.
- Kept the stage docs/showcase-only: no connector calls, no child scripts, no
  real actions, no private outputs, no git remote changes, and no git push.

## HUB-V2-012 Public Showcase Release Check

- Added `docs/PUBLIC_RELEASE_CHECKLIST.md` as the final local public-showcase
  gate.
- Added `docs/V2_RELEASE_READINESS_REPORT.md` with feature snapshot, asset
  status, screenshot inventory, manifest/contract status, test status,
  security policy, git hygiene, limitations, release recommendation, suggested
  commit message, and next stage.
- Added `tests/test_public_release_readiness.py` to validate README screenshot
  paths, release docs, `.gitignore` boundaries, manifest/contract JSON loading,
  immediate project manifests, launcher configuration, and public-doc
  secret-like patterns.
- Updated README and showcase docs for V2-012 release readiness.
- Kept this stage review-only: no git add, commit, push, remote change, live
  connector, child script, external API, real action, or private output.

## HUB-V2-013 GitHub Showcase Update Decision

- Added `docs/GITHUB_SHOWCASE_UPDATE_DECISION.md` to record the commit/push
  decision and release notes draft.
- Added `docs/PUBLIC_COMMIT_FILE_MANIFEST.md` with recommended public commit
  categories, screenshot inventory, test inventory, child manifest inventory,
  risk notes, and a suggested future staging command.
- Added `docs/PUBLIC_EXCLUSION_MANIFEST.md` with excluded generated, private,
  local-only, cache, and sibling-project path classes.
- Added tests for the V2-013 decision docs.
- Updated README, project status, public release checklist, release readiness
  report, and public showcase manifest for the decision checkpoint.
- Kept this stage decision-only: no git add, commit, push, reset, clean, rm,
  remote change, live connector, child script, external API, real action, or
  private output.

## HUB-V2-014 Git Commit / Push / Live Showcase Verification

- Used `docs/PUBLIC_COMMIT_FILE_MANIFEST.md` as the exact public-safe staging
  source.
- Reran pytest, compileall, Streamlit smoke check, launcher smoke check,
  AppTest-style UI checks, JSON validation, policy counts, and public-safe
  scans.
- Staged only manifest-listed files and kept generated reports under
  `outputs/public_reports/*.md`, `*.json`, and `*.csv` excluded.
- Created a normal release commit and pushed the current branch to the existing
  remote without changing remotes or using force push.
- Verified the live GitHub README, screenshot assets, docs, and remote tree
  after push.

## Later Stages

- HUB-V2-015 Profile Pin / Portfolio Placement Decision, if the user wants to
  decide whether AgentHubControlCenter should be pinned on the GitHub profile
  after the V2 public showcase update.

## Safety Boundary

This project is a dashboard for local portfolio management and workflow planning.
It does not execute external actions, access private credentials, or use force
push. GitHub publishing is limited to public-safe release commits.
