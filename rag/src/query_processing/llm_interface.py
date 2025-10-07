from typing import List, Dict, Protocol


class LLMInterface(Protocol):
    def generate_answer(self, messages: List[Dict[str, str]]) -> str: ...


