import gradio as gr
from Chatbot.bedrock_chatbot import ChatBotWithBedrock
from Chatbot.abstract_chatbot import AbstractChatbot


class GradioInterface:
    """
    使用gradio.ChatInterface的界面, 调用chatbot的respond函数
    """

    def __init__(self, chatbot: AbstractChatbot):
        self.chatbot = chatbot
        self.demo = gr.ChatInterface(
            self.chatbot.master_main
        ).queue()

    def launch(self):
        self.demo.launch(share=True)


def main():
    # 使用HuggingFace模型
    # chatbot = LlamaChatBot(
    #     "meta-llama/Meta-Llama-3-8B-Instruct",
    #     token="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"
    # )

    # 使用AWS Bedrock模型
    chatbot = ChatBotWithBedrock(
        # region_name="eu-central-1",
        # model_id="amazon.titan-text-express-v1"
        region_name="us-east-1",
        model_id="meta.llama3-8b-instruct-v1:0"
    )

    interface = GradioInterface(chatbot)
    interface.launch()


if __name__ == "__main__":
    main()