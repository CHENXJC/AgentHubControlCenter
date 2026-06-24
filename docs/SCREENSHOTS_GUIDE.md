# Screenshots Guide

HUB-006 screenshot status: ready.

The public showcase screenshots are saved under `docs/images/` and are intended
for the GitHub README screenshot section. They were captured from the local
Streamlit demo app using the public-safe registry view.

## Public-Safe Screenshot Rules

- Do not include `.env`, API keys, tokens, credentials, customer data, private
  documents, or generated private reports.
- Use local demo portfolio metadata only.
- Keep screenshot areas focused on product UI, metrics, planning, readiness, and
  export preview.
- Avoid exposing local filesystem paths or command-pack details in public README
  screenshots.

## Prepared Screenshots

### 1. `docs/images/01_command_center_home.png`

UI area: Overview tab.

Shows the Command Center hero, public-safe portfolio metrics, and Command Center
Summary cards.

### 2. `docs/images/02_portfolio_metrics.png`

UI area: Agent Registry tab.

Shows portfolio metrics and the registry table. The screenshot uses the top
viewport only so it does not expose local path or command-pack details.

### 3. `docs/images/03_project_matrix_view.png`

UI area: Portfolio Matrix tab.

Shows the fixed Project Matrix View for portfolio capability groups.

### 4. `docs/images/04_priority_action_summary.png`

UI area: Next Actions tab.

Shows priority metrics and current next-action planning. No automation is
executed from this view.

### 5. `docs/images/05_report_export_preview.png`

UI area: Export Report tab.

Shows the Command Center Export Summary and local Markdown report preview entry
point.

### 6. `docs/images/06_public_showcase_readiness.png`

UI area: Health Check tab.

Shows public-showcase readiness through local file health metrics and the health
table preview.

## Capture Notes

- Recommended browser width: 1440px.
- Current HUB-006 images were captured at 1440x1000.
- Screenshot review confirmed no `.env`, token, API key, password, credential,
  or private customer data is visible.
