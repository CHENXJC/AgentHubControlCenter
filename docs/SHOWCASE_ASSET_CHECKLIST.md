# Showcase Asset Checklist

Use this checklist before preparing or publishing the GitHub public showcase.

## HUB-006 Asset Status

| Asset | Status | Location / Notes |
| --- | --- | --- |
| Command Center Overview screenshot | Complete | `docs/images/01_command_center_home.png` |
| Portfolio Metrics screenshot | Complete | `docs/images/02_portfolio_metrics.png` |
| Project Matrix View screenshot | Complete | `docs/images/03_project_matrix_view.png` |
| Priority Action Summary screenshot | Complete | `docs/images/04_priority_action_summary.png` |
| Report Export Preview screenshot | Complete | `docs/images/05_report_export_preview.png` |
| Public Showcase Readiness screenshot | Complete | `docs/images/06_public_showcase_readiness.png` |
| README screenshot section | Complete | Relative paths point to `docs/images/`. |
| Public showcase manifest | Complete | `docs/PUBLIC_SHOWCASE_MANIFEST.md` |
| Screenshot guide | Complete | `docs/SCREENSHOTS_GUIDE.md` |
| Project plan | Complete | `docs/PROJECT_PLAN.md` |
| Project status | Complete | `PROJECT_STATUS.md` |
| Pytest | Complete | `python -m pytest` passed: 24 tests passed. |
| Compile check | Complete | `python -m compileall agent_hub app.py` passed. |
| Streamlit smoke check | Complete | Local app opened for screenshot capture. |

## Public-Safe Asset Rules

- Do not include `.env`, credentials, tokens, customer data, private documents,
  private screenshots, or generated private reports.
- Review local path visibility before publishing screenshots.
- Keep generated reports in `outputs/`; this folder is ignored by git except
  `outputs/.gitkeep`.
- Do not run external actions, initialize a remote, modify git remote settings,
  or push to GitHub during screenshot preparation.

## README Screenshot Order

1. `01_command_center_home.png`
2. `02_portfolio_metrics.png`
3. `03_project_matrix_view.png`
4. `04_priority_action_summary.png`
5. `05_report_export_preview.png`
6. `06_public_showcase_readiness.png`
