from model.action import Action
from response_generator.response_generator import ResponseGenerator


class DespedidaGenerator(ResponseGenerator):

    @classmethod
    def generate(cls, action: Action) -> str:
        return 'Até logo!'
