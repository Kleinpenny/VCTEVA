from abc import ABC, abstractmethod


class RAGInterface(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> str:
        pass
