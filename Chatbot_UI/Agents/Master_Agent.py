from typing import List, Tuple, Dict, Any
import gradio as gr
from huggingface_hub import InferenceClient


def respond(messages: list[dict[str, str]]):
    llm_client = InferenceClient(
        "meta-llama/Meta-Llama-3-8B-Instruct", token="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")
    
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



def master_main(message: str, history: List[Tuple[str, str]]):
        system_message = '''
        You are hired as a data scientist on a new VALORANT esports team and have been tasked by the team's general manager to support the scouting and recruitment process.
        1. 如果关于组建队伍，直接回答: "team build"
        2. 如果关于VALORANT比赛, 请直接回答: "game info"
        3. 如果关于选手的信息，请直接回答: "player info"
        '''
        messages = [{"role": "system", "content": system_message}]
        
        for user_msg, assistant_msg in history:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append(
                    {"role": "assistant", "content": assistant_msg})

        messages.append({"role": "user", "content": message})
        response = respond(messages)
        if "team build" in response.lower():
             print("好耶")

        return response
