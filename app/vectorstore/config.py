from dataclasses import dataclass


@dataclass
class VectorStoreConfig:

    provider: str = "qdrant"

    host: str = "localhost"

    port: int = 6333

    collection_name: str = "github_chunks"

    vector_size: int = 768

    distance: str = "cosine"

    recreate_collection: bool = False