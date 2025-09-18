from abc import ABC, abstractmethod
from model.action import Action


class ResponseGenerator(ABC):

    @classmethod
    @abstractmethod
    def generate(cls, action: Action) -> str:
        pass

    @classmethod
    def _create_list(cls, items: list[str]) -> str:
        s = ', '.join(items[:-1])
        s += ' e ' + items[-1]
        return s
