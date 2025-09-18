from enum import Enum


class Intent(str, Enum):
    """
    Enumeração das possíveis intenções identificáveis em uma mensagem.

    Options:
        SAUDACAO (str): Intenção de saudação.
        DESPEDIDA (str): Intenção de despedida.
        INFORMAR (str): Intenção de informar algo.
        REALIZAR (str): Intenção de realizar uma ação.
        CONFIRMAR (str): Intenção de confirmar.
        NAO_CONFIRMAR (str): Intenção de não confirmar.
        PERGUNTAR (str): Intenção de fazer uma pergunta.
        SUMARIZAR (str): Intenção de sumarizar informações.
        LLM (str): Intenção relacionada ao uso de um modelo de linguagem.
        FORA_CONTEXTO (str): Intenção fora do contexto esperado.
        FORA_CONTEXTO_LLM (str): Intenção fora do contexto para o modelo de linguagem.

    Methods:
        from_str(s): Converte uma string em uma instância de Intent correspondente.
    """
    
    SAUDACAO = 'saudação'
    DESPEDIDA = 'despedida'
    INFORMAR = 'informar'
    REALIZAR = 'realizar'
    CONFIRMAR = 'confirmar'
    NAO_CONFIRMAR = 'não confirmar'
    PERGUNTAR = 'perguntar'
    SUMARIZAR = 'sumarizar'
    LLM = 'llm'
    FORA_CONTEXTO = 'fora de contexto'
    FORA_CONTEXTO_LLM = 'fora de contexto llm'

    @staticmethod
    def from_str(s):
        """
        Converte uma string em uma instância da classe Intent correspondente, se possível.

        Args:
            s (str): Texto representando a intenção.

        Returns:
            Intent | None: Instância correspondente de Intent ou None se não for encontrada.
        """
        s = s.lower()
        if s == 'saudação':
            return Intent.SAUDACAO
        elif s == 'despedida':
            return Intent.DESPEDIDA
        elif s == 'informar':
            return Intent.INFORMAR
        elif s == 'realizar':
            return Intent.REALIZAR
        elif s == 'confirmar':
            return Intent.CONFIRMAR
        elif s == 'nao_confirmar':
            return Intent.NAO_CONFIRMAR
        else:
            return None

    def __str__(self) -> str:
        """
        Representa a intenção como uma string.

        Returns:
            str: Valor da intenção.
        """
        return self.value

    def __repr__(self) -> str:
        """
        Representação formal da intenção.

        Returns:
            str: Valor da intenção.
        """
        return self.value
