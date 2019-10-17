from unittest import TestCase

from common.types import BuildLink
from resolvers.Appveyor import Appveyor
from settings import settings


class TestAppveyor(TestCase):
    URL = "https://ci.appveyor.com/project/Reflexe/lmms/builds/27690217"

    def setUp(self) -> None:
        self._appveyor = Appveyor(BuildLink(self.URL))

    def test_build_id(self):
        self.assertEqual(self._appveyor.build_id(), "27690217")

    def test_match(self):
        self.assertTrue(self._appveyor.is_resolver_url(self.URL))

    def test_artifacts_urls(self):
        result = ('https://ci.appveyor.com/api/buildjobs/mtfijtpui5gxjgq7/artifacts/build/lmms-1.2.0-win32.exe',
                  'https://ci.appveyor.com/api/buildjobs/7y6625olfy340sj5/artifacts/build/lmms-1.2.0-win64.exe')

        self.assertTupleEqual(tuple(download.link.link for download in
                                    self._appveyor.create_build_result(settings.platforms).artifact_downloads),
                              result)

    def test__resolve_jobs(self):
        jobs = tuple(self._appveyor._resolve_jobs())
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]['jobId'], 'mtfijtpui5gxjgq7')
        self.assertEqual(jobs[1]['jobId'], '7y6625olfy340sj5')

    def test__resolve_job_artifacts(self):
        job = {'jobId': 'mtfijtpui5gxjgq7'}
        artifacts = tuple(self._appveyor._resolve_job_artifacts(job))
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts[0]['fileName'], 'build/lmms-1.2.0-win32.exe')
