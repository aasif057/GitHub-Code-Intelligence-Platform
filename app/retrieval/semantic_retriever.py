from app.retrieval.base_retriever import BaseRetriever
from app.embeddings.base_embedder import BaseEmbedder
from app.vectorstore.base_vectorstore import BaseVectorStore
from app.retrieval.retrieval_config import RetrievalConfig

class SemanticRetriever(BaseRetriever):

    def __init__(
        self,
        embedder: BaseEmbedder,
        vectorstore: BaseVectorStore,
        config: RetrievalConfig,
    ):

        self.embedder = embedder
        self.vectorstore = vectorstore
        self.config = config

    def retrieve(
        self,
        query: str,
    ):

        # TODO:
        # Replace with embedder.embed_text()
        # after embedding API is expanded.

        query_vector = self.embedder.model.encode(
            query,
            normalize_embeddings=self.embedder.config.normalize,
        ).tolist()

        return self.vectorstore.search(
            query_vector=query_vector,
            limit=self.config.top_k,
        )