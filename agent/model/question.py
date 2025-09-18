from enum import Enum
from typing_extensions import Self

# --------------------------------------------------------------
# Enumeração para representar tipos de perguntas
# --------------------------------------------------------------

class Question(str, Enum):
    """
    Objetivo: Representar os tipos de perguntas que podem ser feitas.
    Tipos de perguntas:
        - O_QUE: Pergunta sobre o que algo é ou acontece.
        - ONDE: Pergunta sobre o local onde algo ocorre.
        - QUANDO: Pergunta sobre o tempo ou momento de algo.
        - COMO: Pergunta sobre o modo ou maneira como algo acontece.
    Métodos:
        - from_str: Converte uma string para um tipo de pergunta correspondente.
        - __str__: Retorna a representação em string da pergunta.
        - __repr__: Retorna uma representação para depuração da pergunta.
    """
    O_QUE = 'o que'
    ONDE = 'onde'
    QUANDO = 'quando'
    COMO = 'como'

    # --------------------------------------------------------------
    # Método estático para converter uma string para o tipo de pergunta
    # --------------------------------------------------------------
    @staticmethod
    def from_str(s: str) -> Self:
        """
        Objetivo: Converter uma string para o tipo de pergunta correspondente.
        Descrição: Este método permite transformar strings que representem
                   tipos de perguntas em um valor enumerado do tipo `Question`.
        Entradas:
            - s (str): A string representando o tipo de pergunta.
        Saídas:
            - Question: O tipo correspondente de pergunta como valor enumerado.
        """
        
        # Normaliza a string para minúsculo
        s = s.lower()

        if s == 'o_que':
            return Question.O_QUE
        elif s == 'onde':
            return Question.ONDE
        elif s == 'quando':
            return Question.QUANDO
        elif s == 'como':
            return Question.COMO

    # --------------------------------------------------------------
    # Método para converter o tipo de pergunta para uma string
    # --------------------------------------------------------------
    def __str__(self) -> str:
        return self.value

    # --------------------------------------------------------------
    # Método para representação do tipo de pergunta para depuração
    # --------------------------------------------------------------
    def __repr__(self) -> str:
        return self.value
