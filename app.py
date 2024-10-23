import gradio as gr
from Chatbot.Master_Agent import master_main

class GradioInterface:
    def __init__(self):
        self.demo = gr.ChatInterface(
            master_main
        ).queue()

    def launch(self):
        self.demo.launch(server_name="0.0.0.0", server_port=7862, share=True)


def main():
    interface = GradioInterface()
    interface.launch()


if __name__ == "__main__":
    main()
