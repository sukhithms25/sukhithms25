import os
import json
import urllib.request
import subprocess
from datetime import datetime

def get_local_git_info():
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        commit_time = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        if commit_time:
            # Handle possible ISO format offsets
            t_str = commit_time.replace("Z", "+00:00")
            dt = datetime.fromisoformat(t_str)
            formatted_time = dt.strftime("%Y-%m-%d %H:%M UTC")
        else:
            formatted_time = "N/A"
            
        return {
            "branch": branch,
            "last_commit": formatted_time
        }
    except Exception:
        return {
            "branch": "N/A",
            "last_commit": "N/A"
        }

def get_github_stats(username="sukhithms25"):
    stats = {
        "repositories": "N/A",
        "stars": "N/A",
        "last_push": "N/A",
        "top_language": "N/A"
    }
    
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "User-Agent": "Specter-OS-Profile-Engine"
    }
    if token:
        headers["Authorization"] = f"token {token}"
        
    try:
        url = f"https://api.github.com/users/{username}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            user_data = json.loads(response.read().decode())
            stats["repositories"] = user_data.get("public_repos", "N/A")
            
        url_repos = f"https://api.github.com/users/{username}/repos?per_page=100"
        req_repos = urllib.request.Request(url_repos, headers=headers)
        with urllib.request.urlopen(req_repos, timeout=5) as response:
            repos = json.loads(response.read().decode())
            stars = sum(repo.get("stargazers_count", 0) for repo in repos)
            stats["stars"] = stars
            
            if repos:
                repos_sorted = sorted(repos, key=lambda r: r.get("pushed_at", ""), reverse=True)
                stats["last_push"] = repos_sorted[0].get("pushed_at", "N/A")
                
                langs = {}
                for r in repos:
                    lang = r.get("language")
                    if lang:
                        langs[lang] = langs.get(lang, 0) + 1
                if langs:
                    stats["top_language"] = max(langs, key=langs.get)
    except Exception:
        pass
        
    return stats
