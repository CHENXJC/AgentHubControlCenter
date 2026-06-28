# Cross-Project Commit Manifest

Checkpoint:
`HUB-V2-018-CROSS-PROJECT-BACKLINK-EXPLICIT-COMMIT-COMPLETE`

This manifest lists the exact files used or approved for the explicit V2-018
cross-project backlink commit stage. It is not a staging command. Do not use
`git add .`.

## Recommended Stage Files

| Repo | Recommended Files | Reason | Public-Safe | Contains Backlink | Contains Agent Manifest | Suggested Commit Message |
| --- | --- | --- | --- | --- | --- | --- |
| AgentHubControlCenter | `PROJECT_STATUS.md`; `docs/PROJECT_PLAN.md`; `docs/CROSS_PROJECT_BACKLINK_PLAN.md`; `docs/CROSS_PROJECT_BACKLINK_STATUS.md`; `docs/CROSS_PROJECT_BACKLINK_COMMIT_DECISION.md`; `docs/CROSS_PROJECT_REPO_STATUS.md`; `docs/CROSS_PROJECT_COMMIT_MANIFEST.md`; `docs/CROSS_PROJECT_EXCLUSION_MANIFEST.md`; `docs/CROSS_PROJECT_BACKLINK_COMMIT_RESULTS.md` | Records V2-016/V2-017/V2-018 backlink plan, status, decision, commit manifest, exclusions, and explicit commit results. | Yes | N/A | N/A | `Document cross-project AgentHub backlink commit plan` |
| BusinessOpsAgent | `README.md`; `agent_manifest.json` | README contains AgentHub backlink; manifest registers the project in AgentHub. | Yes | Yes | Yes | `Add AgentHubControlCenter backlink and manifest` |
| CareerPilotAgent | `README.md`; `agent_manifest.json` | README contains AgentHub backlink; manifest registers the project in AgentHub. | Yes | Yes | Yes | `Add AgentHubControlCenter backlink and manifest` |
| IdeaScoreAgent | `README.md`; `agent_manifest.json` | README contains AgentHub backlink; manifest registers the project in AgentHub. Proceed only after excluding unrelated artifacts. | Yes | Yes | Yes | `Add AgentHubControlCenter backlink and manifest` |
| NewsSignalAgent | `README.md`; `agent_manifest.json` | README contains AgentHub backlink; manifest registers the project in AgentHub. | Yes | Yes | Yes | `Add AgentHubControlCenter backlink and manifest` |
| NextOpsAgent | `README.md`; `agent_manifest.json` | README contains AgentHub backlink; manifest registers the project in AgentHub. | Yes | Yes | Yes | `Add AgentHubControlCenter backlink and manifest` |
| PersonalKnowledgeAgent | `README.md`; `agent_manifest.json` | README merges the backlink into the existing AgentHub section; manifest registers the project in AgentHub. | Yes | Yes | Yes | `Add AgentHubControlCenter portfolio backlink and manifest` |
| QuantLabAgent | `README.md`; `agent_manifest.json` | README contains AgentHub backlink; manifest registers the project in AgentHub. | Yes | Yes | Yes | `Add AgentHubControlCenter backlink and manifest` |
| SocialPainFinderAgent | `README.md`; `agent_manifest.json` | README contains AgentHub backlink; manifest registers the project in AgentHub. | Yes | Yes | Yes | `Add AgentHubControlCenter backlink and manifest` |

## Non-Git Directories

| Project | Decision | Reason |
| --- | --- | --- |
| MarketSenseAgent | `skip_non_git` | Current local folder is not a git repo. |
| VideoExtractSkill | `skip_non_git` | Current local folder is not a git repo. |

## V2-018 Execution Result

The child repo commit/push stage was completed in this order:

1. BusinessOpsAgent.
2. CareerPilotAgent.
3. IdeaScoreAgent after excluding unrelated deploy/report/bat artifacts.
4. NewsSignalAgent.
5. NextOpsAgent.
6. PersonalKnowledgeAgent.
7. QuantLabAgent.
8. SocialPainFinderAgent.

MarketSenseAgent and VideoExtractSkill were skipped because their current local
folders are not git repos.

AgentHubControlCenter is committed last so this manifest can include the final
V2-018 result documentation.

## Explicit Reminder

Do not use `git add .`.

Use exact file paths only. Do not stage generated reports, deploy artifacts,
local databases, credentials, private outputs, virtual environments, caches,
logs, or temporary files.
