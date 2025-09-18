from datetime import datetime
from enum import Enum
from pydantic import BaseModel

# --------------------------------------------------------------
# Modelo de dados para representar uma mensagem no diálogo
# --------------------------------------------------------------

class DialogRole(str, Enum):
    """
    Objetivo: Representar os papéis possíveis em uma interação de diálogo.
    Papéis:
        - USER: Representa o usuário que está interagindo.
        - SYSTEM: Representa o sistema que está respondendo ou interagindo.
    """
    USER = 'user'
    SYSTEM = 'system'


class MessageModel(BaseModel):
    """
    Objetivo: Representar uma mensagem no diálogo, contendo informações sobre o conteúdo, 
              papel do remetente e o horário do envio.
    Atributos:
        - content (str): Texto da mensagem.
        - role (DialogRole): Papel do remetente da mensagem (USER ou SYSTEM).
        - sent_time (datetime): Horário em que a mensagem foi enviada.
    Métodos:
        - to_dict: Converte a mensagem em um dicionário contendo papel e conteúdo.
        - to_str: Retorna uma representação em string da mensagem no formato "ROLE: CONTENT".
    """
    
    content: str
    role: DialogRole
    sent_time: datetime

    # --------------------------------------------------------------
    # Método para converter a mensagem em um dicionário
    # --------------------------------------------------------------
    def to_dict(self) -> dict[str, str]:
        """
        Objetivo: Converter a mensagem em um dicionário contendo papel e conteúdo.
        Entradas: Nenhuma.
        Saídas:
            - Dicionário com as chaves 'role' e 'content'.
        """
        return {
            'role': str(self.role),
            'content': self.content
        }

    # --------------------------------------------------------------
    # Método para converter a mensagem em uma string formatada
    # --------------------------------------------------------------
    def to_str(self) -> str:
        """
        Objetivo: Retornar uma representação em string da mensagem no formato "ROLE: CONTENT".
        Entradas: Nenhuma.
        Saídas:
            - String representando o papel e o conteúdo da mensagem.
        """
        return self.role.upper() + ': ' + self.content
