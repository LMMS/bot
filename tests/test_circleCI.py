from unittest import TestCase

from common.types import BuildLink
from resolvers.CircleCi import CircleCI
from settings import settings


class TestCircleCIBase(TestCase):
    URL = "https://circleci.com/gh/Reflexe/lmms/1040?utm_campaign=vcs-integration-link&utm_medium=referral&utm_source" \
          "=github-build-link "

    def setUp(self) -> None:
        self._circleci = CircleCI(url=BuildLink(self.URL))

    def test_build_id(self):
        self.assertEqual(self._circleci.build_id(), '1040')

    def test_match(self):
        self.assertTrue(self._circleci.is_resolver_url(url=self.URL))

    def test_artifacts_urls(self):
        result = ('https://1040-143851518-gh.circle-artifacts.com/0/lmms-1.2.0-rc6.686-win64.exe',)

        self.assertTupleEqual(tuple(download.link.link for download in
                                    self._circleci.create_build_result(settings.platforms).artifact_downloads),
                              result)
