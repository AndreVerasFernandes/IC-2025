from pydantic import BaseModel, Field


class InputMessage(BaseModel):
    """
    Representa uma mensagem de entrada enviada por um usuário.

    Attributes:
        message (str): O conteúdo da mensagem do usuário.
        user (str): Identificador do usuário que enviou a mensagem.
        domain (str): Domínio da mensagem, usado para definir o contexto. O valor padrão é 'transacional'.
    """
    message: str
    user: str
    domain: str = Field(default='transacional')
