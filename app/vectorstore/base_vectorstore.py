from abc import ABC, abstractmethod

from app.chunking.models import CodeChunk
from app.vectorstore.search_result import SearchResult


class BaseVectorStore(ABC):

    @abstractmethod
    def ensure_collection(self):
        pass

    @abstractmethod
    def collection_exists(self) -> bool:
        pass

    @abstractmethod
    def delete_collection(self):
        pass

    @abstractmethod
    def upsert(
        self,
        chunks: list[CodeChunk],
        vectors: list[list[float]],
    ):
        pass

    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[SearchResult]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass