from typing import Sequence

from pydantic import BaseModel, SecretStr

from common.types import Platform


class Settings(BaseModel):
    Platform = Platform

    class Comment(BaseModel):
        header: str
        footer: str
        download_line: str
        json_header: str
        json_footer: str
        section_title: str

    class Github(BaseModel):
        username: str
        token: SecretStr

    comment: Comment
    github: Github
    platforms: Sequence[Platform]
