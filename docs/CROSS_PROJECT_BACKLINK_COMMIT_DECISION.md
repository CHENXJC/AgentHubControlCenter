# Cross-Project Backlink Commit Decision

Checkpoint:
`HUB-V2-017-CROSS-PROJECT-BACKLINK-COMMIT-DECISION-COMPLETE`

V2-018 follow-up: the explicitly approved commit/push stage is complete. Final
commit hashes and push results are recorded in
`docs/CROSS_PROJECT_BACKLINK_COMMIT_RESULTS.md`.

## Decision Scope

This document reviews the cross-project backlink changes created in
HUB-V2-016 and decides what should be committed later if the user explicitly
approves a commit stage.

This stage does not run `git add`, does not commit, does not push, does not
modify remotes, does not run child project scripts, and does not connect live
providers.

## Decision Summary

| Project | Git State | Decision | Reason |
| --- | --- | --- | --- |
| AgentHubControlCenter | Git repo | `ready_to_commit` | Only docs/status decision files are changed. |
| BusinessOpsAgent | Git repo | `ready_to_commit` | README backlink and public-safe manifest are relevant to AgentHub. |
| CareerPilotAgent | Git repo | `ready_to_commit` | README backlink and public-safe manifest are relevant to AgentHub. |
| IdeaScoreAgent | Git repo | `needs_review` | README/manifest are relevant, but unrelated deploy/report/bat artifacts must be excluded. |
| MarketSenseAgent | Non-git local directory | `skip_non_git` | No local git commit is available from this folder. |
| NewsSignalAgent | Git repo | `ready_to_commit` | README backlink and public-safe manifest are relevant to AgentHub. |
| NextOpsAgent | Git repo | `ready_to_commit` | README backlink and public-safe manifest are relevant to AgentHub. |
| PersonalKnowledgeAgent | Git repo | `ready_to_commit` | README backlink merged into existing AgentHub section and manifest is public-safe. |
| QuantLabAgent | Git repo | `ready_to_commit` | README backlink and public-safe manifest are relevant to AgentHub. |
| SocialPainFinderAgent | Git repo | `ready_to_commit` | README backlink and public-safe manifest are relevant to AgentHub. |
| VideoExtractSkill | Non-git local directory | `skip_non_git` | No local git commit is available from this folder. |

## Commit Policy

- Use exact file paths only.
- Do not use `git add .`.
- Do not stage generated reports.
- Do not stage deploy artifacts or batch files unless a separate review proves
  they are intentional public launchers.
- Do not stage `.env`, credential, token, secret, private output, local
  database, cache, virtual environment, or log files.
- Commit each git repo separately.
- Push only in a later explicitly approved stage.

## Recommended Follow-Up Order

1. Commit AgentHubControlCenter decision docs after final review.
2. Commit ready child repos one at a time with exact files.
3. Review IdeaScoreAgent unrelated files before committing that repo.
4. Leave MarketSenseAgent and VideoExtractSkill as local non-git README changes
   unless the user separately decides to initialize or map a repo.

## Suggested Commit Messages

| Project | Suggested Commit Message |
| --- | --- |
| AgentHubControlCenter | `Document cross-project backlink commit decision` |
| BusinessOpsAgent | `Add AgentHubControlCenter backlink and manifest` |
| CareerPilotAgent | `Add AgentHubControlCenter backlink and manifest` |
| IdeaScoreAgent | `Add AgentHubControlCenter backlink and manifest` |
| NewsSignalAgent | `Add AgentHubControlCenter backlink and manifest` |
| NextOpsAgent | `Add AgentHubControlCenter backlink and manifest` |
| PersonalKnowledgeAgent | `Add AgentHubControlCenter portfolio backlink and manifest` |
| QuantLabAgent | `Add AgentHubControlCenter backlink and manifest` |
| SocialPainFinderAgent | `Add AgentHubControlCenter backlink and manifest` |

MarketSenseAgent and VideoExtractSkill are skipped for git commit in their
current local directory state.

## Safety Result

The backlink review found:

- 10/10 child READMEs exist.
- 10/10 child READMEs contain AgentHubControlCenter backlinks.
- Duplicate backlink violations: 0.
- 10/10 child manifests load as JSON.
- README backlink text secret-like hits: 0.
- Child manifest secret-like hits: 0.
- Decision docs secret-like hits: 0.
