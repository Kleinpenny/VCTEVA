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
        
    return response