from typing import List, Dict

from .llm_interface import LLMInterface
from .hugging_face_manager import HuggingFaceManager
from ..config.models import LLMConfig


class HuggingFaceLLMAdapter(LLMInterface):
    def __init__(self, config: LLMConfig, log_domain: str = "LLM (HF)"):
        self._manager = HuggingFaceManager(config=config, log_domain=log_domain)

    def generate_answer(self, messages: List[Dict[str, str]]) -> str:
        # For HF text_generation, we can form a single prompt from messages
        # Strategy: join system role (if any) and user/assistant messages into plain text
        parts: List[str] = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if not content:
                continue
            if role == "system":
                parts.append(f"[SYSTEM]\n{content}\n")
            elif role == "assistant":
                parts.append(f"Assistant: {content}\n")
            else:
                parts.append(f"User: {content}\n")

        prompt = "\n".join(parts) if parts else ""
        # Use manager's method that expects (question, context_prompt)
        # Here we pass prompt as context; question is the last user content if available
        last_user = next((m["content"] for m in reversed(messages) if m.get("role") == "user" and m.get("content")), prompt)
        return self._manager.generate_answer(question=last_user, context_prompt=prompt)



