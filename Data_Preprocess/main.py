import json
import os
import re
import all_players_processor
import mapping_data_processor

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


    
def damage_analysis(file_path, target_path, LEAGUE, year, players_map):

    #读取对应场次的比赛的json记录
    with open(file_path, "r") as json_file:
        game_json_data = json.load(json_file)

    #读取每位选手的json数据，用于拓展
    with open(target_path, "r") as json_file:
        players_json_data = json.load(json_file)

    damage_records = find_values(game_json_data, "damageEvent")

    #得到部位的唯一值
    #unique_locations = set()
    #for item in damage_records:
    #   unique_locations.add(item['location'])
    #print(unique_locations) #{'LEG', 'BODY', 'GENERAL', 'HEAD'}

    subset_year = f"{LEAGUE}-{year}"
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
            players_json_data[c_playerID][subset_year]["damage_caused"][location_count] += 1
            players_json_data[c_playerID][subset_year]["damage_caused"][location_amount] += damage_record['damageAmount']
            players_json_data[v_playerID][subset_year]["damage_received"][location_count] += 1
            players_json_data[v_playerID][subset_year]["damage_received"][location_amount] += damage_record['damageAmount']

    with open(target_path, "w") as output_file:
        json.dump(players_json_data, output_file, indent=4)

def game_round_analyse(file_path, target_path, LEAGUE, year, players_map, teams_map):
    #读取对应场次的比赛的json记录
    with open(file_path, "r") as json_file:
        game_json_data = json.load(json_file)

    #读取每位选手的json数据，用于拓展
    with open(target_path, "r") as json_file:
        players_json_data = json.load(json_file)

    subset_year = f"{LEAGUE}-{year}"
    winner_records = find_values(game_json_data, "gameDecided")
    playersInTeam = find_values(game_json_data, "teams")
    teamID_to_players = {}
    # 遍历数据，提取 teamId 和对应的 playersInTeam
    for team in playersInTeam[0]:
        team_id = team['teamId']['value']
        players = [player['value'] for player in team['playersInTeam']]
        teamID_to_players[team_id] = players

    playerIDs_list = {key:players_map[key] for key in players_map.keys() if players_map[key] in players_json_data}
    print(playerIDs_list)
    
    if len(winner_records) != 0:
        if winner_records[0]['state'] == 'WINNER_DECIDED':
            #添加进行的game数量
            for player in playerIDs_list.keys():
                playerID = playerIDs_list[player]
                players_json_data[playerID][subset_year]["games_count"] += 1

            #添加赢得的game数量
            winning_team = winner_records[0]["winningTeam"]["value"]
            w_number = f"{winning_team}"

            for id in teamID_to_players[winning_team]:
                id_string = f"{id}"
                playerID = playerIDs_list[id_string]
                players_json_data[playerID][subset_year]["games_win"] += 1
            losing_team = [key for key in teams_map.keys() if key != w_number][0]

            #添加进行的round数量
            completedRounds = winner_records[0]['spikeMode']['completedRounds']
            rounds_count = len(completedRounds)
            for player in playerIDs_list.keys():
                playerID = playerIDs_list[player]
                players_json_data[playerID][subset_year]["rounds_taken"] += rounds_count

            #添加赢得的round数量
            for round in completedRounds:
                round_winning_team = round["winningTeam"]["value"]
                for id in teamID_to_players[round_winning_team]:
                    id_string = f"{id}"
                    playerID = playerIDs_list[id_string]
                    players_json_data[playerID][subset_year]["rounds_win"] += 1

        with open(target_path, "w") as output_file:
            json.dump(players_json_data, output_file, indent=4)

        #平局或者其他未被记录的情况，就不做任何处理，即抛弃这些数据
        #平局的数据在"val:d7bc6669-96e0-4800-a8ed-87a7de369f53"中没有进行的轮数
        #{'state': 'DRAW', 'spikeMode': {'currentRound': 1, 'attackingTeam': {'value': 16}, 'completedRounds': [], 'roundsToWin': 13, 'defendingTeam': {'value': 17}}}
        #因此得到了的数据也不能使用，因为无法统计入场均的数据中
        return winner_records[0]['state']



def main():
    #这是按照不同的subset来自动化提取对应数据，用于拓展all_players_begin_with_ID.json的信息

    LEAGUE = "game-changers" # "vct-challengers", "vct-international"
    saved_path = "../DATA/ID_to_players_damage.json"
    
    participantMapping_data = mapping_data_processor.platformIDs_to_participantMapping(LEAGUE)
    teamMapping_data = mapping_data_processor.platformIDs_to_teamMapping(LEAGUE)

    keys = list(participantMapping_data.keys())
    unique_state = set()
    current_year = 0
    for val_key in [0]: #keys:
        #这里举个例子
        #下面这个是没有game decided
        #val_key = "val:27d62958-08be-448b-9e93-0dee481d1909"
        #下面这个是平局
        #val_key = "val:d7bc6669-96e0-4800-a8ed-87a7de369f53"
        #下面这个是正常的winner_decided
        val_key = "val:0a63934c-9907-4b7c-a553-ac945cc9eea4"
        file_path = get_game_json_path(val_key, LEAGUE)
        if file_path == "":
            continue
        else:
            ##############################################################################
            # 将会先基于all_players_begin_with_ID.json添加额外的初始的数据， 保存在saved_path中
            year = 0
            match = re.search(r'/(\d{4})/', file_path)
            if match:
                year = match.group(1)
            if year != current_year and current_year == 0:
                #每次重启程序重置之前的数据
                all_players_processor.init_additional_data(saved_path, LEAGUE, year)
                current_year = year
            elif year != current_year and current_year != 0:
                #增添不同年份的数据
                all_players_processor.additional_summary_data(saved_path, LEAGUE, year)
                current_year = year
            ##############################################################################

            players_map = participantMapping_data[val_key]
            teams_map = teamMapping_data[val_key]
            state = game_round_analyse(file_path, saved_path, LEAGUE, year, players_map, teams_map)
            unique_state.add(state)
            if state == 'WINNER_DECIDED':
                damage_analysis(file_path, saved_path, LEAGUE, year, players_map)
    print(unique_state)
    #最终效果:
    # 1 (选手的ID):{
    #    game-changers-2020:{
    #       games_count:0,
    #       rounds_taken:0, -> 每局比赛最后进行的轮数不同
    #       games_win:0, -> 获胜场数
    #       rounds_win:0, -> 获胜轮数
    #       damage_caused: {
    #           LEG_count:0,
    #           LEG_amount:0,
    #           BODY_count:0,
    #           BODY_amount:0,
    #           GENERAL_count:0,
    #           GENERAL_amount:0,
    #           HEAD_count:0,
    #           HEAD_amount:0,
    #        },
    #       damage_received:{
    #           LEG_count:0,
    #           LEG_amount:0,
    #           BODY_count:0,
    #           BODY_amount:0,
    #           GENERAL_count:0,
    #           GENERAL_amount:0,
    #           HEAD_count:0,
    #           HEAD_amount:0,
    #       }
    #   },...
    #}
main()




