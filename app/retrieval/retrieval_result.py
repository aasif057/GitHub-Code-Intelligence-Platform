from dataclasses import dataclass

from app.chunking.models import CodeChunk


@dataclass
class RetrievalResult:

    chunk: CodeChunk

    score: float