import json

with open("../DATA/all_players.json") as f:
    data = json.load(f)

MAPNAME = ["Infinity", "Ascent", "Duality", "Foxtrot", "Canyon", "Triad", "Port", "Jam", "Pitt", "Bonsai", "Juliett"]

for player_id in data:
    player = data[player_id]
    for MAP in MAPNAME:
        if MAP in player["game-changers-2023"]:
            game_data = player["game-changers-2023"][MAP]
            if "SummaryPerGame" in game_data:
                if "name" in game_data["SummaryPerGame"]:
                    if game_data["SummaryPerGame"]["name"] == "Houssein":
                        print(game_data["SummaryPerGame"]["KPR"])