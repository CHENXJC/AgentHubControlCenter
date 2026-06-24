from agent_hub.health_checker import check_agent_health


def test_check_agent_health_missing_path_does_not_crash(tmp_path):
    missing_path = tmp_path / "missing-agent"
    agent = {
        "agent_name": "Missing Agent",
        "local_path": str(missing_path),
        "github_url": "",
    }

    result = check_agent_health(agent)

    assert result["path_exists"] is False
    assert result["health_status"] == "Missing or Incomplete"
    assert "Local path not found" in result["warnings"]
    assert "Local path" in result["missing_items"]


def test_check_agent_health_returns_missing_items(tmp_path):
    project_path = tmp_path / "partial-agent"
    project_path.mkdir()
    (project_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    agent = {
        "agent_name": "Partial Agent",
        "local_path": str(project_path),
        "github_url": "https://github.com/example/partial",
    }

    result = check_agent_health(agent)

    assert "missing_items" in result
    assert "requirements.txt" in result["missing_items"]
    assert result["health_status"] in {"Partial", "Missing or Incomplete"}
