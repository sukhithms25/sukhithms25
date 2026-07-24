import os
import json
import urllib.request
import subprocess
from datetime import datetime, timezone

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
        "primary_language": "N/A",
        "latest_project": "N/A",
        "last_updated": "N/A"
    }
    
    token = os.environ.get("GITHUB_TOKEN")

    def make_request(url, use_token=True):
        headers = {
            "User-Agent": "Specter-OS-Profile-Engine"
        }
        if use_token and token:
            headers["Authorization"] = f"token {token}"
        req = urllib.request.Request(url, headers=headers)
        return urllib.request.urlopen(req, timeout=10)

    try:
        # Step 1: User Profile info (total public repos)
        try:
            url = f"https://api.github.com/users/{username}"
            with make_request(url, use_token=True) as response:
                user_data = json.loads(response.read().decode())
                stats["repositories"] = user_data.get("public_repos", "N/A")
            use_auth = True
        except urllib.error.HTTPError as e:
            if e.code == 401:
                # Token unauthorized, retry without token
                url = f"https://api.github.com/users/{username}"
                with make_request(url, use_token=False) as response:
                    user_data = json.loads(response.read().decode())
                    stats["repositories"] = user_data.get("public_repos", "N/A")
                use_auth = False
            else:
                raise e

        # Step 2: List Repositories
        url_repos = f"https://api.github.com/users/{username}/repos?per_page=100"
        with make_request(url_repos, use_token=use_auth) as response:
            repos = json.loads(response.read().decode())

        non_forks = [r for r in repos if not r.get("fork", False)]

        # Step 3: Calculate Primary Language
        lang_bytes = {}
        for r in non_forks:
            lang_url = r.get("languages_url")
            fetched = False
            if lang_url and use_auth:
                try:
                    with make_request(lang_url, use_token=use_auth) as resp:
                        bytes_data = json.loads(resp.read().decode())
                        for lang, count in bytes_data.items():
                            lang_bytes[lang] = lang_bytes.get(lang, 0) + count
                        fetched = True
                except Exception:
                    pass

            if not fetched:
                lang = r.get("language")
                if lang:
                    lang_bytes[lang] = lang_bytes.get(lang, 0) + 100000

        if lang_bytes:
            stats["primary_language"] = max(lang_bytes, key=lang_bytes.get)

        # Step 4: Calculate Latest Project (excluding specified repos)
        exclude_repos = {"sukhithms25", "specter-template"}
        valid_repos = [r for r in non_forks if r["name"] not in exclude_repos]
        if valid_repos:
            valid_repos.sort(key=lambda r: r.get("pushed_at", ""), reverse=True)
            stats["latest_project"] = valid_repos[0]["name"]

        # Step 5: Last Updated
        stats["last_updated"] = datetime.now(timezone.utc).strftime("%d %b %Y")

    except Exception:
        pass

    return stats
