from dataclasses import dataclass, field
from typing import Iterator

from model.intent import Intent
from model.question import Question


@dataclass
class SemanticDocument:
    """
    Representa um documento semântico contendo informações sobre intenções, operações, perguntas, entidades, 
    sentimentos, dependência e complexidade de uma mensagem ou conjunto de mensagens.

    Atributos:
        intents (list[Intent | None]): Lista de intenções identificadas no texto.
        operations (list[str | None]): Lista de operações identificadas no texto.
        questions (list[Question | None]): Lista de perguntas identificadas no texto.
        entities (list[tuple[str, str]]): Lista de entidades identificadas no texto (tupla de nome e tipo).
        sentiment (str): Sentimento extraído do texto, como 'positivo' ou 'negativo'.
        domain (str): O domínio da mensagem, por padrão 'transacional'.
        dependent (bool): Indica se a pergunta depende de uma mensagem anterior.

    Métodos:
        get_sentences(): Retorna um iterador de sentenças, onde cada sentença é uma string gerada a partir dos tokens do texto.
    """
    intents: list[Intent | None] = field(default_factory=list)
    operations: list[str | None] = field(default_factory=list)
    questions: list[Question | None] = field(default=list)
    entities: list[tuple[str, str]] = field(default_factory=list)
    sentiment: str = ''
    out_of_context: bool = False
    domain: str = 'transacional'
    dependent: bool = False

    def get_sentences(self) -> Iterator[str]:
        """
        Retorna um iterador de sentenças construídas a partir dos tokens do documento semântico.

        Cada sentença é uma combinação dos textos dos tokens em uma string.

        Returns:
            Iterator[str]: Um iterador que gera sentenças no formato de strings.
        """
        for sen in self.sentences:
            yield ' '.join([token.text for token in sen])
