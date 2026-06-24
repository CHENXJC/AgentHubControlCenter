# Public Showcase Manifest

## Public Showcase Identity

AgentHubControlCenter is a local-first AgentOps / PortfolioOps dashboard that
shows how a personal AI Agent and Skill ecosystem can be registered, validated,
checked, organized, exported, and presented from one product-style Streamlit
command center.

## Current Status

HUB-006-PUBLIC-SHOWCASE-PACKAGING-COMPLETE

## HUB-006 Public Showcase Packaging

HUB-006 packages the completed HUB-005 feature set for a GitHub public showcase
pass. It does not expand core app logic or add new runtime integrations.

Packaging status:

| Area | Status | Notes |
| --- | --- | --- |
| README screenshot section | Complete | Uses relative `docs/images/` paths and public-safe captions. |
| Screenshot assets | Complete | Six PNG screenshots saved under `docs/images/`. |
| Screenshots guide | Complete | Documents each image, UI area, and public-safe capture rule. |
| Showcase asset checklist | Complete | Tracks screenshot, README, manifest, status, docs, and validation readiness. |
| Project status | Complete | Records the HUB-006 checkpoint and next-stage recommendation. |
| Tests | Complete | `python -m pytest` passed: 24 tests passed. |
| Compile check | Complete | `python -m compileall agent_hub app.py` passed. |
| Streamlit smoke check | Complete | Local app opened at `http://127.0.0.1:8501` for screenshot capture. |
| Safety check | Complete | No `.env` read, no secrets output, no remote change, no push. |

## HUB-005 Showcase Capabilities

- Product-style dashboard
- Screenshot-ready UI
- Command center hero section
- Six metric cards
- Agent detail panel
- Command pack display
- Health and priority cards
- Capability cluster cards
- Fixed project matrix view
- Enhanced Markdown portfolio report
- Command Center Summary report section
- Priority Action Summary
- Public Showcase Readiness report section
- Saved local report export flow
- Public-safe showcase asset checklist

## Prepared Screenshot Assets

- `docs/images/01_command_center_home.png`
- `docs/images/02_portfolio_metrics.png`
- `docs/images/03_project_matrix_view.png`
- `docs/images/04_priority_action_summary.png`
- `docs/images/05_report_export_preview.png`
- `docs/images/06_public_showcase_readiness.png`

## Safety Boundary

This dashboard is for local portfolio management and workflow planning only. It
does not execute external actions or access private credentials.

The HUB-006 package does not create `.env`, read credentials, call external APIs,
initialize a remote, modify git remote settings, or push to GitHub.

## Public Showcase Notes

- Registry entries describe existing portfolio projects.
- Health checks only inspect local path/file presence.
- Launch and command-pack strings are displayed as text and are not executed by
  the dashboard.
- README screenshots are captured from public-safe top-level UI regions.
- Exported reports are generated from local registry, validation, health, and
  next-action data.
- Saved reports are local `outputs/` artifacts and are ignored by git except
  `outputs/.gitkeep`.
