import boto3
import json
from .base_llm_client import BaseLLMClient


class AWSBedrockLLMClient(BaseLLMClient):
    def __init__(self, model_id: str, region_name: str):
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )
        self.model_id = model_id

    def chat_completion(self, message, max_tokens, stream, temperature, top_p):

        body = json.dumps({
            "inputText": message,
            "textGenerationConfig": {
                "maxTokenCount": 2048,
                "stopSequences": ["User:"],
                "temperature": 0.7,
                "topP": 0.9
            }
        })

        response = self.bedrock_runtime.invoke_model_with_response_stream(
            body=body,
            modelId=self.model_id,
            accept='application/json',
            contentType='application/json'
        )

        stream = response.get('body')
        # response_body = json.loads(response['body'].read())

        # return response_body['results'][0]['outputText']
        return stream

    # def _format_messages(self, messages):
    #     formatted_messages = []

    #     for message in messages:
    #         if message['role'] == 'system':
    #             formatted_messages.append(f"System: {message['content']}")
    #         elif message['role'] == 'user':
    #             formatted_messages.append(f"Human: {message['content']}")
    #         elif message['role'] == 'assistant':
    #             formatted_messages.append(f"Assistant: {message['content']}")
    #     return "\n".join(formatted_messages)
