# VCTEVA
Repository for VCT Hackathon: Esports Manager Challenge

## Python Environment Setup

### 1. Conda Environment Set Up

```
conda create --name=eva python=3.10
conda activate eva
pip install -r requirements.txt
```
### 2. Download Dataset From AWS S3 Bucket

```
git clone https://github.com/Kleinpenny/VCTEVA.git
cd /VCTEVA/Data_Preprocess/
python download_dataset.py
```

### 3. Preprocess Dataset

```
cd /VCTEVA/Data_Preprocess/
python main.py
```

### 4. Run the Chatbot

```
cd /VCTEVA/Chatbot_UI/
python app.py
```

# Project Story

This project implements a flexible and extensible chatbot system that can work with different Large Language Models (LLMs) and incorporate Retrieval-Augmented Generation (RAG) capabilities. The system is designed with modularity and ease of use in mind, allowing for seamless integration of various LLM providers and easy switching between them.

## Project Components

1. **Base LLM Client (base_llm_client.py)**: 
   An abstract base class that defines the interface for all LLM clients. It ensures that all concrete implementations provide a `chat_completion` method.

2. **HuggingFace LLM Client (llm_client.py)**: 
   A concrete implementation of the BaseLLMClient for HuggingFace models. It uses the HuggingFace InferenceClient to interact with models hosted on the HuggingFace platform.

3. **AWS Bedrock LLM Client (aws_bedrock_client.py)**: 
   Another concrete implementation of the BaseLLMClient, this time for AWS Bedrock models. It uses the boto3 library to interact with AWS Bedrock services.

4. **Chatbot (chatbot.py)**: 
   The core class that handles the chat logic. It takes an LLM client as a parameter, allowing it to work with any LLM implementation that follows the BaseLLMClient interface. It also supports an optional RAG interface for enhanced context retrieval.

5. **Gradio Interface (app.py)**: 
   Sets up the user interface using Gradio, creating a chat interface that users can interact with. It initializes the chosen LLM client and the Chatbot, then launches the interface.

## Key Features

- **Modular Design**: The use of a base class for LLM clients allows for easy addition of new LLM providers without changing the core chatbot logic.
- **Flexible LLM Selection**: Users can easily switch between different LLM providers (e.g., HuggingFace, AWS Bedrock) by changing the client initialization in the main function.
- **RAG Support**: The chatbot can optionally use a Retrieval-Augmented Generation interface to enhance responses with relevant context.

## Challenges we ran into
1. 构建怎么样的数据库。