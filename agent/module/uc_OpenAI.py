import logging
import os
from model.filter_result import FilterResult
from model.input_message import InputMessage
from model.env import Env
from openai import OpenAI
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
            # Obter a chave de API da OpenAI
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API Key não fornecida.")
            
            # Configurar a chave da OpenAI
            OpenAI.api_key = openai_api_key
            log.info("Configuração da OpenAI API bem-sucedida.")
            self.client = OpenAI()
            # Não há necessidade de login como na Hugging Face. A API da OpenAI usa apenas a chave de API.

    def generate(self, prompt, model="gpt-4o-mini", max_tokens=100):
        """
        Gera uma resposta utilizando a API da OpenAI (GPT-4 ou outro modelo).
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                n=1,
                temperature=0.7  # Controla a aleatoriedade da resposta gerada
            )
            generated_text = response.choices[0].message.content.strip()
            return generated_text
        except Exception as e:
            log.error(f"Erro ao gerar resposta com a OpenAI API: {e}")
            return None

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
                # Usar a API da OpenAI para processar a entrada
                log.debug(f"Processando texto de entrada: {text}")
                response = self.generate(text, model="gpt-4", max_tokens=100)
                
                # Verificar se a resposta gerada é válida
                if response and len(response) > 0:
                    log.info("Texto de entrada filtrado com sucesso.")
                    return FilterResult(True)
                else:
                    log.warning("Texto de entrada gerou uma resposta inválida.")
                    return FilterResult(False, error_code='llm.filter.invalid')
            except Exception as e:
                log.error(f"Erro ao filtrar entrada com a API da OpenAI: {str(e)}")
                return FilterResult(False, error_code=f'API Error: {str(e)}')
    
    def filter_output(self, output_text: str) -> FilterResult:
        '''Filtra o texto de saída, retornando True se o texto gerado for
           válido e pode ser retornado ao usuário, ou False se for inválido.'''

        log.debug("Iniciando filtragem de saída")
        
        if not self.use_llm:
            log.debug("LLM não habilitado, retornando resultado positivo para o filtro.")
            return FilterResult(True)

        try:
            # Usar a API da OpenAI para verificar a saída
            log.debug(f"Processando texto de saída: {output_text}")
            response = self.generate(output_text, model="gpt-4", max_tokens=100)

            # Verificar se a resposta gerada é válida
            if response and len(response) > 0:
                log.info("Texto de saída filtrado com sucesso.")
                return FilterResult(True)
            else:
                log.warning("Texto de saída gerou uma resposta inválida.")
                return FilterResult(False, error_code='llm.output.invalid')
        except Exception as e:
            log.error(f"Erro ao filtrar saída com a API da OpenAI: {str(e)}")
            return FilterResult(False, error_code=f'API Error: {str(e)}')
