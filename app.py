from typing import List, Tuple, Dict, Any
from abc import ABC, abstractmethod
import gradio as gr
from huggingface_hub import InferenceClient


class RAGInterface(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> str:
        pass


class LLMClient:
    def __init__(self, model_name: str, token: str):
        self.client = InferenceClient(model_name, token=token)

    def generate(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float, top_p: float) -> str:
        response = ""
        for message in self.client.chat_completion(
            messages,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        ):
            token = message.choices[0].delta.content
            response += token
        return response


class ChatBot:
    """
    A chatbot class that interacts with a language model client (LLMClient) and optionally a 
    retrieval-augmented generation (RAG) interface to generate responses based on user input 
    and conversation history.

    Attributes:
        llm_client (LLMClient): The language model client used to generate responses.
        rag (RAGInterface, optional): The retrieval-augmented generation interface used to 
                                      retrieve context for the input message.

    Methods:
        respond(message: str, history: List[Tuple[str, str]], system_message: str, 
            Generates a response to the input message based on the conversation history and 
            system message. If a RAG interface is provided, it retrieves context for the 
            input message before generating the response.
    """

    def __init__(self, llm_client: LLMClient, rag: RAGInterface = None):
        self.llm_client = llm_client
        self.rag = rag

    def respond(self, message: str, history: List[Tuple[str, str]], system_message: str,
                max_tokens: int, temperature: float, top_p: float) -> str:
        messages = [{"role": "system", "content": system_message}]

        for user_msg, assistant_msg in history:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append(
                    {"role": "assistant", "content": assistant_msg})

        if self.rag:
            context = self.rag.retrieve(message)
            message = f"Context: {context}\n\nQuestion: {message}"

        messages.append({"role": "user", "content": message})

        return self.llm_client.generate(messages, max_tokens, temperature, top_p)


class GradioInterface:
    def __init__(self, chatbot: ChatBot):
        self.chatbot = chatbot
        self.demo = gr.ChatInterface(
            self.chatbot.respond,
            additional_inputs=[
                gr.Textbox(
                    value="You are a helpful chatbot answers any question in details. Give any answer within 50 words without any emoji!", label="System message"),
                gr.Slider(minimum=1, maximum=2048, value=512,
                          step=1, label="Max new tokens"),
                gr.Slider(minimum=0.1, maximum=4.0, value=0.7,
                          step=0.1, label="Temperature"),
                gr.Slider(minimum=0.1, maximum=1.0, value=0.95,
                          step=0.05, label="Top-p"),
            ],
        )

    def launch(self):
        self.demo.launch()


def main():
    llm_client = LLMClient(
        "meta-llama/Meta-Llama-3-8B-Instruct", token="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")

    chatbot = ChatBot(llm_client)
    # extends the chatbot to use RAG
    # chatbot = ChatBot(llm_client, rag=RAGInterface())

    interface = GradioInterface(chatbot)
    interface.launch()


if __name__ == "__main__":
    main()
