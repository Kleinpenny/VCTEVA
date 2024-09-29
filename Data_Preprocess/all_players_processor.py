import json
def begin_with_ID():

    json_file_path = "../DATA/all_players.json"

    with open(json_file_path, "r") as file:
        data = json.load(file)

    result = {}

    for item in data:
        # 以'id'字段的值为键，整个item去掉'id'字段后的内容为值
        result[item["id"]] = {
            "handle": item["handle"],
            "name": item["name"],
            "homeTeam": item["homeTeam"],
            "favorite_heroes": item["favorite_heroes"]
        }

    with open("../DATA/all_players_begin_with_ID.json", "w") as output_file:
        json.dump(result, output_file, indent=4)



# 应该后续添加更多的信息以完备
def init_additional_data(saved_file, subset_name, year):
    json_file_path = "../DATA/all_players_begin_with_ID.json"

    with open(json_file_path, "r") as file:
        data = json.load(file)

    default_stats = {
        f"{subset_name}-{year}": {
            "games_count": 0,
            "rounds_taken": 0,
            "games_win": 0,
            "rounds_win": 0,
            "damage_caused": {
                "LEG_count": 0,
                "LEG_amount": 0,
                "BODY_count": 0,
                "BODY_amount": 0,
                "GENERAL_count": 0,
                "GENERAL_amount": 0,
                "HEAD_count": 0,
                "HEAD_amount": 0,
            },
            "damage_received": {
                "LEG_count": 0,
                "LEG_amount": 0,
                "BODY_count": 0,
                "BODY_amount": 0,
                "GENERAL_count": 0,
                "GENERAL_amount": 0,
                "HEAD_count": 0,
                "HEAD_amount": 0,
            }
        }
    }
    
    key_name = f"{subset_name}-{year}"
    for player_id, player_data in data.items():
        if key_name not in player_data:
            player_data[key_name] = default_stats[key_name]

    with open("../DATA/ID_to_players_damage.json", "w") as output_file:
        json.dump(data, output_file, indent=4)

def additional_summary_data(saved_file, subset_name, year):

    with open(saved_file, "r") as file:
        data = json.load(file)

    default_stats = {
        f"{subset_name}-{year}": {
            "games_count": 0,
            "rounds_taken": 0,
            "games_win": 0,
            "rounds_win": 0,
            "damage_caused": {
                "LEG_count": 0,
                "LEG_amount": 0,
                "BODY_count": 0,
                "BODY_amount": 0,
                "GENERAL_count": 0,
                "GENERAL_amount": 0,
                "HEAD_count": 0,
                "HEAD_amount": 0,
            },
            "damage_received": {
                "LEG_count": 0,
                "LEG_amount": 0,
                "BODY_count": 0,
                "BODY_amount": 0,
                "GENERAL_count": 0,
                "GENERAL_amount": 0,
                "HEAD_count": 0,
                "HEAD_amount": 0,
            }
        }
    }
    
    key_name = f"{subset_name}-{year}"
    for player_id, player_data in data.items():
        if key_name not in player_data:
            player_data[key_name] = default_stats[key_name]

    with open(saved_file, "w") as output_file:
        json.dump(data, output_file, indent=4)
