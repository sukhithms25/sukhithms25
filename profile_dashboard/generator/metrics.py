def compute_diagnostics_metrics(projects_data, github_stats, dashboard_data):
    featured = projects_data.get("featured_projects", [])
    total_repos = github_stats.get("repositories", "N/A")
    
    roadmap = dashboard_data.get("roadmap", {})
    current_sprint = "N/A"
    for sprint in roadmap.get("sprints", []):
        if sprint.get("status") == "Building":
            current_sprint = sprint.get("name", current_sprint)
            
    metrics = {
        "projects_building": len(featured),
        "total_repositories": total_repos,
        "current_sprint": current_sprint,
        "architecture_docs": "N/A",
        "automation_level": "N/A"
    }
    return metrics
