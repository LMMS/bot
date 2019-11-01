import os

from dotenv import load_dotenv

from common.DefaultSettings import settings
from common.Settings import Settings

load_dotenv()
settings.github = Settings.Github(
    username=os.getenv("GITHUB_USERNAME"),
    token=os.getenv("GITHUB_TOKEN")
)
