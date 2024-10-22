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

### 5. 配置mysql
```bash
mysql -u root -p
```
初次使用mysql，没有设置密码，因此直接回车即可

```mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'vcteva_2024';
FLUSH PRIVILEGES;
```

<details>
  <summary>OPTIONAL(或者遇到登陆问题)</summary>

- 若需要更多用户，可以创建例如: ‘admin’ 账户并为其设置密码：

````mysql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'PASSWORD';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
````

- 如果你忘记了 `root` 或 `admin` 用户的密码，可以尝试以下步骤来重置密码：
  -  首先停止 MySQL 服务：
     ```bash
     sudo systemctl stop mysql
     ```
  - 然后以跳过权限表的模式启动 MySQL：
     ```bash
     sudo mysqld_safe --skip-grant-tables &
     ```
  - 再次登录 MySQL，此时不需要密码：
    ```bash
    mysql -u root
    ```
  - 登录成功后，重置 `admin` 或 `root` 用户的密码：
    ```mysql
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
    FLUSH PRIVILEGES;
    ```
  - 最后，重启 MySQL 服务：
    ```bash
    sudo systemctl start mysql
    ```
</details>

### 6. 创建database以及创建TABLES
```mysql
Create database VCTEVA;
exit;
mysql -u root -p VCTEVA < VCTEVA/Data_Preprocess/Database/VCTEVA_backup.sql
cd VCTEVA/Data_Preprocess/Database
python db_test.py
```
<details>
  <summary>OPTIONAL(删除数据库)</summary>

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

### 7. 设置AWS Bedrock和LLM客户端

1. 安装AWS CLI
   根据[AWS CLI安装指南](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)安装AWS CLI。

2. 创建IAM用户
   在AWS控制台的IAM服务中创建一个新用户，并获取该用户的访问凭证（Access Key ID和Secret Access Key）。

3. 配置AWS CLI
   打开终端，运行以下命令：
   ```
   aws configure
   ```
   按照提示输入您的AWS凭证信息。

4. 验证凭证
   运行以下命令验证您的AWS凭证是否正确配置：
   ```
   aws sts get-caller-identity
   ```
   如果凭证有效，您将看到类似以下的输出：
   ```json
   {
       "UserId": "AIDAI...",
       "Account": "123456789012",
       "Arn": "arn:aws:iam::123456789012:user/username"
   }
   ```
   如果凭证无效，您将收到错误消息。

完成以上步骤后，您就可以使用AWS Bedrock服务和选定的LLM客户端了。

### 8. Run the Chatbot

```
python app.py
```

# Project Story

This project implements a flexible and extensible chatbot system that can work with different Large Language Models (LLMs) and incorporate Retrieval-Augmented Generation (RAG) capabilities. The system is designed with modularity and ease of use in mind, allowing for seamless integration of various LLM providers and easy switching between them.
## 系统工作流程

以下流程图展示了我们的聊天机器人系统如何处理用户输入并生成响应：

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

这个流程图展示了用户输入如何通过不同的代理和决策点进行处理，最终生成适当的响应。



## 系统工作流程

以下流程图展示了我们的聊天机器人系统如何处理用户输入并生成响应：

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

这个流程图展示了用户输入如何通过不同的代理和决策点进行处理，最终生成适当的响应。


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