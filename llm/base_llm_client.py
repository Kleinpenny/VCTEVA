from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    @abstractmethod
    def chat_completion(self, messages, max_tokens, stream, temperature, top_p):
        pass
