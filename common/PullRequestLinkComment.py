from typing import Optional

from github.IssueComment import IssueComment
from github.PullRequest import PullRequest

from common.BotComment import BotComment
from common.Settings import Settings
from common.types import CiBuildResult


class PullRequestLinkComment:
    def __init__(self, settings: Settings):
        self._settings = settings

    def _update_links_comment(self, github_pr: PullRequest, github_comment, build_result: CiBuildResult):
        bot_comment = BotComment.from_text(github_comment.body, self._settings.comment)

        if bot_comment is not None and str(bot_comment.commit_sha) == github_pr.head.sha:
            bot_comment.add_build_result(build_result)
        else:
            bot_comment = self._generate_comment(github_pr, build_result)

        github_comment.edit(bot_comment.to_text(self._settings.comment))

    def update_or_create_links_comment(self, github_pr: PullRequest,
                                       build_result: CiBuildResult):
        github_comment = self._find_bot_pr_comment(github_pr)

        if github_comment:
            self._update_links_comment(github_pr, github_comment, build_result)
        else:
            new_bot_comment = self._generate_comment(github_pr, build_result)
            github_pr.create_issue_comment(new_bot_comment.to_text(self._settings.comment))

    @staticmethod
    def _generate_comment(github_pr: PullRequest, build_result: CiBuildResult):
        comment = BotComment(commit_sha=github_pr.head.sha)
        comment.add_build_result(build_result)
        return comment

    def _find_bot_pr_comment(self, github_pr: PullRequest) -> Optional[IssueComment]:
        for comment in github_pr.get_issue_comments():
            if comment.user.login == self._settings.github.username:
                return comment

        return None
