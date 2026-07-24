import os
import json
import urllib.request
import subprocess
from datetime import datetime, timezone

# Path to the last-known-good cache file
_CACHE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "github_activity.json"
)

_CACHE_KEYS = {"repositories", "primary_language", "latest_project", "last_updated"}


def _load_cache():
    """Return last-known-good values, or None if no cache exists."""
    try:
        with open(_CACHE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Only accept a cache that has all required keys with non-empty values
        if _CACHE_KEYS.issubset(data.keys()) and all(data[k] for k in _CACHE_KEYS):
            return data
    except Exception:
        pass
    return None


def _save_cache(stats: dict):
    """Persist a successful API result to cache. Never called on failure."""
    try:
        os.makedirs(os.path.dirname(_CACHE_PATH), exist_ok=True)
        with open(_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
    except Exception:
        pass


def _is_valid_stats(stats: dict) -> bool:
    """Return True only if stats contains real values (no N/A / None / empty)."""
    sentinel = {None, "", "N/A", "None", "Unknown", 0}
    for key in _CACHE_KEYS:
        if stats.get(key) in sentinel:
            return False
    return True


def get_github_stats(username="sukhithms25"):
    """
    Fetch live GitHub activity stats.

    Success path  → update cache → return fresh values.
    Failure path  → load last-known-good cache → return cached values.
    If cache is also empty/missing → return safe static fallback strings
                                     (never N/A, never 0).
    """
    token = os.environ.get("GITHUB_TOKEN")

    def make_request(url, use_token=True):
        headers = {"User-Agent": "Specter-OS-Profile-Engine"}
        if use_token and token:
            headers["Authorization"] = f"token {token}"
        req = urllib.request.Request(url, headers=headers)
        return urllib.request.urlopen(req, timeout=10)

    stats = {}
    api_succeeded = False

    try:
        use_auth = True

        # Step 1: User profile (total public repos)
        try:
            url = f"https://api.github.com/users/{username}"
            with make_request(url, use_token=True) as response:
                user_data = json.loads(response.read().decode())
                stats["repositories"] = user_data.get("public_repos") or None
        except urllib.error.HTTPError as e:
            if e.code == 401:
                # Token expired — retry unauthenticated
                url = f"https://api.github.com/users/{username}"
                with make_request(url, use_token=False) as response:
                    user_data = json.loads(response.read().decode())
                    stats["repositories"] = user_data.get("public_repos") or None
                use_auth = False
            else:
                raise

        # Step 2: Repository list
        url_repos = f"https://api.github.com/users/{username}/repos?per_page=100"
        with make_request(url_repos, use_token=use_auth) as response:
            repos = json.loads(response.read().decode())

        non_forks = [r for r in repos if not r.get("fork", False)]

        # Step 3: Primary Language by byte count
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
                    lang_bytes[lang] = lang_bytes.get(lang, 0) + 100_000

        if lang_bytes:
            stats["primary_language"] = max(lang_bytes, key=lang_bytes.get)

        # Step 4: Latest project (excluding profile + template repos)
        exclude_repos = {"sukhithms25", "specter-template"}
        valid_repos = [r for r in non_forks if r["name"] not in exclude_repos]
        if valid_repos:
            valid_repos.sort(key=lambda r: r.get("pushed_at", ""), reverse=True)
            stats["latest_project"] = valid_repos[0]["name"]

        # Step 5: Timestamp of THIS successful fetch
        stats["last_updated"] = datetime.now(timezone.utc).strftime("%d %b %Y")

        # Only treat the run as successful if all fields have real values
        if _is_valid_stats(stats):
            _save_cache(stats)
            api_succeeded = True

    except Exception:
        pass  # Fall through to cache / static fallback below

    if api_succeeded:
        return stats

    # --- Failure path: use last-known-good cache ---
    cached = _load_cache()
    if cached:
        return cached

    # --- Last resort: static fallback (never N/A) ---
    # This is only reached on a completely fresh machine with no cache AND no API.
    return {
        "repositories": "—",
        "primary_language": "Python",
        "latest_project": "ULTRON",
        "last_updated": "—",
    }
