import logging
import os
import json
#import spacy
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from dotenv import load_dotenv
log = logging.getLogger(__name__)

path = "D:\\llama-3.2" 

logging.basicConfig(
    level=logging.DEBUG,  # Define o nível mínimo de mensagens que serão registradas
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato da mensagem
)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Classe NLU para processamento semântico
class NLU:
    def __init__(self, model_name="unsloth/Llama-3.2-3B", device=None):
        """
        Inicializa o modelo Llama-3.2-3B-Instruct e configura os recursos necessários.
        Args:
            model_name (str): Nome do modelo a ser carregado.
            device (str): Dispositivo de execução ('cpu' ou 'cuda'). Se None, detecta automaticamente.
        """
        logging.info("Inicializando a classe NLU ...")

        # Carregar o token do Hugging Face Hub a partir do arquivo .env
        hf_token = os.getenv("HuggingFace_API_KEY")
        if hf_token is None:
            logging.error("HF_TOKEN não encontrado nas variáveis de ambiente.")
            raise ValueError("HF_TOKEN não encontrado nas variáveis de ambiente.")

        # Log in to Hugging Face Hub
        login(token=hf_token)

        # Detectar dispositivo se não fornecido
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        logging.info(f"Dispositivo detectado: {self.device}")

        # Carregar o modelo Llama-3.2-3B-Instruct
        logging.info(f"Carregando o modelo {model_name} ...")
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            cache_dir="D:/cache",
    
        ).to(self.device)
        self.model = self.model.eval()
        logging.info("Modelo carregado com sucesso.")

        # Carregar o tokenizador correspondente
        logging.info("Carregando o tokenizador ...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir="D:/cache")
        logging.info("Tokenizador carregado com sucesso.")

        #activated = spacy.prefer_gpu()
        #self.nlp = spacy.load("pt_core_news_sm")
        #logging.info("Modelo e pipeline spaCy carregados com sucesso.")

    def generate(self, prompt, add_special_tokens=True):
        """
        Gera texto baseado em um prompt usando o modelo e tokenizador da classe.

        Args:
            prompt (str): Texto de entrada para o modelo.
            add_special_tokens (bool): Se True, adiciona tokens especiais ao prompt.

        Returns:
            str: Texto gerado pelo modelo.
        """
        logging.info("___ Gerando texto a partir do prompt ...")
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            add_special_tokens=add_special_tokens,
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=True
            )

        result = outputs[0][inputs["input_ids"].shape[-1]:]
        generated_text = self.tokenizer.decode(result, skip_special_tokens=False)

        logging.info(f"___ Texto gerado com sucesso: {generated_text}")
        return generated_text

#    def tokenize_with_spacy(self, text: str) -> list:
#        """
#        Tokeniza o texto usando o modelo spaCy.
#
#        Args:
#            text (str): Texto a ser tokenizado.
#
#        Returns:
#            list: Lista de frases tokenizadas.
#        """
#        logging.info("Tokenizando o texto com spaCy ...")
#        doc = self.nlp(text)
#        sentences = [sent.text for sent in doc.sents]
#        logging.info(f"Texto tokenizado com sucesso: {sentences}")
#        return sentences

    def generate_semantic_information(self, text: str) -> dict:
        """
        Usa o modelo Llama-3.2-3B-Instruct para gerar informações semânticas.

        Args:
            text (str): Texto de entrada do usuário.

        Returns:
            dict: Informações semânticas extraídas pelo modelo.
        """
        logging.info("Gerando informações semânticas com o modelo Llama-3.2-3B-Instruct.")

        if not text:
            logging.warning("Texto vazio fornecido. Retornando JSON com valores nulos.")
            return {
                "original_sentence": None,
                "analysis": None
            }

        # Definir as instruções do sistema e o prompt do usuário
        system_instruction = """\
<|start_header_id|>system<|end_header_id|>

Você é um especialista em análise semântica, sintática e pragmática de textos em português do Brasil.
Sua tarefa é analisar uma mensagem textual e gerar um objeto JSON com as seguintes informações:

1. Entrada
    - Mensagem em português (pode conter uma ou mais frases).
    - Se a mensagem for nula ou vazia, ainda deve retornar o JSON com todos os campos preenchidos com valores vazios ou padrão.

2. Saída (Formato JSON)
    json
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

3. Descrição das Chaves:
    - original_sentence (string): A frase original analisada.

    - analysis (objeto):

        - intents (lista de strings): Intenções da mensagem. Ex: ["question", "information_request"].

        - operations (lista de strings): Ações práticas solicitadas. Ex: ["cancel_service"].

        - questions (lista de strings): Perguntas explícitas no texto.

        - entities (lista de objetos):
          json
          { "entity": "<texto_da_entidade>", "type": "<object|attribute|concept|event|action|possessive_pronoun|time|place|organization|person>" }

        - sentiment (string): "positivo", "negativo", "neutro", "misto", "incerto", ou "".

        - domain (string): "informacional" ou "transacional".

        - dependent (bool): true se depende de contexto anterior; senão false.

        - complexity (string ou null): "simples", "complexa" ou null.

4. Casos de Mensagem Vazia:
    - Retornar o mesmo JSON com:
        - Strings vazias
        - Listas vazias
        - dependent: false
        - complexity: null

5. Restrições:
    - Não adicionar explicações ou comentários.
    - Não incluir campos extras.
    - Mesmo em falha, o JSON deve ser gerado com os campos conforme estrutura.

6.	Processo de Geração (Ordem Interna Sugerida ao LLM):
(Não incluir no resultado final, apenas orientação interna)
a) Identifique se há perguntas, intenções, operações.
b) Extraia entidades.
c) Defina sentimento com base no tom geral.
d) Defina domínio conforme contexto (informacional versus transacional)
...
<|eot_id|><|start_header_id|>"""

        user_prompt = f"""
Analise a seguinte frase:
<<<
{text}
>>>
"""
        # Formatar o prompt completo
        prompt = f"{system_instruction}{user_prompt}<|eot_id|><|start_header_id|>"

        # Gerar texto com o modelo
        try:
            model_response = self.generate(prompt)
            logging.info(f"\n+++ Resposta bruta do modelo: {model_response}")
            log.debug(f"Resposta bruta do modelo: {model_response}")
            # Extração do JSON gerado
            json_start = model_response.find("{")
            json_end = model_response.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                json_str = model_response[json_start:json_end]
                try:
                    semantic_info = json.loads(json_str)
                    logging.info(f"\n+++JSON extraído com sucesso: {semantic_info}")
                    return semantic_info
                except json.JSONDecodeError as e:
                    logging.error(f"Erro ao decodificar o JSON: {e}")
                    return {"error": "Erro ao processar JSON."}
            else:
                logging.error("JSON não encontrado na resposta.")
                return {"error": "JSON não encontrado na resposta."}
        except Exception as e:
            logging.error(f"Erro ao gerar informações semânticas: {e}")
            return {"error": str(e)}

    def process(self, message: str) -> dict:
        """
        Processa a frase do usuário e gera um documento semântico estruturado.
        Args:
            message (str): Mensagem de entrada do usuário.
        Returns:
            dict: Documento semântico estruturado no formato JSON.
        """
        logging.info("Iniciando processamento da mensagem.")

        # Validar entrada
        if not message:
            logging.warning("Nenhuma mensagem fornecida. Retornando JSON nulo.")
            return {
                "original_sentence": None,
                "analysis": None
            }

        # Tokenizar mensagem usando spaCy
        #sentences = self.tokenize_with_spacy(message)

        # Gerar informações semânticas usando o modelo
        semantic_info = self.generate_semantic_information(message)
        logging.info(f"\n+++ Gerado informações semânticas: {semantic_info}")

        if "error" in semantic_info:
            logging.error(f"Erro ao gerar informações semânticas: {semantic_info['error']}")
            return {
                "original_sentence": message,
                "analysis": None,
                "error": semantic_info["error"]
            }

        # Log do documento gerado
        logging.info(f"\n+++ Documento semântico gerado com sucesso: {json.dumps(semantic_info, indent=4, ensure_ascii=False)}")
        return semantic_info
