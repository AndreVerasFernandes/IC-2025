from model.action import Action
from response_generator.response_generator import ResponseGenerator


class ForaContextoGenerator(ResponseGenerator):

    @classmethod
    def generate(cls, action: Action) -> str:
        return 'Ainda não sei comentar sobre essa dúvida, mas posso te orientar sobre operações de transferência, pagamento e consulta de saldo.'
