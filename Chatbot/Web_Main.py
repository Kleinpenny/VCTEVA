from typing import List, Tuple, Dict, Any
import gradio as gr
import os,sys
from huggingface_hub import InferenceClient
from Agents.Master_Agent import master_main

class GradioInterface:
    def __init__(self):
        self.demo = gr.ChatInterface(
            master_main
        ).queue()

    def launch(self):
        self.demo.launch(share=True)


def main():
    interface = GradioInterface()
    interface.launch()


if __name__ == "__main__":
    main()
