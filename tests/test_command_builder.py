from agent_hub.command_builder import build_project_command_pack


def test_build_project_command_pack_returns_expected_commands():
    agent = {
        "local_path": "F:\\AIProjects\\DemoAgent",
        "github_url": "https://github.com/example/demo",
        "run_command": "streamlit run app.py",
    }

    command_pack = build_project_command_pack(agent)

    assert "launch_streamlit" in command_pack
    assert "open_folder" in command_pack
    assert "open_github" in command_pack
    assert "run_tests" in command_pack
    assert "check_git_status" in command_pack
    assert command_pack["open_folder"] == 'explorer "F:\\AIProjects\\DemoAgent"'
