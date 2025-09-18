import logging
from model.action import Action
from model.question import Question
from response_generator.response_generator import ResponseGenerator

log = logging.getLogger(__name__)


class InformarGenerator(ResponseGenerator):

    @classmethod
    def generate(cls, action: Action) -> str:
        log.info('informar generator')
        log.info(action.question)
        if action.operation in ['transferência', 'transferencia']:
            return f'Transferência realizada no valor de {action.slots["valor"]} para {action.slots["pessoa"]}'
        elif action.operation in ['consulta de saldo', 'consulta_de_saldo']:
            return 'Seu saldo é de R$ 5.000,00'
        elif action.question == Question.O_QUE:
            log.info('question o que')
            response = action.slots['definition']
            log.info('response')
            return response
