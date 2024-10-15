import json
import pprint

def extract_player_information(league, year, data, mapping_data):

    result = {}

    # 从data中找出包含'configuration'键的元素
    configuration_element = next((element for element in data if isinstance(element, dict) and 'configuration' in element), None)

    if configuration_element:
        if 'configuration' in configuration_element and 'players' in configuration_element['configuration']:
            players = configuration_element['configuration']['players']
            for player in players:
                if 'selectedAgent' in player:
                    player_id = map_player_id(configuration_element['platformGameId'], player['playerId']['value'], mapping_data)
                    result[player_id] = player['selectedAgent']['fallback']['guid']
        else:
            print("在configuration中没有找到'players'键")
    else:
        print("没有找到包含 'configuration' 键的元素")

    return result  


def map_player_id(platform_game_id, player_id, mappings):
    # Find the mapping for the platformGameId
    for mapping in mappings:
        if mapping['platformGameId'] == platform_game_id:
            # Return the corresponding esports player ID from participantMapping
            return mapping['participantMapping'].get(str(player_id), player_id)  # Return player_id if not found
    return player_id  # Return the original player_id if platformGameId is not found