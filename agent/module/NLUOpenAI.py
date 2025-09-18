import logging
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

log = logging.getLogger(__name__)

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class NLU:
    def __init__(self, model_name="gpt-4o-mini", device=None):
        """
        Inicializa a classe NLU e configura os recursos necessários.
        Args:
            model_name (str): Nome do modelo da OpenAI a ser carregado.
            device (str): Dispositivo de execução ('cpu' ou 'cuda'). Se None, não será utilizado.
        """
        logging.info("Inicializando a classe NLU ...")

        # Carregar o token da OpenAI a partir do arquivo .env
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")
        if OpenAI.api_key is None:
            logging.error("OPENAI_API_KEY não encontrado nas variáveis de ambiente.")
            raise ValueError("OPENAI_API_KEY não encontrado nas variáveis de ambiente.")

        self.model_name = model_name
        logging.info(f"Modelo {model_name} configurado com sucesso.")
        self.client = OpenAI()

    def generate(self, messages):
        """
        Gera texto baseado em um prompt usando a API da OpenAI.
        
        Args:
            prompt (str): Texto de entrada para o modelo.

        Returns:
            str: Texto gerado pela OpenAI.
        """
        logging.info("___ Gerando texto a partir do prompt ...")
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7
            )
            generated_text = response.choices[0].message.content.strip()
            logging.info(f"___ Texto gerado com sucesso: {generated_text}")
            return generated_text
        except Exception as e:
            logging.error(f"Erro ao gerar texto: {e}")
            return str(e)

    def generate_semantic_information(self, text: str) -> dict:
        """
        Usa o modelo da OpenAI para gerar informações semânticas.

        Args:
            text (str): Texto de entrada do usuário.

        Returns:
            dict: Informações semânticas extraídas pelo modelo.
        """
        logging.info("Gerando informações semânticas com a API da OpenAI.")

        if not text:
            logging.warning("Texto vazio fornecido. Retornando JSON com valores nulos.")
            return {
                "original_sentence": None,
                "analysis": None
            }

        # Definir o sistema de instrução
        system_instruction = """Você é um especialista em análise semântica, sintática e pragmática de textos em português do Brasil.
Sua tarefa é analisar uma mensagem textual e gerar um objeto JSON com as seguintes informações:

1. Entrada:
    - Mensagem em português.

2. Saída (Formato JSON):
    {
      "original_sentence": "<mensagem_original>",
      "analysis": {
        "intents": [],
        "operations": [],
        "questions": [],
        "entities": [],
        "sentiment": "",
        "domain": "",
        "dependent": false,
        "complexity": null
      }
    }
3. Detalhes das chaves:
    - original_sentence: Frase original.
    - analysis: Detalhamento semântico.
        - intents: Intenções.
        - operations: Ações solicitadas.
        - questions: Perguntas explícitas.
        - entities: Entidades identificadas.
        - sentiment: Sentimento da frase.
        - domain: Domínio da frase (informacional ou transacional).
        - dependent: Se a frase depende de contexto anterior.
        - complexity: Complexidade da frase.
"""

        user_prompt = f"Analise a seguinte frase: {text}"

        messages = [
            {"role": "system", "content": system_instruction},  # A instrução do sistema
            {"role": "user", "content": user_prompt}  # A frase do usuário
        ]

        # Gerar texto com a OpenAI API
        try:
            model_response = self.generate(messages)
            logging.info(f"\n+++ Resposta bruta da OpenAI: {model_response}")
            # Extração do JSON gerado
            try:
                semantic_info = json.loads(model_response)
                logging.info(f"\n+++ JSON extraído com sucesso: {semantic_info}")
                return semantic_info
            except json.JSONDecodeError as e:
                logging.error(f"Erro ao decodificar o JSON: {e}")
                return {"error": "Erro ao processar JSON."}
        except Exception as e:
            logging.error(f"Erro ao gerar informações semânticas: {e}")
            return {"error": str(e)}

    def process(self, message: str) -> dict:
        """
        Processa a frase do usuário e gera um documento semântico estruturado.
        
        Args:
            message (str): Mensagem de entrada do usuário.
        
        Returns:
            dict: Documento semântico estruturado.
        """
        logging.info("Iniciando processamento da mensagem.")

        # Validar entrada
        if not message:
            logging.warning("Nenhuma mensagem fornecida. Retornando JSON nulo.")
            return {
                "original_sentence": None,
                "analysis": None
            }

        # Gerar informações semânticas usando a OpenAI API
        semantic_info = self.generate_semantic_information(message)
        logging.info(f"\n+++ Informações semânticas geradas: {semantic_info}")

        if "error" in semantic_info:
            logging.error(f"Erro ao gerar informações semânticas: {semantic_info['error']}")
            return {
                "original_sentence": message,
                "analysis": None,
                "error": semantic_info["error"]
            }

        logging.info(f"\n+++ Documento semântico gerado com sucesso: {json.dumps(semantic_info, indent=4, ensure_ascii=False)}")
        return semantic_info
