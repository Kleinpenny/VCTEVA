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
#### Processed data stored in /DATA/all.players.json

### 4. Install MYSQL in Linux

```bash
apt-get install mysql-server
apt-get install mysql-client
apt-get install libmysqlclient-dev
```

### 5. Configure MySQL
```bash
mysql -u root -p
```
When using MySQL for the first time, there is no password set, so just press Enter.

```mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'vcteva_2024';
FLUSH PRIVILEGES;
```

<details>
  <summary>OPTIONAL(or if you encounter login issues)</summary>

- If you need more users, you can create an account like 'admin' and set a password for it:

````mysql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'PASSWORD';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
````

- If you forget the password for the `root` or `admin` user，you can try the following steps to reset it:
  -  First, stop the MySQL service:
     ```bash
     sudo systemctl stop mysql
     ```
  - Then start MySQL in skip-grant-tables mode:
     ```bash
     sudo mysqld_safe --skip-grant-tables &
     ```
  - Log in to MySQL again, this time without a password:
    ```bash
    mysql -u root
    ```
    
  - Once logged in, reset the password for the `admin` or `root` user:
    ```mysql
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
    FLUSH PRIVILEGES;
    ```
  - Finally, restart the MySQL service:
    ```bash
    sudo systemctl start mysql
    ```
</details>

### 6. Create database and tables
```mysql
Create database VCTEVA;
exit;
mysql -u root -p VCTEVA < VCTEVA/Data_Preprocess/Database/VCTEVA_backup.sql
cd VCTEVA/Data_Preprocess/Database
python db_test.py
```
<details>
  <summary>OPTIONAL(Delete the database)</summary>

```mysql
SET FOREIGN_KEY_CHECKS = 0;
Use VCTEVA;
DELETE FROM PerformanceDetails;
DELETE FROM Summary;
DELETE FROM Agents;
DELETE FROM Maps;
DELETE FROM Tournaments;
DELETE FROM Players;
DELETE FROM DamageDetails;

SET FOREIGN_KEY_CHECKS = 1;
```
</details>

### 7. Configure AWS Bedrock and LLM Client

1. Install AWS CLI
Install the AWS CLI following the (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. Create an IAM User
In the AWS console under the IAM service, create a new user and obtain the access credentials (Access Key ID and Secret Access Key) for this user.

3. Configure AWS CLI
Open the terminal and run the following command:
   ```
   aws configure
   ```
   Follow the prompts to input your AWS credential information.

4. Verify Credentials
Run the following command to verify if your AWS credentials are correctly configured:
   ```
   aws sts get-caller-identity
   ```
   If the credentials are valid, you will see an output similar to the following:
   ```json
   {
       "UserId": "AIDAI...",
       "Account": "123456789012",
       "Arn": "arn:aws:iam::123456789012:user/username"
   }
   ```
   If the credentials are invalid, you will receive an error message.

After completing these steps, you can use the AWS Bedrock service and the selected LLM client.

### 8. Run the Chatbot

```
python app.py
```

# Project Story

This project implements a flexible and extensible chatbot system that can work with different Large Language Models (LLMs) and incorporate Retrieval-Augmented Generation (RAG) capabilities. The system is designed with modularity and ease of use in mind, allowing for seamless integration of various LLM providers and easy switching between them.
## System Workflow


The following flowchart shows how our chatbot system processes user input and generates responses:

```mermaid
flowchart TD
    A[User Input] -->|Message| B[Chatbot - master_main]
    B --> C[queryclassifier - Classifier Agent]
    C -->|Classifier: others| D[Normal Agent]
    C -->|Classifier: SQL Query| E[SQL Agent]
    
    subgraph " "
        E[SQL Agent]
        F[Team Builder Agent]
        G[Valorant Player Agent]
    end

    E --> G
    E --> F
    D --> H[Return Response]
    F --> H
    G --> H

```

This flowchart illustrates how user input is processed through different agents and decision points to generate the appropriate response.



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
2. ![alt text](image.png)
