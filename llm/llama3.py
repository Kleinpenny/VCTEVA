from huggingface_hub import InferenceClient
from .base_llm_client import BaseLLMClient


class HuggingFaceLLMClient(BaseLLMClient):
    def __init__(self, model_name: str, token: str):
        self.client = InferenceClient(model_name, token=token)

    def chat_completion(self, messages, max_tokens, stream, temperature, top_p):
        return self.client.chat_completion(
            messages,
            max_tokens=max_tokens,
            stream=stream,
            temperature=temperature,
            top_p=top_p,
        )
