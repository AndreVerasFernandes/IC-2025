import logging
from collections import deque

from model.semantic_document import SemanticDocument
from model.state import State
from model.intent import Intent

log = logging.getLogger('bt')


class BeliefTracker:
    """Módulo do Belief Tracker para um único usuário.

    Responsável por gerenciar o contexto do diálogo e os estados de intenção/operacional, além de
    gerenciar a proatividade com base no feedback do usuário.

    Atributos:
        context (deque[State]): Fila que armazena os estados atuais do diálogo.
        user (str): Identificador do usuário.
    """

    def __init__(self, user: str):
        # Inicializa o Belief Tracker com o usuário especificado.
        self.context: deque[State] = deque()
        self.user = user

    def update_state(self, semantic_doc: SemanticDocument) -> list[State]:
        """
        Atualiza o estado do diálogo com base no documento semântico observado.

        Args:
            semantic_doc (SemanticDocument): Documento semântico produzido pelo NLU.

        Returns:
            list[State]: Representação dos estados atualizados do diálogo.
        """
        self._toggle_off_current_state()

        # Para cada intenção, operação e questão no documento semântico
        for intent, operation, question in zip(
            #semantic_doc.get('intents', []), 
            #semantic_doc.get('operations', []), 
            #semantic_doc.get('questions', [])

            semantic_doc.intents, 
            semantic_doc.operations, 
            semantic_doc.questions
        ):
            if not self.context:
                state = State(intent, operation, question)
                state = self._fill_state(state, semantic_doc)
                self.context.append(state)
                log.debug('Creating first state')
            else:
                if not intent:
                    log.debug('Updating last state')
                    # Atualiza o último estado na fila de contexto
                    state = self.context.pop()
                    state = self._fill_state(state, semantic_doc)
                    state.update_question(question)
                    state.current = True
                    self.context.append(state)
                else:
                    state = self._find_same_context_state(intent, operation)
                    if not state:
                        log.debug('No state with same intent found, creating a new one')
                        state = State(intent, operation, question)
                        state = self._fill_state(state, semantic_doc)
                    state.current = True
                    state = self._fill_state(state, semantic_doc)
                    state.update_question(question)
                    self.context.append(state)
            log.debug(self.context)
        self._sort_context(semantic_doc)
        return list(self.context)

    def reset(self, intent: Intent, operation: str):
        """
        Reseta o estado do diálogo para um novo estado com a intenção e operação especificadas.

        Args:
            intent (Intent): Intenção que se deseja resetar.
            operation (str): Operação associada à intenção que será resetada.
        """
        log.debug('reseting  ' + str(intent) + ' ' + str(operation))
        for _ in range(len(self.context)):
            state = self.context.pop()
            if state.intent == intent and state.operation == operation:
                continue
            self.context.appendleft(state)
        log.debug(str(self.context))

    def clear(self):
        """Limpa o contexto e os contextos armazenados."""
        self.context = deque()

    def _fill_state(self, state: State, semantic_doc: SemanticDocument) -> State:
        """
        Preenche o estado com informações adicionais extraídas do documento semântico.

        Args:
            state (State): Estado atual a ser preenchido.
            semantic_doc (SemanticDocument): Documento semântico com dados adicionais.

        Returns:
            State: Estado preenchido com dados do documento semântico.
        """
        state.update_slots(convert_to_slots(semantic_doc.entities))
        state.out_of_context = semantic_doc.out_of_context
        state.domain = semantic_doc.domain
        state.dependent = semantic_doc.dependent
        return state

    def _sort_context(self, semantic_doc: SemanticDocument):
        """Ordena o contexto, movendo para o topo as operações mais importantes."""
        priority_state = []
        for _ in range(len(self.context)):
            state = self.context.pop()
            if state.current:
                priority_state.append(state)
                continue
            self.context.appendleft(state)
        for state in priority_state:
            self.context.append(state)

    def _toggle_off_current_state(self):
        # Desativa o estado atual, tornando todos os estados não atuais.
        for state in self.context:
            state.current = False

    def _select_state(self) -> State:
        # Seleciona o último estado no contexto.
        return self.context[-1]

    def _find_same_context_state(self, intent: Intent, operation: str) -> State:
        """
        Procura por um estado no contexto que tenha a mesma intenção e operação.

        Args:
            intent (Intent): Intenção procurada.
            operation (str): Operação procurada.

        Returns:
            State: Estado correspondente com a mesma intenção e operação ou None.
        """

        same_context_state = None
        for _ in range(len(self.context)):
            state = self.context.pop()
            if self._is_same_context(intent, operation, state):
                same_context_state = state
            else:
                self.context.appendleft(state)
        return same_context_state

    def _is_same_context(self, intent: Intent, operation: str, state: State) -> bool:
        # Verifica se o estado possui a mesma intenção e operação.
        return intent == state.intent and operation == state.operation


def convert_to_slots(entities: list[tuple[str, str]]) -> dict[str, str]:
    """
    Converte uma lista de entidades (pares de nome-valor) em um dicionário de slots.

    Args:
        entities (list[tuple[str, str]]): Lista de entidades representadas como tuplas de nome e valor.

    Returns:
        dict[str, str]: Dicionário de slots com nomes e valores das entidades.
    """
    """
    slots = {}
    for value, name in entities:
        slots[name] = value
    return slots
    """
    slots = {}
    for entity in entities:
        if isinstance(entity, (tuple, list)) and len(entity) == 2:
            value, name = entity
            slots[name] = value
        elif isinstance(entity, str):
            slots[entity] = entity  # usa o valor como chave e valor
    return slots
