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
    current_mission = f"""Building **{mission["title"]}** — {mission["description"]}

**Status:** {mission["status"]}"""

    # 2. Featured Projects (2-column layout)
    health_rows = ""
    projects = projects_data["featured_projects"]
    for i in range(0, len(projects), 2):
        p1 = projects[i]
        p2 = projects[i+1] if i+1 < len(projects) else None
        
        col1 = f"""      <h4>{p1["emoji"]} {p1["name"]}</h4>
      <p>{p1["description"]}</p>
      <p>🛠️ {" ".join(f"<code>{t}</code>" for t in p1["tech_stack"])}</p>
      <p>
        <a href="{p1["repo_url"]}"><b>Explore Repository »</b></a>
      </p>"""
         
        if p2:
            col2 = f"""      <h4>{p2["emoji"]} {p2["name"]}</h4>
      <p>{p2["description"]}</p>
      <p>🛠️ {" ".join(f"<code>{t}</code>" for t in p2["tech_stack"])}</p>
      <p>
        <a href="{p2["repo_url"]}"><b>Explore Repository »</b></a>
      </p>"""
        else:
            col2 = ""
            
        health_rows += f"""  <tr>
    <td valign="top" width="50%">
{col1}
    </td>
    <td valign="top" width="50%">
{col2}
    </td>
  </tr>\n"""
     
    featured_projects = f"""<table border="0" cellpadding="10" cellspacing="0" width="100%">
{health_rows.rstrip()}
</table>"""

    # 3. Statistics
    kernel_stats = f"""<div align="center">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
      <td valign="top" width="50%">
        <img src="https://github-readme-stats.vercel.app/api?username=sukhithms25&show_icons=true&theme=tokyonight&bg_color=0b0e14&title_color=00f0ff&text_color=c9d1d9&icon_color=00f0ff&hide_border=true" alt="Sukhith's GitHub Stats" width="100%" />
      </td>
      <td valign="top" width="50%">
        <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=sukhithms25&layout=compact&theme=tokyonight&bg_color=0b0e14&title_color=00f0ff&text_color=c9d1d9&icon_color=00f0ff&hide_border=true" alt="Sukhith's Top Languages" width="100%" />
      </td>
    </tr>
  </table>
</div>"""

    # 4. Connection Ports
    user = dashboard_data["user"]
    connection_ports = f"""<div align="center">

[![Email](https://img.shields.io/badge/Email-{user["email"]}-00f0ff?style=flat-square&logo=gmail&logoColor=0b0e14&labelColor=30363d)](mailto:{user["email"]})
&nbsp;&nbsp;&nbsp;&nbsp;
[![LinkedIn](https://img.shields.io/badge/LinkedIn-sukhithms25-00f0ff?style=flat-square&logo=linkedin&logoColor=0b0e14&labelColor=30363d)](https://{user["linkedin"]})

</div>"""

    # Load template
    template_path = os.path.join(base_dir, "README.template.md")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # Replace tokens
    final_content = template_content
    final_content = final_content.replace("{{ CURRENT_MISSION }}", current_mission)
    final_content = final_content.replace("{{ FEATURED_PROJECTS }}", featured_projects)
    final_content = final_content.replace("{{ KERNEL_STATISTICS }}", kernel_stats)
    final_content = final_content.replace("{{ CONNECTION_PORTS }}", connection_ports)
    
    # Output to ROOT README.md
    output_path = os.path.join(os.path.dirname(base_dir), "README.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"Successfully generated profile README.md at: {output_path}")

if __name__ == "__main__":
    main()
