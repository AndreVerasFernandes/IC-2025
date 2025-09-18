class KnowledgeManagement:

    def __init__(self):
        self._definitions: dict[str, str] = {
            'DOC': 'Documento de Ordem de Crédito (DOC) é o meio usado para transações com o valor máximo de até R$ 4.999,99.',
            'TED': 'A Transferência Eletrônica Disponível (TED) é a movimentação de dinheiro entre contas sem restrição de valor.',
            'PIX': 'Criado pelo Banco Central do Brasil, o Pix é um novo meio de pagamentos que surgiu com o objetivo de simplificar e facilitar as transações bancárias. A principal diferença do Pix para o TED ou para o DOC é o fato de ser instantâneo: o dinheiro é enviado e recebido na hora, em questão de instantes.'
        }

    def get_primary_slots(self, operation: str, domain: str = 'transacional') -> list[str]:
        if operation == 'transferencia':
            return ['valor', 'pessoa', 'tipo_transferencia']
        return []

    def confirmation_demand(self, operation: str, domain: str = 'transacional') -> bool:
        return operation == 'transferencia'

    def get_label(self, element_id: str, domain: str = 'transacional') -> str:
        return element_id

    def get_definition(self, element_id: str, domain: str = 'transacional') -> str | None:
        return self._definitions.get(element_id)
