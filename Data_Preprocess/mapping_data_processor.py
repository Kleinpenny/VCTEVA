import json

def platformIDs_to_participantMapping(LEAGUE):
    ### Example###
    #"val:a02b939b-d53b-4d6c-9cf9-8df5cbecdec6":{
    #"1": "110196391536301033",
    #"2": "108550500823868280",
    #"3": "107691403279337920",
    #"4": "108231581673551401",
    #"5": "107282823220699313",
    #"6": "107025879465378213",
    #"7": "107025879556684669",
    #"8": "107186009704881408",
    #"9": "107186009230387255",
    #"10": "110615094848109973"
    #}

    mapping_file_path = f"../DATA/{LEAGUE}/esports-data/mapping_data_v2.json"
    with open(mapping_file_path, "r") as json_file:
        mapping_data = json.load(json_file)
    result = {}
    for data in mapping_data:
        platform_game_id = data["platformGameId"]
        participant_mapping = data["participantMapping"]
        result[platform_game_id] = participant_mapping
    return result

def platformIDs_to_teamMapping(LEAGUE):
    ### Example###
    #"val:a02b939b-d53b-4d6c-9cf9-8df5cbecdec6":{
    #"17": "108452432292545538",
    #"18": "112127218115639934"
    #}

    mapping_file_path = f"../DATA/{LEAGUE}/esports-data/mapping_data_v2.json"
    with open(mapping_file_path, "r") as json_file:
        mapping_data = json.load(json_file)
    result = {}
    for data in mapping_data:
        platform_game_id = data["platformGameId"]
        teamMapping = data["teamMapping"]
        result[platform_game_id] = teamMapping
    return result