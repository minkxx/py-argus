import ollama
from typing import Generator
from argus.engines.base import LLMEngine


class OllamaEngine(LLMEngine):
    """Ollama local AI engine implementation."""

    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        super().__init__(model_name)

    def stream_chat(
        self, system_prompt: str, user_prompt: str
    ) -> Generator[str, None, None]:
        response_stream = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
        )
        for chunk in response_stream:
            yield chunk["message"]["content"]
