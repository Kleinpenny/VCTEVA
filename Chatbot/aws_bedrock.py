import boto3
import json

def bedrock_completion(messages: list[dict[str, str]]):

    # 初始化 bedrock 客户端
    bedrock_client = boto3.client(
        service_name='bedrock-runtime', region_name="us-east-1")
    model_id = 'meta.llama3-70b-instruct-v1:0' #'meta.llama3-70b-instruct-v1:0'
    
    # Inference parameters to use.
    #temperature = 0.7
    top_k = 0.9

    # Base inference parameters to use.
    #inference_config = {"temperature": temperature}
    # Additional inference parameters to use.
    # additional_model_fields = {"top_k": top_k}

    # Send the message.
    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        #system=system_prompts, #效果不太好
        #inferenceConfig=inference_config
        # additionalModelRequestFields=additional_model_fields
    )

    return response['output']['message']['content'][0]['text']