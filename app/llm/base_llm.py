from abc import ABC, abstractmethod

from app.llm.config import LLMConfig
from app.llm.response import LLMResponse
from langchain_core.prompts import ChatPromptTemplate

class BaseLLM(ABC):
    """
    Base interface for all LLM providers.
    """

    def __init__(
        self,
        config: LLMConfig,
    ):

        self.config = config

    @abstractmethod
    def generate(
        self,
        prompt: ChatPromptTemplate,
    ) -> LLMResponse:
        pass

    @abstractmethod
    def model_name(
        self,
    ) -> str:
        """
        Returns the underlying model name.
        """
        pass