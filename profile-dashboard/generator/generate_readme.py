import os
import sys
import json
from datetime import datetime

# Programmatic dependency loading
try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
    import yaml

# Import generator sub-modules
from github_api import get_github_stats

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, "config")
    
    # Load Configurations
    with open(os.path.join(config_dir, "theme.yaml"), "r", encoding="utf-8") as f:
        theme_data = yaml.safe_load(f)
        
    with open(os.path.join(config_dir, "dashboard.yaml"), "r", encoding="utf-8") as f:
        dashboard_data = yaml.safe_load(f)
        
    with open(os.path.join(config_dir, "projects.yaml"), "r", encoding="utf-8") as f:
        projects_data = yaml.safe_load(f)
        
    # Get Live Stats
    github_stats = get_github_stats()
    
    # 1. Current Mission
    mission = dashboard_data["current_mission"]
    current_mission = f"""Building **{mission["title"]}** — {mission["description"]}"""

    # 2. Featured Projects (Vertical stack)
    project_blocks = []
    projects = projects_data["featured_projects"]
    for p in projects:
        tags = " ".join(f"`{t}`" for t in p["tech_stack"])
        block = f"""### {p["emoji"]} {p["display_name"]}

{p["description"]}

🛠️ {tags}

<a href="{p["repo_url"]}"><b>View Project →</b></a>"""
        project_blocks.append(block)
        
    featured_projects = "\n\n---\n\n".join(project_blocks)

    # 3. Technologies
    catalog = projects_data["tech_stack_catalog"]
    langs_badges = " ".join(f'![{t["name"]}]({t["badge_url"]})' for t in catalog["languages"])
    backend_badges = " ".join(f'![{t["name"]}]({t["badge_url"]})' for t in catalog["backend"])
    ai_ml_badges = " ".join(f'![{t["name"]}]({t["badge_url"]})' for t in catalog["ai_ml"])
    tools_badges = " ".join(f'![{t["name"]}]({t["badge_url"]})' for t in catalog["tools_infra"])

    technologies = f"""**Languages**

{langs_badges}

**Backend**

{backend_badges}

**AI / ML**

{ai_ml_badges}

**Tools & Infrastructure**

{tools_badges}"""

    # 4. GitHub Activity (Vertical stack)
    kernel_stats = f"""**Repositories**
{github_stats["repositories"]}

**Primary Language**
{github_stats["primary_language"]}

**Latest Project**
{github_stats["latest_project"]}

**Updated**
{github_stats["last_updated"]}"""

    # 5. Connection Ports
    user = dashboard_data["user"]
    connection_ports = f"""<div align="center">
  <a href="mailto:{user["email"]}">
    <img src="https://img.shields.io/badge/Email-Contact_Me-00f0ff?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  &nbsp;
  <a href="https://{user["linkedin"]}">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
</div>"""

    # Load template
    template_path = os.path.join(base_dir, "README.template.md")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # Replace tokens
    final_content = template_content
    final_content = final_content.replace("{{ CURRENT_MISSION }}", current_mission)
    final_content = final_content.replace("{{ FEATURED_PROJECTS }}", featured_projects)
    final_content = final_content.replace("{{ TECHNOLOGIES }}", technologies)
    final_content = final_content.replace("{{ KERNEL_STATISTICS }}", kernel_stats)
    final_content = final_content.replace("{{ CONNECTION_PORTS }}", connection_ports)
    
    # Output to ROOT README.md
    output_path = os.path.join(os.path.dirname(base_dir), "README.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"Successfully generated profile README.md at: {output_path}")

if __name__ == "__main__":
    main()
