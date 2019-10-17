import re
from typing import Iterable, Optional, Sequence

from common.types import CiTitle, ArtifactLink, CiBuildResult, BuildLink, Platform


class ArtifactResolver:
    _REPO_REGEX = r"[\w_-]+/[\w_-]+"
    CAPTURING_REPO_REGEX = r"(?P<repo>{})".format(_REPO_REGEX)

    @property
    def ci_title(self) -> CiTitle:
        raise NotImplementedError

    def __init__(self, url: BuildLink):
        self._url = url
        self._repo = self._parse_link_regex().group('repo')

    def build_id(self):
        return self._parse_link_regex().group('id')

    def artifacts_urls(self) -> Iterable[ArtifactLink]:
        raise NotImplementedError

    @classmethod
    def is_resolver_url(cls, url):
        return bool(re.search(cls._get_link_regex(), url))

    @staticmethod
    def _get_link_regex():
        raise NotImplementedError

    def _parse_link_regex(self):
        return re.match(self._get_link_regex(), self._url)

    def create_build_result(self, platforms: Sequence[Platform]) -> Optional[CiBuildResult]:
        return CiBuildResult.from_links(self.artifacts_urls(), platforms, self.ci_title, self._url)
