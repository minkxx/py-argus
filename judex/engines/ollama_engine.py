import ollama
from ollama import ResponseError
from typing import Generator
from judex.engines.base import LLMEngine


def checkModelExists(model_name: str):
    try:
        ollama.show(model_name)
    except ResponseError as re:
        if re.status_code == 404:
            print(
                f"The model '{model_name}' does not exist. Please download it using 'ollama pull {model_name}'"
            )
            exit()
        else:
            print(f"An unexpected error occurred: {re}")
            exit()


class OllamaEngine(LLMEngine):
    """Ollama local AI engine implementation."""

    def __init__(self, model_name: str = "qwen2.5-coder:7b"):
        checkModelExists(model_name)
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
