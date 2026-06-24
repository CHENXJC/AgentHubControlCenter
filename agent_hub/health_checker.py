from __future__ import annotations

from pathlib import Path


HEALTH_CHECKS = [
    ("path_exists", "Local path", 20),
    ("readme_exists", "README.md", 15),
    ("requirements_exists", "requirements.txt", 10),
    ("app_exists", "app.py", 10),
    ("git_folder_exists", ".git", 10),
    ("tests_folder_exists", "tests/", 10),
    ("docs_folder_exists", "docs/", 8),
    ("project_status_exists", "PROJECT_STATUS.md", 8),
    ("portfolio_folder_exists", "portfolio/", 4),
    ("github_url_exists", "GitHub URL", 5),
]


def _health_status_from_score(health_score: int) -> str:
    """Map a numeric health score to a portfolio health label."""
    if health_score >= 85:
        return "Showcase Ready"
    if health_score >= 70:
        return "Healthy"
    if health_score >= 50:
        return "Partial"
    return "Missing or Incomplete"


def _suggest_fix(missing_items: list[str]) -> str:
    """Build a short remediation suggestion from missing health check items."""
    if not missing_items:
        return "Project looks showcase-ready."
    if "Local path" in missing_items:
        return "Local path not found. Confirm project location or update registry."

    core_items = [item for item in missing_items if item in {"README.md", "requirements.txt", "app.py"}]
    if core_items:
        return "Add " + " and ".join(core_items[:2]) + " before public showcase."

    return "Complete missing project structure files before public showcase."


def check_agent_health(agent: dict) -> dict:
    """Check local project files for one registered agent."""
    local_path = agent.get("local_path", "").strip()
    project_path = Path(local_path) if local_path else Path()

    path_exists = bool(local_path) and project_path.exists()
    readme_exists = path_exists and (project_path / "README.md").is_file()
    requirements_exists = path_exists and (project_path / "requirements.txt").is_file()
    app_exists = path_exists and (project_path / "app.py").is_file()
    git_folder_exists = path_exists and (project_path / ".git").is_dir()
    tests_folder_exists = path_exists and (project_path / "tests").is_dir()
    docs_folder_exists = path_exists and (project_path / "docs").is_dir()
    project_status_exists = path_exists and (project_path / "PROJECT_STATUS.md").is_file()
    portfolio_folder_exists = path_exists and (project_path / "portfolio").is_dir()
    github_url_exists = bool(agent.get("github_url", "").strip())

    check_values = {
        "path_exists": path_exists,
        "readme_exists": readme_exists,
        "requirements_exists": requirements_exists,
        "app_exists": app_exists,
        "git_folder_exists": git_folder_exists,
        "tests_folder_exists": tests_folder_exists,
        "docs_folder_exists": docs_folder_exists,
        "project_status_exists": project_status_exists,
        "portfolio_folder_exists": portfolio_folder_exists,
        "github_url_exists": github_url_exists,
    }
    health_score = sum(points for key, _label, points in HEALTH_CHECKS if check_values[key])
    health_status = _health_status_from_score(health_score)
    missing_items = [label for key, label, _points in HEALTH_CHECKS if not check_values[key]]
    warnings = []

    if not path_exists:
        warnings.append("Local path not found")
    warnings.extend(f"{item} missing" for item in missing_items if item != "Local path")

    return {
        "agent_name": agent.get("agent_name", ""),
        "local_path": local_path,
        "path_exists": path_exists,
        "readme_exists": readme_exists,
        "requirements_exists": requirements_exists,
        "app_exists": app_exists,
        "git_folder_exists": git_folder_exists,
        "tests_folder_exists": tests_folder_exists,
        "docs_folder_exists": docs_folder_exists,
        "project_status_exists": project_status_exists,
        "portfolio_folder_exists": portfolio_folder_exists,
        "github_url_exists": github_url_exists,
        "health_score": health_score,
        "health_status": health_status,
        "missing_items": missing_items,
        "warnings": "; ".join(warnings),
        "suggested_fix": _suggest_fix(missing_items),
        "last_checked_note": "Local filesystem presence check only.",
    }


def check_all_agents_health(agents: list[dict]) -> list[dict]:
    """Run local health checks for all registered agents."""
    return [check_agent_health(agent) for agent in agents]
