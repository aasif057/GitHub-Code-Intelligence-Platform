from dataclasses import dataclass


@dataclass
class IndexingReport:

    repository: str

    files_processed: int

    chunks_generated: int

    vectors_uploaded: int

    elapsed_time: float