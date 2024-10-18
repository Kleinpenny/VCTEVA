import json
import mysql.connector
import pandas as pd
from mysql.connector import Error

# 连接数据库
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="vct",
        password="Leon1234",
        database="VCTEVA",  # 更改为你所使用的数据库
    )
    if connection.is_connected():
        print("Connected to MySQL server")

    # 使用新游标
    cursor = connection.cursor()

    # 读取 JSON 文件
    with open("../../DATA/all_players.json", "r") as file:
        data = json.load(file)

    # 1. 导入 Players 表的数据
    players_list = []
    for player_id, player_info in data.items():
        if isinstance(player_info, dict) and "handle" in player_info:
            handle = player_info.get("handle")
            if isinstance(handle, list):
                handle = ", ".join(handle)  # 将列表转换为字符串，使用逗号分隔
            elif not isinstance(handle, str):
                handle = str(handle) if handle is not None else None

            players_list.append(
                (
                    str(player_id),
                    handle,
                    str(player_info.get("name")) if player_info.get("name") else None,
                    (
                        str(player_info.get("team_id"))
                        if player_info.get("team_id")
                        else None
                    ),
                    (
                        str(player_info.get("region"))
                        if player_info.get("region")
                        else None
                    ),
                    (
                        str(player_info.get("league"))
                        if player_info.get("league")
                        else None
                    ),
                )
            )
    print(f"Inserting {len(players_list)} records into Players table...")
    cursor.executemany(
        """
        INSERT INTO Players (player_id, handle, name, team_id, region, league)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        players_list
    )
    connection.commit()

    # 2. 导入 Tournaments 表的数据
    tournaments_list = []
    for player_id, player_info in data.items():
        if isinstance(player_info, dict):
            for tournament_name, tournament_data in player_info.items():
                if tournament_name.startswith("vct-"):
                    tournaments_list.append((str(player_id), tournament_name))
    print(f"Inserting {len(tournaments_list)} records into Tournaments table...")
    cursor.executemany(
        """
        INSERT INTO Tournaments (player_id, tournament_name)
        VALUES (%s, %s)
        """,
        tournaments_list
    )
    connection.commit()

    # 3. 导入 Maps 表的数据
    maps_list = []
    for player_id, player_info in data.items():
        if isinstance(player_info, dict):
            for tournament_name, tournament_data in player_info.items():
                if tournament_name.startswith("vct-") and isinstance(
                    tournament_data, dict
                ):
                    cursor.execute(
                        """
                        SELECT tournament_id FROM Tournaments WHERE player_id=%s AND tournament_name=%s
                        """,
                        (str(player_id), tournament_name),
                    )
                    tournament_id = cursor.fetchone()
                    # print(f"Tournament ID for player {player_id}, tournament {tournament_name}: {tournament_id}")
                    if tournament_id:
                        for map_name in tournament_data.keys():
                            maps_list.append((tournament_id[0], map_name))
    print(f"Inserting {len(maps_list)} records into Maps table...")
    cursor.executemany(
        """
        INSERT INTO Maps (tournament_id, map_name)
        VALUES (%s, %s)
        """,
        maps_list
    )
    connection.commit()

    # 4. 导入 Agents 表的数据
    agents_list = []
    for player_id, player_info in data.items():
        if isinstance(player_info, dict):
            for tournament_name, tournament_data in player_info.items():
                if tournament_name.startswith("vct-") and isinstance(
                    tournament_data, dict
                ):
                    for map_name, map_data in tournament_data.items():
                        cursor.execute(
                            """
                            SELECT map_id FROM Maps WHERE tournament_id=(SELECT tournament_id FROM Tournaments WHERE player_id=%s AND tournament_name=%s) AND map_name=%s
                            """,
                            (str(player_id), tournament_name, map_name),
                        )
                        map_id = cursor.fetchone()
                        # print(f"Map ID for player {player_id}, tournament {tournament_name}, map {map_name}: {map_id}")
                        if map_id and isinstance(map_data, dict):
                            for agent_id, agent_data in map_data.items():
                                agents_list.append(
                                    (
                                        map_id[0],
                                        int(agent_data.get("games_win", 0)),
                                        int(agent_data.get("games_count", 0)),
                                    )
                                )
    print(f"Inserting {len(agents_list)} records into Agents table...")
    cursor.executemany(
        """
        INSERT INTO Agents (map_id, games_win, games_count)
        VALUES (%s, %s, %s)
        """,
        agents_list
    )
    connection.commit()

    # 5. 导入 PerformanceDetails 表的数据
    performance_list = []
    for player_id, player_info in data.items():
        if isinstance(player_info, dict):
            for tournament_name, tournament_data in player_info.items():
                if tournament_name.startswith("vct-") and isinstance(
                    tournament_data, dict
                ):
                    for map_name, map_data in tournament_data.items():
                        cursor.execute(
                            """
                            SELECT map_id FROM Maps WHERE tournament_id=(SELECT tournament_id FROM Tournaments WHERE player_id=%s AND tournament_name=%s) AND map_name=%s
                            """,
                            (str(player_id), tournament_name, map_name),
                        )
                        map_id = cursor.fetchone()
                        if cursor.with_rows:
                            cursor.fetchall()  # 清除未读结果
                        if map_id and isinstance(map_data, dict):
                            for agent_key, agent_data in map_data.items():
                                cursor.execute(
                                    """
                                    SELECT agent_id FROM Agents WHERE map_id=%s AND games_count=%s
                                    """,
                                    (map_id[0], int(agent_data.get("games_count", 0))),
                                )
                                agent_id = cursor.fetchone()
                                if cursor.with_rows:
                                    cursor.fetchall()  # 清除未读结果
                                if agent_id:
                                    for mode in ["attacking", "defending"]:
                                        if mode in agent_data:
                                            performance_list.append(
                                                (
                                                    agent_id[0],
                                                    mode,
                                                    int(
                                                        agent_data[mode].get("Kills", 0)
                                                    ),
                                                    int(
                                                        agent_data[mode].get(
                                                            "Deaths", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[mode].get(
                                                            "Assists", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[mode].get(
                                                            "rounds_taken", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[mode].get(
                                                            "rounds_win", 0
                                                        )
                                                    ),
                                                    json.dumps(
                                                        agent_data[mode].get(
                                                            "cause", {}
                                                        )
                                                    ),
                                                )
                                            )
    if performance_list:
        cursor.executemany(
            """
            INSERT INTO PerformanceDetails (agent_id, mode, kills, deaths, assists, rounds_taken, rounds_win, cause)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            performance_list
        )
        connection.commit()

    # 6. 导入 Summary 表的数据
    summary_list = []
    for player_id, player_info in data.items():
        if isinstance(player_info, dict):
            for tournament_name, tournament_data in player_info.items():
                if tournament_name.startswith("vct-") and isinstance(
                    tournament_data, dict
                ):
                    for map_name, map_data in tournament_data.items():
                        cursor.execute(
                            """
                            SELECT map_id FROM Maps WHERE tournament_id=(SELECT tournament_id FROM Tournaments WHERE player_id=%s AND tournament_name=%s) AND map_name=%s
                            """,
                            (str(player_id), tournament_name, map_name),
                        )
                        map_id = cursor.fetchone()
                        if cursor.with_rows:
                            cursor.fetchall()  # 清除未读结果
                        # print(f"Map ID for summary: {map_id}")
                        if map_id and isinstance(map_data, dict):
                            for agent_key, agent_data in map_data.items():
                                cursor.execute(
                                    """
                                    SELECT agent_id FROM Agents WHERE map_id=%s AND games_count=%s
                                    """,
                                    (map_id[0], int(agent_data.get("games_count", 0))),
                                )
                                agent_id = cursor.fetchone()
                                if cursor.with_rows:
                                    cursor.fetchall()  # 清除未读结果
                                # print(f"Agent ID for summary per game: {agent_id}")
                                if agent_id and "Summary" in agent_data:
                                    summary_list.append(
                                        (
                                            agent_id[0],
                                            float(
                                                agent_data["Summary"].get(
                                                    "CombatScore", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "AverageCombatScore", 0
                                                )
                                            ),
                                            int(
                                                agent_data["Summary"].get(
                                                    "Kills", 0
                                                )
                                            ),
                                            int(
                                                agent_data["Summary"].get(
                                                    "Deaths", 0
                                                )
                                            ),
                                            int(
                                                agent_data["Summary"].get(
                                                    "Assists", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "KPR", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "DPR", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "totalDamageTaken", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "totalDamageCaused", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "AverageDamagePerRound", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "AverageDamageTakenPerRound", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "DDDelta", 0
                                                )
                                            ),
                                            float(
                                                agent_data["Summary"].get(
                                                    "headshotHitRate", 0
                                                )
                                            ),
                                        )
                                    )
    print(f"Inserting {len(summary_list)} records into Summary table...")
    if summary_list:
        cursor.executemany(
            """
            INSERT INTO Summary (agent_id, combat_score, average_combat_score, kills, deaths, assists, kpr, dpr, total_damage_taken, total_damage_caused, average_damage_per_round, average_damage_taken_per_round, dddelta, headshot_hit_rate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            summary_list
        )
        connection.commit()

    # 7. 导入 DamageDetails 表的数据
    damage_list = []
    for player_id, player_info in data.items():
        if isinstance(player_info, dict):
            for tournament_name, tournament_data in player_info.items():
                if tournament_name.startswith("vct-") and isinstance(
                    tournament_data, dict
                ):
                    for map_name, map_data in tournament_data.items():
                        cursor.execute(
                            """
                            SELECT map_id FROM Maps WHERE tournament_id=(SELECT tournament_id FROM Tournaments WHERE player_id=%s AND tournament_name=%s) AND map_name=%s
                            """,
                            (str(player_id), tournament_name, map_name),
                        )
                        map_id = cursor.fetchone()
                        if cursor.with_rows:
                            cursor.fetchall()  # 清除未读结果
                        print(f"Map ID for damage details: {map_id}")
                        if map_id and isinstance(map_data, dict):
                            for agent_key, agent_data in map_data.items():
                                cursor.execute(
                                    """
                                    SELECT agent_id FROM Agents WHERE map_id=%s AND games_count=%s
                                    """,
                                    (map_id[0], int(agent_data.get("games_count", 0))),
                                )
                                agent_id = cursor.fetchone()
                                if cursor.with_rows:
                                    cursor.fetchall()  # 清除未读结果
                                print(f"Agent ID for damage details: {agent_id}")
                                if agent_id:
                                    for damage_type in [
                                        "damageCausedPerGame",
                                        "damageReceivedPerGame",
                                    ]:
                                        if damage_type in agent_data:
                                            damage_list.append(
                                                (
                                                    agent_id[0],
                                                    damage_type[
                                                        :20
                                                    ],  # 限制类型字段的长度为20个字符以内，避免过长
                                                    int(
                                                        agent_data[damage_type].get(
                                                            "HEAD_count", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[damage_type].get(
                                                            "HEAD_amount", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[damage_type].get(
                                                            "BODY_count", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[damage_type].get(
                                                            "BODY_amount", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[damage_type].get(
                                                            "LEG_count", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[damage_type].get(
                                                            "LEG_amount", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[damage_type].get(
                                                            "GENERAL_count", 0
                                                        )
                                                    ),
                                                    int(
                                                        agent_data[damage_type].get(
                                                            "GENERAL_amount", 0
                                                        )
                                                    ),
                                                )
                                            )
    print(f"Inserting {len(damage_list)} records into DamageDetails table...")
    if damage_list:
        cursor.executemany(
            """
            INSERT INTO DamageDetails (agent_id, type, head_count, head_amount, body_count, body_amount, leg_count, leg_amount, general_count, general_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            damage_list,
        )
        connection.commit()

    # 提交更改并关闭连接
    cursor.close()
    connection.close()

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
