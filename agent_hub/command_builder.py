from __future__ import annotations


def build_launch_command(agent: dict) -> str:
    """Build a local launch command string without executing it."""
    local_path = agent.get("local_path", "").strip()
    run_command = agent.get("run_command", "").strip()

    if run_command:
        return f'cd "{local_path}" && {run_command}'
    return f'cd "{local_path}"'


def build_open_github_command(agent: dict) -> str:
    """Return the GitHub URL for an agent, if one is registered."""
    return agent.get("github_url", "").strip()


def build_windows_open_folder_command(agent: dict) -> str:
    """Build a Windows Explorer command for the local project folder."""
    local_path = agent.get("local_path", "").strip()
    if not local_path:
        return ""
    return f'explorer "{local_path}"'


def build_project_command_pack(agent: dict) -> dict:
    """Build common local project commands without executing them."""
    local_path = agent.get("local_path", "").strip()
    return {
        "launch_streamlit": build_launch_command(agent),
        "open_folder": build_windows_open_folder_command(agent),
        "open_github": build_open_github_command(agent),
        "run_tests": f'cd "{local_path}" && python -m pytest' if local_path else "",
        "check_git_status": f'cd "{local_path}" && git status' if local_path else "",
    }
