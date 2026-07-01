from agent_hub.portfolio_matrix import (
    build_capability_summary,
    build_category_matrix,
    build_portfolio_positioning,
    build_priority_summary,
    build_project_matrix_view,
)


def test_build_category_matrix_returns_dict():
    agents = [
        {
            "agent_name": "Demo Agent",
            "category": "Demo",
            "primary_capability": "Demo workflow",
            "showcase_status": "GitHub Public Showcase",
            "pin_status": "Pinned",
        }
    ]

    matrix = build_category_matrix(agents)
    summary = build_capability_summary(agents)

    assert isinstance(matrix, dict)
    assert "Demo" in matrix
    assert summary[0]["agent_count"] == 1


def test_build_portfolio_positioning_returns_statement():
    positioning = build_portfolio_positioning(
        [
            {
                "agent_name": "VideoExtractSkill",
                "category": "Media Intelligence",
            }
        ]
    )

    assert "positioning_statement" in positioning
    assert "Media Intelligence" in positioning["capability_clusters"]


def test_build_project_matrix_view_returns_fixed_groups():
    matrix = build_project_matrix_view(
        [
            {
                "agent_name": "QuantLabAgent",
                "category": "quant_research",
                "status": "Complete",
                "showcase_status": "GitHub Public Showcase",
                "pin_status": "Pinned",
                "next_action": "Paused",
                "portfolio_value": "Shows quant research workflow.",
            }
        ]
    )

    groups = {item["category_group"]: item for item in matrix}

    assert "Finance / Market" in groups
    assert "Client Delivery / AI Consulting" in groups
    assert "Knowledge Base" in groups
    assert "Control Center / Meta Agent" in groups
    assert groups["Finance / Market"]["projects"][0]["name"] == "QuantLabAgent"
    assert groups["Knowledge Base"]["projects"] == []
    assert groups["Control Center / Meta Agent"]["projects"][0]["name"] == "AgentHubControlCenter"


def test_build_project_matrix_view_lists_client_delivery_spoke():
    matrix = build_project_matrix_view(
        [
            {
                "agent_name": "ClientDeliveryKitAgent",
                "category": "client_delivery",
                "status": "github_live_showcase_verified",
                "showcase_status": "live_showcase_verified",
                "pin_status": "recommend_pin",
                "next_action": "CLIENTDELIVERYKIT-011-PROFILE-PIN-OR-MAINTAIN-SHOWCASE-DECISION",
                "portfolio_value": "Shows client-facing AI automation consulting delivery workflow.",
            }
        ]
    )

    groups = {item["category_group"]: item for item in matrix}

    assert groups["Client Delivery / AI Consulting"]["projects"][0]["name"] == "ClientDeliveryKitAgent"
    assert groups["Client Delivery / AI Consulting"]["projects"][0]["showcase_status"] == "live_showcase_verified"
    assert "1 public showcase" in groups["Client Delivery / AI Consulting"]["status_summary"]
    assert "Review GitHub profile pin decision for ClientDeliveryKitAgent" in groups["Client Delivery / AI Consulting"]["next_step"]


def test_build_project_matrix_view_lists_data_workflow_spoke():
    matrix = build_project_matrix_view(
        [
            {
                "agent_name": "DataToInsightWorkflowAgent",
                "category": "Data Workflow / Insight Engine",
                "status": "agenthub_integration_complete",
                "showcase_status": "local_demo_dashboard_ready",
                "pin_status": "not_ready_for_pin_until_public_showcase",
                "next_action": "D2I-005 Public showcase preparation",
                "portfolio_value": "Shows data-to-insight scoring and action recommendation workflow.",
            }
        ]
    )

    groups = {item["category_group"]: item for item in matrix}

    assert "Data Workflow / Insight Engine" in groups
    assert groups["Data Workflow / Insight Engine"]["projects"][0]["name"] == "DataToInsightWorkflowAgent"


def test_build_project_matrix_view_lists_workflow_command_center_spoke():
    matrix = build_project_matrix_view(
        [
            {
                "agent_name": "WorkflowCommandCenterAgent",
                "category": "Workflow Orchestration / AgentOps / Project Command",
                "status": "Complete",
                "showcase_status": "GitHub Public Showcase",
                "pin_status": "Not pinned",
                "next_action": "Optional profile pin decision or maintain-showcase",
                "portfolio_value": "Shows Codex-ready workflow command and delivery report infrastructure.",
            }
        ]
    )

    groups = {item["category_group"]: item for item in matrix}

    assert "Workflow Orchestration / AgentOps" in groups
    wcc_projects = groups["Workflow Orchestration / AgentOps"]["projects"]
    assert wcc_projects[0]["name"] == "WorkflowCommandCenterAgent"
    assert wcc_projects[0]["showcase_status"] == "GitHub Public Showcase"
    assert "1 public showcase" in groups["Workflow Orchestration / AgentOps"]["status_summary"]
    assert "Review GitHub profile pin decision for WorkflowCommandCenterAgent" in groups["Workflow Orchestration / AgentOps"]["next_step"]


def test_build_priority_summary_returns_portfolio_buckets():
    summary = build_priority_summary(
        [
            {
                "agent_name": "NextOpsAgent",
                "category": "Workflow Automation",
                "status": "Complete",
                "showcase_status": "GitHub Public Showcase",
                "pin_status": "Not pinned",
                "next_action": "Profile pin optional, screenshots pending",
            },
            {
                "agent_name": "VideoExtractSkill",
                "category": "Media Intelligence",
                "status": "Complete",
                "showcase_status": "GitHub Public Showcase",
                "pin_status": "Pinned",
                "next_action": "Paused",
            },
        ],
        [
            {
                "agent_name": "NextOpsAgent",
                "priority": "Medium",
                "recommended_action": "Capture showcase screenshots",
            }
        ],
    )

    assert summary["next_best_project"] == "AgentHubControlCenter"
    assert summary["portfolio_follow_up"] == "NextOpsAgent: Capture showcase screenshots"
    assert "VideoExtractSkill" in summary["paused_projects"]
    assert "NextOpsAgent" in summary["github_showcase_projects"]
    assert summary["commercialization_candidates"][0]["agent_name"] == "NextOpsAgent"
