from dotenv import load_dotenv
from github import Github
import os

load_dotenv()


def get_github_client():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError(
            "GITHUB_TOKEN not found"
        )

    return Github(token)