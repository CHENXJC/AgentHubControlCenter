# Showcase Asset Checklist

Use this checklist before preparing or publishing the GitHub public showcase.

## HUB-006 Asset Status

| Asset | Status | Location / Notes |
| --- | --- | --- |
| Command Center Overview screenshot | Complete | `docs/images/01_command_center_home.png` |
| Portfolio Metrics screenshot | Complete | `docs/images/02_portfolio_metrics.png` |
| Project Matrix View screenshot | Complete | `docs/images/03_project_matrix_view.png` |
| Priority Action Summary screenshot | Complete | `docs/images/04_priority_action_summary.png` |
| Report Export Preview screenshot | Complete | `docs/images/05_report_export_preview.png` |
| Public Showcase Readiness screenshot | Complete | `docs/images/06_public_showcase_readiness.png` |
| README screenshot section | Complete | Relative paths point to `docs/images/`. |
| Public showcase manifest | Complete | `docs/PUBLIC_SHOWCASE_MANIFEST.md` |
| Screenshot guide | Complete | `docs/SCREENSHOTS_GUIDE.md` |
| Project plan | Complete | `docs/PROJECT_PLAN.md` |
| Project status | Complete | `PROJECT_STATUS.md` |
| Pytest | Complete | `python -m pytest` passed: 24 tests passed. |
| Compile check | Complete | `python -m compileall agent_hub app.py` passed. |
| Streamlit smoke check | Complete | Local app opened for screenshot capture. |

## HUB-007 GitHub Public Release Status

| Asset / Release Item | Status | Location / Notes |
| --- | --- | --- |
| Public GitHub repository | Complete | <https://github.com/CHENXJC/AgentHubControlCenter> |
| Main branch | Complete | `main` exists on GitHub. |
| README GitHub rendering | Complete | README displays on the repository page. |
| README screenshot rendering | Complete | Screenshot links use `docs/images/`. |
| About description | Complete | Repository About description is filled. |
| Topics | Complete | Repository topics are added. |
| Latest published base commit | Complete | `1170134` |
| Profile Pin | Pending | Pending user decision. |

## HUB-V2-001 Local Command Center Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Command Overview | Complete | `app.py` tab: Command Overview |
| My Tools / Agent Registry | Complete | `app.py` tab: My Tools / Agent Registry |
| My Workflows | Complete | `app.py` tab: My Workflows |
| Useful Signals | Complete | `app.py` tab: Useful Signals |
| Action Center | Complete | `app.py` tab: Action Center |
| Connectors | Complete | `app.py` tab: Connectors |
| Future Plugin Interface | Complete | `app.py` tab: Future Plugin Interface |
| Agent manifest example | Complete | `agent_manifest.json` |
| Agent contract example | Complete | `agent_contract.json` |
| Agent interface standard | Complete | `docs/AGENT_INTERFACE_STANDARD.md` |
| Future plugin interface | Complete | `docs/FUTURE_PLUGIN_INTERFACE.md` |
| Desktop launcher guide | Complete | `docs/DESKTOP_LAUNCHER_GUIDE.md` |
| Windows launcher | Complete | `launch_command_center.cmd` |
| Desktop shortcut script | Complete | `scripts/create_desktop_shortcut.ps1` |

## HUB-V2-002 Manifest Import Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Manifest loader module | Complete | `agent_hub/manifest_loader.py` |
| Agent onboarding module | Complete | `agent_hub/agent_onboarding.py` |
| Manifest loader tests | Complete | `tests/test_manifest_loader.py` |
| Agent onboarding tests | Complete | `tests/test_agent_onboarding.py` |
| Manifest import guide | Complete | `docs/MANIFEST_IMPORT_GUIDE.md` |
| Agent onboarding flow guide | Complete | `docs/AGENT_ONBOARDING_FLOW.md` |
| Onboarding UI | Complete | Future Plugin Interface tab |
| Pytest | Complete | `.venv\Scripts\python.exe -m pytest` passed: 37 tests passed. |
| Compile check | Complete | `.venv\Scripts\python.exe -m compileall .` passed. |
| Streamlit smoke check | Complete | `http://localhost:8525` returned HTTP 200. |

## HUB-V2-003 Child Manifest Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| BusinessOpsAgent manifest | Complete | `F:\AIProjects\BusinessOpsAgent\agent_manifest.json` |
| CareerPilotAgent manifest | Complete | `F:\AIProjects\CareerPilotAgent\agent_manifest.json` |
| IdeaScoreAgent manifest | Complete | `F:\AIProjects\IdeaScoreAgent\agent_manifest.json` |
| MarketSenseAgent manifest | Complete | `F:\AIProjects\MarketSenseAgent\agent_manifest.json` |
| NewsSignalAgent manifest | Complete | `F:\AIProjects\NewsSignalAgent\agent_manifest.json` |
| NextOpsAgent manifest | Complete | `F:\AIProjects\NextOpsAgent\agent_manifest.json` |
| PersonalKnowledgeAgent manifest | Complete | `F:\AIProjects\PersonalKnowledgeAgent\agent_manifest.json` |
| QuantLabAgent manifest | Complete | `F:\AIProjects\QuantLabAgent\agent_manifest.json` |
| SocialPainFinderAgent manifest | Complete | `F:\AIProjects\SocialPainFinderAgent\agent_manifest.json` |
| VideoExtractSkill manifest | Complete | `F:\AIProjects\VideoExtractSkill\agent_manifest.json` |
| Discovery result | Complete | 11 valid manifests, 0 invalid, 0 missing. |
| Pytest | Complete | `.venv\Scripts\python.exe -m pytest` passed: 38 tests passed. |
| Compile check | Complete | `.venv\Scripts\python.exe -m compileall .` passed. |
| Streamlit smoke check | Complete | `http://localhost:8525` returned HTTP 200. |
| Agent Onboarding UI check | Complete | Streamlit AppTest confirmed 11 valid manifests and 0 missing/invalid manifests. |
| Launcher smoke check | Complete | `launch_command_center.cmd` returned HTTP 200 on fixed port 8525. |
| V2 onboarding screenshots | Complete | Superseded by HUB-V2-004 screenshot refresh below. |

## HUB-V2-004 V2 Screenshot Refresh Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Command Overview screenshot | Complete | `docs/images/01_command_center_home.png` |
| My Tools / Agent Registry screenshot | Complete | `docs/images/02_portfolio_metrics.png` shows 11 available tools and reviewed Agent cards. |
| My Workflows screenshot | Complete | `docs/images/03_project_matrix_view.png` |
| Action Center screenshot | Complete | `docs/images/04_priority_action_summary.png` |
| Future Plugin Interface screenshot | Complete | `docs/images/05_report_export_preview.png` shows imported manifest Agents without default local path columns. |
| Useful Signals screenshot | Complete | `docs/images/06_public_showcase_readiness.png` |
| Connectors screenshot | Complete | `docs/images/07_connectors.png` |
| Agent Onboarding metrics screenshot | Complete | `docs/images/08_agent_onboarding_metrics.png` shows 11 valid, 0 invalid, 0 missing. |
| Agent card wording review | Complete | Cards show readable category labels, source badges, demo mode, safe mode, display-only actions, and connector previews. |
| Public-safe screenshot review | Complete | No `.env`, token, API key, password, credential, or private customer data visible. |

## HUB-V2-005 Local Action Schema Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Action schema module | Complete | `agent_hub/action_schema.py` |
| Action registry module | Complete | `agent_hub/action_registry.py` |
| Action schema tests | Complete | `tests/test_action_schema.py` |
| Action registry tests | Complete | `tests/test_action_registry.py` |
| Action schema docs | Complete | `docs/ACTION_SCHEMA.md` |
| Manual runbook | Complete | `docs/MANUAL_RUNBOOK.md` |
| Action safety policy | Complete | `docs/ACTION_SAFETY_POLICY.md` |
| Manifest action upgrade | Complete | 11 manifests declare 55 schema-backed actions. |
| Action Center metrics | Complete | Total, manual-only, display-only, future connector, approval, and blocked metrics visible. |
| Codex prompt reservation | Complete | `codex_prompt` action type is template-only for HUB-V2-006. |

## HUB-V2-006 Codex Prompt Generator Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Prompt generator module | Complete | `agent_hub/codex_prompt_generator.py` |
| Prompt generator tests | Complete | `tests/test_codex_prompt_generator.py` |
| Prompt generator docs | Complete | `docs/CODEX_PROMPT_GENERATOR.md` |
| Action Center UI | Complete | `app.py` section: Codex Prompt Generator |
| Supported prompt types | Complete | `continue_next_stage`, `fix_or_polish`, `github_showcase_update` |
| Reserved prompt types | Complete | `add_manifest`, `refresh_screenshots`, `run_tests_only`, `create_connector_plan`, `generate_report` |
| Text-only safety policy | Complete | Generated prompts are preview/download text only; no auto-send and no execution. |

## HUB-V2-007 Useful Signals Engine Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Useful signal schema module | Complete | `agent_hub/useful_signal_schema.py` |
| Useful signal data module | Complete | `agent_hub/useful_signal_data.py` |
| Useful signal engine module | Complete | `agent_hub/useful_signal_engine.py` |
| Useful signal tests | Complete | `tests/test_useful_signal_schema.py`, `tests/test_useful_signal_engine.py` |
| Useful signal docs | Complete | `docs/USEFUL_SIGNALS_ENGINE.md` |
| Useful Signals UI | Complete | `app.py` tab: Useful Signals |
| Signal metrics | Complete | Total, high-value, needs-action, watchlist, ignored/low-priority, and average usefulness. |
| Signal sections | Complete | Top 5 Useful Signals, Needs Action, Watchlist, Low Priority / Ignored. |
| Display-only safety policy | Complete | Recommendations are text-only and no real action is executed. |

## HUB-V2-008 Connector Readiness Simulator Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Connector readiness schema module | Complete | `agent_hub/connector_readiness_schema.py` |
| Connector readiness data module | Complete | `agent_hub/connector_readiness_data.py` |
| Connector readiness engine module | Complete | `agent_hub/connector_readiness_engine.py` |
| Connector readiness tests | Complete | `tests/test_connector_readiness_schema.py`, `tests/test_connector_readiness_engine.py` |
| Connector readiness docs | Complete | `docs/CONNECTOR_READINESS_SIMULATOR.md` |
| Connector safety gates docs | Complete | `docs/CONNECTOR_SAFETY_GATES.md` |
| Connectors UI | Complete | `app.py` tab: Connectors |
| Readiness metrics | Complete | Total, design-only, ready-for-demo, needs-review, blocked, high-risk, and average readiness. |
| Display-only safety policy | Complete | All connector records are `not_connected`; no OAuth, credentials, API calls, sends, writes, webhooks, or pushes. |

## HUB-V2-009 Local Workflow Simulation + Approval Gates Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Workflow simulation schema module | Complete | `agent_hub/workflow_simulation_schema.py` |
| Workflow simulation data module | Complete | `agent_hub/workflow_simulation_data.py` |
| Workflow simulation engine module | Complete | `agent_hub/workflow_simulation_engine.py` |
| Approval gate schema module | Complete | `agent_hub/approval_gate_schema.py` |
| Approval gate engine module | Complete | `agent_hub/approval_gate_engine.py` |
| Workflow simulation tests | Complete | `tests/test_workflow_simulation_schema.py`, `tests/test_workflow_simulation_engine.py`, `tests/test_approval_gate_engine.py` |
| Workflow simulation docs | Complete | `docs/LOCAL_WORKFLOW_SIMULATION.md` |
| Approval gate docs | Complete | `docs/APPROVAL_GATE_PLANNER.md` |
| My Workflows UI | Complete | `app.py` tab: My Workflows |
| Workflow metrics | Complete | Total demo workflows, manual review, blocked steps, manual-only steps, template-only outputs, approval gates, average readiness. |
| Approval Gates table | Complete | Shows action/connector, risk, approval status, checks, allowed execution mode, and block reason. |
| Simulation-only safety policy | Complete | No live connector, credentials, child scripts, real actions, remote changes, or git push. |

## HUB-V2-010 Demo Workflow Report Export Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Report export schema module | Complete | `agent_hub/report_export_schema.py` |
| Demo report builder module | Complete | `agent_hub/demo_report_builder.py` |
| Demo report exporter module | Complete | `agent_hub/demo_report_exporter.py` |
| Report export tests | Complete | `tests/test_demo_report_builder.py`, `tests/test_demo_report_exporter.py` |
| Report export docs | Complete | `docs/DEMO_WORKFLOW_REPORT_EXPORT.md` |
| Public reports folder marker | Complete | `outputs/public_reports/.gitkeep` |
| My Workflows UI | Complete | `app.py` section: Demo Workflow Report Export |
| Report export metrics | Complete | Available sections, export formats, public-safe status, and target report path. |
| Text previews | Complete | Markdown, JSON, and CSV preview/download content. |
| Public-safe export policy | Complete | No credentials, live connectors, external API calls, child scripts, real actions, git remote changes, git push, or `outputs/private/`. |

## HUB-V2-011 Report Showcase / Screenshot Refresh Status

| Asset / Interface Item | Status | Location / Notes |
| --- | --- | --- |
| Command Overview screenshot | Complete | `docs/images/01_command_overview.png` |
| Agent Registry screenshot | Complete | `docs/images/02_agent_registry.png` |
| Action Center screenshot | Complete | `docs/images/03_action_center.png` |
| Codex Prompt Generator screenshot | Complete | `docs/images/04_codex_prompt_generator.png` |
| Useful Signals screenshot | Complete | `docs/images/05_useful_signals.png` |
| Workflow Simulation screenshot | Complete | `docs/images/06_workflow_simulation.png` |
| Connectors screenshot | Complete | `docs/images/07_connectors.png` |
| Agent Onboarding metrics screenshot | Complete | `docs/images/08_agent_onboarding_metrics.png` |
| Report Export screenshot | Complete | `docs/images/09_report_export.png` |
| Approval Gates screenshot | Complete | `docs/images/10_approval_gates.png` |
| README screenshot section | Complete | Uses the V2-011 canonical 10-image set. |
| Screenshot guide | Complete | `docs/SCREENSHOTS_GUIDE.md` documents capture order and public-safe rules. |
| Sample report summary | Complete | `docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md` summarizes the latest public-safe demo report without dumping the full report into README. |
| Public-safe screenshot review | Complete | No `.env`, secret, token, password, API key, credential, private output, live connector data, or real execution visible. |

## HUB-V2-012 Public Showcase Release Check Status

| Asset / Release Item | Status | Location / Notes |
| --- | --- | --- |
| Public release checklist | Complete | `docs/PUBLIC_RELEASE_CHECKLIST.md` |
| V2 release readiness report | Complete | `docs/V2_RELEASE_READINESS_REPORT.md` |
| README screenshot references | Complete | All 10 current README image paths exist under `docs/images/`. |
| Screenshot inventory | Complete | 10 canonical V2 screenshots verified. |
| Sample report summary | Complete | Compact public-safe summary only; full report is not dumped into README. |
| Manifest and contract JSON | Complete | Root `agent_manifest.json` and `agent_contract.json` load successfully. |
| Child manifests | Complete | 11 immediate Agent manifests load successfully. |
| Output boundary | Complete | `outputs/public_reports/` generated files remain ignored; `.gitkeep` is the intended tracked marker. |
| Private outputs | Complete | `outputs/private/` absent. |
| Launcher | Complete | `launch_command_center.cmd` uses `.venv` and fixed port `8525`. |
| Git hygiene | Complete | Review-only stage; no git add, commit, push, or remote modification. |

## HUB-V2-013 GitHub Showcase Update Decision Status

| Asset / Release Item | Status | Location / Notes |
| --- | --- | --- |
| GitHub showcase update decision | Complete | `docs/GITHUB_SHOWCASE_UPDATE_DECISION.md` |
| Public commit file manifest | Complete | `docs/PUBLIC_COMMIT_FILE_MANIFEST.md` |
| Public exclusion manifest | Complete | `docs/PUBLIC_EXCLUSION_MANIFEST.md` |
| Recommended screenshot commit set | Complete | 10 canonical README screenshots under `docs/images/` |
| Historical screenshot decision | Complete | Six older public-safe screenshots may be committed with the image set for legacy checklist continuity. |
| Output boundary decision | Complete | Commit `outputs/public_reports/.gitkeep` only; exclude generated Markdown/JSON/CSV reports. |
| Suggested staging command | Complete | Documented for a future explicit HUB-V2-014 stage; not executed in V2-013. |
| Git hygiene | Complete | No git add, commit, push, reset, clean, rm, remote modification, or force push. |

## HUB-V2-014 Git Commit / Push / Live Verification Status

| Asset / Release Item | Status | Location / Notes |
| --- | --- | --- |
| Exact public staging source | Complete | `docs/PUBLIC_COMMIT_FILE_MANIFEST.md` |
| Public-safe exclusion source | Complete | `docs/PUBLIC_EXCLUSION_MANIFEST.md` |
| Local final validation | Complete | Pytest, compileall, Streamlit smoke, launcher smoke, UI, JSON, and policy checks passed. |
| Generated report exclusion | Complete | Only `outputs/public_reports/.gitkeep` is staged; generated Markdown/JSON/CSV reports stay ignored. |
| Normal commit and push | Complete | Existing remote/current branch only; no remote modification and no force push. |
| Live README and screenshot check | Complete | GitHub README and canonical screenshot assets are verified after push. |
| Remote unsafe artifact check | Complete | Remote tree checked for `.env`, credentials, `.venv`, private outputs, caches, and generated reports. |

## Public-Safe Asset Rules

- Do not include `.env`, credentials, tokens, customer data, private documents,
  private screenshots, or generated private reports.
- Review local path visibility before publishing screenshots.
- Keep generated reports in `outputs/public_reports/` for this stage; generated
  report files remain local output artifacts and should be reviewed before any
  public release.
- Do not run external actions, initialize a remote, modify git remote settings,
  or push to GitHub during screenshot preparation.

## README Screenshot Order

1. `01_command_overview.png`
2. `02_agent_registry.png`
3. `03_action_center.png`
4. `04_codex_prompt_generator.png`
5. `05_useful_signals.png`
6. `06_workflow_simulation.png`
7. `07_connectors.png`
8. `08_agent_onboarding_metrics.png`
9. `09_report_export.png`
10. `10_approval_gates.png`
