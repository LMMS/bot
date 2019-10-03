import re


class ArtifactResolver:
    _REPO_REGEX = r"[\w_-]+/[\w_-]+"
    CAPTURING_REPO_REGEX = r"(?P<repo>{})".format(_REPO_REGEX)

    def __init__(self, url: str):
        self._url = url
        self._repo = self._parse_link_regex().group('repo')

    def build_id(self):
        return self._parse_link_regex().group('id')

    def artifacts_urls(self):
        raise NotImplementedError

    @classmethod
    def is_resolver_url(cls, url):
        return bool(re.search(cls._get_link_regex(), url))

    @staticmethod
    def _get_link_regex():
        raise NotImplementedError

    def _parse_link_regex(self):
        return re.match(self._get_link_regex(), self._url)
