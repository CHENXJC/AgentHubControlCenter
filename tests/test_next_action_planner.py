from agent_hub.next_action_planner import build_next_action_plan, summarize_next_actions


def test_build_next_action_plan_returns_priority():
    agents = [
        {
            "agent_name": "Demo Agent",
            "status": "Complete",
            "category": "Demo",
            "next_action": "Paused",
            "pin_status": "Pinned",
        }
    ]
    health_results = [
        {
            "agent_name": "Demo Agent",
            "health_status": "Missing or Incomplete",
            "missing_items": ["Local path"],
        }
    ]
    validation_results = [
        {
            "agent_name": "Demo Agent",
            "is_valid": True,
            "missing_required_fields": [],
        }
    ]

    action_plan = build_next_action_plan(agents, health_results, validation_results)

    assert action_plan[0]["priority"] == "High"


def test_summarize_next_actions_returns_high_priority():
    summary = summarize_next_actions(
        [
            {
                "agent_name": "Demo Agent",
                "priority": "High",
                "recommended_action": "Fix registry metadata",
            }
        ]
    )

    assert summary["high_priority"] == 1


def test_build_next_action_plan_handles_workflow_command_center_pin_review():
    agents = [
        {
            "agent_name": "WorkflowCommandCenterAgent",
            "status": "Complete",
            "category": "Workflow Orchestration / AgentOps / Project Command",
            "next_action": "Optional profile pin decision or maintain-showcase",
            "pin_status": "Not pinned",
        }
    ]
    health_results = [
        {
            "agent_name": "WorkflowCommandCenterAgent",
            "health_status": "Showcase Ready",
            "missing_items": [],
        }
    ]
    validation_results = [
        {
            "agent_name": "WorkflowCommandCenterAgent",
            "is_valid": True,
            "missing_required_fields": [],
        }
    ]

    action_plan = build_next_action_plan(agents, health_results, validation_results)

    assert action_plan[0]["priority"] == "Low"
    assert action_plan[0]["recommended_action"] == "Review GitHub profile pin decision"
    assert action_plan[0]["category"] == "Workflow Orchestration / AgentOps / Project Command"
