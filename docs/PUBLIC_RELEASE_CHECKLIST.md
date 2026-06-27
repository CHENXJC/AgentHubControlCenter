# Public Release Checklist

Status: HUB-V2-014-GIT-COMMIT-PUSH-LIVE-SHOWCASE-VERIFICATION-COMPLETE

This checklist is the final local public-showcase gate for the AgentHubControlCenter
V2 update. It is a review artifact only. It does not run real actions, connect
providers, change git remotes, create commits, or push to GitHub.

## Release Scope

| Area | Status | Evidence |
| --- | --- | --- |
| Current checkpoint | Ready | `HUB-V2-012-PUBLIC-SHOWCASE-RELEASE-CHECK-COMPLETE` |
| README screenshot paths | Ready | README references the 10 V2-011 canonical PNG files under `docs/images/`. |
| README capability claims | Ready | README describes local/demo metadata, connector readiness, workflow simulation, report export, and release check boundaries. |
| Showcase docs | Ready | `PUBLIC_SHOWCASE_MANIFEST.md`, `SHOWCASE_ASSET_CHECKLIST.md`, and `SCREENSHOTS_GUIDE.md` are aligned with the 10-image V2 set. |
| Sample report summary | Ready | `SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md` is compact and public-safe. |
| Manifest and contract | Ready | Root JSON files load and declare V2-012 release check metadata. |
| Child manifests | Ready | 11 `agent_manifest.json` files load from immediate Agent project folders. |
| Launcher | Ready | `launch_command_center.cmd` uses `.venv` and fixed port `8525`. |
| Public reports boundary | Ready | `outputs/public_reports/` keeps generated reports local; only `.gitkeep` is intended for git. |
| Private outputs boundary | Ready | `outputs/private/` is absent. |

## Required Public-Safe Statements

The public showcase must keep these statements visible in README/docs:

- Demo/local metadata only
- No live connector connected
- No credentials loaded
- No real action executed
- No external API called
- Public-safe demo reports

## Screenshot Inventory

| File | Status | Showcase Area |
| --- | --- | --- |
| `docs/images/01_command_overview.png` | Ready | Command Overview |
| `docs/images/02_agent_registry.png` | Ready | Agent Registry |
| `docs/images/03_action_center.png` | Ready | Action Center |
| `docs/images/04_codex_prompt_generator.png` | Ready | Codex Prompt Generator |
| `docs/images/05_useful_signals.png` | Ready | Useful Signals |
| `docs/images/06_workflow_simulation.png` | Ready | Workflow Simulation |
| `docs/images/07_connectors.png` | Ready | Connector Readiness |
| `docs/images/08_agent_onboarding_metrics.png` | Ready | Agent Onboarding |
| `docs/images/09_report_export.png` | Ready | Report Export |
| `docs/images/10_approval_gates.png` | Ready | Approval Gates |

## Git Hygiene

- `git status` and `git diff --stat` are allowed for review.
- `git add`, `git commit`, and `git push` are not part of this checkpoint.
- Git remote settings must not be changed in this checkpoint.
- Suggested commit message is documented in
  `docs/V2_RELEASE_READINESS_REPORT.md` for a future explicit commit stage.

## Output Boundary

- `.venv/` is ignored.
- `.env`, `.env.*`, `credentials.json`, `token.json`, `*.pem`, `*.key`, and
  `secrets.toml` are ignored.
- `outputs/*` is ignored by default.
- `outputs/public_reports/.gitkeep` is the only intended tracked file under
  `outputs/public_reports/`.
- Generated Markdown/JSON/CSV report files under `outputs/public_reports/`
  remain local artifacts unless separately reviewed and explicitly approved.
- `outputs/private/` must not be created.

## Release Decision

Release readiness: Ready for a separate explicit commit/push decision.

This checkpoint does not publish. The next stage should only commit/push if the
user explicitly asks for a GitHub update.

## HUB-V2-013 GitHub Showcase Update Decision

Status: HUB-V2-013-GITHUB-SHOWCASE-UPDATE-DECISION-COMPLETE

The GitHub showcase update decision is complete. The current working tree has
been classified into public commit candidates and intentional exclusions.

Decision artifacts:

- `docs/GITHUB_SHOWCASE_UPDATE_DECISION.md`
- `docs/PUBLIC_COMMIT_FILE_MANIFEST.md`
- `docs/PUBLIC_EXCLUSION_MANIFEST.md`

Decision result:

- Recommended public commit files are documented.
- Excluded generated/private/local-only files are documented.
- The 10 canonical README screenshots are recommended for commit.
- `outputs/public_reports/.gitkeep` is recommended for commit.
- Generated `outputs/public_reports/*.md`, `*.json`, and `*.csv` files are not
  recommended for commit.
- Sibling child Agent manifests were scanned as metadata but are not part of
  this repo's staging plan.
- No `git add`, `git commit`, `git push`, remote modification, or force push was
  performed.

Next gate: proceed to `HUB-V2-014-GIT-COMMIT-PUSH` only after explicit user
approval.

## HUB-V2-014 Git Commit / Push / Live Showcase Verification

Status: HUB-V2-014-GIT-COMMIT-PUSH-LIVE-SHOWCASE-VERIFICATION-COMPLETE

The explicit public showcase publish stage is complete. It uses
`docs/PUBLIC_COMMIT_FILE_MANIFEST.md` as the exact staging source, excludes
generated report files, creates a normal commit, pushes to the existing
remote/current branch, and verifies the live GitHub showcase surface.

Final V2-014 gates:

- Final local validation passed.
- Staged file list matched `docs/PUBLIC_COMMIT_FILE_MANIFEST.md`.
- Staged public-safe scan passed before commit.
- Generated public report files were not staged.
- Git remote settings were not changed.
- No force push was used.
- Live README, screenshots, docs, and remote tree were verified after push.
