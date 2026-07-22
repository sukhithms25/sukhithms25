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
from github_api import get_github_stats, get_local_git_info
from mermaid import generate_mermaid_diagram
from metrics import compute_diagnostics_metrics

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
        
    # Get Live Stats & Local Git Info
    github_stats = get_github_stats()
    git_info = get_local_git_info()
    
    # Calculate Diagnostics Metrics
    computed_metrics = compute_diagnostics_metrics(projects_data, github_stats, dashboard_data)
    
    # Generate Components
    
    # 1. Command Center (using real local Git branch and commit info)
    user = dashboard_data["user"]
    command_center = f"""<div align="center">

```text
┌──────────────────────────────────────────────────────────┐
│                     SPECTER OS v2.0                      │
├──────────────────────────────────────────────────────────┤
│  USER      : {user["name"].upper():<44} │
│  ROLE      : {user["role"].upper():<44} │
│  STATUS    : {user["status"].upper():<44} │
│  PROJECT   : {dashboard_data["current_mission"]["title"].upper():<44} │
│  BRANCH    : {git_info["branch"].upper():<44} │
│  COMMIT    : {git_info["last_commit"].upper():<44} │
└──────────────────────────────────────────────────────────┘
```

</div>"""

    # 2. Mission & Philosophy
    mission = dashboard_data["current_mission"]
    philosophy_list = ""
    for item in dashboard_data["philosophy"]:
        philosophy_list += f'        <li><b>{item["title"]}</b> {item["desc"]}</li>\n'
        
    mission_philosophy = f"""<table border="0" cellpadding="10" cellspacing="0" width="100%">
  <tr>
    <td valign="top" width="50%">
      <h3>🚀 Current Mission</h3>
      <p>Building <b>{mission["title"]}</b>, {mission["description"]}</p>
      <p><b>Status:</b> {mission["status"]}</p>
    </td>
    <td valign="top" width="50%">
      <h3>🧠 Engineering Philosophy</h3>
      <ul>
{philosophy_list.rstrip()}
      </ul>
    </td>
  </tr>
</table>"""

    # 3. Ecosystem & Roadmap
    roadmap = dashboard_data["roadmap"]
    sprints_str = ""
    for sprint in roadmap["sprints"]:
        sprints_str += f'{sprint["name"]:<10} : {sprint["status"]}\n'
        
    ecosystem_roadmap = f"""<table border="0" cellpadding="10" cellspacing="0" width="100%">
  <tr>
    <td valign="top" width="55%">
      <h3>🌐 Repository Ecosystem</h3>
      <pre>
          SPECTER ECOSYSTEM

                ULTRON
                   │
   ┌───────────────┼───────────────┐
   │               │               │
git_ai          CAPA        Krishi Setu
   │
   │
Developer Tooling
      </pre>
    </td>
    <td valign="top" width="45%">
      <h3>📅 System Roadmap</h3>
      <pre>
Year: {roadmap["year"]}
Status: {roadmap["status"]}

{sprints_str.rstrip()}
      </pre>
    </td>
  </tr>
</table>"""

    # 4. Journal & AI Agent Architecture
    journal = dashboard_data["journal"]
    today_logs = ""
    for log in journal["today"]:
        if log.startswith("✓") or log.startswith("→") or log.startswith("-"):
            today_logs += f"{log}\n"
        else:
            today_logs += f"✓ {log}\n"
            
    next_logs = ""
    for log in journal["next"]:
        next_logs += f"- {log}\n"
        
    journal_agents = f"""<table border="0" cellpadding="10" cellspacing="0" width="100%">
  <tr>
    <td valign="top" width="55%">
      <h3>🗒️ Live Development Journal</h3>
      <pre>
Today's Progress:
{today_logs.rstrip()}

Next:
{next_logs.rstrip()}
      </pre>
    </td>
    <td valign="top" width="45%">
      <h3>🤖 AI Agent Architecture</h3>
      <pre>
Target Agents:
• Planner Agent      [In Development]
• Memory Agent       [In Development]
• Reasoner Agent     [In Development]
• Executor Agent     [In Development]
      </pre>
    </td>
  </tr>
</table>"""

    # 5. Mermaid Architecture
    mermaid_diagram = generate_mermaid_diagram(projects_data)

    # 6. Repository Health Matrix
    health_rows = ""
    projects = projects_data["featured_projects"]
    for i in range(0, len(projects), 2):
        p1 = projects[i]
        p2 = projects[i+1] if i+1 < len(projects) else None
        
        col1 = f"""      <h4>{p1["emoji"]} {p1["name"]}</h4>
      <pre>
Version    : {p1["version"]}
Status     : {p1["status"]}
Tests      : {p1["tests"]}
Coverage   : {p1["coverage"]}
Deployment : {p1["deployment"]}
      </pre>
      <a href="{p1["repo_url"]}"><b>Explore {p1["name"]} »</b></a><br />
      [![Status: {p1["badge_status"]}](https://img.shields.io/badge/Status-{p1["badge_status"]}-{p1["badge_color"]}?style=flat-square&labelColor=30363d)](#)"""
         
        if p2:
            col2 = f"""      <h4>{p2["emoji"]} {p2["name"]}</h4>
      <pre>
Version    : {p2["version"]}
Status     : {p2["status"]}
Tests      : {p2["tests"]}
Coverage   : {p2["coverage"]}
Deployment : {p2["deployment"]}
      </pre>
      <a href="{p2["repo_url"]}"><b>Explore {p2["name"]} »</b></a><br />
      [![Status: {p2["badge_status"]}](https://img.shields.io/badge/Status-{p2["badge_status"]}-{p2["badge_color"]}?style=flat-square&labelColor=30363d)](#)"""
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
     
    repository_health = f"""<table border="0" cellpadding="10" cellspacing="0" width="100%">
{health_rows.rstrip()}
</table>"""

    # 7. Tech Radar
    radar = projects_data["tech_radar"]
    learning = "\n".join(f"        <li>{tech}</li>" for tech in radar["learning"])
    building = "\n".join(f"        <li>{tech}</li>" for tech in radar["building"])
    mastered = "\n".join(f"        <li>{tech}</li>" for tech in radar["mastered"])
    
    tech_radar = f"""<table border="0" cellpadding="10" cellspacing="0" width="100%">
  <tr>
    <td valign="top" width="33%">
      <h4>🟢 Learning</h4>
      <ul>
{learning}
      </ul>
    </td>
    <td valign="top" width="33%">
      <h4>🔵 Building</h4>
      <ul>
{building}
      </ul>
    </td>
    <td valign="top" width="33%">
      <h4>🟣 Mastered</h4>
      <ul>
{mastered}
      </ul>
    </td>
  </tr>
</table>"""

    # 8. Diagnostics panel
    system_diagnostics = f"""<table border="0" cellpadding="10" cellspacing="0" width="100%">
  <tr>
    <td valign="top" width="100%">
      <h3>📊 System Diagnostics</h3>
      <pre>
Projects Configured : {computed_metrics["projects_building"]}
Total Repositories  : {computed_metrics["total_repositories"]}
Current Sprint      : {computed_metrics["current_sprint"]}
Architecture Docs   : {computed_metrics["architecture_docs"]}
Automation Level    : {computed_metrics["automation_level"]}
      </pre>
    </td>
  </tr>
</table>"""

    # 9. Statistics
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

    # 10. Console Commands (Interactive clickables)
    command_console = f"""<pre>
guest@specter:~$ <a href="https://github.com/sukhithms25/ULTRON/tree/main/specter-rfcs">system status</a>
Kernel: Active | Cognitive Budget: 92% | Logs: Normal

guest@specter:~$ <a href="mailto:{user["email"]}">whoami</a>
User: Sukhith M S | Role: AI Systems Engineer | Status: Ready

guest@specter:~$ <a href="https://github.com/sukhithms25?tab=repositories">ls</a>
bin/  ultron/  git_ai/  capa/  krishi-setu/
</pre>"""

    # 11. Connection Ports
    connection_ports = f"""<div align="center">

[![Email](https://img.shields.io/badge/Email-{user["email"]}-00f0ff?style=flat-square&logo=gmail&logoColor=0b0e14&labelColor=30363d)](mailto:{user["email"]})
&nbsp;&nbsp;&nbsp;&nbsp;
[![LinkedIn](https://img.shields.io/badge/LinkedIn-sukhithms25-00f0ff?style=flat-square&logo=linkedin&logoColor=0b0e14&labelColor=30363d)](https://{user["linkedin"]})
&nbsp;&nbsp;&nbsp;&nbsp;
[![Portfolio-Coming Soon](https://img.shields.io/badge/Portfolio-Coming%20Soon-58a6ff?style=flat-square&logo=github&logoColor=0b0e14&labelColor=30363d)](#)

</div>"""

    # Load template
    template_path = os.path.join(base_dir, "README.template.md")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # Replace tokens
    final_content = template_content
    final_content = final_content.replace("{{ COMMAND_CENTER }}", command_center)
    final_content = final_content.replace("{{ MISSION_PHILOSOPHY }}", mission_philosophy)
    final_content = final_content.replace("{{ ECOSYSTEM_ROADMAP }}", ecosystem_roadmap)
    final_content = final_content.replace("{{ JOURNAL_AGENTS }}", journal_agents)
    final_content = final_content.replace("{{ MERMAID_DIAGRAM }}", mermaid_diagram)
    final_content = final_content.replace("{{ REPOSITORY_HEALTH }}", repository_health)
    final_content = final_content.replace("{{ TECH_RADAR }}", tech_radar)
    final_content = final_content.replace("{{ KERNEL_STATISTICS }}", kernel_stats)
    final_content = final_content.replace("{{ COMMAND_CONSOLE }}", command_console)
    final_content = final_content.replace("{{ CONNECTION_PORTS }}", connection_ports)
    
    # Output to ROOT README.md
    output_path = os.path.join(os.path.dirname(base_dir), "README.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    print(f"Successfully generated profile README.md at: {output_path}")

if __name__ == "__main__":
    main()
