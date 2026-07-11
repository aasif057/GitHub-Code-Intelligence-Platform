from app.vectorstore.config import VectorStoreConfig


class VectorStoreFactory:

    @staticmethod
    def get(
        provider: str,
        config: VectorStoreConfig,
    ):

        provider = provider.lower()

        if provider == "qdrant":

            from app.vectorstore.qdrant_vectorstore import (
                QdrantVectorStore,
            )

            return QdrantVectorStore(config)

        raise ValueError(
            f"Unsupported vector store: {provider}"
        )