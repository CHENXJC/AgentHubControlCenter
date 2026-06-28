# Cross-Project Exclusion Manifest

Checkpoint:
`HUB-V2-018-CROSS-PROJECT-BACKLINK-EXPLICIT-COMMIT-COMPLETE`

This manifest lists files and path classes that should not be staged for the
cross-project backlink commit set.

## Global Exclusions

| Excluded Path / Pattern | Reason | Usually Covered By `.gitignore` | Follow-Up Required |
| --- | --- | --- | --- |
| `.env`, `.env.*`, `*.env` | Environment secrets must not be committed. | Yes | None |
| `.streamlit/secrets.toml`, `secrets.toml` | Streamlit secrets must remain local. | Usually | None |
| `credentials.json`, `token.json`, `*.pem`, `*.key`, `id_rsa`, `id_rsa.pub` | Credential, token, key, or certificate material. | Usually | None |
| `outputs/private/` | Private generated output must not be committed. | Usually | None |
| Generated reports under `outputs/`, `reports/`, `exports/`, or similar folders | Generated artifacts may contain private or stale data. | Usually | Review only in a separate stage |
| `.venv/`, `venv/`, `env/` | Local virtual environments are large and machine-specific. | Yes | None |
| `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `*.pyc` | Runtime/test/cache artifacts. | Yes | None |
| `*.log`, `*.tmp` | Local logs and temporary files. | Usually | None |
| Local databases, private exports, cache folders | May contain private local data. | Varies | Review only if explicitly requested |
| Deploy artifacts and ad-hoc batch files | Not related to backlink commit. | Varies | Review separately |

## Repo-Specific Exclusions

| Repo | Excluded Files / Paths | Reason | Covered By `.gitignore` | Follow-Up Required |
| --- | --- | --- | --- | --- |
| AgentHubControlCenter | Generated report files under `outputs/public_reports/*.md`, `*.json`, `*.csv`; `.venv/`; cache files; secrets; `AGENTS.md` | Outside V2-017 backlink decision commit or local-only. | Yes for known generated/local patterns | None |
| BusinessOpsAgent | Generated outputs, private data, `.env`, `.venv`, caches | Not part of backlink commit. | Core local patterns covered | None |
| CareerPilotAgent | `data/private/`, generated outputs, `.env`, `.venv`, caches | Private or generated local data. | Core local patterns covered | None |
| IdeaScoreAgent | `IDEASCORE_WINDOWS_DEPLOY_REPORT.md`; `check_ideascore_windows.bat`; `run_ideascore_windows.bat`; generated outputs; `.env`; `.venv`; caches | Unrelated deploy/report/bat artifacts are not required for backlink commit. | Not confirmed for the three untracked deploy/report/bat files | Review separately |
| NewsSignalAgent | Generated cache/reports/exports/logs, `.env`, `.venv`, caches | Not part of backlink commit. | Core local patterns covered | None |
| NextOpsAgent | Generated demo outputs/reports, `.env`, `.venv`, caches | Not part of backlink commit. | Core local patterns covered | None |
| PersonalKnowledgeAgent | Real `knowledge_base/`, private outputs, generated reports, `.env`, `.venv`, caches | Private/local knowledge material must remain excluded. | Core local patterns covered | None |
| QuantLabAgent | Generated market reports, local data, `.env`, `.venv`, caches | Not part of backlink commit. | Core local patterns covered | None |
| SocialPainFinderAgent | Generated reports/exports, private datasets, `.env`, `.venv`, caches | Not part of backlink commit. | Core local patterns covered | None |
| MarketSenseAgent | No git commit recommended from current folder | Non-git local directory. | N/A | Separate repo decision required |
| VideoExtractSkill | No git commit recommended from current folder | Non-git local directory. | N/A | Separate repo decision required |

## IdeaScoreAgent Special Decision

IdeaScoreAgent currently has these unrelated untracked files:

- `IDEASCORE_WINDOWS_DEPLOY_REPORT.md`
- `check_ideascore_windows.bat`
- `run_ideascore_windows.bat`

Default recommendation: exclude all three from the backlink commit. They are
not required for the AgentHubControlCenter backlink, and this stage did not
review them as public-safe launch or release assets.

The only IdeaScoreAgent files recommended for the backlink commit are:

- `README.md`
- `agent_manifest.json`

V2-018 result: the two recommended files were committed and pushed. The three
unrelated deploy/report/bat files remained untracked and unstaged.

## Cleanup Recommendation

No deletion, cleanup, reset, or `git clean` is recommended in this stage.
Unrelated files should be reviewed in a separate project-specific stage.
