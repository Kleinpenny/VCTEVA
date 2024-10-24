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

    message = [{"text": system_prompt + "### Based on the requirements above, respond to the following qeury: "+ message}]
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
        user="root",
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
        if retry <= 1:
            messages = []
            error_msg = f"An error occurred: {e}"
            correction_instruction = [{"text": response + "The above SQL code executes with the following problem:  " + error_msg + "Please rewrite the SQL code according to the error message. You need to follow the requests of the users listed below when making changes. : #" + message + "#" + system_message}]
            messages.append({"role": "user", "content": correction_instruction})
            response = bedrock_completion(messages)
            print(messages)
            print(response)
            return ensure_sql_execute(system_message, message, response, retry)
        else:
            return False #重试超过1次就直接返回False


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
        tournament_name:	Name of the tournament. Only one of items list below: ["game-changers-2022", "game-changers-2023", "game-changers-2024", "vct-challengers-2023", "vct-challengers-2024", "vct-international-2022", "vct-international-2023", "vct-international-2024"]

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
    if "create" in response.lower() or "insert" in response.lower():
        return False
    result_df = ensure_sql_execute(system_message, message, response, 0)

    if isinstance(result_df, pd.DataFrame): # 不管得到的数据是空与否
        df_json_string = result_df.to_json(orient='records', force_ascii=False)
        print(df_json_string)
        return df_json_string
    else:
        print("Check Database Status!")
        return False
    

def team_builder_agent(message: str, history: List[Tuple[str, str]]):
    ###为了确定联赛
    clf_league_msg = '''
    Complete the text classification task of categorizing the "user" query into one specific category of Leagues / Tournaments provided in the following list. 
    Your output can only be one of the items from the list: ["game-changers", "vct-challengers", "vct-international"]
    '''
    messages = []
    msg = [{"text": message + clf_league_msg}]
    messages.append({"role": "user", "content": msg})
    clf_league_response = bedrock_completion(messages)

    league_sig = 0
    league_list = ["game-changers", "vct-challengers", "vct-international"]
    league_name = "vct-international"
    for idx, league in enumerate(league_list):
        if league in clf_league_response.lower():
            league_sig = 1
            league_name = league
            break
        elif idx == len(league_list) - 1 and league_sig == 0:
            pass
            
    
    ###为了确定Map
    map_dict = {
    "Abyss": "Infinity",
    "Ascent": "Ascent",
    "Bind": "Duality",
    "Breeze": "Foxtrot",
    "Fracture": "Canyon",
    "Haven": "Triad",
    "Icebox": "Port",
    "Lotus": "Jam",
    "Pearl": "Pitt",
    "Split": "Bonsai",
    "Sunset": "Juliett",
    "District": "HURM_Alley",
    "Drift": "HURM_Helix",
    "Kasbah": "HURM_Bowl",
    "Piazza": "HURM_Yard",
    "Range": "Poveglia"
    }
    clf_map_msg = '''
    Complete the text classification task of categorizing the "user" query into one specific category of Maps provided in the following list. 
    Your output can only be one of the items from the list: ['Fracture', 'Haven', 'Infinity', 'Sunset', 'Triad', 'Range', 'Canyon', 'Port', 'HURM_Helix', 'Bonsai', 'HURM_Bowl', 'Kasbah', 'Ascent', 'Duality', 'District', 'HURM_Yard', 'Pitt', 'Pearl', 'Bind', 'Icebox', 'Drift', 'HURM_Alley', 'Poveglia', 'Breeze', 'Foxtrot', 'Juliett', 'Piazza', 'Abyss', 'Lotus', 'Split', 'Jam']
    '''
    messages = []
    msg = [{"text": "Query: " + message + clf_map_msg}]
    messages.append({"role": "user", "content": msg})
    clf_map_response = bedrock_completion(messages)

    map_sig = 0
    map_list = ['Fracture', 'Haven', 'Infinity', 'Sunset', 'Triad', 'Range', 'Canyon', 'Port', 'HURM_Helix', 'Bonsai', 'HURM_Bowl', 'Kasbah', 'Ascent', 'Duality', 'District', 'HURM_Yard', 'Pitt', 'Pearl', 'Bind', 'Icebox', 'Drift', 'HURM_Alley', 'Poveglia', 'Breeze', 'Foxtrot', 'Juliett', 'Piazza', 'Abyss', 'Lotus', 'Split', 'Jam']
    map_name = "Jam"
    explanation = ""
    for idx, map in enumerate(map_list):
        if map in clf_map_response.lower():
            map_sig = 1
            map_name = map
            explanation = f'''
            1. Use the "recommened_team_combination" as the final team, and find the best players in the given program: "{league_name}" for each agent in the team.
            2. In 'best_player_for_each_agent', there are at most 3 players for a gent, they are ordered descendingly by their win rate. If there are several same agents in the chosen team combination, choose the the corresponding players with the greatest win rate for the agent.
            '''
            break
        elif idx == len(map_list) - 1 and map_sig == 0:
            map_name = ""
            explanation = f'''
            1. Find the best team for the given map: "{map_name}" in 'best_team_combination_for_each_map' and find the best players in the given program: "{league_name}" for each agent in the team.
            2. In 'best_player_for_each_agent', there are at most 3 players for a gent, they are ordered descendingly by their win rate. If there are several same agents in the chosen team combination, choose the the corresponding players with the greatest win rate for the agent.
            '''
    
    task = f'''
        Based on the above data, build a team using only players from "{league_name}". Below are the tasks for the "user" query "{message}" in details:
        1. Assign roles to players on the team and explain their contribution using the above data
        1.1 Offensive vs. defensive roles
        1.2 Category of in-game playable character / agent (duelist, sentinel, controller, initiator)

        2. explain why the composition would be effective in a competitive match using the above data
        3. Assign a team IGL (team leader, primary strategist and shotcaller) using the above data
        4. Provide insights on team strategy and hypothesize team strengths and weaknesses using the above data
    '''

    if "vct-international" in league_name:
        data_msg = '''
        {
        "program": "vct-international",
        "best player for each agent": [{'player_id': '107769216664661606', 'agent': 'Breach', 'round_number': 255, 'winning_round_number': 141, 'winning_rate': 0.5529411764705883}, {'player_id': '111850184153949891', 'agent': 'Breach', 'round_number': 252, 'winning_round_number': 135, 'winning_rate': 0.5357142857142857}, {'player_id': '107769215396408908', 'agent': 'Breach', 'round_number': 246, 'winning_round_number': 129, 'winning_rate': 0.524390243902439}, {'player_id': '106230316470125268', 'agent': 'Brimstone', 'round_number': 572, 'winning_round_number': 320, 'winning_rate': 0.5594405594405595}, {'player_id': '107764993804063401', 'agent': 'Brimstone', 'round_number': 1046, 'winning_round_number': 581, 'winning_rate': 0.5554493307839388}, {'player_id': '109795063140126742', 'agent': 'Brimstone', 'round_number': 262, 'winning_round_number': 145, 'winning_rate': 0.5534351145038168}, {'player_id': '108256001569272928', 'agent': 'Chamber', 'round_number': 203, 'winning_round_number': 114, 'winning_rate': 0.5615763546798029}, {'player_id': '109636696799297087', 'agent': 'Cypher', 'round_number': 222, 'winning_round_number': 130, 'winning_rate': 0.5855855855855856}, {'player_id': '107926951905638936', 'agent': 'Cypher', 'round_number': 209, 'winning_round_number': 118, 'winning_rate': 0.5645933014354066}, {'player_id': '109630635013669017', 'agent': 'Cypher', 'round_number': 327, 'winning_round_number': 176, 'winning_rate': 0.5382262996941896}, {'player_id': '106230316470125268', 'agent': 'Fade', 'round_number': 426, 'winning_round_number': 247, 'winning_rate': 0.57981220657277}, {'player_id': '109918865741533645', 'agent': 'Fade', 'round_number': 242, 'winning_round_number': 134, 'winning_rate': 0.5537190082644629}, {'player_id': '99566407765334300', 'agent': 'Fade', 'round_number': 416, 'winning_round_number': 228, 'winning_rate': 0.5480769230769231}, {'player_id': '109641698140602206', 'agent': 'Gekko', 'round_number': 237, 'winning_round_number': 136, 'winning_rate': 0.5738396624472574}, {'player_id': '107760834954512281', 'agent': 'Gekko', 'round_number': 269, 'winning_round_number': 154, 'winning_rate': 0.5724907063197026}, {'player_id': '106532686424986077', 'agent': 'Gekko', 'round_number': 301, 'winning_round_number': 172, 'winning_rate': 0.5714285714285714}, {'player_id': '106156773024391652', 'agent': 'Harbor', 'round_number': 504, 'winning_round_number': 285, 'winning_rate': 0.5654761904761905}, {'player_id': '106724771285467852', 'agent': 'Harbor', 'round_number': 229, 'winning_round_number': 115, 'winning_rate': 0.5021834061135371}, {'player_id': '107769215396408908', 'agent': 'Harbor', 'round_number': 274, 'winning_round_number': 127, 'winning_rate': 0.4635036496350365}, {'player_id': '106724771285467852', 'agent': 'Jett', 'round_number': 278, 'winning_round_number': 170, 'winning_rate': 0.6115107913669064}, {'player_id': '112688316138301116', 'agent': 'Jett', 'round_number': 229, 'winning_round_number': 124, 'winning_rate': 0.5414847161572053}, {'player_id': '106156773024391652', 'agent': 'Jett', 'round_number': 361, 'winning_round_number': 184, 'winning_rate': 0.5096952908587258}, {'player_id': '109980839435632237', 'agent': 'KAY/O', 'round_number': 215, 'winning_round_number': 132, 'winning_rate': 0.6139534883720931}, {'player_id': '107042214535152515', 'agent': 'KAY/O', 'round_number': 382, 'winning_round_number': 229, 'winning_rate': 0.599476439790576}, {'player_id': '112688316138301116', 'agent': 'KAY/O', 'round_number': 205, 'winning_round_number': 120, 'winning_rate': 0.5853658536585366}, {'player_id': '107764993804063401', 'agent': 'Killjoy', 'round_number': 374, 'winning_round_number': 207, 'winning_rate': 0.553475935828877}, {'player_id': '107769215086183858', 'agent': 'Killjoy', 'round_number': 358, 'winning_round_number': 196, 'winning_rate': 0.547486033519553}, {'player_id': '106605824072688095', 'agent': 'Killjoy', 'round_number': 550, 'winning_round_number': 295, 'winning_rate': 0.5363636363636364}, {'player_id': '111850184153949891', 'agent': 'Omen', 'round_number': 1175, 'winning_round_number': 666, 'winning_rate': 0.5668085106382978}, {'player_id': '103537287230111095', 'agent': 'Omen', 'round_number': 590, 'winning_round_number': 329, 'winning_rate': 0.5576271186440678}, {'player_id': '106229920360816436', 'agent': 'Omen', 'round_number': 1038, 'winning_round_number': 571, 'winning_rate': 0.5500963391136802}, {'player_id': '109630636704842016', 'agent': 'Phoenix', 'round_number': 548, 'winning_round_number': 306, 'winning_rate': 0.5583941605839416}, {'player_id': '106229950694048376', 'agent': 'Phoenix', 'round_number': 439, 'winning_round_number': 245, 'winning_rate': 0.5580865603644647}, {'player_id': '108329605365228616', 'agent': 'Phoenix', 'round_number': 1042, 'winning_round_number': 577, 'winning_rate': 0.553742802303263}, {'player_id': '99566407765334300', 'agent': 'Raze', 'round_number': 362, 'winning_round_number': 208, 'winning_rate': 0.574585635359116}, {'player_id': '106230316470125268', 'agent': 'Raze', 'round_number': 679, 'winning_round_number': 365, 'winning_rate': 0.5375552282768777}, {'player_id': '106724767436961366', 'agent': 'Raze', 'round_number': 451, 'winning_round_number': 229, 'winning_rate': 0.5077605321507761}, {'player_id': '106724767436961366', 'agent': 'Sage', 'round_number': 284, 'winning_round_number': 167, 'winning_rate': 0.5880281690140845}, {'player_id': '108695555965222493', 'agent': 'Sage', 'round_number': 327, 'winning_round_number': 189, 'winning_rate': 0.5779816513761468}, {'player_id': '106116440965658227', 'agent': 'Sage', 'round_number': 228, 'winning_round_number': 129, 'winning_rate': 0.5657894736842105}, {'player_id': '106116524342027888', 'agent': 'Skye', 'round_number': 246, 'winning_round_number': 130, 'winning_rate': 0.5284552845528455}, {'player_id': '103537287230111095', 'agent': 'Sova', 'round_number': 241, 'winning_round_number': 127, 'winning_rate': 0.5269709543568465}, {'player_id': '111850184153949891', 'agent': 'Sova', 'round_number': 250, 'winning_round_number': 131, 'winning_rate': 0.524}, {'player_id': '107735298728316922', 'agent': 'Sova', 'round_number': 228, 'winning_round_number': 112, 'winning_rate': 0.49122807017543857}, {'player_id': '106229950694048376', 'agent': 'Viper', 'round_number': 317, 'winning_round_number': 183, 'winning_rate': 0.5772870662460567}, {'player_id': '109630636704842016', 'agent': 'Viper', 'round_number': 315, 'winning_round_number': 179, 'winning_rate': 0.5682539682539682}, {'player_id': '106532684877070738', 'agent': 'Viper', 'round_number': 352, 'winning_round_number': 199, 'winning_rate': 0.5653409090909091}, {'player_id': '106230271915475632', 'agent': 'Yoru', 'round_number': 373, 'winning_round_number': 214, 'winning_rate': 0.5737265415549598}, {'player_id': '107723772674746660', 'agent': 'Yoru', 'round_number': 217, 'winning_round_number': 121, 'winning_rate': 0.5576036866359447}, {'player_id': '107042219372351080', 'agent': 'Yoru', 'round_number': 240, 'winning_round_number': 111, 'winning_rate': 0.4625}],
        "recommended_team_combination": [
            "Gekko",
            "Fade",
            "Omen",
            "Phoenix",
            "Viper"
        ],
        "best_team_combination_for_each_map": [{'team_combination': 'Brimstone KAY/O KAY/O Omen Phoenix', 'map': 'Ascent', 'round_number': 2206, 'winning_round_number': 1131, 'winning_rate': 0.5126926563916591}, {'team_combination': 'Gekko KAY/O Omen Raze Viper', 'map': 'Bonsai', 'round_number': 340, 'winning_round_number': 189, 'winning_rate': 0.5558823529411765}, {'team_combination': 'Gekko Harbor Killjoy Raze Viper', 'map': 'Duality', 'round_number': 178, 'winning_round_number': 96, 'winning_rate': 0.5393258426966292}, {'team_combination': 'Brimstone KAY/O Sova Viper Yoru', 'map': 'Foxtrot', 'round_number': 185, 'winning_round_number': 100, 'winning_rate': 0.5405405405405406}, {'team_combination': 'Brimstone Cypher KAY/O KAY/O Omen', 'map': 'Infinity', 'round_number': 187, 'winning_round_number': 106, 'winning_rate': 0.5668449197860963}, {'team_combination': 'Fade Jett Jett Omen Sage', 'map': 'Jam', 'round_number': 101, 'winning_round_number': 65, 'winning_rate': 0.6435643564356436}, {'team_combination': 'Gekko Cypher Omen Raze Viper', 'map': 'Juliett', 'round_number': 143, 'winning_round_number': 85, 'winning_rate': 0.5944055944055944}, {'team_combination': 'Jett KAY/O KAY/O Phoenix Viper', 'map': 'Port', 'round_number': 109, 'winning_round_number': 69, 'winning_rate': 0.6330275229357798}, {'team_combination': 'Brimstone Cypher Iso Omen Yoru', 'map': 'Triad', 'round_number': 119, 'winning_round_number': 78, 'winning_rate': 0.6554621848739496}]
        }
        '''
    elif "game-changers" in league_name:
        data_msg = '''
        {
        "program": "game-changers",
        "team_combination": ["Gekko", "Fade", "Omen", "Phoenix", "Viper"],
        "best player for each agent": [{'player_id': '106371712554417774', 'agent': 'Brimstone', 'round_number': 337, 'winning_round_number': 217, 'winning_rate': 0.6439169139465876}, {'player_id': '107691453225086388', 'agent': 'Brimstone', 'round_number': 201, 'winning_round_number': 129, 'winning_rate': 0.6417910447761194}, {'player_id': '110745687059117485', 'agent': 'Brimstone', 'round_number': 231, 'winning_round_number': 122, 'winning_rate': 0.5281385281385281}, {'player_id': '107600796790972557', 'agent': 'Cypher', 'round_number': 410, 'winning_round_number': 255, 'winning_rate': 0.6219512195121951}, {'player_id': '109993752630503080', 'agent': 'Cypher', 'round_number': 206, 'winning_round_number': 124, 'winning_rate': 0.6019417475728155}, {'player_id': '108748093351174554', 'agent': 'Cypher', 'round_number': 214, 'winning_round_number': 122, 'winning_rate': 0.5700934579439252}, {'player_id': '112127568302800017', 'agent': 'Gekko', 'round_number': 208, 'winning_round_number': 143, 'winning_rate': 0.6875}, {'player_id': '107600798796177555', 'agent': 'Gekko', 'round_number': 322, 'winning_round_number': 204, 'winning_rate': 0.6335403726708074}, {'player_id': '110196698617452805', 'agent': 'Gekko', 'round_number': 213, 'winning_round_number': 127, 'winning_rate': 0.596244131455399}, {'player_id': '110196450235676141', 'agent': 'Jett', 'round_number': 259, 'winning_round_number': 151, 'winning_rate': 0.583011583011583}, {'player_id': '108748093751316801', 'agent': 'Jett', 'round_number': 210, 'winning_round_number': 122, 'winning_rate': 0.580952380952381}, {'player_id': '108449806078327743', 'agent': 'Jett', 'round_number': 208, 'winning_round_number': 117, 'winning_rate': 0.5625}, {'player_id': '112127568302800017', 'agent': 'KAY/O', 'round_number': 287, 'winning_round_number': 178, 'winning_rate': 0.6202090592334495}, {'player_id': '106371709362814570', 'agent': 'KAY/O', 'round_number': 230, 'winning_round_number': 142, 'winning_rate': 0.6173913043478261}, {'player_id': '112127374030331222', 'agent': 'KAY/O', 'round_number': 394, 'winning_round_number': 207, 'winning_rate': 0.5253807106598984}, {'player_id': '106371668436500067', 'agent': 'Killjoy', 'round_number': 305, 'winning_round_number': 176, 'winning_rate': 0.5770491803278689}, {'player_id': '106371572811742769', 'agent': 'Killjoy', 'round_number': 215, 'winning_round_number': 124, 'winning_rate': 0.5767441860465117}, {'player_id': '108449806078327743', 'agent': 'Killjoy', 'round_number': 219, 'winning_round_number': 111, 'winning_rate': 0.5068493150684932}, {'player_id': '106620786007238114', 'agent': 'Omen', 'round_number': 369, 'winning_round_number': 244, 'winning_rate': 0.6612466124661247}, {'player_id': '107600792569471113', 'agent': 'Omen', 'round_number': 426, 'winning_round_number': 267, 'winning_rate': 0.6267605633802817}, {'player_id': '111007943120168151', 'agent': 'Omen', 'round_number': 230, 'winning_round_number': 143, 'winning_rate': 0.6217391304347826}, {'player_id': '107176840785143570', 'agent': 'Phoenix', 'round_number': 374, 'winning_round_number': 243, 'winning_rate': 0.6497326203208557}, {'player_id': '109993752630503080', 'agent': 'Phoenix', 'round_number': 286, 'winning_round_number': 148, 'winning_rate': 0.5174825174825175}, {'player_id': '108490268439372476', 'agent': 'Phoenix', 'round_number': 283, 'winning_round_number': 139, 'winning_rate': 0.4911660777385159}, {'player_id': '107025877954628831', 'agent': 'Raze', 'round_number': 229, 'winning_round_number': 131, 'winning_rate': 0.5720524017467249}, {'player_id': '108490307883176100', 'agent': 'Viper', 'round_number': 206, 'winning_round_number': 104, 'winning_rate': 0.5048543689320388}, {'player_id': '108748093751316801', 'agent': 'Viper', 'round_number': 226, 'winning_round_number': 111, 'winning_rate': 0.4911504424778761}, {'player_id': '108490286624740396', 'agent': 'Viper', 'round_number': 265, 'winning_round_number': 126, 'winning_rate': 0.47547169811320755}],
        "best_team_combination_for_each_map": [{'team_combination': 'Brimstone KAY/O KAY/O Omen Phoenix', 'map': 'Ascent', 'round_number': 1989, 'winning_round_number': 994, 'winning_rate': 0.4997486173956762}, {'team_combination': 'Cypher Gekko Omen Raze Viper', 'map': 'Bonsai', 'round_number': 339, 'winning_round_number': 165, 'winning_rate': 0.48672566371681414}, {'team_combination': 'Breach Gekko Killjoy Raze Viper', 'map': 'Duality', 'round_number': 488, 'winning_round_number': 265, 'winning_rate': 0.5430327868852459}, {'team_combination': 'Brimstone Cypher KAY/O Viper Yoru', 'map': 'Foxtrot', 'round_number': 131, 'winning_round_number': 70, 'winning_rate': 0.5343511450381679}, {'team_combination': 'Brimstone Cypher Jett KAY/O Omen', 'map': 'Infinity', 'round_number': 143, 'winning_round_number': 52, 'winning_rate': 0.36363636363636365}, {'team_combination': 'Cypher Fade Gekko Jett Omen', 'map': 'Jam', 'round_number': 168, 'winning_round_number': 102, 'winning_rate': 0.6071428571428571}, {'team_combination': 'Cypher Gekko KAY/O Killjoy Omen', 'map': 'Juliett', 'round_number': 328, 'winning_round_number': 175, 'winning_rate': 0.5335365853658537}, {'team_combination': 'Brimstone Harbor KAY/O Phoenix Viper', 'map': 'Port', 'round_number': 225, 'winning_round_number': 134, 'winning_rate': 0.5955555555555555}, {'team_combination': 'Brimstone Jett KAY/O Omen Phoenix', 'map': 'Triad', 'round_number': 313, 'winning_round_number': 167, 'winning_rate': 0.5335463258785943}]
        }
        '''
    elif "vct challengers" in league_name:
        data_msg = '''
        {
        "programe": "vct challengers",
        "best_team_combination": ["Gekko", "Fade", "Omen", "Phoenix", "Viper"],
                "best_team_combination_for_each_map": [{'player_id': '107742457930562464', 'agent': 'Brimstone', 'round_number': 268, 'winning_round_number': 178, 'winning_rate': 0.664179104477612}, {'player_id': '109716300201480697', 'agent': 'Cypher', 'round_number': 270, 'winning_round_number': 164, 'winning_rate': 0.6074074074074074}, {'player_id': '109716301124936931', 'agent': 'Fade', 'round_number': 417, 'winning_round_number': 217, 'winning_rate': 0.5203836930455635}, {'player_id': '111799897691920449', 'agent': 'Gekko', 'round_number': 205, 'winning_round_number': 126, 'winning_rate': 0.6146341463414634}, {'player_id': '107723775567381623', 'agent': 'Jett', 'round_number': 207, 'winning_round_number': 117, 'winning_rate': 0.5652173913043478}, {'player_id': '109642058238535401', 'agent': 'KAY/O', 'round_number': 228, 'winning_round_number': 152, 'winning_rate': 0.6666666666666666}, {'player_id': '109642061824796407', 'agent': 'Omen', 'round_number': 204, 'winning_round_number': 140, 'winning_rate': 0.6862745098039216}, {'player_id': '109794901178650563', 'agent': 'Phoenix', 'round_number': 238, 'winning_round_number': 143, 'winning_rate': 0.6008403361344538}, {'player_id': '107760837763873282', 'agent': 'Raze', 'round_number': 252, 'winning_round_number': 154, 'winning_rate': 0.6111111111111112}, {'player_id': '109699665612693935', 'agent': 'Viper', 'round_number': 204, 'winning_round_number': 130, 'winning_rate': 0.6372549019607843}, {'player_id': '111936107541022413', 'agent': 'Yoru', 'round_number': 209, 'winning_round_number': 105, 'winning_rate': 0.5023923444976076}]
        [{'team_combination': 'Brimstone Cypher Deadlock KAY/O Omen', 'map': 'Ascent', 'round_number': 309, 'winning_round_number': 166, 'winning_rate': 0.5372168284789643}, {'team_combination': 'Gekko Jett Omen Raze Viper', 'map': 'Bonsai', 'round_number': 102, 'winning_round_number': 63, 'winning_rate': 0.6176470588235294}, {'team_combination': 'Gekko Breach Raze Sage Viper', 'map': 'Duality', 'round_number': 177, 'winning_round_number': 96, 'winning_rate': 0.5423728813559322}, {'team_combination': 'Brimstone Cypher KAY/O Viper Yoru', 'map': 'Foxtrot', 'round_number': 768, 'winning_round_number': 398, 'winning_rate': 0.5182291666666666}, {'team_combination': 'Gekko Cypher Jett Killjoy Omen', 'map': 'Jam', 'round_number': 141, 'winning_round_number': 77, 'winning_rate': 0.5460992907801419}, {'team_combination': 'Gekko Cypher Fade Omen Sage', 'map': 'Juliett', 'round_number': 120, 'winning_round_number': 77, 'winning_rate': 0.6416666666666667}, {'team_combination': 'Gekko Brimstone KAY/O Phoenix Viper', 'map': 'Port', 'round_number': 141, 'winning_round_number': 88, 'winning_rate': 0.624113475177305}, {'team_combination': 'Brimstone Cypher Iso Omen Yoru', 'map': 'Triad', 'round_number': 115, 'winning_round_number': 76, 'winning_rate': 0.6608695652173913}],
        "best player for each agent": [{'player_id': '107742457930562464', 'agent': 'Brimstone', 'round_number': 268, 'winning_round_number': 178, 'winning_rate': 0.664179104477612}, {'player_id': '108245714426081938', 'agent': 'Brimstone', 'round_number': 223, 'winning_round_number': 146, 'winning_rate': 0.6547085201793722}, {'player_id': '109794898623952350', 'agent': 'Brimstone', 'round_number': 214, 'winning_round_number': 134, 'winning_rate': 0.6261682242990654}, {'player_id': '109716300201480697', 'agent': 'Cypher', 'round_number': 270, 'winning_round_number': 164, 'winning_rate': 0.6074074074074074}, {'player_id': '106230374904906489', 'agent': 'Cypher', 'round_number': 254, 'winning_round_number': 152, 'winning_rate': 0.5984251968503937}, {'player_id': '107760836242104357', 'agent': 'Cypher', 'round_number': 263, 'winning_round_number': 157, 'winning_rate': 0.596958174904943}, {'player_id': '109716301124936931', 'agent': 'Fade', 'round_number': 417, 'winning_round_number': 217, 'winning_rate': 0.5203836930455635}, {'player_id': '111799897691920449', 'agent': 'Gekko', 'round_number': 205, 'winning_round_number': 126, 'winning_rate': 0.6146341463414634}, {'player_id': '109782837972073866', 'agent': 'Gekko', 'round_number': 221, 'winning_round_number': 134, 'winning_rate': 0.6063348416289592}, {'player_id': '111895125601693468', 'agent': 'Gekko', 'round_number': 476, 'winning_round_number': 283, 'winning_rate': 0.5945378151260504}, {'player_id': '107723775567381623', 'agent': 'Jett', 'round_number': 207, 'winning_round_number': 117, 'winning_rate': 0.5652173913043478}, {'player_id': '109642085281284141', 'agent': 'Jett', 'round_number': 220, 'winning_round_number': 111, 'winning_rate': 0.5045454545454545}, {'player_id': '108844339857245737', 'agent': 'Jett', 'round_number': 247, 'winning_round_number': 114, 'winning_rate': 0.46153846153846156}, {'player_id': '109642058238535401', 'agent': 'KAY/O', 'round_number': 228, 'winning_round_number': 152, 'winning_rate': 0.6666666666666666}, {'player_id': '107760838322240015', 'agent': 'KAY/O', 'round_number': 276, 'winning_round_number': 179, 'winning_rate': 0.6485507246376812}, {'player_id': '107924876600456932', 'agent': 'KAY/O', 'round_number': 211, 'winning_round_number': 125, 'winning_rate': 0.5924170616113744}, {'player_id': '109642061824796407', 'agent': 'Omen', 'round_number': 204, 'winning_round_number': 140, 'winning_rate': 0.6862745098039216}, {'player_id': '109069441499422398', 'agent': 'Omen', 'round_number': 254, 'winning_round_number': 172, 'winning_rate': 0.6771653543307087}, {'player_id': '107760968223023641', 'agent': 'Omen', 'round_number': 249, 'winning_round_number': 157, 'winning_rate': 0.6305220883534136}, {'player_id': '109794901178650563', 'agent': 'Phoenix', 'round_number': 238, 'winning_round_number': 143, 'winning_rate': 0.6008403361344538}, {'player_id': '107760839352836185', 'agent': 'Phoenix', 'round_number': 269, 'winning_round_number': 160, 'winning_rate': 0.5947955390334573}, {'player_id': '109862190324414565', 'agent': 'Phoenix', 'round_number': 245, 'winning_round_number': 144, 'winning_rate': 0.5877551020408164}, {'player_id': '107760837763873282', 'agent': 'Raze', 'round_number': 252, 'winning_round_number': 154, 'winning_rate': 0.6111111111111112}, {'player_id': '111919330470270854', 'agent': 'Raze', 'round_number': 257, 'winning_round_number': 152, 'winning_rate': 0.5914396887159533}, {'player_id': '107760966594060796', 'agent': 'Raze', 'round_number': 278, 'winning_round_number': 163, 'winning_rate': 0.5863309352517986}, {'player_id': '109699665612693935', 'agent': 'Viper', 'round_number': 204, 'winning_round_number': 130, 'winning_rate': 0.6372549019607843}, {'player_id': '106489818447340448', 'agent': 'Viper', 'round_number': 258, 'winning_round_number': 160, 'winning_rate': 0.6201550387596899}, {'player_id': '107760838373328863', 'agent': 'Viper', 'round_number': 228, 'winning_round_number': 136, 'winning_rate': 0.5964912280701754}, {'player_id': '111936107541022413', 'agent': 'Yoru', 'round_number': 209, 'winning_round_number': 105, 'winning_rate': 0.5023923444976076}]
        }
        '''
    else:
        return valorant_agent(message, history)

    messages = []
    complete_msg = [{"text": "DATA: " + data_msg + "DATA Explanation: " + explanation + task}]
    messages.append({"role": "user", "content": complete_msg})
    response = bedrock_completion(messages)
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
        if "team build" in response.lower():
                return team_builder_agent(message, history)
        else:
            additional_info = sql_agent(message, history)
            print("game / player info")
            if additional_info:
                    message += "Answer the questions based on the following information."
                    message += additional_info
                    print(additional_info)
                    return valorant_agent(message, history)
            else:
                return valorant_agent(message, history)

