from abc import ABC, abstractmethod

from app.chunking.models import CodeChunk


class BaseVectorStore(ABC):

    @abstractmethod
    def create_collection(self):
        pass

    @abstractmethod
    def collection_exists(self) -> bool:
        pass

    @abstractmethod
    def delete_collection(self):
        pass

    @abstractmethod
    def index(
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
    ):
        pass

    @abstractmethod
    def count(self) -> int:
        pass