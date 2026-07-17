from dataclasses import dataclass


@dataclass
class LLMConfig:
    provider: str
    model_name: str
    api_key: str

    temperature: float = 0.0
    max_tokens: int | None = None
    timeout: int | None = None