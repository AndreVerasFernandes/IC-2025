import logging
import os
import json
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

class NLU:
    def __init__(self, model_name="gemini-2.0-flash", device=None):
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

        # Cliente OpenAI compatível com Gemini
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        logging.info(f"Modelo '{model_name}' configurado com sucesso para uso com Gemini.")

    def generate(self, messages):
        """
        Gera resposta do modelo Gemini com base em mensagens no estilo OpenAI chat.
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
                max_tokens=1024,
                temperature=0.7
            )

            generated_text = response.choices[0].message.content.strip()
            logging.info(f"___ Texto gerado: {generated_text}")
            return generated_text

        except Exception as e:
            logging.error(f"Erro ao gerar texto: {e}")
            return str(e)

    def generate_semantic_information(self, text: str) -> dict:
        """
        Usa o modelo Gemini para gerar informações semânticas estruturadas.
        """
        logging.info("Gerando informações semânticas ...")

        if not text:
            logging.warning("Texto de entrada está vazio.")
            return {
                "original_sentence": None,
                "analysis": None
            }

        system_instruction = (
                "Você é um especialista em análise semântica, sintática e pragmática de textos em português do Brasil. "
                "Sua tarefa é analisar uma mensagem textual e gerar um objeto JSON com as seguintes informações:\n\n"
                "IMPORTANTE: Retorne APENAS o JSON puro, sem comentários, explicações ou blocos de código markdown como ```json \n"
                "Formato de saída esperado:\n"
                "{\n"
                '  "original_sentence": "<mensagem_original>",\n'
                '  "analysis": {\n'
                '    "intents": [],\n'
                '    "operations": [],\n'
                '    "questions": [],\n'
                '    "entities": [],\n'
                '    "sentiment": "",\n'
                '    "domain": "",\n'
                '    "dependent": false,\n'
                '    "complexity": null\n'
                "  }\n"
                "}\n\n"
                "Regra adicional: caso a mensagem seja uma pergunta, adicione obrigatoriamente o valor \"question\" na lista \"intents\"."
        )

        user_prompt = f"Analise a seguinte frase: {text}"

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]

        model_response = self.generate(messages)
        cleaned_response = re.sub(r"^```(?:json)?|```$", "", model_response.strip(), flags=re.MULTILINE).strip()
        try:
            semantic_info = json.loads(cleaned_response)
            logging.info(f"JSON extraído com sucesso: {json.dumps(semantic_info, indent=2, ensure_ascii=False)}")
            return semantic_info

        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar JSON: {e}")
            return {"error": "Erro ao processar resposta como JSON."}

    def process(self, message: str) -> dict:
        """
        Processa a mensagem do usuário e gera um documento semântico estruturado.
        """
        logging.info("Iniciando o processamento da mensagem.")

        if not message:
            logging.warning("Mensagem vazia recebida.")
            return {
                "original_sentence": None,
                "analysis": None
            }

        semantic_info = self.generate_semantic_information(message)

        if "error" in semantic_info:
            logging.error(f"Erro ao processar mensagem: {semantic_info['error']}")
            return {
                "original_sentence": message,
                "analysis": None,
                "error": semantic_info["error"]
            }

        return semantic_info
