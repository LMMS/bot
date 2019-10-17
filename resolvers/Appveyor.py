import logging

import requests

from common.types import ArtifactLink, CiTitle
from resolvers.ArtifactResolver import ArtifactResolver


class Appveyor(ArtifactResolver):
    @property
    def ci_title(self) -> CiTitle:
        return CiTitle("Appveyor")

    @staticmethod
    def _get_link_regex():
        return r'http[s]?://ci.appveyor.com/project/{repo}/builds/(?P<id>[0-9]+)' \
            .format(repo=ArtifactResolver.CAPTURING_REPO_REGEX)

    def artifacts_urls(self):
        artifact_link = 'https://ci.appveyor.com/api/buildjobs/{job_id}/artifacts/{artifact_file_name}'

        for job in self._resolve_jobs():
            for artifact in self._resolve_job_artifacts(job):
                yield ArtifactLink(artifact_link.format(job_id=job['jobId'],
                                                        artifact_file_name=artifact['fileName']))

    def _resolve_jobs(self):
        build_api = 'https://ci.appveyor.com/api/projects/{repo}/builds/{build_id}'.format(build_id=self.build_id(),
                                                                                           repo=self._repo)

        r = requests.get(build_api)
        r.raise_for_status()
        try:
            jobs = r.json()['build']['jobs']
        except KeyError:
            logging.warning("Could not parse result from url: '{}'".format(build_api))
            return ()

        for job in jobs:
            yield job

    def _resolve_job_artifacts(self, job):
        job_api_artifacts = 'https://ci.appveyor.com/api/buildjobs/{job_id}/artifacts'.format(job_id=job['jobId'])

        r = requests.get(job_api_artifacts)
        r.raise_for_status()
        return r.json()
