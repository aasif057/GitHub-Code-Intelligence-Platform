import ast

from app.chunking.base_chunker import BaseChunker
from app.chunking.models import CodeChunk

MAX_CHARS = 4000

class PythonChunker(BaseChunker):

    def chunk(self, document):

        chunks = []

        try:
            tree = ast.parse(document.content)

        except Exception:
            return chunks

        for node in tree.body:

            # -------------------------
            # CLASS CHUNKING
            # -------------------------

            if isinstance(node, ast.ClassDef):

                class_content = ast.get_source_segment(
                    document.content,
                    node
                )

                if (
                    class_content
                    and
                    len(class_content) <= MAX_CHARS
                ):

                    chunks.append(
                        CodeChunk(
                            chunk_type="class",
                            name=node.name,
                            language=document.language,
                            file_path=document.file_path,
                            content=class_content,
                            metadata={
                                "start_line": node.lineno,
                                "end_line": getattr(
                                    node,
                                    "end_lineno",
                                    node.lineno
                                )
                            }
                        )
                    )

                else:

                    for child in node.body:

                        if isinstance(
                            child,
                            (
                                ast.FunctionDef,
                                ast.AsyncFunctionDef
                            )
                        ):

                            method_content = (
                                ast.get_source_segment(
                                    document.content,
                                    child
                                )
                            )

                            if not method_content:
                                continue

                            chunks.append(
                                CodeChunk(
                                    chunk_type="method",
                                    name=f"{node.name}.{child.name}",
                                    language=document.language,
                                    file_path=document.file_path,
                                    content=method_content,
                                    metadata={
                                        "parent_class":
                                            node.name,
                                        "start_line":
                                            child.lineno,
                                        "end_line":
                                            getattr(
                                                child,
                                                "end_lineno",
                                                child.lineno
                                            )
                                    }
                                )
                            )

            # -------------------------
            # TOP LEVEL FUNCTIONS
            # -------------------------

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef
                )
            ):

                function_content = (
                    ast.get_source_segment(
                        document.content,
                        node
                    )
                )

                if not function_content:
                    continue

                chunks.append(
                    CodeChunk(
                        chunk_type="function",
                        name=node.name,
                        language=document.language,
                        file_path=document.file_path,
                        content=function_content,
                        metadata={
                            "start_line":
                                node.lineno,
                            "end_line":
                                getattr(
                                    node,
                                    "end_lineno",
                                    node.lineno
                                )
                        }
                    )
                )

        return chunks