from dataclasses import dataclass

@dataclass
class RepositoryDocument:
    source_type: str
    file_path: str
    content: str
    metadata: dict
    language: str