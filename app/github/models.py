from dataclasses import dataclass

@dataclass
class RepositoryDocument:
    source_type: str
    file_path: str
    content: str
    language: str
    metadata: dict
    repo: str