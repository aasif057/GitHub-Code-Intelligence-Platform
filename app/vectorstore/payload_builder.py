from app.chunking.models import CodeChunk


class PayloadBuilder:

    @staticmethod
    def build(
        chunk: CodeChunk,
    ) -> dict:

        return {

            "chunk_id": chunk.chunk_id,

            "repo": chunk.repo,

            "language": chunk.language,

            "chunk_type": chunk.chunk_type,

            "symbol": chunk.name,

            "file_path": chunk.file_path,

            "content": chunk.content,

            "metadata": chunk.metadata,
        }

    @staticmethod
    def parse(
        payload: dict,
    ) -> CodeChunk:
        """
        Converts a vector database payload
        back into a CodeChunk.
        """

        return CodeChunk(

            chunk_id=payload["chunk_id"],

            chunk_type=payload["chunk_type"],

            name=payload["symbol"],

            language=payload["language"],

            file_path=payload["file_path"],

            content=payload["content"],

            metadata=payload["metadata"],

            repo=payload["repo"],
        )