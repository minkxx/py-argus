from abc import ABC, abstractmethod
from typing import Generator


class LLMEngine(ABC):
    @abstractmethod
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def stream_chat(
        self, system_prompt: str, user_prompt: str
    ) -> Generator[str, None, None]:
        pass
