import logging
import spacy
import nltk
from unidecode import unidecode
from model.question import Question
from model.intent import Intent
from model.semantic_document import SemanticDocument
from model.semantic_token import SemanticToken
from model.input_message import InputMessage

nltk.download('punkt_tab')

log = logging.getLogger(__name__)


class NLU:
    """
    Classe responsável por realizar o processamento de linguagem natural (NLU) de mensagens,
    incluindo classificação de intenções, operações, perguntas (inclusive sua dependência e complexidade), e entidades.
    """

    def process(self, message: InputMessage) -> SemanticDocument:
        """
        Processa a mensagem de entrada e classifica seus componentes semânticos.

        Args:
            message (InputMessage): Mensagem de entrada do usuário.

        Returns:
            SemanticDocument: Documento semântico contendo as classificações da mensagem.
        """
        text = message.message
        domain = message.domain
        document = SemanticDocument()
        document.sentences = self._pre_process(text)
        document.intents = self._classify_intents(document, domain)
        document.operations = self._classify_operations(document, domain)
        document.questions = self._classify_questions(document, domain)
        document.entities = self._ner(document, domain)
        document.domain = domain
        return document

    def _pre_process(self, text: str) -> list[list[SemanticToken]]:
        """
        Pré-processa o texto normalizando e tokenizando em sentenças e palavras usando a biblioteca NLTK.

        Args:
            text (str): Texto a ser pré-processado.

        Returns:
            list[list[SemanticToken]]: Lista de sentenças tokenizadas.
        """
        sentences = []
        normalized_text = unidecode(text.lower())

        for sentence in nltk.sent_tokenize(normalized_text, language='portuguese'):
            tokens = []
            pipeline = spacy.blank('pt')

            for token in pipeline(sentence, disable=['parser', 'ner', 'textcat']):
                semantic_token = SemanticToken(token.text, token.pos_)
                tokens.append(semantic_token)

            sentences.append(tokens)

        return sentences

    def _classify_intents(self, document: SemanticDocument, domain: str = 'transacional') -> list[Intent]:
        """
        Classifica as intenções em um documento semântico dentro de um domínio específico.

        Args:
            document (SemanticDocument): Documento contendo as sentenças processadas.
            domain (str): Domínio para classificação (default é 'transacional').

        Returns:
            list[Intent]: Lista de intenções identificadas.
        """
        intents = []
        for sentence in document.get_sentences():
            if sentence.startswith('ola') or sentence.startswith('bom'):
                intents.append(Intent.SAUDACAO)
            elif sentence.startswith('tchau'):
                intents.append(Intent.DESPEDIDA)
            elif sentence.startswith('qual'):
                intents.append(Intent.REALIZAR)
            elif sentence.startswith('o que'):
                intents.append(Intent.INFORMAR)
            else:
                intents.append(None)
                log.warning('Nenhuma intenção classificada')
        return intents

    def _classify_operations(self, document: SemanticDocument, domain: str = 'transacional') -> list[str]:
        """
        Classifica as operações em um documento semântico dentro de um domínio específico.

        Args:
            document (SemanticDocument): Documento contendo as sentenças processadas.
            domain (str): Domínio para classificação (default é 'transacional').

        Returns:
            list[str]: Lista de operações identificadas.
        """
        operations = []
        for sentence in document.get_sentences():
            if sentence.startswith('qual'):
                operations.append('consulta_de_saldo')
            else:
                operations.append(None)
        return operations

    def _classify_questions(self, document: SemanticDocument, domain: str = 'transacional') -> list[Question]:
        """
        Classifica as perguntas em um documento semântico dentro de um domínio específico.

        Args:
            document (SemanticDocument): Documento contendo as sentenças processadas.
            domain (str): Domínio para classificação (default é 'transacional').

        Returns:
            list[Question]: Lista de perguntas identificadas.
        """
        questions = []
        for sentence in document.get_sentences():
            if sentence.startswith('o que'):
                questions.append(Question.O_QUE)
            else:
                questions.append(None)
        return questions

    def _ner(self, document: SemanticDocument, domain: str = 'transacional') -> list[tuple[str, str]]:
        """
        Extrai entidades nomeadas em um documento semântico dentro de um domínio específico.

        Args:
            document (SemanticDocument): Documento contendo as sentenças processadas.
            domain (str): Domínio para classificação (default é 'transacional').

        Returns:
            list[tuple[str, str]]: Lista de entidades nomeadas e seus tipos.
        """
        entities = []
        for sentence in document.get_sentences():
            words = nltk.word_tokenize(sentence, language='portuguese')
            if 'ted' in words:
                entities.append(('TED', 'tipo_transferencia'))
            if 'doc' in words:
                entities.append(('DOC', 'tipo_transferencia'))
            if 'pix' in words:
                entities.append(('PIX', 'tipo_transferencia'))
        return entities
