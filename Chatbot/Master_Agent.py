from typing import List, Tuple, Dict, Any
import gradio as gr
from huggingface_hub import InferenceClient
from llama3 import llama_completion
from DB_Connector import sql_connector
import pandas as pd

def message_builder(message: str, history: List[Tuple[str, str]], system_message: str):
    messages = [{"role": "system", "content": system_message}]
    for user_msg, assistant_msg in history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if assistant_msg:
            messages.append(
                {"role": "assistant", "content": assistant_msg[:20]})

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
    return llama_completion(message_builder(message, history, system_message))


def sql_agent(message: str, history: List[Tuple[str, str]]):
    system_message = '''你要根据得到的语句直接输出SQL语句, 你只能输出SQL语句, 没有任何注释。
        在###之后是你需要参考的数据库中table信息的概览。
        ###
        1. Players Table
        Column_Name	Description
        player_id	Primary key, unique identifier for each player (e.g., "109881619945257706").
        handle	Player's in-game handle (e.g., "may").
        name	Full name of the player (e.g., "Mayara Diniz").
        team_id	Foreign key to reference the player's team.
        region	Player's region (e.g., "LATAM").
        league	League associated with the player (e.g., "game-changers").

        2. Teams Table
        Column_Name	Description
        team_id	Primary key, unique identifier for each team (e.g., "107894513703662486").
        team_name	Name of the team.
        region	Team's region.

        3. Matches Table
        Column_Name	Description
        match_id	Primary key, auto-incrementing match identifier.
        league	League the match belongs to (e.g., "game-changers-2023").
        date	Date of the match.

        4. Maps Table
        Column_Name	Description
        map_id	Primary key, auto-incrementing identifier for each map.
        match_id	Foreign key to reference the match.
        map_name	Name of the map (e.g., "Canyon").

        5. Agents Table
        Column_Name	Description
        agent_id	Primary key, unique identifier for each agent (e.g., "117ED9E3-49F3-6512-3CCF-0CADA7E3823B").
        agent_name	Name or identifier of the agent.

        6. Player_Performance Table
        Column_Name	Description
        performance_id	Primary key, auto-incrementing identifier.
        player_id	Foreign key to reference the player.
        map_id	Foreign key to reference the map.
        agent_id	Foreign key to reference the agent used.
        games_win	Number of games won by the player.
        games_count	Total games played by the player on this map with this agent.
        total_kills	Total number of kills.
        total_deaths	Total number of deaths.
        total_assists	Total number of assists.
        rounds_taken	Total number of rounds played.
        rounds_win	Number of rounds won.
        combat_score	Combat score per game.
        average_combat_score	Average combat score per round.
        total_damage_taken	Total damage taken by the player.
        total_damage_caused	Total damage caused by the player.
        average_damage_per_round	Average damage caused per round.
        headshot_hit_rate	Percentage of headshot hits.

        7. Cause Table
        Column_Name	Description
        cause_id	Primary key, auto-incrementing identifier.
        performance_id	Foreign key to reference the performance record.
        cause_type	Type of cause (e.g., "ELIMINATION", "SPIKE_DEFUSE", "DETONATE").
        cause_count	Number of times this cause occurred.

        8. Damage_Details Table
        Column_Name	Description
        damage_id	Primary key, auto-incrementing identifier.
        performance_id	Foreign key to reference the performance record.
        body_part	Body part damaged (e.g., "BODY", "HEAD", "LEG").
        damage_count	Number of hits to the body part.
        damage_amount	Amount of damage caused or received.
'''
    ##得到response中的sql语句之后，直接执行，然后将得到的数据返回。(json?csv?)
    #response = llama_completion(message_builder(message, history, system_message))
    response = '''
        SELECT Tournaments.player_id, PerformanceDetails.*,Maps.map_id  FROM PerformanceDetails
        JOIN Agents ON PerformanceDetails.agent_id = Agents.agent_id
        JOIN Maps ON Agents.map_id = Maps.map_id
        JOIN Tournaments ON Maps.tournament_id = Tournaments.tournament_id
        WHERE Tournaments.player_id = '106230271915475632';
        '''
    result_df = sql_connector(response)
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
    return llama_completion(message_builder(message, history, system_message))
     

def normal_agent(message: str, history: List[Tuple[str, str]]):
    system_message = '''
    You are an AI chatbot designed to enthusiastically answer questions and provide detailed explanations to users. Your primary goal is to engage with users in a friendly, warm, and positive manner, making them feel welcome and valued. 
    '''
    return llama_completion(message_builder(message, history, system_message))


def classifier_agent(message: str, history: List[Tuple[str, str]]):
    system_message = '''
        You are a data scientist on a new VALORANT esports team.
        Complete the text classification task for the "user" query, categorizing the request into one of the items provided in the following list. 
        Your output can only be one of the items from the list: ["Team Build", "Game Infomation", "Player Info", "Others"]
        '''
    return llama_completion(message_builder(message, history, system_message))


def master_main(message: str, history: List[Tuple[str, str]]):
        
        response = classifier_agent(message, history)
        print(response)
        if 'others' in response.lower():
            return normal_agent(message, history)
        else:
            #需要使用sql语句获得信息
            additional_info = sql_agent(message, history)
            if additional_info: # not False
                message += "Answer the question based on the following infomation: "
                message += additional_info
                if "team build" in response.lower():
                    return team_builder_agent(message, history)
                else:
                    return valorant_agent(message, history)
            else:
                #说明数据库出了问题，无法获得相关信息
                return valorant_agent(message, history)
