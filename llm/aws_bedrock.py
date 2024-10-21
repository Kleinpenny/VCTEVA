import boto3
import json

def bedrock_completion(messages: list[dict[str, str]]):
    bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name="eu-central-1" # 请根据您的AWS配置更改区域
        )
    model_id = "amazon.titan-text-express-v1"
    
    body = json.dumps({
        "inputText": messages,
        "textGenerationConfig": {
            "maxTokenCount": 2048,
            "stopSequences": ["User:"],
            "temperature": 0.7,
            "topP": 0.9
        }
    })

    response = bedrock_client.invoke_model_with_response_stream(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )

    stream = response.get('body')
    # response_body = json.loads(response['body'].read())

    # return response_body['results'][0]['outputText']
    return stream