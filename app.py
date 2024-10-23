import gradio as gr
from llm.chatbot import ChatBot
from llm.hf_llm_client import HuggingFaceLLMClient
from llm.aws_bedrock_client import AWSBedrockLLMClient


class GradioInterface:
    def __init__(self, chatbot: ChatBot):
        self.chatbot = chatbot
        self.demo = gr.ChatInterface(
            self.chatbot.respond
        ).queue()

    def launch(self):
        self.demo.launch(share=True)


def main():
    # 使用HuggingFace模型
    # llm_client = HuggingFaceLLMClient(
    #     "meta-llama/Meta-Llama-3-8B-Instruct",
    #     token="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"
    # )

    # 使用AWS Bedrock模型
    llm_client = AWSBedrockLLMClient(
        model_id="amazon.titan-text-express-v1",
        region_name="eu-central-1"  # 请根据您的AWS配置更改区域
    )

    chatbot = ChatBot(llm_client)
    interface = GradioInterface(chatbot)
    interface.launch()


if __name__ == "__main__":
    main()
