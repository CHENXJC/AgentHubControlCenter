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
                "status": "streamlit_consultant_dashboard_complete",
                "showcase_status": "not_published_dashboard_demo",
                "pin_status": "not_applicable",
                "next_action": "CLIENTDELIVERYKIT-006-PUBLIC-SHOWCASE-PREP",
                "portfolio_value": "Shows client-facing AI automation consulting delivery workflow.",
            }
        ]
    )

    groups = {item["category_group"]: item for item in matrix}

    assert groups["Client Delivery / AI Consulting"]["projects"][0]["name"] == "ClientDeliveryKitAgent"


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
