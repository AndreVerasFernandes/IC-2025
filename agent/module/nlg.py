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
        if action.intent == Intent.FORA_CONTEXTO_LLM:
            return 'Desculpe, mas parece que esse assunto está fora do esperado para essa conversa. Se quiser falar sobre assuntos bancários eu posso te ajudar'
        response = self._internal_generate(action)
        return response

    def _internal_generate(self, action: Action) -> str:
        if action.intent in self._response_generators_dict:
            return self._response_generators_dict[action.intent].generate(action)
        log.error('No response generator found for action with intent ' + action.intent)
