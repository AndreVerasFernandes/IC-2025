from dataclasses import dataclass


@dataclass
class SemanticToken:
    """
    Representa um token semântico extraído de um texto, contendo informações sobre o próprio token e seu contexto linguístico.

    Atributos:
        text (str): O texto do token, ou seja, a palavra ou unidade de texto.
        pos (str): A parte do discurso (POS) do token, como 'substantivo', 'verbo', etc. O valor padrão é uma string vazia.
        word_sense (str): O sentido ou significado do token, caso identificado. O valor padrão é uma string vazia.
    """
    text: str
    pos: str = ''
    word_sense: str = ''
