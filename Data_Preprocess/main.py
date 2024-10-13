import copy
import json
import os
import re
import all_players_processor
import mapping_data_processor
import pandas as pd
from Feature_Modules import Game_Damage, Game_KDA

def find_values(data, key="damageEvent"):
    values = []

    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                values.append(v)
            else:
                values.extend(find_values(v, key))
    elif isinstance(data, list):
        for item in data:
            values.extend(find_values(item, key))
    
    return values

def get_game_json_path(search_term, LEAGUE):
    #需要检索的路径
    directory_path = f"../DATA/{LEAGUE}/games"

    file_path = ""
    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # 如果文件名包含要匹配的字符串
            if search_term in file:
                # 打印匹配文件的完整路径
                file_path = os.path.join(root, file)
                print(f"匹配到的文件路径: {file_path}")
    return file_path


def round_kda_for_each_game(LEAGUE, year, game_file_path, target_path, ):
    mapping_file_path = f"../DATA/{LEAGUE}/esports-data/mapping_data_v2.json"
    player_file_path = f"../DATA/{LEAGUE}/esports-data/players.json"
    team_file_path = f"../DATA/{LEAGUE}/esports-data/teams.json"
    league_file_path = f"../DATA/{LEAGUE}/esports-data/leagues.json"
    game_info_kda = Game_KDA.main(game_file_path, mapping_file_path, player_file_path, team_file_path, league_file_path)
    LEAGUE_year = f"{LEAGUE}-{year}"
    info = {
        "games_win": 0,
        "games_count": 0,
        "attacking":{
            "Kills": 0,
            "Deaths": 0,
            "Assists": 0,
            "rounds_taken": 0,
            "rounds_win": 0
        },
        "defending":{
            "Kills": 0,
            "Deaths": 0,
            "Assists": 0,
            "rounds_taken": 0,
            "rounds_win": 0
        }
    }
    #读取每位选手的json数据，用于拓展
    with open(target_path, "r") as json_file:
        players_json_data = json.load(json_file)

    #108076829264740999
    for idx, player in enumerate(game_info_kda):
        print(len(player['RoundInfo']))
        if player['PlayerId'] not in players_json_data:
            players_json_data[player['PlayerId']] = {}
        players_json_data[player['PlayerId']]["name"] = f"{player['first_name']} {player['last_name']}"
        players_json_data[player['PlayerId']]["team_id"] = player['team_id']
        players_json_data[player['PlayerId']]["handle"] = player['handle']
        players_json_data[player['PlayerId']]["region"] = player['league_region']
        if LEAGUE_year not in players_json_data[player['PlayerId']]:
            players_json_data[player['PlayerId']][LEAGUE_year] = {}
        if player['Map'] not in players_json_data[player['PlayerId']][LEAGUE_year]:
            players_json_data[player['PlayerId']][LEAGUE_year] = {player['Map']: copy.deepcopy(info)}
        if player['Summary']['result'] == 'win':
            players_json_data[player['PlayerId']][LEAGUE_year][player['Map']]["games_win"] += 1
        players_json_data[player['PlayerId']][LEAGUE_year][player['Map']]["games_count"] += 1

        for round_info in player['RoundInfo']:
            if round_info['role'] == 'attacking':
                a = players_json_data[player['PlayerId']][LEAGUE_year][player['Map']]["attacking"]
                for kda in list(a.keys())[:3]:
                    a[kda] += round_info[kda]
                a["rounds_taken"] += 1
                if round_info['result'] == 'win':
                    a["rounds_win"] += 1
            else:
                d = players_json_data[player['PlayerId']][LEAGUE_year][player['Map']]["defending"]
                for kda in list(d.keys())[:3]:
                    d[kda] += round_info[kda]
                d["rounds_taken"] += 1
                if round_info['result'] == 'win':
                    d["rounds_win"] += 1

    with open(target_path, "w") as output_file:
        json.dump(players_json_data, output_file, indent=4)
    return player['Map']

def damage_performance_analysis(game_file_path, target_path, LEAGUE, year, players_map, selected_map):

    game_damage_event_df =Game_Damage.main(game_file_path)
    #df.columns

    #读取对应场次的比赛的json记录
    with open(game_file_path, "r") as json_file:
        game_json_data = json.load(json_file)

    #读取每位选手的json数据，用于拓展
    with open(target_path, "r") as json_file:
        players_json_data = json.load(json_file)

    LEAGUE_year = f"{LEAGUE}-{year}"
    for p_id  in game_damage_event_df['PlayerID']:
        id_string = f"{p_id}"
        playerID = players_map[id_string]
        game_dict = players_json_data[playerID][LEAGUE_year][selected_map]
        for col in game_damage_event_df.columns[1:]:
            #这里对于数据进行平均计算
            if 'SummaryPerGame' not in game_dict:
                game_dict['SummaryPerGame'] = {}
            if col not in game_dict['SummaryPerGame']:
                game_dict['SummaryPerGame'][col] = float(game_damage_event_df[col][p_id - 1])
            else:
                game_dict['SummaryPerGame'][col] = (game_dict['SummaryPerGame'][col] + float(game_damage_event_df[col][p_id - 1])) / 2

    damage_records = find_values(game_json_data, "damageEvent")

    #得到部位的唯一值
    #unique_locations = set()
    #for item in damage_records:
    #   unique_locations.add(item['location'])
    #print(unique_locations) #{'LEG', 'BODY', 'GENERAL', 'HEAD'}
    flags = [0 for _ in players_map]
    for idx, id in enumerate(players_map.values()):
        if "damage_caused" not in players_json_data[id][LEAGUE_year][selected_map] or "damage_received" not in players_json_data[id][LEAGUE_year][selected_map]:
            players_json_data[id][LEAGUE_year][selected_map]["damage_caused"] = {}
            players_json_data[id][LEAGUE_year][selected_map]["damage_received"] = {}
            flags[idx] = 1 #表明对应的选手是第一次进行这样的计算，因此不需要取平均值
    for damage_record in damage_records:
        causedID = damage_record['causerId']['value']
        c_string = f"{causedID}"
        c_playerID = players_map[c_string]
        victimID = damage_record['victimId']['value']
        v_string = f"{victimID}"
        v_playerID = players_map[v_string]
        location = damage_record['location']
        if c_playerID in players_json_data:
            location_count = location + "_count"
            location_amount = location + "_amount"
            if location_count not in players_json_data[c_playerID][LEAGUE_year][selected_map]["damage_caused"]:
                players_json_data[c_playerID][LEAGUE_year][selected_map]["damage_caused"][location_count] = 0
            if location_amount not in players_json_data[c_playerID][LEAGUE_year][selected_map]["damage_caused"]:
                players_json_data[c_playerID][LEAGUE_year][selected_map]["damage_caused"][location_amount] = 0

            if location_count not in players_json_data[v_playerID][LEAGUE_year][selected_map]["damage_received"]:
                players_json_data[v_playerID][LEAGUE_year][selected_map]["damage_received"][location_count] = 0
            if location_amount not in players_json_data[v_playerID][LEAGUE_year][selected_map]["damage_received"]:
                players_json_data[v_playerID][LEAGUE_year][selected_map]["damage_received"][location_amount] = 0

            players_json_data[c_playerID][LEAGUE_year][selected_map]["damage_caused"][location_count] += 1
            players_json_data[c_playerID][LEAGUE_year][selected_map]["damage_caused"][location_amount] += round(damage_record['damageAmount'], 2)
            players_json_data[v_playerID][LEAGUE_year][selected_map]["damage_received"][location_count] += 1
            players_json_data[v_playerID][LEAGUE_year][selected_map]["damage_received"][location_amount] += round(damage_record['damageAmount'], 2)

    #同样的，对于每场比赛造成/接受的伤害进行平均计算
    for idx, id in enumerate(players_map.values()):
        if flags[idx] == 0: #表明这个选手不是第一次进行这样的统计
            players_json_data[id][LEAGUE_year][selected_map]["damage_caused"][location_count] = round(
                players_json_data[id][LEAGUE_year][selected_map]["damage_caused"][location_count] / 2, 2)
            
            players_json_data[id][LEAGUE_year][selected_map]["damage_caused"][location_amount] = round(
                players_json_data[id][LEAGUE_year][selected_map]["damage_caused"][location_amount] / 2, 2)
            
            players_json_data[id][LEAGUE_year][selected_map]["damage_received"][location_count] = round(
                players_json_data[id][LEAGUE_year][selected_map]["damage_received"][location_count] / 2, 2)
            
            players_json_data[id][LEAGUE_year][selected_map]["damage_received"][location_amount] = round(
                players_json_data[id][LEAGUE_year][selected_map]["damage_received"][location_amount] / 2, 2)

    with open(target_path, "w") as output_file:
        json.dump(players_json_data, output_file, indent=4)


def main():
    #数据提取的最开始，需要创建一个以playerID作为key的包含所有选手基本数据的json文件.
    all_players_processor.all_players()

    #这是按照不同的LEAGUE来提取对应数据，用于拓展all_players_begin_with_ID.json的信息

    LEAGUE = "game-changers" # "vct-challengers", "vct-international"
    saved_path = "../DATA/all_players.json"
    
    #不是按照年份来提取，但是是根据mapping_data中保存的比赛来
    participantMapping_data = mapping_data_processor.platformIDs_to_participantMapping(LEAGUE)
    teamMapping_data = mapping_data_processor.platformIDs_to_teamMapping(LEAGUE)

    keys = list(participantMapping_data.keys())
    unique_state = set()
    for val_key in [0]: #keys:
        #这里举个例子
        #下面这个是没有game decided
        #val_key = "val:27d62958-08be-448b-9e93-0dee481d1909"
        #下面这个是平局
        #val_key = "val:d7bc6669-96e0-4800-a8ed-87a7de369f53"
        #下面这个是正常的winner_decided
        val_key = "val:0be4d5e2-5e95-40c8-8ade-7b98ca6c24d4"

        #找不到比赛就跳过，直到匹配上比赛的数据
        game_file_path = get_game_json_path(val_key, LEAGUE)
        if game_file_path == "":
            print(f"{val_key}比赛没有记录")
            continue
        else:
            year = 0
            match = re.search(r'/(\d{4})/', game_file_path)
            if match:
                year = match.group(1) #找到了文件的话，一般就都会有年份。
            else:
                print("找不到该比赛对应的年份")
                break
            #########################################################
            # 只考虑有获胜队伍的比赛，因为平局的比赛有的数据有点奇怪，不利于数据分析
            #########################################################

            #读取对应场次的比赛的json记录
            with open(game_file_path, "r") as json_file:
                game_json_data = json.load(json_file)
            state = find_values(game_json_data, "gameDecided")[0]['state']
            if state == 'WINNER_DECIDED':
                players_map = participantMapping_data[val_key]#{playerID in game: 实际的PlayerID}
                teams_map = teamMapping_data[val_key]#{teamID in game: 实际的TeamID}
                selected_map = round_kda_for_each_game(LEAGUE, year, game_file_path, saved_path)
                damage_performance_analysis(game_file_path, saved_path, LEAGUE, year, players_map, selected_map)
                #df_dict = {col: 0 for col in damage_event_df.columns[1:]}

    #print(unique_state)#{DRAW, WINNER_DECIDED}
main()
#all_players_processor.all_players()



