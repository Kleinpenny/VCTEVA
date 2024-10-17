from .RoundInfo import generate_game_summary, map_player_id, map_team_id
import json
import pandas as pd


# Initialize player KDA if not already done
def initialize_player_kda(
    player_id, kda_per_player_list, platform_game_id, selected_map
):
    existing_player = next(
        (player for player in kda_per_player_list if player["PlayerId"] == player_id),
        None,
    )
    if existing_player is None:
        kda_per_player_list.append(
            {
                "PlayerId": player_id,
                "GameId": platform_game_id,
                "Map": selected_map,
                "RoundInfo": [],
            }
        )
    return next(
        player for player in kda_per_player_list if player["PlayerId"] == player_id
    )


def get_round_number_from_event(rounds_summary, event):
    wall_time = event["metadata"]["wallTime"]

    for round_info in rounds_summary:
        if round_info["endTime"] == "Game End":
            if round_info["startTime"] <= wall_time:
                return round_info["roundNumber"]
        elif round_info["startTime"] <= wall_time <= round_info["endTime"]:
            return round_info["roundNumber"]
    return None


# Helper function to map player ID using the platformGameId and participantMapping
def map_player_id(player_id, mapping):
    # Find the mapping for the platformGameId

    # Return the corresponding esports player ID from participantMapping
    return mapping["participantMapping"].get(
        str(player_id), player_id
    )  # Return player_id if not found


def generate_kda_per_player(game_data, mapping_data, game_summary):

    # Ensure rounds_summary is a list of dictionaries
    rounds_summary = game_summary["round_details"]
    platform_game_id = game_summary["platformGameId"]
    selected_map = game_summary["selectedMap"]

    # Initialize a list to store KDA information for each player
    kda_per_player_list = []

    # Iterate through events to collect KDA information
    for event in game_data:
        if "playerDied" in event:
            round_number = get_round_number_from_event(rounds_summary, event)

            if round_number is None:
                continue

            player_died_data = event["playerDied"]
            deceased_id = player_died_data.get("deceasedId", {}).get("value")
            killer_id = player_died_data.get("killerId", {}).get("value")

            # Map deceased and killer IDs using the participantMapping
            mapped_deceased_id = (
                map_player_id(deceased_id, mapping_data) if deceased_id else None
            )
            mapped_killer_id = (
                map_player_id(killer_id, mapping_data) if killer_id else None
            )

            if mapped_deceased_id:
                deceased_player = initialize_player_kda(
                    mapped_deceased_id,
                    kda_per_player_list,
                    platform_game_id,
                    selected_map,
                )
                deceased_player["RoundInfo"].append(
                    {"RoundNumber": round_number, "Deaths": 1, "Kills": 0, "Assists": 0}
                )

            if mapped_killer_id:
                killer_player = initialize_player_kda(
                    mapped_killer_id,
                    kda_per_player_list,
                    platform_game_id,
                    selected_map,
                )
                killer_player["RoundInfo"].append(
                    {"RoundNumber": round_number, "Deaths": 0, "Kills": 1, "Assists": 0}
                )

            # Check for assistants and update their assist counts
            if "assistants" in event["playerDied"]:
                for assistant in event["playerDied"]["assistants"]:
                    assistant_id = assistant["assistantId"]["value"]
                    mapped_assistant_id = map_player_id(assistant_id, mapping_data)
                    assistant_player = initialize_player_kda(
                        mapped_assistant_id,
                        kda_per_player_list,
                        platform_game_id,
                        selected_map,
                    )
                    assistant_player["RoundInfo"].append(
                        {
                            "RoundNumber": round_number,
                            "Deaths": 0,
                            "Kills": 0,
                            "Assists": 1,
                        }
                    )

    return kda_per_player_list


def merge_kda_per_round(game_data, mapping_data, game_summary):
    kda_per_player_list = generate_kda_per_player(game_data, mapping_data, game_summary)
    # merge kda info
    for player in kda_per_player_list:
        filtered_round_info = [round_info for round_info in player["RoundInfo"]]
        merged_rounds = {}
        for round_info in filtered_round_info:
            round_number = round_info["RoundNumber"]
            if round_number not in merged_rounds:
                merged_rounds[round_number] = {
                    "RoundNumber": round_number,
                    "Kills": 0,
                    "Deaths": 0,
                    "Assists": 0,
                }
            merged_rounds[round_number]["Kills"] += round_info.get("Kills", 0)
            merged_rounds[round_number]["Deaths"] += round_info.get("Deaths", 0)
            merged_rounds[round_number]["Assists"] += round_info.get("Assists", 0)

        # Add a summary KDA for each player
        total_kills = sum(info["Kills"] for info in merged_rounds.values())
        total_deaths = sum(info["Deaths"] for info in merged_rounds.values())
        total_assists = sum(info["Assists"] for info in merged_rounds.values())
        player["RoundInfo"] = [
            info
            for info in merged_rounds.values()
            if not (info["Kills"] == 0 and info["Deaths"] == 0 and info["Assists"] == 0)
        ]
        player["Summary"] = {
            "Kills": total_kills,
            "Deaths": total_deaths,
            "Assists": total_assists,
        }
    return kda_per_player_list


def find_player_by_id_and_team(player_data, id_value, home_team_id_value):
    for player in player_data:
        if player["id"] == id_value and player["home_team_id"] == home_team_id_value:
            return player
    return None


def find_team_by_player(game_summary, player_id):
    for team in game_summary["teams"]:
        if player_id in team["playersInTeam"]:
            return team["teamId"]
    return None


def merge_player_data(game_data, mapping_data, player_data, game_summary):
    kda_per_player_list = merge_kda_per_round(game_data, mapping_data, game_summary)
    # Load player data

    # Normalize and clean player data
    for player_kda in kda_per_player_list:
        player_kda["team_id"] = find_team_by_player(
            game_summary, player_kda["PlayerId"]
        )

        player_info = find_player_by_id_and_team(
            player_data, player_kda["PlayerId"], player_kda["team_id"]
        )
        if player_info is not None:
            player_kda["handle"] = player_info["handle"]
            player_kda["first_name"] = player_info["first_name"]
            player_kda["last_name"] = player_info["last_name"]
        else:
            player_kda["handle"] = ""
            player_kda["first_name"] = ""
            player_kda["last_name"] = ""
    return kda_per_player_list


def merge_team_league_data(
    data, mapping_data, player_data, teams, leagues, game_summary
):
    kda_per_player_list = merge_player_data(
        data, mapping_data, player_data, game_summary
    )

    # 确保 kda_per_player_list 中有 'team_id' 列
    for player_kda in kda_per_player_list:
        if 'team_id' not in player_kda:
            player_kda['team_id'] = ""  # 或者其他合适的默认值

    # Create a dictionary to map league_id to league details
    league_dict = {league["league_id"]: league for league in leagues}

    # List to hold the new matched data
    matched_data = []

    # Match teams with their corresponding leagues
    for team in teams:
        home_league_id = team["home_league_id"]
        if home_league_id in league_dict:
            league = league_dict[home_league_id]
            matched_data.append(
                {
                    "team_id": team["id"],
                    "acronym": team["acronym"],
                    "league_id": league["league_id"],
                    "team_name": team["name"],
                    "league_region": league["region"],
                    "league_name": league["name"],
                }
            )

    # Remove duplicates and keep only the first match for each team_id
    matched_data_df = pd.DataFrame(matched_data).drop_duplicates(
        subset="team_id", keep="first"
    )

    matched_data_df = matched_data_df[matched_data_df['team_id'] != ""]

    # Merge team and league data with KDA data
    kda_df = pd.DataFrame(kda_per_player_list)
    # 确保 kda_df 包含 'team_id' 列
    if 'team_id' not in kda_df.columns:
        kda_df['team_id'] = ""  # 如果没有 team_id 列，添加空字符串作为默认值
    kda_df = kda_df[kda_df['team_id'] != ""]
    final_df = kda_df.merge(
        matched_data_df, left_on="team_id", right_on="team_id", how="left"
    )

    # Convert the merged DataFrame back to a list of dictionaries
    kda_per_player_list = final_df.to_dict(orient="records")

    return kda_per_player_list


def main(
    game_file_path,
    mapping_file_path,
    player_file_path,
    team_file_path,
    league_file_path,
):
    # Read files first
    with open(game_file_path, "r") as f:
        game_data = json.load(f)

    # load mapping
    with open(mapping_file_path, "r") as mf:
        mapping_data = json.load(mf)

    for mapping in mapping_data:
        if mapping["platformGameId"] == game_data[1]["platformGameId"]:
            mapping_data = mapping

    # load player
    with open(player_file_path, "r") as f:
        player_data = json.load(f)

    # Load the team data
    with open(team_file_path, "r") as team_file:
        teams = json.load(team_file)

    # Load the league data
    with open(league_file_path, "r") as league_file:
        leagues = json.load(league_file)

    game_summary = generate_game_summary(game_data, mapping_data)

    player_league_data = merge_team_league_data(
        game_data, mapping_data, player_data, teams, leagues, game_summary
    )

    round_details = game_summary["round_details"]
    # Extract team mapping from mapping_data

    # Add round details to the KDA data
    for player in player_league_data:
        player_round_info = player["RoundInfo"]
        existing_round_numbers = {
            round_info["RoundNumber"] for round_info in player_round_info
        }

        # Find the player's team ID based on the mapping

        # Iterate through all round details and update or add information, excluding the last round
        for round_detail in round_details:
            round_number = round_detail["roundNumber"]

            role = (
                "attacking"
                if player["team_id"] == round_detail["attackingTeam"]
                else "defending"
            )
            result = (
                "win" if player["team_id"] == round_detail["winningTeam"] else "lose"
            )
            cause = round_detail['cause']
            # Update existing rounds
            for round_info in player_round_info:
                if round_info["RoundNumber"] == round_number:
                    round_info["role"] = role
                    round_info["result"] = result
                    round_info["cause"] = cause
                    break
                else:
                    # Add missing rounds with KDA as 0 if not present
                    if round_number not in existing_round_numbers:
                        player_round_info.append(
                            {
                                "RoundNumber": round_number,
                                "Kills": 0,
                                "Deaths": 0,
                                "Assists": 0,
                                "role": role,
                                "result": result,
                                "cause": cause,
                            }
                        )
                        existing_round_numbers.add(round_number)

        # Add game result to summary
        player_round_info.sort(key=lambda x: x["RoundNumber"])
        last_round = round_details[-1]
        final_result = (
            "win" if player["team_id"] == last_round["winningTeam"] else "lose"
        )
        player["Summary"]["result"] = final_result
    return player_league_data

