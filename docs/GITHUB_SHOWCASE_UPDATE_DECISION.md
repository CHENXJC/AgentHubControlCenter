# GitHub Showcase Update Decision

Checkpoint:
`HUB-V2-013-GITHUB-SHOWCASE-UPDATE-DECISION-COMPLETE`

This document records the local decision for the next GitHub showcase update.
It is an audit and planning artifact only. It does not run `git add`, does not
create a commit, does not push, and does not change git remotes.

## Decision Summary

Decision: ready to enter a separate explicit commit/push stage.

Recommended next stage:
`HUB-V2-014-GIT-COMMIT-PUSH`

The current V2 showcase update is suitable for a public commit because the
working tree contains local-first product UI, metadata schemas, docs, tests,
launcher files, public-safe screenshots, and `.gitignore` output boundaries.
Generated report files, virtual environment files, collaboration instructions,
private outputs, caches, logs, and sibling project files must remain excluded.

## Review Scope

Allowed review commands used for this decision:

- `git status --short`
- `git diff --stat`
- `git diff --name-only`
- `git ls-files --others --exclude-standard`
- Targeted `git check-ignore` checks for output and environment boundaries

Commands intentionally not run:

- `git add`
- `git commit`
- `git push`
- `git reset`
- `git clean`
- `git rm`
- `git remote set-url`
- Force push

## Working Tree Snapshot

Initial V2-013 audit snapshot:

- `git status --short`: 91 paths
- Modified tracked paths: 20
- Untracked public candidate paths: 71
- `git diff --stat -- . ':!docs/images/*.png'`: 14 tracked text files, 4358
  insertions, 243 deletions

Final V2-013 snapshot after adding the decision docs and tests:

- `git status --short`: 95 paths
- Modified tracked paths: 20
- Untracked public candidate paths: 75
- `git diff --stat -- . ':!docs/images/*.png'`: 14 tracked text files, 4559
  insertions, 243 deletions

The untracked set includes V2 schemas, registries, docs, tests, launcher files,
10 canonical screenshots, and `outputs/public_reports/.gitkeep`. Generated
Markdown/JSON/CSV report files are ignored and are not part of the candidate
set.

## Category Decision

| Category | Decision | Notes |
| --- | --- | --- |
| Core app | Commit | Includes V2 UI surfaces, stage label, registry merge, and report/export wiring. |
| `agent_hub` modules | Commit | Required for action schema, onboarding, prompts, useful signals, connector readiness, workflow simulation, approval gates, and demo reports. |
| Tests | Commit | Required to prove the public showcase update remains stable and policy-safe. |
| Docs | Commit | Required for public showcase explanation, runbooks, safety policies, release check, and commit decision. |
| Screenshots | Commit | Commit the 10 canonical V2 screenshots. The six historical tracked screenshots are also public-safe and can be committed with the image set. |
| Manifests/contracts | Commit root files | Commit root `agent_manifest.json` and `agent_contract.json`; sibling project manifests are scanned but are outside this repo's staging scope. |
| Launch scripts | Commit | `launch_command_center.cmd` and `scripts/create_desktop_shortcut.ps1` are public-safe local launch helpers. |
| Sample summary | Commit | `docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md` is compact and public-safe. |
| Outputs boundary | Commit marker only | Commit `outputs/public_reports/.gitkeep`; do not commit generated report files. |

## Public-Safe Results

- Candidate text files scanned: 79
- Candidate binary/image files skipped from text scan: 16
- Secret-like candidate hits: 0
- 11 immediate `F:\AIProjects` agent manifests load as JSON.
- Child manifest secret-like hits: 0
- `outputs/private/` is absent.
- `.venv/` is ignored.
- `outputs/public_reports/*.md`, `*.json`, and `*.csv` report files are
  ignored.
- `outputs/public_reports/.gitkeep` is intentionally unignored.

## Child Agent Manifest Decision

The 11 immediate manifests under `F:\AIProjects` are valid and public-safe for
metadata scanning:

- `agent_hub_control_center`
- `business_ops_agent`
- `career_pilot_agent`
- `idea_score_agent`
- `market_sense_agent`
- `news_signal_agent`
- `next_ops_agent`
- `personal_knowledge_agent`
- `quant_lab_agent`
- `social_pain_finder_agent`
- `video_extract_skill`

Only the root AgentHubControlCenter `agent_manifest.json` belongs to this repo's
staging plan. Sibling project manifests should be committed in their own repos
only if a separate explicit stage asks for that.

## Release Notes Draft

- Upgrades AgentHubControlCenter from a public showcase dashboard into a V2
  local AgentOps command center.
- Adds manifest onboarding for 11 local Agents and Skills.
- Adds local action schema, manual runbook, Codex Prompt Generator, Useful
  Signals, connector readiness simulation, workflow simulation, approval gates,
  and public-safe demo report export.
- Refreshes README with 10 public-safe screenshots and compact sample report
  summary docs.
- Adds release readiness, commit manifest, and exclusion manifest docs.
- Preserves local-first safety: no live connectors, no real actions, no
  credential reads, no external API calls, no child script execution, and no
  generated report files in git.

## Suggested Commit Message

`Complete AgentHubControlCenter V2 public showcase upgrade`

Alternative:

`Complete HUB-V2 public showcase release readiness`

## Suggested Next Stage

Proceed to `HUB-V2-014-GIT-COMMIT-PUSH` only after explicit user approval.
That stage should review the final file list again, run the full validation
suite, then perform normal staging/commit/push without remote changes or force
push.

## HUB-V2-014 Follow-Up

The user explicitly approved the next stage:
`HUB-V2-014-GIT-COMMIT-PUSH-LIVE-SHOWCASE-VERIFICATION`.

The V2-014 stage uses `docs/PUBLIC_COMMIT_FILE_MANIFEST.md` as the exact
staging source, keeps generated reports excluded, creates a normal commit,
pushes to the existing remote/current branch, and verifies the live GitHub
README, screenshots, docs, and remote tree. This follow-up does not change the
V2-013 decision record; it records that the planned publish gate has been
authorized and completed in the next checkpoint.
