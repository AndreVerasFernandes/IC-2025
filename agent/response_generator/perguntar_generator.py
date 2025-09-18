from model.action import Action
from response_generator.response_generator import ResponseGenerator


class PerguntarGenerator(ResponseGenerator):

    @classmethod
    def generate(cls, action: Action) -> str:
        if action.operation == 'recomendar':
            return 'Gostou da recomendação?'
        # slot_labels = [self.km.get_label(info) for info in action.slots['info']]
        slot_labels = [info for info in action.slots['info']]
        labels_str = cls._create_list(slot_labels)
        return f'Para concluir a operação de {action.operation} preciso que me informe {labels_str}'
