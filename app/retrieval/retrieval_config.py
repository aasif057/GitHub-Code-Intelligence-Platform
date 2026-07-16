from dataclasses import dataclass


@dataclass
class RetrievalConfig:

    top_k: int = 10

    score_threshold: float | None = None

    repository: str | None = None

    language: str | None = None