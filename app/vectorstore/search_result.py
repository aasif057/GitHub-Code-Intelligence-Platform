from dataclasses import dataclass

from app.chunking.models import CodeChunk


@dataclass
class SearchResult:
    """
    Represents one retrieved chunk from
    the vector database.
    """

    chunk: CodeChunk

    score: float