from typing import Tuple

import github
from github.PullRequest import PullRequest
from github.Repository import Repository


class GithubHelper:
    FIND_MAX_ENTRIES = 30

    def __init__(self, settings):
        self._settings = settings
        self._github = github.Github(self._settings.GITHUB_USER, self._settings.GITHUB_TOKEN)

    def find_pr_from_commit(self, repo, commit_sha):
        if not isinstance(repo, Repository):
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


