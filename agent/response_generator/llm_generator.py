from model.action import Action
from response_generator.response_generator import ResponseGenerator


class LLMGenerator(ResponseGenerator):

    @classmethod
    def generate(cls, action: Action) -> str:
        response = 'buscando respostas com llm...'
        return response
