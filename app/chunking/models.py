from dataclasses import dataclass

@dataclass
class CodeChunk:
    chunk_type: str
    name: str
    language: str
    file_path: str
    content: str
    metadata: dict
