from typing import Tuple

import github
from github.PullRequest import PullRequest


class PullRequestLinkComment:
    SHA_PREFIX = "SHA: "

    def __init__(self, settings):
        self._settings = settings
        self._github = github.Github(self._settings.GITHUB_USER, self._settings.GITHUB_TOKEN)

    def _platform_from_link(self, link):
        for extension, title in self._settings.EXTENSION_TO_PLATFORM_TITLE.items():
            if link.endswith(extension):
                return title

        return None

    def _generate_sha_line(self, sha):
        return "{sha_prefix}{sha}".format(sha=sha, sha_prefix=self.SHA_PREFIX)

    def _parse_sha_line(self, comment_body: str):
        return comment_body.splitlines()[-1][len(self.SHA_PREFIX):]

    def _generate_comment_from_platforms_and_links(self, links_and_platforms):
        comment = self._settings.BOT_COMMENT_BODY_TEMPLATE

        comment += ''.join(self._generate_comment_download_lines(links_and_platforms))

        comment += self._settings.BOT_COMMENT_FOOTER

        return comment

    def _generate_comment_download_lines(self, links_and_platforms):
        for link, platform in links_and_platforms:
            yield self._settings.BOT_COMMENT_DOWNLOAD_LINE_TEMPLATE.format(platform=platform, link=link)

    def _update_links_comment(self, github_pr: PullRequest, bot_comment, links_and_platform_names):
        # Check the sha line, if it is not up to date to pr.head.sha, regenerate the whole comment.
        sha = self._parse_sha_line(bot_comment.body)

        if sha == github_pr.head.sha:
            # Skip sha line.
            new_body = bot_comment.body[:bot_comment.body.rfind('\n')]

            new_body = new_body[:-len(self._settings.BOT_COMMENT_FOOTER)]
            new_body += ''.join(self._generate_comment_download_lines(links_and_platform_names)) + \
                        self._settings.BOT_COMMENT_FOOTER + '\n' + self._generate_sha_line(sha)
        else:
            new_body = self._generate_comment(github_pr, links_and_platform_names)

        bot_comment.edit(new_body)

    def update_or_create_links_comment(self, github_pr: PullRequest, artifact_links: Tuple[str]):
        links_and_platform_names = tuple(self._resolve_artifact_links_titles(artifact_links))
        if not links_and_platform_names:
            return

        bot_comment = self._find_bot_pr_comment(github_pr)

        if bot_comment is not None:
            self._update_links_comment(github_pr, bot_comment, links_and_platform_names)
        else:
            new_body = self._generate_comment(github_pr, links_and_platform_names)
            github_pr.create_issue_comment(new_body)

    def _generate_comment(self, github_pr, links_and_platform_names):
        new_body = self._generate_comment_from_platforms_and_links(
            links_and_platform_names) + "\n" + self._generate_sha_line(github_pr.head.sha)
        return new_body

    def _resolve_artifact_links_titles(self, artifact_links):
        for link in artifact_links:
            link_title = self._platform_from_link(link)

            if link_title is not None:
                yield link, link_title

    def _find_bot_pr_comment(self, github_pr):
        for comment in github_pr.get_issue_comments():
            if comment.user.login == self._settings.GITHUB_USER:
                return comment

        return None
