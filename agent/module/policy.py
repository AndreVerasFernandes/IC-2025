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
        """
        Inicializa a classe Policy com o rastreador de crenças e configurações para o uso do modelo de linguagem (LLM).

        Objetivo: Definir os parâmetros iniciais necessários para a política de ações com base no estado do usuário.
        Entradas:
            - bt (BeliefTracker): O rastreador de crenças do usuário.
            - km (KnowledgeManagement): O gerenciador de conhecimento
            - use_llm (bool): Determina se o modelo de linguagem será utilizado.
        Saídas: Nenhuma.
        """

        self.bt = bt
        self.km = km
        self._action_pending_confirmation = None
        self._check_next_operation = False
        self._use_llm = use_llm

    # --------------------------------------------------------------
    # Função para agir com base no estado do usuário
    # --------------------------------------------------------------
    def act(self, user: str, states: list[State]) -> list[Action]:
        """
        Objetivo: Gerenciar as ações a serem executadas com base nos estados atuais de um usuário.
        Descrição: Verifica os estados do usuário e executa ações relacionadas a eles, incluindo resumo de ações
                   anteriores ou execução de uma operação específica com base no estado atual.
        Entradas:
            - user (str): Identificador do usuário.
            - states (list[State]): Lista de estados atuais do usuário.
        Saídas:
            - list[Action]: Lista de ações a serem executadas.
        """
        actions = []
        for state in self._select_states(states):
            actions.extend(self.act_single_state(user, state))
        return actions

    def act_single_state(self, user: str, state: State) -> list[Action]:
        """
        Objetivo: Executar uma ação específica com base em um único estado do usuário.
        Descrição: Dependendo da intenção do estado (ex. saudação, confirmação, realizar operação), a função
                   executa a ação apropriada, como enviar uma saudação, confirmar uma operação ou solicitar
                   mais informações.
        Entradas:
            - user (str): Identificador do usuário.
            - state (State): O estado atual do usuário.
        Saídas:
            - list[Action]: Lista de ações a serem executadas.
        """

        if state.out_of_context:
            return [Action(intent=Intent.FORA_CONTEXTO_LLM)]
        elif state.intent == Intent.SAUDACAO:
            return [self._act_hello(user, state)]
        elif state.intent == Intent.DESPEDIDA:
            return [self._act_goodbye(user, state)]
        elif state.intent == Intent.REALIZAR:
            actions = []
            action = self._act_realizar(user, state)
            actions.append(action)
            return actions
        elif state.intent == Intent.INFORMAR:
            action = self._act_informar(user, state)
            return [action]
        elif self._use_llm:
            return [Action(intent=Intent.LLM)]
        else:
            return [Action(intent=Intent.FORA_CONTEXTO)]

    def _act_hello(self, user: str, state: State) -> Action:
        """
        Objetivo: Enviar uma saudação ao usuário e restaurar o contexto da conversa, se necessário.
        Descrição: Ao iniciar a conversa, verifica se o contexto pode ser restaurado a partir da memória de longo prazo.
        Entradas:
            - user (str): Identificador do usuário.
            - state (State): O estado atual do usuário.
        Saídas:
            - Action: Ação de saudação, possivelmente restaurando o contexto.
        """
        username = ''
        slots = {'nome': username}
        return Action(intent=Intent.SAUDACAO, slots=slots)

    def _act_goodbye(self, user: str, state: State) -> Action:
        """
        Objetivo: Encerrar a conversa com o usuário e limpar o rastreador de crenças.
        Descrição: Ao finalizar esta interação com o usuário, a função de despedida é chamada e o belief tracker
                   é limpo.
        Entradas:
            - user (str): Identificador do usuário.
            - state (State): O estado atual do usuário.
        Saídas:
            - Action: Ação de despedida.
        """
        self.bt.clear()
        return Action(intent=Intent.DESPEDIDA)

    def _act_realizar(self, user: str, state: State) -> Action:
        """
        Objetivo: Realizar uma operação solicitada pelo usuário.
        Descrição: Verifica se todos os slots necessários para a operação estão preenchidos e, se necessário,
                   solicita mais informações.
        Entradas:
            - user (str): Identificador do usuário.
            - state (State): O estado atual do usuário.
        Saídas:
            - Action: Ação para realizar a operação.
        """
        primary_slots = self.km.get_primary_slots(state.operation)
        missing_slots = [slot for slot in primary_slots if slot not in state.slots]
        if missing_slots:
            return Action(intent=Intent.PERGUNTAR, operation=state.operation, slots={'info': missing_slots})

        if self.km.confirmation_demand(state.operation):
            log.debug('Pending confirmation ' + state.operation)
            self._check_next_operation = False
            self._action_pending_confirmation = Action(intent=Intent.INFORMAR, operation=state.operation,
                                                       slots=state.slots)
            remember = len(state.relevant_events) > 0
            return Action(intent=Intent.CONFIRMAR, operation=state.operation, slots=state.slots, remember=remember)

        state.relevant_events = []
        self.bt.reset(state.intent, state.operation)
        # INFO: not checking next operation to show context switching
        # self._check_next_operation = True
        return Action(intent=Intent.INFORMAR, operation=state.operation, slots=state.slots)

    def _act_informar(self, user: str, state: State) -> Action:
        """
        Objetivo: Fornecer informações solicitadas ao usuário.
        Descrição: Quando o usuário solicita informações, busca-se as definições ou dados solicitados para fornecer
                   uma resposta.
        Entradas:
            - user (str): Identificador do usuário.
            - state (State): O estado atual do usuário.
        Saídas:
            - Action: Ação com as informações solicitadas.
        """
        if state.question == Question.O_QUE and 'tipo_transferencia' in state.slots:
            # currently only works for tipo_transferencia entity, generalize for more knowledge
            definition = self.km.get_definition(state.slots['tipo_transferencia'], domain=state.domain)
            if definition:
                action = Action(intent=Intent.INFORMAR, question=state.question)
                action.slots = {'definition': definition}
                return action

        slots = {'domain': state.domain}
        messages = []
        return Action(intent=Intent.LLM, slots=slots, context_messages=messages)

    def _select_states(self, states: list[State]) -> list[State]:
        """
        Objetivo: Selecionar os estados 'current' para executar ações imediatas.
        Descrição: A função verifica os estados atuais ('current') e, se não houver, seleciona o último estado da lista.
        Entradas:
            - states (list[State]): Lista de estados atuais do usuário.
        Saídas:
            - list[State]: Lista de estados a serem considerados para ação.
        """
        current_states = [s for s in states if s.current]
        if not current_states:
            return [states[-1]]
        return current_states
