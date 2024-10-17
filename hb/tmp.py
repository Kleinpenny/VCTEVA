import boto3
import json
brt = boto3.client(service_name='bedrock-runtime')

body = json.dumps({
    "inputText": "hi, how are you?\n",
    "textGenerationConfig": {
        "maxTokenCount": 2048,
        "stopSequences": ["User:"],
        "temperature": 0,
        "topP": 0.9
    }
})

modelId = 'amazon.titan-text-express-v1'
accept = 'application/json'
contentType = 'application/json'

response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())

output_text = response_body['results'][0]['outputText']

output_text