from model.action import Action
from response_generator.response_generator import ResponseGenerator


class SaudacaoGenerator(ResponseGenerator):

    @classmethod
    def generate(cls, action: Action) -> str:
        if action.remember:
            return f'Olá! Como posso te ajudar hoje?\nGostaria de continuar a {action.slots["restored_operation"]} que estava fazendo anteriormente?'
        if 'nome' in action.slots and action.slots['nome']:
            return f'Olá, {action.slots["nome"]}! Como posso te ajudar hoje?'
        return 'Olá! Como posso te ajudar hoje?'
