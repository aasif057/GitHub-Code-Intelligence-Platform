from app.github.client import get_github_client
from app.github.repo_ingestor import RepositoryIngestor

from app.chunking.chunk_factory import ChunkFactory

from app.embeddings.config import EmbeddingConfig
from app.embeddings.factory import EmbeddingFactory


def main():

    github = get_github_client()

    ingestor = RepositoryIngestor(github)

    docs = ingestor.load_code_files(
        "langchain-ai/langgraph"
    )

    chunks = []

    for doc in docs:

        chunker = ChunkFactory.get_chunker(
            doc.language
        )

        if chunker:

            chunks.extend(
                chunker.chunk(doc)
            )

    print(f"Generated {len(chunks)} chunks")

    config = EmbeddingConfig(
        model_name="BAAI/bge-base-en-v1.5",
        batch_size=8,
        device="cpu",
    )

    embedder = EmbeddingFactory.get(
        "sentence_transformer",
        config,
    )

    vectors = embedder.embed_chunks(
        chunks[:10]
    )

    print()

    print("Model:", embedder.model_name())

    print(
        "Dimension:",
        embedder.embedding_dimension(),
    )

    print(
        "Vectors:",
        len(vectors),
    )

    print(
        "Vector Size:",
        len(vectors[0]),
    )


if __name__ == "__main__":
    main()