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
