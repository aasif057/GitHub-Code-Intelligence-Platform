from app.embeddings.config import EmbeddingConfig
from app.embeddings.factory import EmbeddingFactory

from app.vectorstore.config import VectorStoreConfig
from app.vectorstore.factory import VectorStoreFactory

from app.retrieval.retrieval_config import RetrievalConfig
from app.retrieval.semantic_retriever import SemanticRetriever


def main():

    embedder = EmbeddingFactory.get(
        "sentence_transformer",
        EmbeddingConfig(
            model_name="BAAI/bge-base-en-v1.5",
            device="cpu",
        ),
    )

    vectorstore = VectorStoreFactory.get(
        "qdrant",
        VectorStoreConfig(
            collection_name="github_code",
            embedding_dimension=768,
        ),
    )

    retriever = SemanticRetriever(
        embedder=embedder,
        vectorstore=vectorstore,
        config=RetrievalConfig(
            top_k=5,
        ),
    )

    query = "Where is generate_redirects implemented?"

    print(f"\nQuery: {query}\n")

    results = retriever.retrieve(query)

    print(f"Retrieved {len(results)} chunks\n")

    for i, result in enumerate(results, start=1):

        print("=" * 60)
        print(f"Rank : {i}")
        print(f"Score: {result.score:.4f}")
        print(f"File : {result.chunk.file_path}")
        print(f"Type : {result.chunk.chunk_type}")
        print(f"Name : {result.chunk.name}")
        print()

        preview = result.chunk.content[:400]

        print(preview)

        print()
if __name__ == "__main__":
    main()