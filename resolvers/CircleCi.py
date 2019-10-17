import requests

from common.types import CiTitle, ArtifactLink
from resolvers.ArtifactResolver import ArtifactResolver


class CircleCI(ArtifactResolver):
    @property
    def ci_title(self) -> CiTitle:
        return CiTitle("CircleCi")

    def artifacts_urls(self):
        api_link = "https://circleci.com/api/v1.1/project/github/{repo}/{build_id}/artifacts". \
            format(repo=self._repo,
                   build_id=self.build_id())

        r = requests.get(api_link)
        r.raise_for_status()

        for artifact in r.json():
            yield ArtifactLink(artifact['url'])

    @staticmethod
    def _get_link_regex():
        return r'http[s]?://(?:app)?circleci.com/(?:gh|jobs/github)/{repo}/(?P<id>[0-9]+)'. \
            format(repo=CircleCI.CAPTURING_REPO_REGEX)
