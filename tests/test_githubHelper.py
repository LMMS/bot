from unittest import TestCase
from unittest.mock import Mock, patch

from common.GithubHelper import GithubHelper
from settings import settings
from helpers import load_json_object


class TestGithubHelper(TestCase):
    def setUp(self) -> None:
        patcher = patch('github.Github', new_callable=Mock)
        self.GithubMock = patcher.start()
        self.addCleanup(patcher.stop)

    def test_find_pr_from_commit(self):
        github_obj = Mock()
        self.GithubMock.return_value = github_obj

        repo = Mock()
        github_obj.get_repo = Mock(return_value=repo)

        get_pulls_result = load_json_object("data/get_pulls.json")
        repo.get_pulls = Mock(return_value=get_pulls_result)

        self._github = GithubHelper(settings.github)

        for pull in get_pulls_result[:10]:
            self.assertIsNotNone(self._github.find_pr_from_commit("repo", pull.head.sha))

        self.assertIsNone(self._github.find_pr_from_commit("repo", 'invalid_sha'))

