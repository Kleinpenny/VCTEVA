from huggingface_hub import InferenceClient
from .abstract_chatbot import AbstractChatbot


class LlamaChatBot(AbstractChatbot):
    def __init__(self, model_name: str, token: str):
        self.client = InferenceClient(model_name, token=token)

    def respond(self, user_input: str) -> str:
        response = ""
        for mes in llm_client.chat_completion(
            messages,
            max_tokens=2048,
            stream=True,
            temperature=0.7,
            top_p=0.95,
        ):
            token = mes.choices[0].delta.content
            response += token

        return response
