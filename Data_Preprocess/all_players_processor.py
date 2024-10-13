import json
def all_players():
    total_players = {}
    def extract_players(file_path, players):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        for player in data:
            player_id = player['id']
            
            handle = player['handle']
            name = f"{player['first_name']} {player['last_name']}"
            
            if player_id not in players:
                players[player_id] = {
                    'handle': handle,
                    'name': name
                }
            else:
                # 处理handle
                if players[player_id]['handle'] != handle:
                    if isinstance(players[player_id]['handle'], list):
                        if handle not in players[player_id]['handle']:
                            players[player_id]['handle'].append(handle)
                    else:
                        players[player_id]['handle'] = [players[player_id]['handle'], handle]
                
                # 处理name
                if players[player_id]['name'] != name:
                    if isinstance(players[player_id]['name'], list):
                        if name not in players[player_id]['name']:
                            players[player_id]['name'].append(name)
                    else:
                        players[player_id]['name'] = [players[player_id]['name'], name]

        return players

    file_paths = [
        "../DATA/vct-international/esports-data/players.json",
        "../DATA/game-changers/esports-data/players.json",
        "../DATA/vct-challengers/esports-data/players.json"
    ]

    extract_players(file_paths[0], total_players)
    extract_players(file_paths[1], total_players)
    extract_players(file_paths[2], total_players)
    print(f"所有联赛的选手总数: {len(total_players)}")


    file_path = '../DATA/all_players.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(total_players, file, ensure_ascii=False, indent=4)

    print(f"所有选手已写入 {file_path}")

