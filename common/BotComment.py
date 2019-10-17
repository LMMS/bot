from typing import List, Set, Dict

from pydantic import BaseModel, ValidationError

from common.Settings import Settings
from common.types import CommitSHA, CiBuildResult, ArtifactDownload, BuildLink, PlatformName, ArtifactLink


class BotComment:
    class BotCommentModel(BaseModel):
        class ArtifactAndBuildLink(BaseModel):
            artifact: ArtifactDownload
            build_link: BuildLink

        platform_name_to_artifacts: Dict[PlatformName, List[ArtifactAndBuildLink]] = dict()
        commit_sha: CommitSHA

    _model: BotCommentModel
    _links_set: Set[ArtifactLink]

    def __init__(self, commit_sha=None, model=None):
        if model is None:
            assert(commit_sha is not None)
            model = self.BotCommentModel(commit_sha=commit_sha)

        self._model = model
        self._links_set = self._build_links_set_from_model(self._model)

    def to_text(self, settings: Settings.Comment):
        body = settings.header
        for platform_name, artifacts_and_build_link in self._model.platform_name_to_artifacts.items():
            body += settings.section_title.format(platform_title=platform_name)

            for artifact_and_build_link in artifacts_and_build_link:
                artifact = artifact_and_build_link.artifact
                build_link = artifact_and_build_link.build_link

                body += settings.download_line.format(title=artifact.title,
                                                      download_link=artifact.link,
                                                      build_link=build_link)

        body += settings.json_header + self._model.json() + settings.json_footer
        body += settings.footer

        return body

    @classmethod
    def from_text(cls, text: str, settings: Settings.Comment):
        json_line_index = (settings.json_footer + settings.footer).count('\n')

        try:
            json_line = text.splitlines()[-json_line_index]
        except IndexError:
            return None

        try:
            return cls(model=BotComment.BotCommentModel.parse_raw(json_line))
        except ValidationError:
            return None

    def add_build_result(self, build_result: CiBuildResult):
        for artifact in build_result.artifact_downloads:
            if artifact.link not in self._links_set:
                l = self._model.platform_name_to_artifacts.setdefault(artifact.title.platform_name, [])
                l.append(
                    self.BotCommentModel.ArtifactAndBuildLink(artifact=artifact,
                                                              build_link=build_result.build_link)
                )
                self._links_set.add(artifact.link)

    @staticmethod
    def _build_links_set_from_model(model: BotCommentModel):
        return set(artifact.artifact.link for artifacts in model.platform_name_to_artifacts.values()
                   for artifact in artifacts)

    @property
    def commit_sha(self):
        return self._model.commit_sha
