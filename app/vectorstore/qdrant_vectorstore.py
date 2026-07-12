import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)
from app.vectorstore.payload_builder import PayloadBuilder
from app.vectorstore.base_vectorstore import BaseVectorStore
from app.vectorstore.search_result import SearchResult


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
    def upsert(
        self,
        chunks,
        vectors,
    ):

        self.ensure_collection()

        points = list(
            self._build_points(
                chunks,
                vectors,
            )
        )

        self.client.upsert(
            collection_name=self.config.collection_name,
            points=points,
            wait=True,
        )
    
    def search(
        self,
        query_vector,
        limit=5,
    ):

        response = self.client.query_points(
            collection_name=self.config.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )

        results = []

        for point in response.points:

            chunk = PayloadBuilder.parse(
                point.payload
            )

            results.append(
                SearchResult(
                    chunk=chunk,
                    score=point.score,
                )
            )

        return results
    
    def _build_points(
        self,
        chunks,
        vectors,
    ):
        """
        Convert CodeChunks and their embeddings
        into Qdrant PointStruct objects.
        """

        if len(chunks) != len(vectors):
            raise ValueError(
                "Number of chunks and vectors must match."
            )

        for chunk, vector in zip(chunks, vectors):

            payload = PayloadBuilder.build(
                chunk
            )
            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_DNS,
                    chunk.chunk_id,
                )
            )

            yield PointStruct(
                id=point_id,
                vector=vector,
                payload=payload,
            )