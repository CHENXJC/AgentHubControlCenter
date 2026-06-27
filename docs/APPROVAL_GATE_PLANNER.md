# Approval Gate Planner

Status: HUB-V2-010-DEMO-WORKFLOW-REPORT-EXPORT-COMPLETE

## Purpose

Approval Gates describe whether a recommended workflow step can remain
display-only, manual-only, template-only, dry-run-only, or blocked. They are
metadata controls for future planning. They do not approve real execution in
HUB-V2-009.

## Approval Gate Schema

Each approval gate includes:

- `gate_id`
- `gate_name`
- `target_action_id`
- `target_connector_id`
- `risk_level`
- `approval_required`
- `approval_status`
- `required_checks`
- `dry_run_required`
- `rollback_required`
- `human_review_required`
- `block_reason`
- `allowed_execution_mode`

The execution policy is always:

`approval_gate_metadata_only_no_execution`

## Approval Status Enum

- `not_required`
- `required`
- `blocked`
- `ready_for_manual_review`
- `approved_demo_only`
- `rejected`

## Allowed Execution Mode Enum

- `display_only`
- `manual_only`
- `template_only`
- `dry_run_only`
- `blocked`

The following real execution modes are forbidden:

- `live_execute`
- `auto_execute`
- `send`
- `push`
- `delete`

## Blocked Gate Examples

HUB-V2-009 explicitly blocks:

- Gmail Send
- GitHub Push / Release

These actions are blocked because they can mutate external systems. They would
require a separate explicit future stage with human approval, dry-run previews,
rollback plans, audit logs, and secret-safe connector handling.

## Required Checks

High-risk or blocked gates must include:

- explicit approval requirement
- human review requirement
- dry-run requirement when a future connector may mutate external systems
- rollback requirement for write/send/push style actions
- clear block reason
- no live connector in HUB-V2-009
- no credential loading
- no external API call

## First Safer Candidates

The safest future connector candidates remain read-only and demo-first:

- GitHub public status read
- Google Sheets local CSV mirror / future read-only scope

Even these candidates remain `not_connected` in HUB-V2-009.

## Completion Rule

An approval gate can be considered complete for this stage only when it is
visible in the My Workflows page, validates against the schema, and uses one of
the allowed non-executing modes. It cannot enable real action execution.

## HUB-V2-010 Report Export Integration

Approval Gates are included in the Demo Workflow Report Export safety snapshot.
The report can summarize gate name, workflow name, target action, target
connector, risk level, approval status, allowed execution mode, and block
reason.

Exporting an Approval Gate to Markdown, JSON, or CSV does not approve real
execution. Blocked gates remain blocked, and approval-required gates remain
manual-review metadata only.

Report export may write public-safe local files only to `outputs/public_reports/`
and must not create `outputs/private/`.
