# HUB-WCC-INTEGRATION

## Purpose

WorkflowCommandCenterAgent is integrated into AgentHubControlCenter as the
project execution command spoke for the local-first AI Agent portfolio.

It represents the layer that helps turn project intent into Codex-ready
instructions, reusable workflow packs, execution checklists, prompt/rule
libraries, exportable delivery reports, and public showcase handoff material.

## WCC Source Metadata

| Field | Value |
| --- | --- |
| Project | `WorkflowCommandCenterAgent` |
| Chinese name | `AI 工作流指令中台 / 项目启动与执行控制台` |
| GitHub repo | `https://github.com/CHENXJC/WorkflowCommandCenterAgent` |
| Local path | `F:\AIProjects\WorkflowCommandCenterAgent` |
| AgentHub checkpoint | `WCC-004-GITHUB-PUBLIC-RELEASE-COMPLETE` |
| Status | `GitHub Public Showcase` |
| Profile pin | `Not pinned` |
| Category | `Workflow Orchestration / AgentOps / Project Command` |

## AgentHub Role

WCC is not a generic prompt library. It is the project execution command
infrastructure for the portfolio:

- Codex-ready project starter generation
- Workflow pack builder
- Execution checklist manager
- Demo project status tracking
- Prompt and rule library
- Delivery report generator
- Markdown / TXT / JSON export
- AgentHub-ready handoff metadata

## Integration Fields

AgentHubControlCenter uses the existing `data/agent_registry.csv` contract:

| AgentHub field | WCC value |
| --- | --- |
| `agent_name` | `WorkflowCommandCenterAgent` |
| `category` | `Workflow Orchestration / AgentOps / Project Command` |
| `status` | `Complete` |
| `stage` | `WCC-004-GITHUB-PUBLIC-RELEASE-COMPLETE` |
| `github_url` | `https://github.com/CHENXJC/WorkflowCommandCenterAgent` |
| `local_path` | `F:\AIProjects\WorkflowCommandCenterAgent` |
| `showcase_status` | `GitHub Public Showcase` |
| `pin_status` | `Not pinned` |
| `next_action` | `Optional profile pin decision or maintain-showcase` |

## Safety Boundary

- WCC manifests were checked in read-only mode.
- WCC project files were not modified.
- WCC scripts were not executed from AgentHub.
- WCC GitHub repo was not modified or pushed.
- No Profile Pin action was performed.
- No `.env`, credentials, tokens, passwords, or API keys were read.

## Validation

This checkpoint is covered by tests for:

- WCC registry fields
- WCC portfolio matrix placement
- WCC next-action handling
- WCC not-pinned UI label display
