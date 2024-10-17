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

    def chat_completion(self, messages, max_tokens, stream, temperature, top_p):
        prompt = self._format_messages(messages)
        
        response = self.bedrock_runtime.invoke_model(
            modelId=self.model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'inputText': prompt,
                'textGenerationConfig': {
                    'maxTokenCount': max_tokens,
                    'temperature': temperature,
                    'topP': top_p
                }
            })
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['results'][0]['outputText']

    def _format_messages(self, messages):
        formatted_messages = []
        for message in messages:
            if message['role'] == 'system':
                formatted_messages.append(f"System: {message['content']}")
            elif message['role'] == 'user':
                formatted_messages.append(f"Human: {message['content']}")
            elif message['role'] == 'assistant':
                formatted_messages.append(f"Assistant: {message['content']}")
        return "\n".join(formatted_messages)
