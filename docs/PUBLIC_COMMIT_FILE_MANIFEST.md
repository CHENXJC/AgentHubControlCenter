# Public Commit File Manifest

Checkpoint:
`HUB-V2-014-GIT-COMMIT-PUSH-LIVE-SHOWCASE-VERIFICATION-COMPLETE`

This manifest lists the files selected for the public showcase commit. It was
prepared in HUB-V2-013 and used as the exact staging source in HUB-V2-014 after
explicit user approval.

## Files Recommended For Commit

### Core App

- `.gitignore`
- `app.py`
- `data/agent_registry.csv`

Why commit: these files contain the V2 app stage label, UI surfaces, local
registry metadata, and public-safe ignore boundaries.

### Existing `agent_hub` Modules

- `agent_hub/__init__.py`
- `agent_hub/portfolio_matrix.py`
- `agent_hub/report_builder.py`
- `agent_hub/report_exporter.py`

Why commit: these tracked modules were changed by earlier V2 work and are part
of the current verified app behavior.

### New `agent_hub` Modules

- `agent_hub/action_registry.py`
- `agent_hub/action_schema.py`
- `agent_hub/agent_interface.py`
- `agent_hub/agent_onboarding.py`
- `agent_hub/approval_gate_engine.py`
- `agent_hub/approval_gate_schema.py`
- `agent_hub/codex_prompt_generator.py`
- `agent_hub/connector_readiness_data.py`
- `agent_hub/connector_readiness_engine.py`
- `agent_hub/connector_readiness_schema.py`
- `agent_hub/demo_report_builder.py`
- `agent_hub/demo_report_exporter.py`
- `agent_hub/manifest_loader.py`
- `agent_hub/report_export_schema.py`
- `agent_hub/useful_signal_data.py`
- `agent_hub/useful_signal_engine.py`
- `agent_hub/useful_signal_schema.py`
- `agent_hub/workflow_simulation_data.py`
- `agent_hub/workflow_simulation_engine.py`
- `agent_hub/workflow_simulation_schema.py`

Why commit: these modules implement the local-only V2 metadata, simulation,
prompt, action, connector readiness, workflow, approval gate, onboarding, and
demo report layers.

### Manifests And Contracts

- `agent_manifest.json`
- `agent_contract.json`

Why commit: these root files document the AgentHubControlCenter public-safe
manifest, action schema, connector policy, and release readiness contract.

### Documentation

- `docs/ACTION_SAFETY_POLICY.md`
- `docs/ACTION_SCHEMA.md`
- `docs/AGENT_INTERFACE_STANDARD.md`
- `docs/AGENT_ONBOARDING_FLOW.md`
- `docs/APPROVAL_GATE_PLANNER.md`
- `docs/CHILD_AGENT_MANIFEST_SUMMARY.md`
- `docs/CODEX_PROMPT_GENERATOR.md`
- `docs/CONNECTOR_READINESS_SIMULATOR.md`
- `docs/CONNECTOR_SAFETY_GATES.md`
- `docs/DEMO_WORKFLOW_REPORT_EXPORT.md`
- `docs/DESKTOP_LAUNCHER_GUIDE.md`
- `docs/FUTURE_PLUGIN_INTERFACE.md`
- `docs/GITHUB_SHOWCASE_UPDATE_DECISION.md`
- `docs/LOCAL_WORKFLOW_SIMULATION.md`
- `docs/MANIFEST_IMPORT_GUIDE.md`
- `docs/MANUAL_RUNBOOK.md`
- `docs/PROJECT_PLAN.md`
- `docs/PUBLIC_COMMIT_FILE_MANIFEST.md`
- `docs/PUBLIC_EXCLUSION_MANIFEST.md`
- `docs/PUBLIC_RELEASE_CHECKLIST.md`
- `docs/PUBLIC_SHOWCASE_MANIFEST.md`
- `docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md`
- `docs/SCREENSHOTS_GUIDE.md`
- `docs/SHOWCASE_ASSET_CHECKLIST.md`
- `docs/USEFUL_SIGNALS_ENGINE.md`
- `docs/V2_RELEASE_READINESS_REPORT.md`
- `PROJECT_STATUS.md`
- `README.md`

Why commit: these files describe the public showcase, manual runbooks, safety
policies, screenshots, report summary, release readiness, and V2-013 commit
decision.

### Screenshots

Canonical V2 screenshots required by README:

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

Historical tracked screenshots that are public-safe and referenced by older
checklist sections:

- `docs/images/01_command_center_home.png`
- `docs/images/02_portfolio_metrics.png`
- `docs/images/03_project_matrix_view.png`
- `docs/images/04_priority_action_summary.png`
- `docs/images/05_report_export_preview.png`
- `docs/images/06_public_showcase_readiness.png`

Why commit: the 10 canonical screenshots are the current README showcase set.
The six historical screenshots remain useful for legacy checklist sections and
are public-safe.

### Launch Scripts

- `launch_command_center.cmd`
- `scripts/create_desktop_shortcut.ps1`

Why commit: these provide the local Windows launcher path for port `8525` and
do not read credentials or call external APIs.

### Tests

- `tests/test_action_registry.py`
- `tests/test_action_schema.py`
- `tests/test_agent_interface.py`
- `tests/test_agent_onboarding.py`
- `tests/test_approval_gate_engine.py`
- `tests/test_codex_prompt_generator.py`
- `tests/test_connector_readiness_engine.py`
- `tests/test_connector_readiness_schema.py`
- `tests/test_demo_report_builder.py`
- `tests/test_demo_report_exporter.py`
- `tests/test_github_showcase_decision.py`
- `tests/test_manifest_loader.py`
- `tests/test_portfolio_matrix.py`
- `tests/test_public_release_readiness.py`
- `tests/test_showcase_assets.py`
- `tests/test_useful_signal_engine.py`
- `tests/test_useful_signal_schema.py`
- `tests/test_workflow_simulation_engine.py`
- `tests/test_workflow_simulation_schema.py`

Why commit: tests prove schema validation, UI metadata, release readiness,
public-safe docs, and policy boundaries.

### Output Boundary Marker

- `outputs/public_reports/.gitkeep`

Why commit: this keeps the public-safe report output folder visible while
generated report files remain ignored.

## Files Intentionally Excluded

See `docs/PUBLIC_EXCLUSION_MANIFEST.md` for the exclusion table. The key
exclusions are `.venv/`, `.env`, secrets, generated report files, `outputs/private/`,
logs, caches, `AGENTS.md`, and sibling project files.

## Child Agent Manifest Inventory

The immediate `F:\AIProjects` manifests were scanned for JSON validity and
secret-like values. They are not included in this repo staging plan except for
the root `agent_manifest.json`.

| Project | Agent ID | Commit In This Repo |
| --- | --- | --- |
| AgentHubControlCenter | `agent_hub_control_center` | Yes |
| BusinessOpsAgent | `business_ops_agent` | No, sibling repo |
| CareerPilotAgent | `career_pilot_agent` | No, sibling repo |
| IdeaScoreAgent | `idea_score_agent` | No, sibling repo |
| MarketSenseAgent | `market_sense_agent` | No, sibling repo |
| NewsSignalAgent | `news_signal_agent` | No, sibling repo |
| NextOpsAgent | `next_ops_agent` | No, sibling repo |
| PersonalKnowledgeAgent | `personal_knowledge_agent` | No, sibling repo |
| QuantLabAgent | `quant_lab_agent` | No, sibling repo |
| SocialPainFinderAgent | `social_pain_finder_agent` | No, sibling repo |
| VideoExtractSkill | `video_extract_skill` | No, sibling repo |

## Risk Notes

- The staging set is large because it combines HUB-V2-001 through HUB-V2-013
  local work into one public showcase upgrade.
- The six historical screenshots are safe, but the README only requires the 10
  canonical V2 screenshots.
- `launch_command_center.cmd` and `scripts/create_desktop_shortcut.ps1` contain
  local `F:\AIProjects\AgentHubControlCenter` paths by design; these are project
  setup paths, not secrets.
- Generated reports under `outputs/public_reports/` should stay local until a
  separate explicit review approves publishing them.

## Suggested Staging Command

Do not run this command in HUB-V2-013. It is for the explicit
`HUB-V2-014-GIT-COMMIT-PUSH` stage only, after final validation and safety
checks.

```powershell
$files = @(
    ".gitignore",
    "PROJECT_STATUS.md",
    "README.md",
    "agent_contract.json",
    "agent_manifest.json",
    "app.py",
    "data/agent_registry.csv",
    "agent_hub/__init__.py",
    "agent_hub/portfolio_matrix.py",
    "agent_hub/report_builder.py",
    "agent_hub/report_exporter.py",
    "agent_hub/action_registry.py",
    "agent_hub/action_schema.py",
    "agent_hub/agent_interface.py",
    "agent_hub/agent_onboarding.py",
    "agent_hub/approval_gate_engine.py",
    "agent_hub/approval_gate_schema.py",
    "agent_hub/codex_prompt_generator.py",
    "agent_hub/connector_readiness_data.py",
    "agent_hub/connector_readiness_engine.py",
    "agent_hub/connector_readiness_schema.py",
    "agent_hub/demo_report_builder.py",
    "agent_hub/demo_report_exporter.py",
    "agent_hub/manifest_loader.py",
    "agent_hub/report_export_schema.py",
    "agent_hub/useful_signal_data.py",
    "agent_hub/useful_signal_engine.py",
    "agent_hub/useful_signal_schema.py",
    "agent_hub/workflow_simulation_data.py",
    "agent_hub/workflow_simulation_engine.py",
    "agent_hub/workflow_simulation_schema.py",
    "docs/ACTION_SAFETY_POLICY.md",
    "docs/ACTION_SCHEMA.md",
    "docs/AGENT_INTERFACE_STANDARD.md",
    "docs/AGENT_ONBOARDING_FLOW.md",
    "docs/APPROVAL_GATE_PLANNER.md",
    "docs/CHILD_AGENT_MANIFEST_SUMMARY.md",
    "docs/CODEX_PROMPT_GENERATOR.md",
    "docs/CONNECTOR_READINESS_SIMULATOR.md",
    "docs/CONNECTOR_SAFETY_GATES.md",
    "docs/DEMO_WORKFLOW_REPORT_EXPORT.md",
    "docs/DESKTOP_LAUNCHER_GUIDE.md",
    "docs/FUTURE_PLUGIN_INTERFACE.md",
    "docs/GITHUB_SHOWCASE_UPDATE_DECISION.md",
    "docs/LOCAL_WORKFLOW_SIMULATION.md",
    "docs/MANIFEST_IMPORT_GUIDE.md",
    "docs/MANUAL_RUNBOOK.md",
    "docs/PROJECT_PLAN.md",
    "docs/PUBLIC_COMMIT_FILE_MANIFEST.md",
    "docs/PUBLIC_EXCLUSION_MANIFEST.md",
    "docs/PUBLIC_RELEASE_CHECKLIST.md",
    "docs/PUBLIC_SHOWCASE_MANIFEST.md",
    "docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md",
    "docs/SCREENSHOTS_GUIDE.md",
    "docs/SHOWCASE_ASSET_CHECKLIST.md",
    "docs/USEFUL_SIGNALS_ENGINE.md",
    "docs/V2_RELEASE_READINESS_REPORT.md",
    "docs/images/01_command_center_home.png",
    "docs/images/02_portfolio_metrics.png",
    "docs/images/03_project_matrix_view.png",
    "docs/images/04_priority_action_summary.png",
    "docs/images/05_report_export_preview.png",
    "docs/images/06_public_showcase_readiness.png",
    "docs/images/01_command_overview.png",
    "docs/images/02_agent_registry.png",
    "docs/images/03_action_center.png",
    "docs/images/04_codex_prompt_generator.png",
    "docs/images/05_useful_signals.png",
    "docs/images/06_workflow_simulation.png",
    "docs/images/07_connectors.png",
    "docs/images/08_agent_onboarding_metrics.png",
    "docs/images/09_report_export.png",
    "docs/images/10_approval_gates.png",
    "launch_command_center.cmd",
    "scripts/create_desktop_shortcut.ps1",
    "outputs/public_reports/.gitkeep",
    "tests/test_action_registry.py",
    "tests/test_action_schema.py",
    "tests/test_agent_interface.py",
    "tests/test_agent_onboarding.py",
    "tests/test_approval_gate_engine.py",
    "tests/test_codex_prompt_generator.py",
    "tests/test_connector_readiness_engine.py",
    "tests/test_connector_readiness_schema.py",
    "tests/test_demo_report_builder.py",
    "tests/test_demo_report_exporter.py",
    "tests/test_github_showcase_decision.py",
    "tests/test_manifest_loader.py",
    "tests/test_portfolio_matrix.py",
    "tests/test_public_release_readiness.py",
    "tests/test_showcase_assets.py",
    "tests/test_useful_signal_engine.py",
    "tests/test_useful_signal_schema.py",
    "tests/test_workflow_simulation_engine.py",
    "tests/test_workflow_simulation_schema.py"
)
git add -- $files
```
