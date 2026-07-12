import time

from app.chunking.chunk_factory import ChunkFactory

from app.indexing.batch_manager import BatchManager
from app.indexing.models import IndexingReport
from app.indexing.progress import ProgressTracker


class RepositoryIndexer:

    def __init__(
        self,
        ingestor,
        embedder,
        vectorstore,
        config,
    ):

        self.ingestor = ingestor
        self.embedder = embedder
        self.vectorstore = vectorstore
        self.config = config

    def index_repository(
        self,
        repo_name: str,
    ) -> IndexingReport:

        start_time = time.time()

        print(f"\nIndexing repository: {repo_name}")

        # --------------------------------------------------
        # Load repository
        # --------------------------------------------------

        documents = self.ingestor.load_code_files(
            repo_name
        )

        print(
            f"Loaded {len(documents)} files"
        )

        # --------------------------------------------------
        # Chunk documents
        # --------------------------------------------------

        chunks = self._chunk_documents(
            documents
        )

        print(
            f"Generated {len(chunks)} chunks"
        )

        # --------------------------------------------------
        # Embed + Upload
        # --------------------------------------------------

        uploaded = self._embed_and_upload(
            chunks
        )

        elapsed = time.time() - start_time

        return IndexingReport(
            repository=repo_name,
            files_processed=len(documents),
            chunks_generated=len(chunks),
            vectors_uploaded=uploaded,
            elapsed_time=elapsed,
        )

    def _chunk_documents(
        self,
        documents,
    ):

        all_chunks = []

        for document in documents:

            chunker = ChunkFactory.get_chunker(
                document.language
            )

            if chunker is None:
                continue

            chunks = chunker.chunk(
                document
            )

            all_chunks.extend(chunks)

        return all_chunks

    def _embed_and_upload(
        self,
        chunks,
    ) -> int:

        progress = ProgressTracker(
            total=len(chunks)
        )

        progress.start(
            "Embedding and Uploading"
        )

        uploaded = 0

        batches = BatchManager.create_batches(
            chunks,
            self.config.embedding_batch_size,
        )

        for batch in batches:

            vectors = self.embedder.embed_chunks(
                batch
            )

            self.vectorstore.upsert(
                batch,
                vectors,
            )

            uploaded += len(batch)

            progress.update(
                len(batch)
            )

        progress.finish()

        return uploaded