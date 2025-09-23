import logging

from model.action import Action
from model.intent import Intent
from model.state import State
from model.question import Question
from module.bt import BeliefTracker
from module.km import KnowledgeManagement

log = logging.getLogger('policy')

CONTEXT = 'context'
RESTORE_CONTEXT_CONFIRMATION = 'restore_confirmation'
RECOMENDAR = 'recomendar'

# --------------------------------------------------------------
# Classe Policy: Define as políticas de ação do sistema com base no estado atual e intenções do usuário
# --------------------------------------------------------------


class Policy:
    def __init__(self, bt: BeliefTracker, km: KnowledgeManagement, use_llm: bool = False):
        self.bt = bt
        self.km = km
        self._use_llm = use_llm

    def act(self, user: str, states: list[State], original_message: str) -> list[Action]:
        """
        Decide quais ações tomar com base no estado atual e na mensagem original do usuário.

        Args:
            user: Nome/ID do usuário.
            states: Lista de estados atuais.
            original_message: Mensagem original enviada pelo usuário.

        Returns:
            Lista de ações a serem executadas.
        """
        actions = []
        for state in self._select_states(states):
            actions.extend(self.act_single_state(user, state, original_message))
        return actions

    def act_single_state(self, user: str, state: State, original_message: str) -> list[Action]:
        if state.out_of_context:
            return [Action(intent=Intent.FORA_CONTEXTO)]

        if state.intent == Intent.SAUDACAO:
            return [self._act_hello(user)]

        elif state.intent == Intent.DESPEDIDA:
            return [self._act_goodbye(user)]

        elif state.intent == Intent.QUESTION or state.intent == Intent.INFORMAR:
            return [self._act_question(original_message, state.domain)]

        # Fora dos intents válidos
        return [Action(intent=Intent.FORA_CONTEXTO)]

    def _act_hello(self, user: str) -> Action:
        return Action(intent=Intent.SAUDACAO, slots={"nome": user})

    def _act_goodbye(self, user: str) -> Action:
        self.bt.clear()
        return Action(intent=Intent.DESPEDIDA)

    def _act_question(self, message: str, domain: str) -> Action:
        """
        Consulta o KM (RAG) com a pergunta original e o domínio identificado.
        """
        try:
            answer = self.km.query_knowledge(message)
            return Action(intent=Intent.INFORMAR, slots={"resposta": answer})
        except Exception as e:
            log.error(f"Erro ao consultar conhecimento: {e}")
            return Action(intent=Intent.INFORMAR, slots={"resposta": "Desculpe, houve um erro ao consultar o conhecimento."})

    def _select_states(self, states: list[State]) -> list[State]:
        current_states = [s for s in states if s.current]
        if not current_states:
            return [states[-1]]
        return current_states
