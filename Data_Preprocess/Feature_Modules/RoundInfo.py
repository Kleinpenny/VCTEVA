def generate_round_summary(game_kda):
    round_started = []
    round_ended = []

    # Extract roundStarted and roundEnded events
    for item in game_kda:
        if 'roundStarted' in item:
            round_started.append({'roundNumber': item['roundStarted']['roundNumber'], 'startTime': item['metadata']['wallTime']})
        elif 'roundEnded' in item:
            round_ended.append({'roundNumber': item['roundEnded']['roundNumber'], 'endTime': item['metadata']['wallTime']})

    # Match roundStarted and roundEnded events
    rounds = []
    for i in range(len(round_ended)):
        rounds.append({
            'roundNumber': round_started[i]['roundNumber'],
            'startTime': round_started[i]['startTime'],
            'endTime': round_ended[i]['endTime']
        })

    # Handle the case where there is an extra roundStarted without a matching roundEnded
    if len(round_started) > len(round_ended):
        rounds.append({
            'roundNumber': round_started[-1]['roundNumber'],
            'startTime': round_started[-1]['startTime'],
            'endTime': 'Game End'
        })

    return rounds

def get_game_decided(game_kda):
    for item in game_kda:
        if 'gameDecided' in item:
            return item
    return ("Incomplete data")

def generate_round_details(game_kda):
    game_decided = get_game_decided(game_kda)
    if not game_decided:
        return "No gameDecided event found"

    spike_mode = game_decided['gameDecided']['spikeMode']
    completed_rounds = spike_mode['completedRounds']

    rounds_summary = generate_round_summary(game_kda)

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
        last_round.update({
            'attackingTeam': spike_mode['attackingTeam']['value'],
            'defendingTeam': spike_mode['defendingTeam']['value'],
            'winningTeam': spike_mode['winningTeam']['value'],
            # 'cause': 'Game End'
        })

    return detailed_rounds

def extract_configuration_details(game_kda):
    first_config = None
    for event in game_kda:
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
        team_info.append({"teamId": team_id, "playersInTeam": players_in_team})

    config_details ={
            "platformGameId":platformGameId,
            "selectedMap": selected_map,
            "teams": team_info
        }
    return config_details

def map_player_id(player_id, mapping):
    # Find the mapping for the platformGameId
    return mapping['participantMapping'].get(str(player_id), player_id)  # 

def map_team_id(team_id, mapping):
    # Find the team mapping for the platformGameId
    return mapping['teamMapping'].get(str(team_id))  # 

def generate_game_summary(game_kda,mapping_data):
    config_details = extract_configuration_details(game_kda)
    if isinstance(config_details, str):  # Handle error message
        return config_details

    round_details = generate_round_details(game_kda)
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
    for round in game_summary["round_details"]:
        round['attackingTeam']=map_team_id(round["attackingTeam"], mapping_data)
        round['defendingTeam']=map_team_id(round["defendingTeam"], mapping_data)
        round['winningTeam']=map_team_id(round["winningTeam"], mapping_data)

    return game_summary