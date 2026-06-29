# Public Showcase Manifest

## Public Showcase Identity

AgentHubControlCenter is a local-first AgentOps / PortfolioOps dashboard that
shows how a personal AI Agent and Skill ecosystem can be registered, validated,
checked, organized, exported, and presented from one product-style Streamlit
command center.

## Current Status

Public release status: HUB-007-GITHUB-PUBLIC-RELEASE-COMPLETE

Current local development status: HUB-V2-022-BILINGUAL-UI-TOGGLE-AND-STAGE-SYNC-CHECK-COMPLETE

## HUB-006 Public Showcase Packaging

HUB-006 packages the completed HUB-005 feature set for a GitHub public showcase
pass. It does not expand core app logic or add new runtime integrations.

Packaging status:

| Area | Status | Notes |
| --- | --- | --- |
| README screenshot section | Complete | Uses relative `docs/images/` paths and public-safe captions. |
| Screenshot assets | Complete | Six PNG screenshots saved under `docs/images/`. |
| Screenshots guide | Complete | Documents each image, UI area, and public-safe capture rule. |
| Showcase asset checklist | Complete | Tracks screenshot, README, manifest, status, docs, and validation readiness. |
| Project status | Complete | Records the HUB-006 checkpoint and next-stage recommendation. |
| Tests | Complete | `python -m pytest` passed: 24 tests passed. |
| Compile check | Complete | `python -m compileall agent_hub app.py` passed. |
| Streamlit smoke check | Complete | Local app opened at `http://127.0.0.1:8501` for screenshot capture. |
| Safety check | Complete | No `.env` read, no secrets output, no remote change, no push. |

## HUB-007 GitHub Public Release

HUB-007 publishes the public-safe showcase package to GitHub.

Release status:

| Area | Status | Notes |
| --- | --- | --- |
| Public repository | Complete | <https://github.com/CHENXJC/AgentHubControlCenter> |
| Main branch | Complete | `main` is available on GitHub. |
| README rendering | Complete | README renders on the GitHub repository page. |
| Screenshot rendering | Complete | README uses relative `docs/images/` screenshot links. |
| About description | Complete | Repository About description is filled. |
| Topics | Complete | Repository topics are added. |
| Profile Pin | Pending | Pending user decision. |

## HUB-V2-001 Unified Command Center Entry

HUB-V2-001 upgrades the local product direction from a portfolio dashboard into
a Personal AI Command Center / AI Agent Operating System entry point.

V2 local status:

| Area | Status | Notes |
| --- | --- | --- |
| Command Overview | Complete | Shows available tools, useful summaries, and next actions. |
| My Tools / Agent Registry | Complete | Preserves the existing registry with V2 tool cards. |
| My Workflows | Complete | Adds workflow-level grouping for portfolio review and Agent onboarding. |
| Useful Signals | Complete | Shows readiness, action pressure, connector links, and safe-mode coverage. |
| Action Center | Complete | Keeps actions display-only and planning-focused. |
| Connectors | Complete | Shows local/demo/planned connector states without live API access. |
| Future Plugin Interface | Complete | Adds manifest, contract, plugin stages, and report export in one page. |
| Desktop Launcher | Complete | Adds local Windows launcher and shortcut creation guide. |

## HUB-V2-002 Manifest Import + Agent Onboarding

HUB-V2-002 adds safe local manifest discovery and onboarding.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Manifest loader | Complete | Scans immediate `F:\AIProjects` child folders for `agent_manifest.json`. |
| Manifest validation | Complete | Missing or invalid required fields become UI warnings. |
| Registry merge | Complete | Valid manifests merge with `data/agent_registry.csv` at runtime. |
| Source labels | Complete | Supports `static_registry`, `local_manifest`, and `demo_manifest`. |
| Onboarding UI | Complete | Added under Future Plugin Interface. |
| Tests | Complete | 37 tests passed. |
| Safety | Complete | No child scripts, credentials, or live connectors are executed/read. |

## HUB-V2-003 Child Agent Manifest Templates

HUB-V2-003 adds manifest templates for the existing child Agent and Skill
projects so AgentHubControlCenter can show a complete local registry view.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Child manifests | Complete | 10 child projects now have `agent_manifest.json`. |
| Discovery result | Complete | 11 projects scanned, 11 manifests found, 11 valid, 0 invalid, 0 missing. |
| Runtime merge | Complete | 9 static CSV records are overridden by local manifest data at runtime. |
| Manifest field preservation | Complete | Imported inputs, outputs, actions, and connectors are shown in the UI model. |
| Tests | Complete | 38 tests passed. |
| Compile check | Complete | `.venv\Scripts\python.exe -m compileall .` passed. |
| Streamlit smoke check | Complete | `http://localhost:8525` returned HTTP 200. |
| Agent Onboarding UI check | Complete | Streamlit AppTest confirmed 11 valid manifests and 0 missing/invalid manifests. |
| Launcher smoke check | Complete | `launch_command_center.cmd` returned HTTP 200 on fixed port 8525. |
| Safety | Complete | No child scripts, credentials, private outputs, or live connectors are executed/read. |

## HUB-V2-004 V2 Onboarding Screenshot Refresh + Registry Review

HUB-V2-004 reviews the manifest-onboarded registry UI and refreshes the V2
screenshot set for the next public showcase update.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Agent card wording review | Complete | 11 cards reviewed for description, category, actions, connectors, demo mode, and safe mode. |
| Category labels | Complete | Standard manifest categories now display as readable product labels. |
| Source badges | Complete | Cards show Demo Manifest or Local Manifest. |
| Safety badges | Complete | Cards show Demo Mode / Safe Mode. |
| Onboarding metrics | Complete | 11 valid manifests, 0 invalid manifests, 0 missing manifests. |
| Public-safe table view | Complete | Future Plugin Interface hides local path columns by default and keeps them in a collapsed manual-review expander. |
| Screenshot refresh | Complete | 8 V2 screenshots saved under `docs/images/`. |
| Tests | Complete | Validation commands passed in local V2-004 verification. |
| Safety | Complete | No child scripts, credentials, private outputs, or live connectors are executed/read. |

## HUB-V2-005 Local Action Schema + Manual Runbook

HUB-V2-005 adds a stricter action declaration layer before any future execution
work is considered.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Action schema module | Complete | `agent_hub/action_schema.py` defines fields, enums, blocked IDs, normalization, validation, and metrics. |
| Action registry module | Complete | `agent_hub/action_registry.py` builds Action Center rows and checks policy violations. |
| Manifest actions | Complete | 11 manifests declare 55 schema-backed actions. |
| Action Center metrics | Complete | Total, manual-only, display-only, future connector, approval, and blocked metrics are visible. |
| Action cards | Complete | Cards are grouped by Agent and show type, execution mode, risk, approval, expected output, safety note, and runbook reference. |
| Manual runbook | Complete | `docs/MANUAL_RUNBOOK.md` explains safe manual operation. |
| Safety policy | Complete | `docs/ACTION_SAFETY_POLICY.md` blocks automatic execution, live connectors, destructive file operations, git remote changes, and git push. |
| Codex prompt reservation | Complete | `codex_prompt` is available as a template-only action type for HUB-V2-006. |

## HUB-V2-006 Codex Prompt Generator

HUB-V2-006 adds a text-only prompt generation layer for safer follow-up work in
Codex. It generates copy-ready task prompts from Agent manifest metadata, local
action rows, checkpoint context, runbook references, safety requirements,
validation requirements, and `next_recommended_action`.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Prompt generator module | Complete | `agent_hub/codex_prompt_generator.py` builds prompt packages and generated text. |
| Supported prompt types | Complete | `continue_next_stage`, `fix_or_polish`, and `github_showcase_update`. |
| Reserved prompt types | Complete | `add_manifest`, `refresh_screenshots`, `run_tests_only`, `create_connector_plan`, and `generate_report`. |
| Action Center UI | Complete | Added Agent selector, prompt type selector, Agent context, action table, safety checklist, validation checklist, prompt preview, text area, and text download. |
| Text-only policy | Complete | Prompts are not auto-sent to Codex and no real action is executed. |
| Prompt docs | Complete | `docs/CODEX_PROMPT_GENERATOR.md` documents inputs, prompt types, UI behavior, and safety rules. |
| Tests | Complete | Prompt generator tests cover required prompt content, missing safe-doc warnings, reserved prompt types, and codex action policy. |

## HUB-V2-007 Useful Signals Engine

HUB-V2-007 adds a local/demo signal ranking layer for AgentHub. The Useful
Signals page now shows scored recommendations, score reasons, related Agents,
safe next-step text, and risk-aware display buckets across project progress,
action required, business opportunity, learning value, portfolio improvement,
connector readiness, workflow automation, and risk warning categories.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Signal schema module | Complete | `agent_hub/useful_signal_schema.py` defines fields, enums, validation, and display-only policy. |
| Signal demo dataset | Complete | `agent_hub/useful_signal_data.py` includes 14 local/demo signals. |
| Signal scoring engine | Complete | `agent_hub/useful_signal_engine.py` scores, explains, filters, buckets, and summarizes signals. |
| Useful Signals UI | Complete | Metrics, filters, Top 5, Needs Action, Watchlist, Low Priority / Ignored, and table are visible. |
| Signal docs | Complete | `docs/USEFUL_SIGNALS_ENGINE.md` documents schema, scoring, UI, and safety. |
| Safety | Complete | Signals are display-only text recommendations and do not execute commands or connect accounts. |

## HUB-V2-008 Connector Readiness Simulator

HUB-V2-008 adds a design-only connector readiness layer. The Connectors page now
shows permissions, data access level, write access, risk, approval requirement,
demo/read-only availability, rollback plan, test plan, safety gates, readiness
score, readiness status, and recommended next step for future connector ideas.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Connector schema module | Complete | `agent_hub/connector_readiness_schema.py` defines fields, enums, validation, and design-only policy. |
| Connector demo dataset | Complete | `agent_hub/connector_readiness_data.py` includes 14 local/demo connector records. |
| Connector engine | Complete | `agent_hub/connector_readiness_engine.py` scores, filters, summarizes, checks policy, and emits Useful Signals. |
| Connectors UI | Complete | Metrics, filters, cards, readiness table, and connector-generated Useful Signals are visible. |
| Connector docs | Complete | `docs/CONNECTOR_READINESS_SIMULATOR.md` and `docs/CONNECTOR_SAFETY_GATES.md`. |
| Safety | Complete | All connectors remain `not_connected`; no OAuth, credentials, provider APIs, sends, writes, or webhooks. |

## HUB-V2-009 Local Workflow Simulation + Approval Gates

HUB-V2-009 adds a local/demo workflow simulation layer. The My Workflows page
now shows workflow metrics, workflow cards, Approval Gates, and
workflow-generated Useful Signals.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Workflow schema module | Complete | `agent_hub/workflow_simulation_schema.py` defines fields, enums, validation, and simulation-only policy. |
| Workflow demo dataset | Complete | `agent_hub/workflow_simulation_data.py` includes 4 local/demo workflow records. |
| Workflow engine | Complete | `agent_hub/workflow_simulation_engine.py` scores, filters, summarizes, checks policy, and emits Useful Signals. |
| Approval gate schema | Complete | `agent_hub/approval_gate_schema.py` defines gate fields, approval statuses, and allowed non-executing modes. |
| Approval gate engine | Complete | `agent_hub/approval_gate_engine.py` evaluates gates, summarizes them, and checks policy violations. |
| My Workflows UI | Complete | Metrics, workflow cards, Approval Gates table, and workflow-generated Useful Signals are visible. |
| Workflow docs | Complete | `docs/LOCAL_WORKFLOW_SIMULATION.md` and `docs/APPROVAL_GATE_PLANNER.md`. |
| Safety | Complete | All workflows remain local simulation only; no live connector, credentials, child scripts, real actions, remote changes, or git push. |

## HUB-V2-010 Demo Workflow Report Export

HUB-V2-010 adds a public-safe report export layer to the My Workflows page. It
turns local/demo metadata into Markdown, JSON, and CSV text reports for
portfolio review without enabling execution.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Report export schema | Complete | `agent_hub/report_export_schema.py` defines fields, formats, sections, output directory, safety notes, and policy validation. |
| Demo report builder | Complete | `agent_hub/demo_report_builder.py` builds Markdown, JSON, and CSV text from existing metadata registries. |
| Demo report exporter | Complete | `agent_hub/demo_report_exporter.py` writes only to `outputs/public_reports/`. |
| Report Export UI | Complete | My Workflows shows section selection, metrics, Markdown preview, JSON preview, CSV preview, and download controls. |
| Report docs | Complete | `docs/DEMO_WORKFLOW_REPORT_EXPORT.md`. |
| Safety | Complete | Reports are demo/local metadata only; no live connector, credentials, external API, child script, real action, git remote change, git push, or `outputs/private/`. |

## HUB-V2-011 Report Showcase / Screenshot Refresh

HUB-V2-011 refreshes the public-facing showcase layer after the V2 workflow,
connector, useful signal, action, prompt, onboarding, and report export surfaces
stabilized.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Screenshot refresh | Complete | 10 canonical V2-011 screenshots saved under `docs/images/`. |
| README screenshot links | Complete | README points to the new 10-image set with public-safe captions. |
| Screenshot guide | Complete | `docs/SCREENSHOTS_GUIDE.md` documents filenames, UI areas, and capture rules. |
| Showcase asset checklist | Complete | `docs/SHOWCASE_ASSET_CHECKLIST.md` tracks the V2-011 image set and sample report summary. |
| Sample report summary | Complete | `docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md` summarizes the latest public-safe report without dumping the full report into README. |
| Safety | Complete | No `.env`, credentials, secrets, private outputs, live connectors, child scripts, external APIs, real actions, git remote changes, or git push. |

## HUB-V2-012 Public Showcase Release Check

HUB-V2-012 performs the local release-readiness audit for the V2 public showcase
surface. It does not publish, commit, push, connect providers, or execute
actions.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| Release checklist | Complete | `docs/PUBLIC_RELEASE_CHECKLIST.md` records the final public-safe release gate. |
| Release readiness report | Complete | `docs/V2_RELEASE_READINESS_REPORT.md` records readiness, limitations, suggested commit message, and next stage. |
| README/docs consistency | Complete | README, screenshot guide, asset checklist, and public showcase manifest use the 10-image V2 screenshot set. |
| Manifest/contract validation | Complete | Root JSON files load and declare V2-012 release check metadata. |
| Output boundary | Complete | Generated public report files remain local artifacts; only `.gitkeep` is intended for git under `outputs/public_reports/`. |
| Git hygiene | Complete | `git status` and `git diff --stat` were reviewed; no add, commit, push, or remote modification is part of this stage. |
| Safety | Complete | No `.env`, credentials, secrets, private outputs, live connectors, child scripts, external APIs, real actions, git remote changes, git add, git commit, or git push. |

## HUB-V2-013 GitHub Showcase Update Decision

HUB-V2-013 reviews the working tree and creates a public commit/exclusion plan
for a future explicit GitHub update. It does not stage, commit, push, modify
remotes, or force push.

Local status:

| Area | Status | Notes |
| --- | --- | --- |
| GitHub update decision | Complete | `docs/GITHUB_SHOWCASE_UPDATE_DECISION.md` records the decision and release notes draft. |
| Public commit manifest | Complete | `docs/PUBLIC_COMMIT_FILE_MANIFEST.md` lists recommended public commit categories and a suggested future staging command. |
| Public exclusion manifest | Complete | `docs/PUBLIC_EXCLUSION_MANIFEST.md` lists generated, private, local-only, cache, and sibling-project exclusions. |
| Screenshot decision | Complete | The 10 canonical README screenshots are recommended for commit. |
| Output boundary decision | Complete | Only `outputs/public_reports/.gitkeep` is recommended under public reports; generated reports stay ignored. |
| Child manifest decision | Complete | 11 immediate manifests were scanned for public safety; sibling manifests are not part of this repo staging plan. |
| Safety | Complete | No `.env`, credentials, secrets, live connectors, child scripts, external APIs, real actions, git add, git commit, git push, remote changes, reset, clean, rm, or force push. |

## HUB-V2-014 Git Commit / Push / Live Showcase Verification

HUB-V2-014 performs the explicit public showcase publish step approved by the
user. It stages only the V2-013 commit-manifest file set, creates a normal
commit, pushes to the existing remote/current branch, and verifies the live
GitHub showcase surface.

Local and remote status:

| Area | Status | Notes |
| --- | --- | --- |
| Final validation | Complete | Pytest, compileall, Streamlit smoke, launcher smoke, UI visibility, JSON, and policy checks passed. |
| Exact staging | Complete | Staging source is `docs/PUBLIC_COMMIT_FILE_MANIFEST.md`; `git add .` is not used. |
| Generated reports | Excluded | Only `outputs/public_reports/.gitkeep` is staged; generated Markdown/JSON/CSV reports remain ignored. |
| Commit / push | Complete | Normal commit and push only; no remote modification and no force push. |
| Live verification | Complete | README, screenshot assets, docs, and remote tree are verified after push. |
| Safety | Complete | No `.env`, credentials, secrets, live connectors, child scripts, external APIs, real actions, generated reports, remote changes, reset, clean, rm, or force push. |

## HUB-V2-015 Profile Pin / Portfolio Placement Decision

HUB-V2-015 decides how AgentHubControlCenter should be positioned after the V2
public showcase update. It does not add product features, modify sibling
projects, call external APIs, connect providers, execute actions, commit, or
push.

Placement status:

| Area | Status | Notes |
| --- | --- | --- |
| Pin decision | Complete | `strongly recommend pin` because AgentHub is the portfolio hub for 12 local AI Agents and Skills after ClientDeliveryKitAgent import. |
| Repo About options | Complete | Three About description variants are documented in `docs/PROFILE_PIN_PORTFOLIO_DECISION.md`. |
| Topic suggestions | Complete | AI Agents, AI automation, workflow automation, command center, approval gates, connector readiness, local-first, and portfolio dashboard topics are recommended. |
| Portfolio positioning copy | Complete | `docs/PORTFOLIO_POSITIONING.md` includes one-line, summary, resume, LinkedIn/portfolio, and interview versions. |
| README first-screen check | Complete | Current first screen passes; a compact portfolio positioning line was added near the top. |
| Cross-project backlinks | Recommended next | Backlinks are useful, but should be handled in a separate explicit stage. |
| Safety | Complete | No `.env`, credentials, secrets, live connectors, child scripts, external APIs, real actions, sibling repo edits, remote changes, commit, or push. |

## HUB-V2-016 to HUB-V2-019 Portfolio Matrix Finalization

HUB-V2-016 through HUB-V2-019 connect the public portfolio surface into a
clearer hub-and-spoke system around AgentHubControlCenter.

Portfolio matrix status:

| Area | Status | Notes |
| --- | --- | --- |
| Cross-project backlink plan | Complete | Public-safe backlink wording was added to 10 child project READMEs. |
| Commit decision | Complete | Repo-by-repo commit and exclusion manifests were documented before push. |
| Explicit backlink commit | Complete | 8 git child repos were committed and pushed with exact files; 2 non-git folders were skipped. |
| Local-only projects | Documented | MarketSenseAgent and VideoExtractSkill remain local-only non-git directories. |
| IdeaScoreAgent exclusions | Documented | Deploy/report/bat artifacts remain untracked and excluded. |
| Portfolio Matrix README section | Complete | README now lists 12/12 projects with category, role, GitHub status, backlink status, manifest status, public-safe status, and next note. |

## CLIENTDELIVERYKIT-005 AgentHub Import And Showcase Prep

ClientDeliveryKitAgent is now documented as a published public spoke project in
the AgentHub portfolio matrix. This is a maintain-only metadata update, not an
AgentHub feature expansion.

| Check | Status | Notes |
| --- | --- | --- |
| Manifest discovery | Complete | `F:\AIProjects\ClientDeliveryKitAgent\agent_manifest.json` loads as a valid local manifest. |
| Portfolio matrix | Complete | Matrix now lists 12/12 local projects including ClientDeliveryKitAgent. |
| GitHub status | Published | `https://github.com/CHENXJC/ClientDeliveryKitAgent` |
| Backlink status | Live | ClientDeliveryKitAgent README links back to AgentHubControlCenter. |
| Public-safe status | Complete | ClientDeliveryKitAgent uses synthetic demo data only. |
| Next note | Optional | Profile pin review or maintain-showcase decision only. |
| Safety | Complete | No `.env`, credentials, live connectors, child scripts, real actions, remote changes, or force push in this maintain-only metadata sync. |

## CLIENTDELIVERYKIT-010 Published Status Sync

| Check | Status | Notes |
| --- | --- | --- |
| ClientDeliveryKitAgent live repo | Complete | Public repo verified at `https://github.com/CHENXJC/ClientDeliveryKitAgent`. |
| AgentHub portfolio matrix | Complete | ClientDeliveryKitAgent row is now published with repo URL and live backlink status. |
| Manifest status | Complete | Client manifest loads as `client_delivery_kit_agent` with `live_showcase_verified` public showcase status. |
| Public-safe status | Complete | Public-safe synthetic demo only; no real client data or live connector. |
| Next note | Complete | Optional profile pin / maintain showcase. |

## HUB-V2-020 Project Pause and Next Portfolio Gap Decision

HUB-V2-020 pauses AgentHubControlCenter feature expansion after the portfolio
hub reached showcase-ready status.

Pause status:

| Area | Status | Notes |
| --- | --- | --- |
| Pause decision | Complete | Decision is `pause_feature_expansion`. AgentHub should move to maintain-only mode. |
| Current coverage review | Complete | The portfolio covers AgentOps, business operations, career operations, idea validation, market intelligence, news intelligence, knowledge management, quant research, opportunity discovery, and content extraction. |
| Gap analysis | Complete | Main gap is client-facing delivery workflow and consultant-style handoff. |
| Top 3 next candidates | Complete | Client Delivery Kit Agent, SME Automation Demo Kit, and Data-to-Insight Workflow Agent. |
| Final recommendation | Complete | Start `ClientDeliveryKitAgent` as the next standalone spoke project if the user chooses to continue portfolio expansion. |
| Safety | Complete | Planning/docs only; no new project code, live connector, child script, real action, remote change, commit, push, or force push. |

## HUB-V2-022 Bilingual UI Toggle And Stage Sync Check

HUB-V2-022 improves the public demo usability of the Streamlit command center
without expanding AgentHub execution features.

UI/display status:

| Area | Status | Notes |
| --- | --- | --- |
| Language toggle | Complete | Sidebar supports `中文` and `English` through `st.session_state`. |
| Translation source | Complete | Local dictionary in `agent_hub/ui_i18n.py`; no translation API. |
| Default language | Complete | Chinese default for local use, English available for public review. |
| Main UI coverage | Complete | Sidebar, hero, metrics, tabs, Command Overview, My Tools, My Workflows, Useful Signals, Action Center, Connectors, Future Plugin Interface, Agent Onboarding, Codex Prompt Generator, Report Export, and safety copy. |
| Stage status sync | Complete | Sidebar shows Product Status, Latest Checkpoint, and Manifest Version separately; stale `HUB-V2-014` hard-code removed. |
| Stage status helper | Complete | `agent_hub/stage_status.py` reads `PROJECT_STATUS.md` and `agent_manifest.json` only. |
| Public-safe boundary | Complete | UI/display-only; no live connector, child script, external API, command execution, credential read, git remote change, commit, push, or force push. |

## HUB-005 Showcase Capabilities

- Product-style dashboard
- Screenshot-ready UI
- Command center hero section
- Six metric cards
- Agent detail panel
- Command pack display
- Health and priority cards
- Capability cluster cards
- Fixed project matrix view
- Enhanced Markdown portfolio report
- Command Center Summary report section
- Priority Action Summary
- Public Showcase Readiness report section
- Saved local report export flow
- Demo Workflow Report Export as Markdown, JSON, and CSV
- Refreshed V2-011 screenshot set covering Action Center, Useful Signals,
  Connectors, Workflow Simulation, Approval Gates, Report Export, Codex Prompt
  Generator, Agent Registry, Command Overview, and Agent Onboarding
- Public-safe sample demo workflow report summary
- V2 public release checklist and readiness report
- GitHub showcase update decision, public commit manifest, and public
  exclusion manifest
- Public-safe showcase asset checklist

## Prepared Screenshot Assets

- `docs/images/01_command_overview.png`
- `docs/images/02_agent_registry.png`
- `docs/images/03_action_center.png`
- `docs/images/04_codex_prompt_generator.png`
- `docs/images/05_useful_signals.png`
- `docs/images/06_workflow_simulation.png`
- `docs/images/07_connectors.png`
- `docs/images/08_agent_onboarding_metrics.png`
- `docs/images/09_report_export.png`
- `docs/images/10_approval_gates.png`

The next GitHub public showcase update should use the V2-011 refreshed
screenshots instead of the older HUB-006/HUB-V2-004 baseline screenshot set.

## Safety Boundary

This dashboard is for local portfolio management and workflow planning only. It
does not execute external actions or access private credentials.

The HUB-007 public release does not create `.env`, read credentials, call
external APIs, or use force push.

## Public Showcase Notes

- Registry entries describe existing portfolio projects.
- Health checks only inspect local path/file presence.
- Launch and command-pack strings are displayed as text and are not executed by
  the dashboard.
- README screenshots are captured from public-safe top-level UI regions.
- Exported reports are generated from local registry, validation, health, and
  next-action data.
- Saved reports are local `outputs/` artifacts and are ignored by git except
  `outputs/.gitkeep` and `outputs/public_reports/.gitkeep`.
