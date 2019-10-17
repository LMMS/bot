from typing import NewType, Sequence, Optional, Dict, Iterable

from pydantic import BaseModel

CiTitle = NewType("CiTitle", str)
BuildLink = NewType("BuildLink", str)
CommitSHA = NewType("CommitSHA", str)
PlatformName = str


class ArtifactLink(BaseModel):
    link: str

    def __init__(self, link):
        super().__init__(link=link)

    def __hash__(self):
        return self.link.__hash__()

    @property
    def basename(self):
        from os.path import basename
        return basename(self.link)

    def __str__(self):
        return self.link


class ArtifactTitle(BaseModel):
    title: str
    platform_name: PlatformName


class Platform(BaseModel):
    name: str
    extension_to_title: Dict[str, str]

    def match_title_to_link(self, link: ArtifactLink) -> Optional[ArtifactTitle]:
        for extension, title in self.extension_to_title.items():
            if link.basename.endswith(extension):
                return ArtifactTitle(platform_name=self.name, title=title)

        return None


class ArtifactDownload(BaseModel):
    title: ArtifactTitle
    link: ArtifactLink


class CiBuildResult(BaseModel):
    @classmethod
    def from_links(cls,
                   links: Iterable[ArtifactLink],
                   platforms: Sequence[Platform],
                   ci_title: CiTitle,
                   build_link: BuildLink):
        def artifact_title_from_link(link):
            for platform in platforms:
                title = platform.match_title_to_link(link)
                if title:
                    return title

        def links_to_download():
            for link in links:
                title = artifact_title_from_link(link)
                if title:
                    yield ArtifactDownload(title=title, link=link)

        downloads = tuple(links_to_download())
        if not downloads:
            return None

        return cls(artifact_downloads=downloads,
                   build_link=build_link,
                   ci_title=ci_title)

    artifact_downloads: Sequence[ArtifactDownload]
    build_link: BuildLink
    ci_title: CiTitle
