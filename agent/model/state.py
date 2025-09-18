from dataclasses import dataclass, field
from typing import Dict
from .intent import Intent
from .question import Question

# --------------------------------------------------------------
# Classe para representar o estado de uma interação semântica
# --------------------------------------------------------------


@dataclass
class State:
    """
    Objetivo: Representar o estado de uma interação semântica, que pode incluir intenções,
              operações, perguntas, e outros detalhes de contexto.
    Atributos:
        - intent: A intenção associada ao estado.
        - operation: Operação relacionada ao estado (opcional).
        - question: Pergunta relacionada ao estado (opcional).
        - current: Indica se o estado é o estado atual da interação (padrão é True).
        - emotion: Emoção associada ao estado (opcional).
        - slots: Dicionário de slots associados ao estado.
        - relevant_events: Lista de eventos relevantes para o estado.
        - out_of_context: Indica se o estado está fora do contexto esperado.
        - domain: Domínio da interação (por padrão 'transacional').
        - whitelisted: Indica se o estado é parte de uma lista branca.
        - dependent: Indica se o estado depende de outro contexto ou interação.
        - complexity: Nível de complexidade da pergunta associada ao estado.
    Métodos:
        - update_slots: Atualiza os slots com novas entidades.
        - update_operacao: Atualiza a operação associada ao estado, se não houver uma já definida.
        - update_question: Atualiza a pergunta associada ao estado.
    """

    intent: Intent
    operation: str = None
    question: Question = None
    current: bool = True
    emotion: str = None
    slots: dict = field(default_factory=dict)
    relevant_events: list = field(default_factory=list)
    out_of_context: bool = False
    domain: str = 'transacional'
    whitelisted: bool = False
    dependent: bool = False

    # --------------------------------------------------------------
    # Método para atualizar os slots com novas entidades
    # --------------------------------------------------------------
    def update_slots(self, entidades: Dict[str, str]):
        """
        Objetivo: Atualizar os slots do estado com novas entidades fornecidas.
        Entradas:
            - entidades: Dicionário de entidades a serem adicionadas aos slots.
        Saídas: Nenhuma.
        """
        self.slots.update(entidades)

    # --------------------------------------------------------------
    # Método para atualizar a operação associada ao estado
    # --------------------------------------------------------------
    def update_operacao(self, operation: str):
        """
        Objetivo: Atualizar a operação associada ao estado, se a operação ainda não foi definida.
        Entradas:
            - operation: A operação a ser associada ao estado.
        Saídas: Nenhuma.
        """
        if not self.operation:
            self.operation = operation

    # --------------------------------------------------------------
    # Método para atualizar a pergunta associada ao estado
    # --------------------------------------------------------------
    def update_question(self, question: Question):
        """
        Objetivo: Atualizar a pergunta associada ao estado, se houver uma pergunta fornecida.
        Entradas:
            - question: A pergunta a ser associada ao estado.
        Saídas: Nenhuma.
        """
        if question:
            self.question = question
