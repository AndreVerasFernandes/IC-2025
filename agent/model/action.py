from pydantic import BaseModel, Field

from model.intent import Intent
from model.message_model import MessageModel
from model.question import Question

# --------------------------------------------------------------
# Modelo de dados para representar uma ação no sistema
# --------------------------------------------------------------

class Action(BaseModel):
    """
    Objetivo: Representar uma ação a ser executada no sistema, incluindo informações sobre
              intenção, operação, pergunta, emoção, níveis de proatividade e mensagens de contexto.
    Atributos:
        - intent (Intent): Intenção da ação.
        - operation (str | None): Nome da operação associada à ação (opcional).
        - question (Question | None): Pergunta associada à ação, se houver (opcional).
        - emotion (str | None): Emoção associada à ação (opcional).
        - slots (dict): Dados estruturados associados à ação (ex.: parâmetros).
        - remember (bool): Indica se a ação deve ser memorizada para contexto futuro.
        - context_messages (list[MessageModel]): Lista de mensagens que formam o contexto da ação.
    """

    intent: Intent
    operation: str | None = None
    question: Question | None = None
    emotion: str | None = None
    slots: dict = Field(default_factory=dict)
    remember: bool = Field(default=False)
    context_messages: list[MessageModel] = Field(default_factory=list)
