import logging
from model.filter_result import FilterResult
from model.input_message import InputMessage
from model.env import Env
from transformers import pipeline
from huggingface_hub import login
from module.NLUTeste import NLU
import os
from dotenv import load_dotenv
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
# Configuração do Logger
log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,  # Define o nível mínimo de mensagens que serão registradas
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem
)

class UserConnection:
    def __init__(self, use_llm=False):
        self.use_llm = use_llm

        # Verificar se o uso de LLM está habilitado
        if self.use_llm:
            # Obter a chave de API da Hugging Face
            huggingface_api_key = os.getenv("HuggingFace_API_KEY")
            if not huggingface_api_key:
                raise ValueError("Hugging Face API Key não fornecida.")
            
            # Realizar login utilizando a chave de API
            try:
                login(huggingface_api_key)
                log.info("Login na Hugging Face bem-sucedido.")
            except Exception as e:
                log.error(f"Erro ao realizar login na Hugging Face: {str(e)}")
                raise

            # Inicializar o pipeline com o modelo Llama-3B-Instruct
            try:
                self.llm_client = NLU()
            except Exception as e:
                log.error(f"Erro ao conectar modelo: {str(e)}")
                raise

    def filter_input(self, text: str) -> FilterResult:
        '''Filtra o texto de entrada, retornando True se o texto for válido e
           deve ser processado ou False se for inválido e o sistema não deve
           prosseguir com a mensagem.'''

        log.debug("Iniciando filtragem de entrada")
        
        if not self.use_llm:
            log.debug("LLM não habilitado, retornando resultado positivo para o filtro.")
            return FilterResult(True)
        else:
            try:
                # Usar o modelo Llama da Hugging Face para processar a entrada
                log.debug(f"Processando texto de entrada: {text}")
                response = self.llm_client.generate(text, max_length=100, truncation=True)
                
                # Verificar se a resposta gerada é válida
                if response and len(response) > 0:
                    log.info("Texto de entrada filtrado com sucesso.")
                    return FilterResult(True)
                else:
                    log.warning("Texto de entrada gerou uma resposta inválida.")
                    return FilterResult(False, error_code='llm.filter.invalid')
            except Exception as e:
                log.error(f"Erro ao filtrar entrada com a API LLM: {str(e)}")
                return FilterResult(False, error_code=f'API Error: {str(e)}')
    
    def filter_output(self, output_text: str) -> FilterResult:
        '''Filtra o texto de saída, retornando True se o texto gerado for
           válido e pode ser retornado ao usuário, ou False se for inválido.'''

        log.debug("Iniciando filtragem de saída")
        
        if not self.use_llm:
            log.debug("LLM não habilitado, retornando resultado positivo para o filtro.")
            return FilterResult(True)

        try:
            # Usar o modelo Llama da Hugging Face para verificar a saída
            log.debug(f"Processando texto de saída: {output_text}")
            response = self.llm_client.generate(output_text, max_length=100, truncation=True)

            # Verificar se a resposta gerada é válida
            if response and len(response) > 0:
                log.info("Texto de saída filtrado com sucesso.")
                return FilterResult(True)
            else:
                log.warning("Texto de saída gerou uma resposta inválida.")
                return FilterResult(False, error_code='llm.output.invalid')
        except Exception as e:
            log.error(f"Erro ao filtrar saída com a API LLM: {str(e)}")
            return FilterResult(False, error_code=f'API Error: {str(e)}')