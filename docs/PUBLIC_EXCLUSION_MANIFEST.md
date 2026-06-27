# Public Exclusion Manifest

Checkpoint:
`HUB-V2-013-GITHUB-SHOWCASE-UPDATE-DECISION-COMPLETE`

This manifest lists files and path classes that should not be staged for the
public AgentHubControlCenter showcase commit.

## Exclusion Table

| Excluded Path / Pattern | Reason | Covered By `.gitignore` | Follow-Up Required |
| --- | --- | --- | --- |
| `.env`, `.env.*`, `*.env` | Environment secrets must never be public. | Yes | None |
| `.streamlit/secrets.toml`, `secrets.toml` | Streamlit secret storage must remain private. | Yes | None |
| `credentials.json`, `token.json`, `*.pem`, `*.key`, `id_rsa`, `id_rsa.pub` | Credentials, OAuth tokens, private keys, and SSH keys must remain private. | Yes | None |
| `.venv/`, `venv/`, `env/` | Local virtual environments are machine-specific and large. | Yes | None |
| `outputs/public_reports/*.md` | Generated report output; keep local unless separately reviewed. | Yes | None |
| `outputs/public_reports/*.json` | Generated report output; keep local unless separately reviewed. | Yes | None |
| `outputs/public_reports/*.csv` | Generated report output; keep local unless separately reviewed. | Yes | None |
| `outputs/private/` | Private output area must not exist or be committed. | `outputs/*` would cover it; current check confirms absent. | None |
| `outputs/*` except allowed `.gitkeep` files | Generated outputs are not public release inputs by default. | Yes | None |
| `*.log`, `*.tmp` | Smoke logs and temp files are not public release inputs. | Yes | None |
| `__pycache__/`, `**/__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `*.pyc` | Runtime/test/cache artifacts. | Yes | None |
| `AGENTS.md` | Local collaboration rules for Codex; not part of the public showcase. | Yes | None |
| `.git/` | Git internals must never be staged manually. | Git-managed | None |
| Sibling project files under `F:\AIProjects\BusinessOpsAgent`, `CareerPilotAgent`, `IdeaScoreAgent`, `MarketSenseAgent`, `NewsSignalAgent`, `NextOpsAgent`, `PersonalKnowledgeAgent`, `QuantLabAgent`, `SocialPainFinderAgent`, and `VideoExtractSkill` | They are outside the AgentHubControlCenter repository. | Not applicable to this repo | Commit separately only if explicitly requested. |

## Output Boundary Check

Current local `outputs/public_reports/` contains:

- `.gitkeep`
- `agenthub_v2_demo_workflow_report_2026-06-28.md`
- `agenthub_v2_demo_workflow_report_2026-06-28.json`
- `agenthub_v2_demo_workflow_report_2026-06-28.csv`

Only `.gitkeep` is recommended for commit. The generated report files remain
ignored by `.gitignore`.

## Private Output Check

`outputs/private/` is absent.

## Ignored Path Evidence

Targeted ignore checks confirm:

- `.venv/Scripts/python.exe` is ignored by `.venv/`.
- Generated public report Markdown/JSON/CSV files are ignored by
  `outputs/public_reports/*`.
- `outputs/public_reports/.gitkeep` is intentionally unignored.
- `AGENTS.md` is ignored.

## Follow-Up

No cleanup, deletion, reset, or git clean operation is recommended in this
stage. If generated reports need to be published later, run a separate explicit
review stage first.
