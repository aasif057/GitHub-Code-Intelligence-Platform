from app.chunking.python_chunker import PythonChunker

class ChunkFactory:
    @staticmethod
    def get_chunker(language):

        if language == "python":
            return PythonChunker()

        return None
