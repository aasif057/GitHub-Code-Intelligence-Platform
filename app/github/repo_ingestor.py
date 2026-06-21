# app/github/repo_ingestor.py

from github import Github
from .models import RepositoryDocument
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".cs",
    ".toml",
    ".cfg",
    ".ini",
    ".md",
    ".txt",
    ".rst",
    ".yaml",
    ".yml",
    ".json"
}

LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".cs": "csharp",
    ".md": "markdown",
    ".rst": "rst",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml"
}

class RepositoryIngestor:
    def __init__(self, github_client: Github):
        self.github = github_client

    def get_repo(self, repo_name: str):
        """
        Example:
        repo_name = "langchain-ai/langgraph"
        """
        return self.github.get_repo(repo_name)

    def load_code_files(self, repo_name: str):

        repo = self.get_repo(repo_name)

        contents = repo.get_contents("")

        documents = []

        while contents:

            item = contents.pop(0)

            if item.type == "dir":
                contents.extend(
                    repo.get_contents(item.path)
                )

            elif item.type == "file":

                if not any(
                    item.path.endswith(ext)
                    for ext in SUPPORTED_EXTENSIONS
                ):
                    continue

                try:

                    content = (
                        item.decoded_content
                        .decode("utf-8")
                    )
                    extension = Path(item.path).suffix
                    language = LANGUAGE_MAP.get(
                        extension,
                        "unknown"
                    )
                    documents.append(
                        RepositoryDocument(
                            source_type="code",
                            file_path=item.path,
                            content=content,
                            language=language,
                            metadata={
                                "repo": repo_name,
                                "sha": item.sha,
                                "size": item.size
                            }
                        )
                    )

                except Exception as e:
                    print(
                        f"Failed to process {item.path}: {e}"
                    )

        return documents
