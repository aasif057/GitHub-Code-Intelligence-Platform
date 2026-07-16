from dataclasses import dataclass


@dataclass
class LLMResponse:
    """
    Standard response returned by every LLM provider.
    """

    answer: str

    model: str

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    total_tokens: int | None = None

    latency_ms: float | None = None