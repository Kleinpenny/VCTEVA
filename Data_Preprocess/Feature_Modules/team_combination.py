AGENT_GUID_TO_AGENT_AND_ROLE = {
  "320B2A48-4D9B-A075-30F1-1F93A9B638FA": {"agent_name": "Brimstone", "role": "Controller"},
  "707EAB51-4836-F488-046A-CDA6BF494859": {"agent_name": "Viper", "role": "Controller"},
  "8E253930-4C05-31DD-1B6C-968525494517": {"agent_name": "Omen", "role": "Controller"},
  "5F8D3A7F-467B-97F3-062C-13ACF203C006": {"agent_name": "Jett", "role": "Duelist"},
  "1DBF2EDD-4729-0984-3115-DAA5EED44993": {"agent_name": "Jett", "role": "Duelist"},
  "1E58DE9C-4950-5125-93E9-A0AEE9F98746": {"agent_name": "Phoenix", "role": "Duelist"},
  "A3BFB853-43B2-7238-A4F1-AD90E9E46BCC": {"agent_name": "Reyna", "role": "Duelist"},
  "6F2A04CA-43E0-BE17-7F36-B3908627744D": {"agent_name": "Raze", "role": "Duelist"},
  "7F37F0E6-44D3-7276-8B4A-AB56D8DDC5A3": {"agent_name": "Yoru", "role": "Duelist"},
  "7F94D92C-4234-0A36-9646-3A87EB8B5C89": {"agent_name": "Yoru", "role": "Duelist"},
  "41FB69C1-4189-7B37-F117-BCAF1E96F1BF": {"agent_name": "Sova", "role": "Initiator"},
  "9F0D8BA9-4140-B941-57D3-A7AD57C6B417": {"agent_name": "Breach", "role": "Initiator"},
  "EB93336A-449B-9C1B-0A54-A891F7921D69": {"agent_name": "Skye", "role": "Initiator"},
  "ADD6443A-41BD-E414-F6AD-E58D267F4E95": {"agent_name": "KAY/O", "role": "Initiator"},
  "601DBBE7-43CE-BE57-2A40-4ABD24953621": {"agent_name": "KAY/O", "role": "Initiator"},
  "A4D4B33D-8F36-5BD5-97E8-DF0F4078C0B1": {"agent_name": "Fade", "role": "Initiator"},
  "DADE69B4-4F5A-8528-247B-219E5A1FACD6": {"agent_name": "Fade", "role": "Initiator"},
  "BB2A4828-46EB-8CD1-E765-15848195D751": {"agent_name": "Sage", "role": "Sentinel"},
  "569FDD95-4D10-43AB-CA70-79BECC718B46": {"agent_name": "Sage", "role": "Sentinel"},
  "117ED9E3-49F3-6512-3CCF-0C21417D5BF2": {"agent_name": "Cypher", "role": "Sentinel"},
  "117ED9E3-49F3-6512-3CCF-0CADA7E3823B": {"agent_name": "Cypher", "role": "Sentinel"},
  "E370FA57-4757-3604-3648-499E1F642D3F": {"agent_name": "Killjoy", "role": "Sentinel"},
  "22697A3D-45BF-8DD7-4FEC-84A9E28C69D7": {"agent_name": "Chamber", "role": "Sentinel"},
  "95B78ED7-4637-86D9-7E41-71BA8C293152": {"agent_name": "Harbor", "role": "Controller"},
  "BB2E7D46-4F11-EC8A-1FAA-C9A78D79C650": {"agent_name": "Neon", "role": "Duelist"},
  "41FDC046-4F00-246C-20D1-5C9F0E6B0175": {"agent_name": "Astra", "role": "Controller"},
  "E22049B7-8B92-FA85-EA86-F5D1F44B6A8F": {"agent_name": "Gekko", "role": "Initiator"},
  "D098A1F1-362E-5E59-BCFB-218A8C4F93FE": {"agent_name": "Deadlock", "role": "Sentinel"},
  "CC8B64C8-4B25-4FF9-6E7F-37B4DA43D235": {"agent_name": "Deadlock", "role": "Sentinel"},
  "ED2666F8-486F-5459-B79A-6E645C02E0B5": {"agent_name": "Iso", "role": "Duelist"},
  "0E38B510-41A8-5780-5E8F-568B2A4F2D6C": {"agent_name": "Iso", "role": "Duelist"},
  "F94C3B30-42BE-E959-889C-5AA313DBA261": {"agent_name": "Agent 22", "role": "Initiator"}
}

#LEAGUE = "vct-challengers"
LEAGUE = "vct-international"
YEAR = 2024

"""
unique key: team combination
- league
- map
- enemy combination
- role(defending or attacking)
- winning_round_count
- round_count
- winning_game_count
- game_count
"""

import json
from pathlib import Path
import pandas as pd

def generate_round_summary(data):
    round_started = []
    round_ended = []

    # Extract roundStarted and roundEnded events
    for item in data:
        if 'roundStarted' in item:
            round_started.append({'roundNumber': item['roundStarted']['roundNumber'], 'startTime': item['metadata']['wallTime']})
        elif 'roundEnded' in item:
            round_ended.append({'roundNumber': item['roundEnded']['roundNumber'], 'endTime': item['metadata']['wallTime']})

    # Match roundStarted and roundEnded events
    rounds = []
    for i in range(len(round_ended)):
        if i < len(round_started):
            rounds.append({
                'roundNumber': round_started[i]['roundNumber'],
                'startTime': round_started[i]['startTime'],
                'endTime': round_ended[i]['endTime']
            })
        else: break

    # Handle the case where there is an extra roundStarted without a matching roundEnded
    if len(round_started) > len(round_ended):
        rounds.append({
            'roundNumber': round_started[-1]['roundNumber'],
            'startTime': round_started[-1]['startTime'],
            'endTime': 'Game End'
        })

    return rounds

def get_game_decided(data):
    for item in data:
        if 'gameDecided' in item:
            return item
    return None

def generate_round_details(data):
    game_decided = get_game_decided(data)
    if not game_decided:
        return "No gameDecided event found"
    spike_mode = game_decided['gameDecided']['spikeMode']
    completed_rounds = spike_mode['completedRounds']

    rounds_summary = generate_round_summary(data)

    # Combine round summary with additional round details
    detailed_rounds = []
    for round_info in rounds_summary:
        round_number = round_info['roundNumber']
        # Find corresponding round in completedRounds
        matching_round = next((r for r in completed_rounds if r['roundNumber'] == round_number), None)

        if matching_round:
            round_info.update({
                'attackingTeam': matching_round['spikeModeResult']['attackingTeam']['value'],
                'defendingTeam': matching_round['spikeModeResult']['defendingTeam']['value'],
                'winningTeam': matching_round['winningTeam']['value'],
                # 'cause': matching_round['spikeModeResult']['cause']
            })

        detailed_rounds.append(round_info)

    # Set winning team for the last round if necessary
    if len(rounds_summary) > len(completed_rounds):
        last_round = detailed_rounds[-1]
        #print(spike_mode)
        if spike_mode.get("winningTeam") and spike_mode.get("attackingTeam") and spike_mode.get("defendingTeam"):
            last_round.update({
                'attackingTeam': spike_mode['attackingTeam']['value'],
                'defendingTeam': spike_mode['defendingTeam']['value'],
                'winningTeam': spike_mode['winningTeam']['value'],
                # 'cause': 'Game End'
            })
        else:
            #print(detailed_rounds)
            detailed_rounds.pop()


    return detailed_rounds

def extract_configuration_details(data):
    first_config = None
    for event in data:
        if 'configuration' in event:
            first_config = event
            break

    if not first_config:
        return "No configuration event found"

    platformGameId = event["platformGameId"]
    # Extract selected map
    selected_map = first_config["configuration"]["selectedMap"]["fallback"]["displayName"]

    # Extract team ID and players in team
    teams = first_config["configuration"]["teams"]
    team_info = []
    for team in teams:
        team_id = team["teamId"]["value"]
        players_in_team = [player["value"] for player in team["playersInTeam"]]
        player_to_agent = {}
        for player in first_config["configuration"]['players']:
            player_to_agent[player['playerId']['value']] = AGENT_GUID_TO_AGENT_AND_ROLE[player['selectedAgent']['fallback']['guid']]['agent_name']
        team_info.append({"teamId": team_id, "playersInTeam": players_in_team, "playerToAgent": player_to_agent})

    # Extract current round number and attacking team value
    current_round = first_config["configuration"]["spikeMode"]["currentRound"]
    attacking_team_value = first_config["configuration"]["spikeMode"]["attackingTeam"]["value"]

    return {
        "platformGameId":platformGameId,
        "selectedMap": selected_map,
        "teams": team_info,
        "currentRound": current_round,
        "attackingTeam": attacking_team_value
    }

# Helper function to map player ID using the platformGameId and participantMapping
def map_player_id(player_id, mapping):
    # Find the mapping for the platformGameId
    return mapping['participantMapping'].get(str(player_id), player_id)  #

def map_team_id(team_id, mapping):
    # Find the mapping for the platformGameId
    return mapping['teamMapping'].get(str(team_id))  #

def generate_game_summary(data,mapping_data):
    config_details = extract_configuration_details(data)
    if isinstance(config_details, str):  # Handle error message
        return config_details

    round_details = generate_round_details(data)
    if isinstance(round_details, str):  # Handle error message
        return round_details

    # Combine all details into a single JSON
    game_summary = {
        "platformGameId":config_details["platformGameId"],
        "selectedMap": config_details["selectedMap"],
        "teams": config_details["teams"],
        "round_details": round_details
    }
    for team in game_summary["teams"]:
        team["teamId"]= map_team_id(team["teamId"], mapping_data)
        for i in range(len(team["playersInTeam"])):
            team["playersInTeam"][i] = map_player_id(team["playersInTeam"][i], mapping_data)
        for i in list(team["playerToAgent"].keys()):
            player_id = map_player_id(i, mapping_data)
            team["playerToAgent"][player_id] = team["playerToAgent"][i]
            del team["playerToAgent"][i]

    filtered_rounds = []

    for round in game_summary["round_details"]:
        if round.get("winningTeam") and round.get("attackingTeam") and round.get("defendingTeam"):
            round['attackingTeam'] = map_team_id(round["attackingTeam"], mapping_data)
            round['defendingTeam'] = map_team_id(round["defendingTeam"], mapping_data)
            round['winningTeam'] = map_team_id(round["winningTeam"], mapping_data)
            filtered_rounds.append(round)

    # Assign the filtered rounds back to game_summary
    game_summary["round_details"] = filtered_rounds
    return game_summary

def generate_df_with_summaries(data):
    rows = {}

    # Initialize list to store all rows for the dataframe

    # Iterate through each game in data
    for game in data:
        if not isinstance(game, dict): continue
        selected_map = game['selectedMap']  # Get map name

        # Create a dictionary for easier access to teams by teamId
        teams = {team['teamId']: team for team in game['teams']}

        # Create rows for both teams
        team_to_combination = {}
        for team_id in teams:
            team = teams[team_id]

            # Get the agents for both teams
            team_combination = [team['playerToAgent'][player_id] for player_id in team['playersInTeam']]
            team_combination.sort()

            team_to_combination[team_id] = " ".join(team_combination)

            # Iterate through each round in the game
        if game.get("round_details") is None or len(game["round_details"]) == 0: continue
        for round_info in game['round_details']:
            winning_team_id = round_info['winningTeam']
            losing_team_id = ""
            for team_id in teams:
                if team_id != winning_team_id:
                    losing_team_id = team_id
                    break
            attacking_team = round_info['attackingTeam']
            defending_team = round_info['defendingTeam']

            # Track winning rounds for each team
            tmp_key0 = (team_to_combination[winning_team_id], team_to_combination[losing_team_id], selected_map, "attacking" if winning_team_id == attacking_team else "defending")
            tmp_key1 = (team_to_combination[losing_team_id], team_to_combination[winning_team_id], selected_map,
                        "attacking" if losing_team_id == attacking_team else "defending")
            if tmp_key0 not in rows:
                rows[tmp_key0] = [0,0]
            rows[tmp_key0][0] += 1
            rows[tmp_key0][1] += 1

            if tmp_key1 not in rows:
                rows[tmp_key1] = [0, 0]
            rows[tmp_key1][0] += 1

            # Append the data to rows
    df = pd.DataFrame(
        [(k[0], k[1], k[2], k[3], LEAGUE, YEAR, v[0], v[1]) for k, v in rows.items()],
        columns=['team_combination', 'enemy_team_combination', 'map', 'role', 'league', 'year', 'round_number', 'winning_round_number']
    )
    df.to_csv(f'{LEAGUE}_{YEAR}.csv', index=False)
    return df

if __name__ == '__main__':
    # Define the directory containing the files
    directory = Path(f"/Users/yi/Projects/Python/VCTEVA/DATA/{LEAGUE}/games/{YEAR}")

    game_summaries = []
    count = 1

    # Iterate over all JSON files in the directory
    for json_file in directory.glob("*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print(f"Error at line {e.lineno}, column {e.colno}, character {e.pos}")
            continue
        except FileNotFoundError:
            print(f"File {json_file} not found.")
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue
        mapping_file_path = f"/Users/yi/Projects/Python/VCTEVA/DATA/{LEAGUE}/esports-data/mapping_data_v2.json"

        with open(mapping_file_path, 'r') as mf:
            mapping_data = json.load(mf)

        for mapping in mapping_data:
            if mapping['platformGameId'] == data[1]['platformGameId']:
                mapping_data = mapping

        game_summary = generate_game_summary(data, mapping_data)
        if count == 1: print(game_summary)

        count += 1
        game_summaries.append(game_summary)

    with open(f'{LEAGUE}_{YEAR}_game_summaries.json', 'w') as json_file:
        json.dump(game_summaries, json_file, indent=4)

    with open(f'{LEAGUE}_{YEAR}_game_summaries.json', 'r') as f:
        data = json.load(f)

    generate_df_with_summaries(data)


"""
    with open("/Users/yi/Projects/Python/VCTEVA/DATA/vct-challengers/games/2024/val:c664f056-7e6a-45f2-8693-7694cfbcf509.json", 'r') as f:
        data = json.load(f)
    mapping_file_path = "/Users/yi/Projects/Python/VCTEVA/DATA/vct-challengers/esports-data/mapping_data_v2.json"

    with open(mapping_file_path, 'r') as mf:
        mapping_data = json.load(mf)

    for mapping in mapping_data:
        if mapping['platformGameId'] == data[1]['platformGameId']:
            mapping_data = mapping

    game_summary = generate_game_summary(data, mapping_data)
    if count == 1: print(game_summary)

    count += 1
    game_summaries.append(game_summary)
"""

