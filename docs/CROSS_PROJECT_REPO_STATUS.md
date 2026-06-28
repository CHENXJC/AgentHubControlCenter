# Cross-Project Repo Status

Checkpoint:
`HUB-V2-017-CROSS-PROJECT-BACKLINK-COMMIT-DECISION-COMPLETE`

Note: this document preserves the V2-017 pre-commit repo status snapshot. The
V2-018 commit and push results are recorded in
`docs/CROSS_PROJECT_BACKLINK_COMMIT_RESULTS.md`.

## Repo Status Table

Remote URLs below are normal public GitHub HTTPS remotes or marked as absent.
No remote settings were modified.

| Project | Git Repo | Branch | Origin | `git status --short` Summary | `git diff --name-only` |
| --- | --- | --- | --- | --- | --- |
| AgentHubControlCenter | Yes | `main` | `https://github.com/CHENXJC/AgentHubControlCenter.git` | Modified docs/status plus new V2-017 docs | `PROJECT_STATUS.md`, `docs/PROJECT_PLAN.md` |
| BusinessOpsAgent | Yes | `main` | `https://github.com/CHENXJC/BusinessOpsAgent.git` | `M README.md`, `?? agent_manifest.json` | `README.md` |
| CareerPilotAgent | Yes | `main` | `https://github.com/CHENXJC/CareerPilotAgent.git` | `M README.md`, `?? agent_manifest.json` | `README.md` |
| IdeaScoreAgent | Yes | `main` | `https://github.com/CHENXJC/IdeaScoreAgent.git` | `M README.md`, `?? IDEASCORE_WINDOWS_DEPLOY_REPORT.md`, `?? agent_manifest.json`, `?? check_ideascore_windows.bat`, `?? run_ideascore_windows.bat` | `README.md` |
| MarketSenseAgent | No | N/A | N/A | Non-git local directory | N/A |
| NewsSignalAgent | Yes | `main` | `https://github.com/CHENXJC/NewsSignalAgent.git` | `M README.md`, `?? agent_manifest.json` | `README.md` |
| NextOpsAgent | Yes | `main` | `https://github.com/CHENXJC/NextOpsAgent.git` | `M README.md`, `?? agent_manifest.json` | `README.md` |
| PersonalKnowledgeAgent | Yes | `main` | `https://github.com/CHENXJC/PersonalKnowledgeAgent.git` | `M README.md`, `?? agent_manifest.json` | `README.md` |
| QuantLabAgent | Yes | `main` | `https://github.com/CHENXJC/QuantLabAgent.git` | `M README.md`, `?? agent_manifest.json` | `README.md` |
| SocialPainFinderAgent | Yes | `main` | `https://github.com/CHENXJC/SocialPainFinderAgent.git` | `M README.md`, `?? agent_manifest.json` | `README.md` |
| VideoExtractSkill | No | N/A | N/A | Non-git local directory | N/A |

## Diff Stat Summary

| Project | `git diff --stat` Summary |
| --- | --- |
| AgentHubControlCenter | `PROJECT_STATUS.md` and `docs/PROJECT_PLAN.md` modified before adding V2-017 docs. |
| BusinessOpsAgent | `README.md`: 6 insertions. |
| CareerPilotAgent | `README.md`: 6 insertions. |
| IdeaScoreAgent | `README.md`: 6 insertions. |
| MarketSenseAgent | N/A because the folder is not a git repo. |
| NewsSignalAgent | `README.md`: 6 insertions. |
| NextOpsAgent | `README.md`: 6 insertions. |
| PersonalKnowledgeAgent | `README.md`: 4 insertions. |
| QuantLabAgent | `README.md`: 6 insertions. |
| SocialPainFinderAgent | `README.md`: 6 insertions. |
| VideoExtractSkill | N/A because the folder is not a git repo. |

## Validation Status

| Project | README Backlink | Duplicate Backlink Violations | Manifest JSON Loads | README Secret-Like Hits | Manifest Secret-Like Hits |
| --- | --- | --- | --- | --- | --- |
| BusinessOpsAgent | Yes | 0 | Yes | 0 | 0 |
| CareerPilotAgent | Yes | 0 | Yes | 0 | 0 |
| IdeaScoreAgent | Yes | 0 | Yes | 0 | 0 |
| MarketSenseAgent | Yes | 0 | Yes | 0 | 0 |
| NewsSignalAgent | Yes | 0 | Yes | 0 | 0 |
| NextOpsAgent | Yes | 0 | Yes | 0 | 0 |
| PersonalKnowledgeAgent | Yes | 0 | Yes | 0 | 0 |
| QuantLabAgent | Yes | 0 | Yes | 0 | 0 |
| SocialPainFinderAgent | Yes | 0 | Yes | 0 | 0 |
| VideoExtractSkill | Yes | 0 | Yes | 0 | 0 |

## Notes

- `agent_manifest.json` is untracked in several child repos, but it is directly
  relevant to AgentHubControlCenter onboarding and passed JSON/public-safe
  checks.
- IdeaScoreAgent has unrelated untracked deploy/report/bat files. They are
  excluded from the backlink commit plan.
- MarketSenseAgent and VideoExtractSkill are local non-git directories, so this
  stage records their README backlink state but does not recommend a git
  commit from those folders.
