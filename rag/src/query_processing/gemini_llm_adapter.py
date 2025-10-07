from typing import List, Dict
import os

from .llm_interface import LLMInterface


class GeminiLLMAdapter(LLMInterface):
    def __init__(self, model_name: str, max_tokens: int, temperature: float):
        # Import locally to avoid hard dependency if agent package is absent
        from agent.generator import Generator

        # Ensure GEMINI_API_KEY presence is validated by Generator itself
        self._generator = Generator(
            model_name=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    def generate_answer(self, messages: List[Dict[str, str]]) -> str:
        return self._generator.generate_answer(messages)



