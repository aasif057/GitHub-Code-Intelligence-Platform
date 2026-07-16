from app.retrieval.retrieval_result import RetrievalResult


class PromptBuilder:
    """
    Builds prompts for the LLM using retrieved repository context.
    """

    SYSTEM_PROMPT = """
You are an expert software engineering assistant.

You answer questions ONLY using the provided repository context.

Guidelines:
- Use the retrieved code as your primary source.
- Mention relevant file names whenever possible.
- Mention function or class names whenever possible.
- If the context is insufficient, clearly state that.
- Do NOT invent implementation details.
- Keep answers concise, technical, and accurate.
- When multiple files are relevant, explain how they relate.
""".strip()

    @staticmethod
    def build(
        question: str,
        results: list[RetrievalResult],
    ) -> str:
        """
        Builds the complete prompt sent to the LLM.
        """

        context = PromptBuilder._build_context(
            results
        )

        prompt = f"""
{PromptBuilder.SYSTEM_PROMPT}

===========================
Repository Context
===========================

{context}

===========================
User Question
===========================

{question}

===========================
Answer
===========================
""".strip()

        return prompt

    @staticmethod
    def _build_context(
        results: list[RetrievalResult],
    ) -> str:
        """
        Converts retrieval results into readable repository context.
        """

        if not results:
            return "No relevant repository context was retrieved."

        sections = []

        for index, result in enumerate(results, start=1):

            chunk = result.chunk

            section = f"""
Source {index}

File:
{chunk.file_path}

Symbol:
{chunk.name}

Type:
{chunk.chunk_type}

Language:
{chunk.language}

Similarity Score:
{result.score:.4f}

Code:
{chunk.content}
""".strip()

            sections.append(section)

        return "\n\n" + ("\n\n" + "-" * 80 + "\n\n").join(sections)