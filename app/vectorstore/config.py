from dataclasses import dataclass


@dataclass
class VectorStoreConfig:

    collection_name: str

    embedding_dimension: int

    distance_metric: str = "cosine"

    recreate_collection: bool = False

    batch_size: int = 128

    host: str = "localhost"

    port: int = 6333