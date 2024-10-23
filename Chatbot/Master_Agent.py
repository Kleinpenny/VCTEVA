from typing import List, Tuple, Dict, Any
import pandas as pd
import mysql.connector
import pandas as pd
from mysql.connector import Error
from llm.llama3 import llama_completion
from llm.aws_bedrock import bedrock_completion


def message_builder(system_prompt: str, message: str, history: List[Tuple[str, str]]):
    messages = []
    for user_msg, assistant_msg in history:
        if user_msg:
            user_msg = [{"text": user_msg}]
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            assistant_msg = [{"text": assistant_msg}]
            messages.append({"role": "assistant", "content": assistant_msg})

    message = [{"text": system_prompt + "### Based on the requirements above, respond to the following words: "+ message}]
    messages.append({"role": "user", "content": message})
    return messages


def valorant_agent(message: str, history: List[Tuple[str, str]]):
    system_message = '''
    You are a Valorant esports expert skilled in analyzing player performances and competition-related issues based on provided information.
    Your objectives:
    ###
    Provide professional and detailed answers to questions about player performances, game strategies, and match outcomes.
    Explain complex concepts clearly, making game mechanics, tactics, and player data easy to understand.
    Use a friendly yet professional tone to engage users warmly while maintaining expertise.
    Encourage interaction, welcoming further questions and guiding discussions to enhance users' understanding and interest in esports.
    ###
    Your responses should help users gain deeper insights into all aspects of Valorant esports. Leverage your professional knowledge and enthusiasm to help users better appreciate and understand the allure of Valorant esports.
    '''

    response = bedrock_completion(message_builder(system_message, message, history))
    return response

def ensure_sql_execute(system_message, message, response, retry):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="vct",
        password="vcteva_2024",
        database="VCTEVA",
        )
        cursor = connection.cursor()
        cursor.execute(response)
        column_names = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        result_df = pd.DataFrame(result, columns=column_names)
        cursor.close()
        connection.close()
        #可执行的SQL语句: 
        print(response)
        return result_df
    
    except Exception as e:
        retry += 1
        if retry <= 3:
            messages = []
            error_msg = f"An error occurred: {e}"
            correction_instruction = [{"text": response + "The above SQL code executes with the following problem:  " + error_msg + "Please rewrite the SQL code according to the error message. You need to follow the requests of the users listed below when making changes. : #" + message + "#" + system_message}]
            messages.append({"role": "user", "content": correction_instruction})
            response = bedrock_completion(messages)
            print(messages)
            print(response)
            return ensure_sql_execute(system_message, message, response, retry)
        else:
            return False #重试超过三次就直接返回False


def sql_agent(message: str, history: List[Tuple[str, str]]):
    system_message = '''You have to output SQL statements directly based on the statements you get, you can only output SQL statements without any comments.
        After the #### is an overview of the tables in the database you need to refer to.
        ###
        1. Players
        Column_Name:	Description
        player_id:	Primary key, unique identifier for each player (e.g., "109881619945257706").
        handle:	Player's in-game handle (e.g., "may").
        name:	Full name of the player (e.g., "Mayara Diniz").
        team_id:	Foreign key to reference the player's team.
        region:	Player's region (e.g., "LATAM").
        league:	League associated with the player (e.g., "game-changers").

        2. Tournaments
        Column_Name:	Description
        tournament_id:	Primary key, unique identifier for each tournament.
        player_id:	Foreign key, references the Players table.
        tournament_name:	Name of the tournament.

        3. Agents
        Column_Name:	Description
        agent_id:	Primary key, unique identifier for each agent (agent is the game character).
        map_id:	Foreign key, references the Maps table.
        games_win:	Number of games won by the agent in this map.
        games_count: 	Total number of games played by the agent in this map.

        4. Maps 
        Column_Name:	Description
        map_id:	Primary key, unique identifier for each map.
        tournament_id:	Foreign key, references the Tournaments table.
        map_name:	Name of the map (e.g., "Canyon").

        5. PerformanceDetails
        Column_Name:	Description
        performance_id:	Primary key, unique identifier for each performance record.
        agent_id:	Foreign key, references the Agents table.
        mode:	Mode of the game ("attacking" or "defending").
        kills:	Number of kills made by the player in this performance.
        deaths:	Number of deaths in the performance.
        assists:	Number of assists in the performance.
        rounds_taken:	Total number of rounds played.
        rounds_win:	Total number of rounds won by the player.
        cause:	JSON object storing details about the cause of certain events (e.g., {"SPIKE_DEFUSE": 9,"ELIMINATION": 32,"DETONATE": 2}).

        6. Summary
        Column_Name:	Description
        summary_id:	Primary key, unique identifier for summary.
        agent_id:	Foreign key, references the Agents table.
        combat_score:	Total combat score.
        average_combat_score:	Average combat score per round.
        kills:	Number of kills.
        deaths:	Number of deaths.
        assists:	Number of assists.
        kpr:	Kill-per-round ratio.
        dpr:	Death-per-round ratio.
        total_damage_taken:	Total damage taken by the player.
        total_damage_caused:	Total damage caused by the player.
        average_damage_per_round:	Average damage caused per round.
        average_damage_taken_per_round:	Average damage taken per round.
        ddelta:	Damage delta (difference between damage taken and caused).
        headshot_hit_rate:	Percentage of hits that were headshots.

        7. DamageDetails 
        Column_Name:	Description
        damage_id:	Primary key, unique identifier for each damage record.
        agent_id:	Foreign key, references the Agents table.
        type:	Type of damage (e.g., "Head", "Body", "LEG", "GENERAL").
        head_count:	Number of hits to the head.
        body_count:	Number of hits to the body.
        leg_count:	Number of hits to the legs.
        general_count:	General count of all hits.
        head_amount:	Total damage caused to the head.
        body_amount:	Total damage caused to the body.
        leg_amount:	Total damage caused to the legs.
        general_amount:	General amount of all damage caused.
'''

    ##得到response中的sql语句之后，直接执行，然后将得到的数据返回。(json_to_str)
    response = bedrock_completion(message_builder(system_message, message, history))
    result_df = ensure_sql_execute(system_message, message, response, 0)
    print(result_df)

    if isinstance(result_df, pd.DataFrame): # 不管得到的数据是空与否
        df_json_string = result_df.to_json(orient='records', force_ascii=False)
        print(df_json_string)
        return df_json_string
    else:
        print("Check Database Status!")
        return False
    

def team_builder_agent(message: str, history: List[Tuple[str, str]]):
    system_message = '''
        You are a manager of a Valorant esports team, tasked with selecting the five best-performing players from the available data to form the strongest team. When assembling the team, you need to adhere to the following requirements:
        ###
        1. For each team composition:
        Analyze Player Performance, Answer questions about players' performances with specific agents (playable characters in the game), providing data support and specific examples.
        2. Assign Roles to Players and Explain Their Contributions:
        Indicate each player's position in the team—whether they lean towards offense or defense—and explain the reasons.
        3. Assign a Team Leader: 
        Select one player as the team's in-game leader (IGL), responsible for primary strategy and shot-calling, and explain your reasoning for choosing them.
        4. Provide Insights on Team Strategy:
        Strategic Analysis: Elaborate on the team's overall strategy and how to leverage each player's strengths to achieve victory.
        Strengths and Weaknesses: Predict and analyze the team's potential strengths and weaknesses, and offer suggestions for improvement.
        ###
        In your responses, please provide detailed explanations and analyses to ensure the strategy is reasonable and competitive. Your goal is to maximize team synergy, creating a top-tier team with balanced offense and defense and excellent teamwork.
    '''
    response = bedrock_completion(message_builder(system_message, message, history))
    return response


def normal_agent(message: str, history: List[Tuple[str, str]]):
    system_message = '''
    You are an AI chatbot designed to enthusiastically answer questions and provide detailed explanations to users. 
    Your primary goal is to engage with users in a friendly, warm, and positive manner, making them feel welcome and valued.
    Responses don't include any emoji. 
    '''
    response = bedrock_completion(message_builder(system_message, message, history))
    return response


def classifier_agent(message: str, history: List[Tuple[str, str]]):
    system_message = '''
    You are a data scientist on a new VALORANT esports team.
    Complete the text classification task for the "user" query, categorizing the request into one of the items provided in the following list. 
    Your output can only be one of the items from the list: ["Team Build", "Game Information", "Player Info", "Others"]
    '''
    response = bedrock_completion(message_builder(system_message, message, history))
    return response


def master_main(message: str, history: List[Tuple[str, str]]):
    response = classifier_agent(message, history)
    print(response)
    if 'others' in response.lower():
        return normal_agent(message, history)
    else:
        additional_info = sql_agent(message, history)
        if additional_info:
            message += "根据以下信息回答问题: "
            message += additional_info
            if "team build" in response.lower():
                return team_builder_agent(message, history)
            else:
                return valorant_agent(message, history)
        else:
            print("无法获取相关信息，可能是数据库问题")
            return valorant_agent(message, history)

