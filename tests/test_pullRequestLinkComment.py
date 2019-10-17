from unittest import TestCase
from unittest.mock import Mock

from common.BotComment import BotComment
from common.PullRequestLinkComment import PullRequestLinkComment
from common.types import CiBuildResult, ArtifactDownload, ArtifactTitle, ArtifactLink, BuildLink, CiTitle, CommitSHA
from helpers import load_json_object
from settings import settings


class TestPullRequestLinkComment(TestCase):
    def setUp(self) -> None:
        self.instance = PullRequestLinkComment(settings)
        self.build_result = CiBuildResult(
            artifact_downloads=(ArtifactDownload(title=ArtifactTitle(title="title", platform_name="platform"),
                                                 link=ArtifactLink("https://link.com/artifact.AppImage")),),
            build_link=BuildLink("https://buildlink.com"),
            ci_title=CiTitle("CiTitle"),
        )

        self.pr = load_json_object("data/5232.json")
        self.pr.get_issue_comments = Mock(return_value=load_json_object('data/pr_5232_comments.json'))

    def test__find_bot_pr_comment(self):
        pr = load_json_object("data/5232.json")
        pr.get_issue_comments = Mock(return_value=load_json_object('data/pr_5232_comments.json'))

        bot_comment = self.instance._find_bot_pr_comment(pr)
        self.assertIsNotNone(bot_comment)

        bot_comment.user.login = "InvalidUser"
        self.assertIsNone(self.instance._find_bot_pr_comment(pr))


class TestUpdatePullRequestLinkComment(TestCase):
    def setUp(self) -> None:
        self.instance = PullRequestLinkComment(settings)
        self.build_result = CiBuildResult(
            artifact_downloads=(ArtifactDownload(title=ArtifactTitle(title="title", platform_name="platform"),
                                                 link=ArtifactLink("https://link.com/artifact.AppImage")),),
            build_link=BuildLink("https://buildlink.com"),
            ci_title=CiTitle("CiTitle"),
        )

        self.pr = load_json_object("data/5232.json")
        self.pr.get_issue_comments = Mock(return_value=load_json_object('data/pr_5232_comments.json'))

        self.invalid_edit_mock = Mock()
        self.valid_edit_mock = Mock()
        for comment in self.pr.get_issue_comments.return_value:
            comment.edit = self.invalid_edit_mock

        self.bot_comment = self.instance._find_bot_pr_comment(self.pr)
        self.bot_comment.edit = self.valid_edit_mock

        # Sometimes a comment is generated from more that one build result.
        self.generated_comment_additional_build_results = []

        self._update_bot_comment(self.instance._generate_comment(self.pr, self.build_result))

    def tearDown(self) -> None:
        self.instance.update_or_create_links_comment(self.pr, self.build_result)
        self.invalid_edit_mock.assert_not_called()

        # Sometimes we need this comment to be generated from two build results together.
        comment = self.instance._generate_comment(self.pr, self.build_result)
        for build_result in self.generated_comment_additional_build_results:
            comment.add_build_result(build_result)

        self.valid_edit_mock.assert_called_once()
        args, kwargs = self.valid_edit_mock.call_args
        text_comment, = args
        new_comment = BotComment.from_text(text_comment, settings.comment)

        self.assertSetEqual(new_comment._links_set, comment._links_set,
                            "edit has been called with different set of links")

    def _update_bot_comment(self, comment: BotComment):
        self.bot_comment.body = comment.to_text(settings.comment)

    def test_update_cant_parse(self):
        self.bot_comment.body = "Invalid"

    def test_update_append_link(self):
        self.generated_comment_additional_build_results.append(
            self.build_result)

        self.build_result = CiBuildResult(
            artifact_downloads=(ArtifactDownload(title=ArtifactTitle(title="Second title",
                                                                     platform_name="Second Platform"),
                                                 link=ArtifactLink("SecondLink.com")),),
            build_link=BuildLink("https://build_link"),
            ci_title=CiTitle('Title'))

    def test_update_commit_sha_invalid(self):
        comment = BotComment(commit_sha=CommitSHA("INVALID_SHA!!!"))
        comment.add_build_result(self.build_result)
        self._update_bot_comment(comment)
