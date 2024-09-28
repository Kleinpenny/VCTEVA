import sys
from torch import cuda, bfloat16
import torch
import transformers
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
from time import time
from langchain.llms import HuggingFacePipeline
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

model_id = "meta-llama/Meta-Llama-3-8B"
time_start = time()
model_config = AutoConfig.from_pretrained(
   model_id,
    trust_remote_code=True,
)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    device_map='auto',
)
tokenizer = AutoTokenizer.from_pretrained(model_id)
time_end = time()
print(f"Prepare model, tokenizer: {round(time_end-time_start, 3)} sec.")

time_start = time()
query_pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        max_length=1024,
        device_map="auto",)
time_end = time()
print(f"Prepare pipeline: {round(time_end-time_start, 3)} sec.")

llm = HuggingFacePipeline(pipeline=query_pipeline)

# checking again that everything is working fine
time_start = time()
question = "Please explain what EU AI Act is."
response = llm(prompt=question)
time_end = time()
total_time = f"{round(time_end-time_start, 3)} sec."
full_response =  f"Question: {question}\nAnswer: {response}\nTotal time: {total_time}"
print(full_response)