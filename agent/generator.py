import logging
import os

from openai import OpenAI
from dotenv import load_dotenv
import re

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Generator:
    def __init__(self, model_name="gemini-2.0-flash", max_tokens: int = 1024, temperature: float = 0.7, device=None):
        """
        Inicializa a classe NLU e configura o cliente para a API do Gemini (via SDK da OpenAI).
        """
        logging.info("Inicializando a classe NLU ...")

        # Carregar chave da API Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logging.error("GEMINI_API_KEY não encontrado nas variáveis de ambiente.")
            raise ValueError("GEMINI_API_KEY não encontrado.")

        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature



        # Cliente OpenAI compatível com Gemini
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        logging.info(f"Modelo '{model_name}' configurado com sucesso para uso com Gemini.")

    def generate_answer(self, messages):
        """
        Gera resposta do modelo Gemini com base em mensagens no estilo OpenAI chat.

        Exemplo para chamar:

            
        system_instruction = (
            "You are a helpful assistant."
                )
            
            user_prompt = f"Analise a seguinte frase: Bom dia!"

            messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
            ]

        model_response = Generator.generate(messages)
        """
        logging.info("___ Gerando texto com o modelo Gemini ...")

        try:
            # Validação de mensagens
            if not isinstance(messages, list) or not messages:
                raise ValueError("Formato inválido para 'messages'.")

            for msg in messages:
                if not msg.get("role") or not msg.get("content"):
                    raise ValueError("Cada mensagem deve conter 'role' e 'content' não nulos.")

            # Chamada à API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            generated_text = response.choices[0].message.content.strip()
            logging.info(f"___ Texto gerado: {generated_text}")
            return generated_text

        except Exception as e:
            logging.error(f"Erro ao gerar texto: {e}")
            return str(e)