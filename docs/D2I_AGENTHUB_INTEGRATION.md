# DataToInsightWorkflowAgent AgentHub Integration

Checkpoint: `HUB-V2-026-D2I-AGENTHUB-INTEGRATION-COMPLETE`

## Scope

AgentHubControlCenter now recognizes DataToInsightWorkflowAgent as a local
spoke project through its `agent_manifest.json` and reads its
`outputs/agenthub_summary.json` as a public-safe demo summary.

D2I public showcase status:

- Checkpoint: `D2I-007-FINAL-PUBLIC-RELEASE-CHECK-AND-GITHUB-RELEASE-COMPLETE`
- GitHub repo: `https://github.com/CHENXJC/DataToInsightWorkflowAgent`
- Next D2I decision: `D2I-008-OPTIONAL-PROFILE-PIN-DECISION`

## Files Read

| D2I file | Purpose |
| --- | --- |
| `F:\AIProjects\DataToInsightWorkflowAgent\agent_manifest.json` | Identity, category, safety flags, capabilities, dashboard path, report path, and summary path. |
| `F:\AIProjects\DataToInsightWorkflowAgent\agent_contract.json` | Contract for inputs, outputs, scoring, actions, and AgentHub summary schema. |
| `F:\AIProjects\DataToInsightWorkflowAgent\outputs\agenthub_summary.json` | Latest synthetic demo pipeline metrics and top routes. |

## Displayed In AgentHub

- Command Overview: D2I summary metrics
- My Tools / Agent Registry: D2I card and registry row
- Agent detail panel: dashboard path, report path, AgentHub summary path, and summary metrics
- Portfolio matrix: Data Workflow / Insight Engine group
- Future Plugin Interface / Agent Onboarding: valid local manifest import

## Displayed Metrics

- Total items processed
- High-value signals
- Medium-value items
- Low/noise/review items
- Recommended actions count
- Top routes
- Latest report path

## Safety Boundary

This integration is read-only metadata display. AgentHub does not execute D2I,
does not process real files, does not connect providers, and does not read
`.env`, token, credential, password, or secret files.
