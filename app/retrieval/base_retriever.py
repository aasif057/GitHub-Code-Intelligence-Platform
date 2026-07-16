from abc import ABC, abstractmethod

from app.retrieval.retrieval_result import RetrievalResult


class BaseRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str,
    ) -> list[RetrievalResult]:
        """
        Retrieve relevant chunks.
        """
        pass