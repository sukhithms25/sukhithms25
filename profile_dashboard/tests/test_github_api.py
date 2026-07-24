import os
import json
import unittest
from unittest.mock import patch, MagicMock

from profile_dashboard.generator import github_api

class TestGitHubApiResilience(unittest.TestCase):

    def setUp(self):
        self.test_cache_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "test_github_activity.json"
        )
        self.original_cache_path = github_api._CACHE_PATH
        github_api._CACHE_PATH = self.test_cache_path

        # Initial valid cache data
        self.valid_cache = {
            "repositories": 36,
            "primary_language": "Python",
            "latest_project": "ULTRON",
            "last_updated": "24 Jul 2026"
        }
        os.makedirs(os.path.dirname(self.test_cache_path), exist_ok=True)
        with open(self.test_cache_path, "w", encoding="utf-8") as f:
            json.dump(self.valid_cache, f)

    def tearDown(self):
        github_api._CACHE_PATH = self.original_cache_path
        if os.path.exists(self.test_cache_path):
            os.remove(self.test_cache_path)

    @patch("profile_dashboard.generator.github_api.urllib.request.urlopen")
    def test_successful_api_fetch_updates_cache(self, mock_urlopen):
        # Setup mock responses for user profile and repos
        user_response = MagicMock()
        user_response.read.return_value = json.dumps({"public_repos": 40}).encode("utf-8")
        user_response.__enter__.return_value = user_response

        repos_response = MagicMock()
        repos_response.read.return_value = json.dumps([
            {"name": "ULTRON-NEW", "fork": False, "pushed_at": "2026-07-24T20:00:00Z", "language": "Python"}
        ]).encode("utf-8")
        repos_response.__enter__.return_value = repos_response

        mock_urlopen.side_effect = [user_response, repos_response]

        stats = github_api.get_github_stats("sukhithms25")

        self.assertEqual(stats["repositories"], 40)
        self.assertEqual(stats["latest_project"], "ULTRON-NEW")
        
        # Verify cache file was updated
        with open(self.test_cache_path, "r", encoding="utf-8") as f:
            cached_data = json.load(f)
        self.assertEqual(cached_data["repositories"], 40)
        self.assertEqual(cached_data["latest_project"], "ULTRON-NEW")

    @patch("profile_dashboard.generator.github_api.urllib.request.urlopen")
    def test_failed_api_fetch_uses_cache(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Network / API failure")

        stats = github_api.get_github_stats("sukhithms25")

        self.assertEqual(stats["repositories"], 36)
        self.assertEqual(stats["primary_language"], "Python")
        self.assertEqual(stats["latest_project"], "ULTRON")
        self.assertEqual(stats["last_updated"], "24 Jul 2026")

    @patch("profile_dashboard.generator.github_api.urllib.request.urlopen")
    def test_failed_api_fetch_does_not_overwrite_cache(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("API Outage")

        github_api.get_github_stats("sukhithms25")

        # Cache file should remain unchanged
        with open(self.test_cache_path, "r", encoding="utf-8") as f:
            cached_data = json.load(f)
        self.assertEqual(cached_data, self.valid_cache)

    @patch("profile_dashboard.generator.github_api.urllib.request.urlopen")
    def test_invalid_or_empty_api_response_does_not_destroy_valid_cache(self, mock_urlopen):
        user_response = MagicMock()
        user_response.read.return_value = json.dumps({}).encode("utf-8") # Missing public_repos
        user_response.__enter__.return_value = user_response

        repos_response = MagicMock()
        repos_response.read.return_value = json.dumps([]).encode("utf-8")
        repos_response.__enter__.return_value = repos_response

        mock_urlopen.side_effect = [user_response, repos_response]

        stats = github_api.get_github_stats("sukhithms25")

        # Should fall back to cached valid values because API returned invalid/empty data
        self.assertEqual(stats, self.valid_cache)

        # Cache file must not be overwritten with empty/invalid data
        with open(self.test_cache_path, "r", encoding="utf-8") as f:
            cached_data = json.load(f)
        self.assertEqual(cached_data, self.valid_cache)

if __name__ == "__main__":
    unittest.main()
