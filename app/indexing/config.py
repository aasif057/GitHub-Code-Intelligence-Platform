from dataclasses import dataclass


@dataclass
class IndexingConfig:

    embedding_batch_size: int = 64

    upload_batch_size: int = 128

    skip_existing: bool = True

    show_progress: bool = True