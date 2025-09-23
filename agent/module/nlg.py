import logging
from model.action import Action
from model.intent import Intent
from response_generator.response_generator import ResponseGenerator
from response_generator.saudacao_generator import SaudacaoGenerator
from response_generator.despedida_generator import DespedidaGenerator
from response_generator.perguntar_generator import PerguntarGenerator
from response_generator.informar_generator import InformarGenerator
from response_generator.fora_contexto_generator import ForaContextoGenerator
from response_generator.llm_generator import LLMGenerator

log = logging.getLogger('nlg')


class NLG:

    def __init__(self, llm: bool):
        self.llm = llm
        self._response_generators_dict: dict[Intent, ResponseGenerator] = {
            Intent.SAUDACAO: SaudacaoGenerator,
            Intent.DESPEDIDA: DespedidaGenerator,
            Intent.PERGUNTAR: PerguntarGenerator,
            Intent.INFORMAR: InformarGenerator,
            Intent.FORA_CONTEXTO: ForaContextoGenerator,
            Intent.LLM: LLMGenerator
        }

    def generate(self, action: Action) -> str:
        if action.intent == Intent.INFORMAR and "resposta" in action.slots:
            return action.slots["resposta"]
        elif action.intent == Intent.SAUDACAO:
            return "Olá! Como posso ajudar?"
        elif action.intent == Intent.DESPEDIDA:
            return "Até logo!"
        else:
            return "Desculpe, não entendi sua solicitação."
