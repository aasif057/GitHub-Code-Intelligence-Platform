from dataclasses import dataclass


@dataclass
class LLMConfig:

    provider: str = "gemini"

    model_name: str = "gemini-2.5-pro"

    temperature: float = 0.0

    max_tokens: int | None = None

    timeout: int = 60

    api_key: str | None = None