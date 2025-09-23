import sys
import os
import logging

# Adiciona a raiz do projeto (/workspaces/IC-2025) ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
rag_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rag'))
from rag.RAGInterface import RAGInterface

class KnowledgeManagement:
    def __init__(self, config_path="../rag/config.toml"):
        # Inicializando o RAGInterface dentro do KM
        self.rag_interface = RAGInterface(config_path=config_path)
    
    def query_knowledge(self, question: str, domain: str = "Teste") -> str:
        """
        Método para consultar o RAGInterface e retornar uma resposta.

        Args:
            question: A pergunta do usuário.
            domain: O domínio relacionado à consulta.

        Returns:
            A resposta gerada pelo RAGInterface.
        """
        try:
            result = self.rag_interface.query_llm(question, domains=["Teste"])
            return result["answer"]
        except Exception as e:
            # Logar erro e retornar uma mensagem padrão
            logging.error(f"Erro ao consultar o RAGInterface: {e}")
            return "Desculpe, houve um erro ao acessar o sistema de conhecimento."