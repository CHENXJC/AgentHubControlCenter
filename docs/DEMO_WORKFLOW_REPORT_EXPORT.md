# Demo Workflow Report Export

Status: HUB-V2-010-DEMO-WORKFLOW-REPORT-EXPORT-COMPLETE

V2-011 showcase companion:
`docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md` provides a compact public-safe
summary of the latest generated demo report. README should link or reference the
summary rather than dumping the full report content.

V2-012 release check companion:
`docs/PUBLIC_RELEASE_CHECKLIST.md` and `docs/V2_RELEASE_READINESS_REPORT.md`
verify that generated public report files remain local artifacts under
`outputs/public_reports/` unless separately reviewed and approved.

## Purpose

HUB-V2-010 adds public-safe Demo Workflow Report Export to
AgentHubControlCenter V2. It turns the current local metadata layers into
copy-ready reports for portfolio review:

- Agent Registry summary
- Local Action Schema summary
- Useful Signals summary and Top Useful Signals
- Connector Readiness summary
- Local Workflow Simulation summary
- Approval Gates summary
- Safety notes and validation snapshot

The export is metadata-only. It does not execute real actions, does not connect
live providers, does not load credentials, and does not call external APIs.

## Report Export Schema

Each report package includes:

- `report_id`
- `title`
- `schema_version`
- `generated_at`
- `export_policy`
- `formats`
- `selected_sections`
- `public_safe`
- `safety_notes`
- `validation_snapshot`
- `sections`

The export policy is always:

`public_safe_demo_report_metadata_only_no_execution`

## Supported Formats

HUB-V2-010 supports three public-safe text formats:

| Format | Purpose |
| --- | --- |
| Markdown | GitHub / portfolio-friendly narrative report. |
| JSON | Structured report package for future AgentHub re-import. |
| CSV | Compact summary table for signals, connectors, workflows, gates, and actions. |

## Report Sections

The Report Export UI supports these selectable sections:

- Agents
- Actions
- Useful Signals
- Connectors
- Workflows
- Approval Gates
- Safety Snapshot

Generated reports include these top-level report topics when all sections are
selected:

1. Executive Summary
2. System Snapshot
3. Agent Registry Summary
4. Useful Signals
5. Connector Readiness
6. Local Workflow Simulation
7. Approval Gates
8. Safety Snapshot
9. Recommended Next Steps
10. Public-Safe Disclaimer

## Manual Use

1. Open the local command center.
2. Go to `My Workflows`.
3. Review Local Workflow Simulation, Approval Gates, and Workflow-Generated
   Useful Signals.
4. Open `Demo Workflow Report Export`.
5. Choose report sections.
6. Preview Markdown, JSON, or CSV.
7. Use the download controls for public-safe text copies.

The UI download controls only provide text content. They do not execute actions,
connect providers, or run child Agent scripts.

## Local File Export

The exporter module may write generated files only under:

`outputs/public_reports/`

The directory exists with `.gitkeep`. Generated report files remain local output
artifacts and should be reviewed before any public release.

`outputs/private/` is not used and must not be created by this stage.

## Required Safety Notes

Every generated package must include:

- Demo/local metadata only
- No live connector connected
- No credentials loaded
- No real action executed
- No external API called

## Validation Snapshot

The report package includes the current safety validation snapshot:

- Valid Manifests
- Invalid Manifests
- Missing Manifests
- Unsafe execution modes
- Action policy violations
- Signal policy violations
- Connector policy violations
- Workflow policy violations
- Approval gate policy violations
- Report export policy violations

For HUB-V2-010 completion, all policy violation counts are expected to remain
`0`.

## Not Allowed

HUB-V2-010 does not:

- read `.env`
- print secrets, tokens, passwords, or API keys
- create OAuth flows
- call external APIs
- connect Gmail, Google Sheets, Notion, Airtable, Telegram, GitHub, n8n, Make,
  Zapier, or other live providers
- run child project scripts
- execute real actions
- modify git remote
- run `git push`
- write to `outputs/private/`

The report is a public-safe planning artifact, not an automation executor.

## HUB-V2-011 Showcase Use

For HUB-V2-011, the latest public-safe report under `outputs/public_reports/`
was reviewed at summary level and represented by
`docs/SAMPLE_DEMO_WORKFLOW_REPORT_SUMMARY.md`.

The summary intentionally includes only demo metadata, high-level counts, and
required safety notes:

- Demo/local metadata only
- No live connector connected
- No credentials loaded
- No real action executed
- No external API called

It must not include private outputs, OAuth account data, live connector data,
or full report dumps in README.
