from agent_hub.registry_loader import (
    get_registry_summary,
    load_agent_registry,
    validate_agent_record,
    validate_registry,
)
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_load_agent_registry_returns_list(tmp_path):
    registry_file = tmp_path / "agent_registry.csv"
    registry_file.write_text(
        "agent_id,agent_name,status,next_action,pin_status,showcase_status,category\n"
        "demo, Demo Agent , Complete , Paused , Pinned , GitHub Public Showcase , Demo\n",
        encoding="utf-8",
    )

    agents = load_agent_registry(registry_file)

    assert isinstance(agents, list)
    assert agents[0]["agent_name"] == "Demo Agent"


def test_load_agent_registry_missing_file_returns_empty_list(tmp_path):
    assert load_agent_registry(tmp_path / "missing.csv") == []


def test_get_registry_summary_returns_total_agents():
    agents = [
        {
            "agent_name": "Demo Agent",
            "status": "Complete",
            "next_action": "Paused",
            "pin_status": "Pinned",
            "showcase_status": "GitHub Public Showcase",
            "category": "Demo",
        }
    ]

    summary = get_registry_summary(agents)

    assert summary["total_agents"] == 1
    assert summary["completed_agents"] == 1
    assert summary["public_showcase_agents"] == 1
    assert summary["pinned_agents"] == 1
    assert summary["public_not_pinned_agents"] == 0
    assert summary["paused_or_completed_agents"] == 1
    assert summary["categories_count"] == 1


def test_validate_agent_record_returns_quality_score():
    agent = {
        "agent_id": "demo",
        "agent_name": "Demo Agent",
        "category": "Demo",
        "project_type": "Agent",
        "local_path": "F:\\AIProjects\\Demo",
        "github_url": "https://github.com/example/demo",
        "status": "Complete",
        "stage": "DEMO-001",
        "primary_capability": "Demo workflow capability for a local dashboard",
        "tech_stack": "Python, Streamlit",
        "run_command": "streamlit run app.py",
        "portfolio_value": "Shows a complete local-first demo workflow.",
        "next_action": "Paused",
        "showcase_status": "GitHub Public Showcase",
        "pin_status": "Pinned",
    }

    result = validate_agent_record(agent)

    assert result["quality_score"] == 100
    assert result["is_valid"] is True


def test_validate_registry_returns_list():
    agents = [
        {
            "agent_name": "Incomplete Agent",
            "category": "Demo",
        }
    ]

    results = validate_registry(agents)

    assert isinstance(results, list)
    assert results[0]["is_valid"] is False


def test_static_registry_includes_workflow_command_center_agent():
    agents = load_agent_registry(ROOT / "data" / "agent_registry.csv")
    wcc = next(
        agent
        for agent in agents
        if agent.get("agent_name") == "WorkflowCommandCenterAgent"
    )

    assert wcc["github_url"] == "https://github.com/CHENXJC/WorkflowCommandCenterAgent"
    assert wcc["stage"] == "WCC-004-GITHUB-PUBLIC-RELEASE-COMPLETE"
    assert wcc["pin_status"] == "Not pinned"
    assert wcc["category"] == "Workflow Orchestration / AgentOps / Project Command"
    assert wcc["showcase_status"] == "GitHub Public Showcase"
    assert "project execution" in wcc["notes"].lower()
