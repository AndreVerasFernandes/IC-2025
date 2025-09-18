import os
from dotenv import load_dotenv
from mistralai import Mistral


class Env:
    """
    Objetivo: Configurar o ambiente para a aplicação, incluindo a inicialização do cliente Mistral.
    Atributos:
        - mistral_client: Cliente para interagir com a API do Mistral, configurado com a chave de API.
    """
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
            raise ValueError("API_KEY não encontrada no arquivo .env")
    
    model = "mistral-small-latest"

    mistral_client = Mistral(api_key=API_KEY)

    HuggingFace_API_KEY = os.getenv("HuggingFace_API_KEY")

    @classmethod
    def get_mistral_client(cls):
        """
        Objetivo: Retornar o cliente Mistral configurado para interações com a API.
        Entradas: Nenhuma.
        Saídas:
            - mistral_client: Instância do cliente Mistral configurada com a chave de API.
        """
        return cls.mistral_client
    @classmethod
    def get_HuggingFace_API_KEY(cls):
        """
        Objetivo: Retornar a chave de API da Hugging Face.
        Entradas: Nenhuma.
        Saídas:
            - HuggingFace_API_KEY: Chave de API da Hugging Face.
        """
        return cls.HuggingFace_API_KEY
    