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

    def respond(self, message: str, history: List[Tuple[str, str]]):

        system_message = '''You are hired as a data scientist on a new VALORANT esports team and have been tasked by the team’s general manager to support the scouting and recruitment process.
        在###之后是目标数据库中不同table的概览。
        ###
            1. Players Table

            player_id (Primary Key): VARCHAR
            handle: VARCHAR
            name: VARCHAR
            team_id: VARCHAR (Foreign Key referencing Teams)
            region: VARCHAR
            league: VARCHAR
            2. Teams Table

            team_id (Primary Key): VARCHAR
            team_name: VARCHAR (Optional field if the name is available)
            3. Maps Table

            map_id (Primary Key): INT (Auto Increment)
            map_name: VARCHAR
            4. Agents Table

            agent_id (Primary Key): INT (Auto Increment)
            player_id (Foreign Key referencing Players): VARCHAR
            map_id (Foreign Key referencing Maps): INT
            agent_name: VARCHAR
            5. Games Table

            game_id (Primary Key): INT (Auto Increment)
            agent_id (Foreign Key referencing Agents): INT
            games_win: INT
            games_count: INT
            6. Performance Table

            performance_id (Primary Key): INT (Auto Increment)
            game_id (Foreign Key referencing Games): INT
            role (attacking/defending): ENUM('attacking', 'defending')
            kills: INT
            deaths: INT
            assists: INT
            rounds_taken: INT
            rounds_win: INT
            7. SummaryPerGame Table

            summary_id (Primary Key): INT (Auto Increment)
            game_id (Foreign Key referencing Games): INT
            combat_score: FLOAT
            average_combat_score: FLOAT
            kills: FLOAT
            deaths: FLOAT
            assists: FLOAT
            plus_minus: FLOAT
            kpr (Kills per Round): FLOAT
            dpr (Deaths per Round): FLOAT
            total_damage_taken: FLOAT
            total_damage_caused: FLOAT
            average_damage_per_round: FLOAT
            average_damage_taken_per_round: FLOAT
            dddelta: FLOAT
            headshot_hit_rate: FLOAT
            8. DamageCausedPerGame Table

            damage_caused_id (Primary Key): INT (Auto Increment)
            game_id (Foreign Key referencing Games): INT
            part (Body part: BODY/HEAD/GENERAL/LEG): ENUM('BODY', 'HEAD', 'GENERAL', 'LEG')
            count: INT
            amount: FLOAT
            9. DamageReceivedPerGame Table

            damage_received_id (Primary Key): INT (Auto Increment)
            game_id (Foreign Key referencing Games): INT
            part (Body part: BODY/HEAD/GENERAL/LEG): ENUM('BODY', 'HEAD', 'GENERAL', 'LEG')
            count: INT
            amount: FLOAT
        '''
        messages = [{"role": "system", "content": system_message}]

        code_msg = '''请你根据这个示例, 给我提供SQL代码, 要求是获得"name"为"Houssein"这个选手的"KPR"数据
        你只需要为我提供可执行的SQL代码即可.

        "What recent performances or statistics justify the inclusion of *player name* in the team?


'''
        messages.append({"role": "user", "content": code_msg})
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

        response = ""
        for mes in self.llm_client.client.chat_completion(
            messages,
            max_tokens=2048,
            stream=True,
            temperature=0.7,
            top_p=0.95,
        ):
            token = mes.choices[0].delta.content
            response += token
            yield response
        print(response)

class GradioInterface:
    def __init__(self, chatbot: ChatBot):
        self.chatbot = chatbot
        self.demo = gr.ChatInterface(
            self.chatbot.respond
        ).queue()

    def launch(self):
        self.demo.launch(share=True)


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
