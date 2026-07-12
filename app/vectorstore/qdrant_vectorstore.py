from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
)

from app.vectorstore.base_vectorstore import BaseVectorStore


class QdrantVectorStore(BaseVectorStore):

    def __init__(self, config):

        self.config = config

        self.client = QdrantClient(
            host=config.host,
            port=config.port,
        )

    def ensure_collection(self):

        if self.config.recreate_collection:

            if self.collection_exists():

                print(
                    f"Deleting collection "
                    f"{self.config.collection_name}"
                )

                self.delete_collection()

        if not self.collection_exists():

            print(
                f"Creating collection "
                f"{self.config.collection_name}"
            )

            self._create_collection()

        else:

            print(
                f"Using existing collection "
                f"{self.config.collection_name}"
            )

    def collection_exists(self) -> bool:

        return self.client.collection_exists(
            self.config.collection_name
        )

    def _create_collection(self):

        distance_map = {
            "cosine": Distance.COSINE,
            "euclidean": Distance.EUCLID,
            "dot": Distance.DOT,
        }

        self.client.create_collection(
            collection_name=self.config.collection_name,
            vectors_config=VectorParams(
                size=self.config.embedding_dimension,
                distance=distance_map[
                    self.config.distance_metric.lower()
                ],
            ),
        )

    def delete_collection(self):

        self.client.delete_collection(
            self.config.collection_name
        )

    def count(self) -> int:

        result = self.client.count(
            collection_name=self.config.collection_name,
            exact=True,
        )

        return result.count