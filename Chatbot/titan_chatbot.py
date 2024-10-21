import boto3
import json
import pandas as pd
from typing import List, Tuple
from .abstract_chatbot import AbstractChatbot
from .DB_Connector import sql_connector


class TitanChatBot(AbstractChatbot):
    def __init__(self, region_name: str = "eu-central-1", model_id: str = "amazon.titan-text-express-v1"):
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )
        self.model_id = model_id

    def respond(self, messages: List[str]) -> str:
        # 将messages列表转换为单个字符串
        user_input = "\n".join(messages)

        body = json.dumps({
            "inputText": user_input,
            "textGenerationConfig": {
                "maxTokenCount": 2048,
                "stopSequences": ["User:"],
                "temperature": 0.7,
                "topP": 0.95
            }
        })

        response = self.bedrock_client.invoke_model(
            body=body,
            modelId=self.model_id,
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response['body'].read())
        return response_body['results'][0]['outputText']

    def message_builder(self, message: str, history: List[Tuple[str, str]], system_message: str):
        # TODO: 需要修改
        messages = f"User: {message}\n{system_message}"

        return message

    def valorant_agent(self, message: str, history: List[Tuple[str, str]]):
        return self.respond(self.message_builder(message, history, self.VALORANT_AGENT_SYSTEM_MESSAGE))

    def sql_agent(self, message: str, history: List[Tuple[str, str]]):
        response = self.respond(json.dumps(self.message_builder(
            message, history, self.SQL_AGENT_SYSTEM_MESSAGE)))
        result_df = sql_connector(response)
        if isinstance(result_df, pd.DataFrame):
            df_json_string = result_df.to_json(
                orient='records', force_ascii=False)
            print(df_json_string)
            return df_json_string
        else:
            print("Check Database Status!")
            return False

    def team_builder_agent(self, message: str, history: List[Tuple[str, str]]):
        return self.respond(self.message_builder(message, history, self.TEAM_BUILDER_SYSTEM_MESSAGE))

    def normal_agent(self, message: str, history: List[Tuple[str, str]]):
        return self.respond(self.message_builder(message, history, self.NORMAL_AGENT_SYSTEM_MESSAGE))

    def classifier_agent(self, message: str, history: List[Tuple[str, str]]):
        messages = f"""You are a data scientist working for a VALORANT esports team. Below are examples of previous query classifications. Classify the provided user's query into one of the categories ['Team Build', 'Game Information', 'Player Info', 'Others'].
        <example>
            <user_query>How can I improve my aim in-game?</user_query>
            <category>Game Information</category>
        </example>
        <example>
            <user_query>What is the best composition for our team against aggressive opponents?</user_query>
            <category>Team Build</category>
        </example>
        <example>
            <user_query>Can you tell me about the stats of our top player?</user_query>
            <category>Player Info</category>
        </example>
        <example>
            <user_query>What is the weather in Berlin?</user_query>
            <category>Others</category>
        </example>
        Now your turn to classify the following user's query, Please provide only the category name as the response, without any additional explanation: {message}
        """
        return self.respond(json.dumps(self.message_builder(message, history, messages)))

    def master_main(self, message: str, history: List[Tuple[str, str]]):
        # 将message和history转换为messages列表
        messages = [msg for msg, _ in history] + [message]

        # response = self.classifier_agent(messages, [])
        # print(response)

        # if 'others' in response.lower():
        #     # if True:
        #     return self.normal_agent(messages, [])
        # else:
        #     additional_info = self.sql_agent(messages, [])
        #     if additional_info:
        #         messages.append(
        #             "Answer the question based on the following information: " + additional_info)
        #         if "team build" in response.lower():
        #             return self.team_builder_agent(messages, [])
        #         else:
        #             return self.valorant_agent(messages, [])
        #     else:
        #         return self.valorant_agent(messages, [])
        return self.valorant_agent(messages, [])
