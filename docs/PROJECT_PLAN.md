# Project Plan

## Project Goal

AgentHubControlCenter is a local-first AI Agent / Skill control center for
managing a personal AI workflow ecosystem. It centralizes registry metadata,
local project health checks, portfolio positioning, GitHub showcase links,
launch command visibility, and next actions.

## HUB-002 MVP

- Created the local project skeleton.
- Registered existing AI Agent and Skill projects in `data/agent_registry.csv`.
- Built a Streamlit dashboard with overview, registry, health check, portfolio
  matrix, and report export tabs.
- Added core Python modules with focused tests.
- Kept all behavior local and credential-free.

## HUB-003 Registry Engine + Health Check Upgrade

- Added registry metadata validation and quality scores.
- Upgraded health scoring for tests, docs, project status, portfolio folder,
  GitHub URL presence, and suggested fixes.
- Added next action planning with High, Medium, Low, and None priority levels.
- Added portfolio positioning analysis with capability clusters, strengths, and
  gaps.
- Added command pack builder for local project workflow commands.
- Enhanced the Markdown portfolio report.
- Upgraded the Streamlit dashboard to six tabs.

## HUB-004 Streamlit Product UI Polish

- Added product-style command center hero.
- Added six metric cards and sidebar filters.
- Added registry detail and command pack panels.
- Added health overview cards and health detail expanders.
- Added capability cluster cards and category matrix cards.
- Added priority summary and grouped action cards.
- Added screenshot-ready spacing and visual hierarchy.
- Updated the screenshot guide for six public-showcase views.

## HUB-005 Report Export & Showcase Assets

- Added saved local Markdown report export flow for `outputs/`.
- Added a stable Windows-safe report filename builder.
- Added enhanced Command Center Summary to the report, Overview tab, and Export
  Report tab.
- Added fixed project matrix view for the core portfolio categories.
- Added Priority Action Summary for paused projects, future commercial
  candidates, GitHub showcase projects, and future AgentHub integration.
- Added public showcase readiness and public-safe showcase asset checklist to
  the report and UI.
- Improved report preview and output organization for screenshot readiness.

## HUB-006 Public Showcase Packaging / Screenshots / GitHub Release Polish

- Captured six public-safe Streamlit screenshots under `docs/images/`.
- Added a GitHub-ready README screenshot section with relative image paths.
- Updated the screenshot guide with UI-area mapping and safety notes.
- Updated the public showcase manifest with packaging status, asset status, and
  safety boundaries.
- Updated the showcase asset checklist for README, screenshot, docs, status, and
  validation readiness.
- Kept the app feature scope stable; no new app logic or core workflow expansion
  was added in this stage.

## Later Stages

- HUB-007 GitHub Public Release / Profile Pin Decision

## Safety Boundary

This project is a dashboard for local portfolio management and workflow planning.
It does not execute external actions, access private credentials, initialize a
remote, or push to GitHub.
