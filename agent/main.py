# agent.py
import logging
from model.input_message import InputMessage
from module.UCGemini import UserConnection
from module.NLUGemini import NLU
from module.km import KnowledgeManagement
from module.bt import BeliefTracker
from module.policy import Policy
from module.nlg import NLG
from model.semantic_document import SemanticDocument

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Agent:
    def __init__(self, llm=True):
        self.nlu = NLU()
        self.km = KnowledgeManagement()
        self.bt = BeliefTracker(self.km)
        self.policy = Policy(self.bt, self.km)
        self.nlg = NLG(llm)
        self.user_connection = UserConnection(use_llm=llm)

    def chat(self, user: str, text: str) -> list[str]:
        message = InputMessage(message=text, user=user)
        filter_result = self.user_connection.filter_input(message.message)

        if not filter_result.valid:
            return ['Não posso responder essa sua mensagem']

        semantic_doc = self.nlu.process(message)
        analysis = semantic_doc.get("analysis", {})

        if not analysis.get('intents'):
            return ['Não posso responder essa sua mensagem']

        semantic_doc_obj = SemanticDocument(
            intents=analysis.get("intents", []),
            operations=analysis.get("operations", []),
            questions=analysis.get("questions", []),
            entities=analysis.get("entities", []),
            sentiment=analysis.get("sentiment", ""),
            domain=analysis.get("domain", ""),
            dependent=analysis.get("dependent", False),
            out_of_context=False
        )

        states = self.bt.update_state(semantic_doc_obj)
        if not states:
            return ['Não posso responder essa sua mensagem']

        actions = self.policy.act(user, states)

        responses = []
        for action in actions:
            response = self.nlg.generate(action)
            if response:
                if not self.user_connection.filter_output(response):
                    response = 'Opa, não posso responder essa mensagem'
                responses.append(response)

        return responses
