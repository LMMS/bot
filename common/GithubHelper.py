from typing import Optional

import github
from github.PullRequest import PullRequest

from common.Settings import Settings


class GithubHelper:
    FIND_MAX_ENTRIES = 30

    def __init__(self, settings: Settings.Github):
        self._settings = settings
        self._github = github.Github(self._settings.username, self._settings.token.get_secret_value())

    @staticmethod
    def has_ignored_labels(settings: Settings.PullRequest, pull_request: PullRequest):
        for ignored_label in settings.ignored_labels:
            if ignored_label in (label.name for label in pull_request.labels):
                return True
        return False

    def find_pr_from_commit(self, repo: str, commit_sha: str) -> Optional[PullRequest]:
        repo = self._github.get_repo(repo)

        '''
        Try to find the pull request from the info we got.
        We currently have just the sha of the commit and nothing else. 
        Therefore, we'll have to lookup each pr by its head and compare it to our hash.
        '''
        pr_or_list = repo.get_pulls(
            sort="updated",
            direction="desc",
        )

        if isinstance(pr_or_list, PullRequest):
            return pr_or_list

        pr: PullRequest
        for pr in pr_or_list[:self.FIND_MAX_ENTRIES]:
            if pr.head.sha == commit_sha:
                return pr

        return None
