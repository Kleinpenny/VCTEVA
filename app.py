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
    hf_client = HuggingFaceLLMClient(
        "meta-llama/Meta-Llama-3-8B-Instruct",
        token="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"
    )
    hf_chatbot = ChatBot(hf_client)

    # 使用AWS Bedrock模型
    # aws_client = AWSBedrockLLMClient(
    #     model_id="amazon.titan-text-express-v1",
    #     region_name="us-west-2"  # 请根据您的AWS配置更改区域
    # )
    # aws_chatbot = ChatBot(aws_client)

    # 选择要使用的chatbot
    chatbot = hf_chatbot  # 或 aws_chatbot

    interface = GradioInterface(chatbot)
    interface.launch()


if __name__ == "__main__":
    main()
