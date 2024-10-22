from huggingface_hub import InferenceClient


def llama_completion(messages: list[dict[str, str]]):
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

    # max_gen_len = 128
    # temperature = 0.1
    # top_p = 0.9

    # # Create request body.
    # body = json.dumps({
    #     "prompt": prompt,
    #     "max_gen_len": max_gen_len,
    #     "temperature": temperature,
    #     "top_p": top_p
    # })

    # bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-east-1")
    # response = bedrock.invoke_model(
    #     body=body, modelId=model_id)

    # response_body = json.loads(response.get('body').read())

    # response_body

    # return response_body
    return response
