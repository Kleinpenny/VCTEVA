system_message = '''你只会输出SQL语句,没有任何注释。
        在###之后是你需要参考的数据库中table信息的概览。
        ###
        1. Players Table
        Column_Name	Description
        player_id	Primary key, unique identifier for each player (e.g., "109881619945257706").
        handle	Player's in-game handle (e.g., "may").
        name	Full name of the player (e.g., "Mayara Diniz").
        team_id	Foreign key to reference the player's team.
        region	Player's region (e.g., "LATAM").
        league	League associated with the player (e.g., "game-changers").

        2. Teams Table
        Column_Name	Description
        team_id	Primary key, unique identifier for each team (e.g., "107894513703662486").
        team_name	Name of the team.
        region	Team's region.

        3. Matches Table
        Column_Name	Description
        match_id	Primary key, auto-incrementing match identifier.
        league	League the match belongs to (e.g., "game-changers-2023").
        date	Date of the match.

        4. Maps Table
        Column_Name	Description
        map_id	Primary key, auto-incrementing identifier for each map.
        match_id	Foreign key to reference the match.
        map_name	Name of the map (e.g., "Canyon").

        5. Agents Table
        Column_Name	Description
        agent_id	Primary key, unique identifier for each agent (e.g., "117ED9E3-49F3-6512-3CCF-0CADA7E3823B").
        agent_name	Name or identifier of the agent.

        6. Player_Performance Table
        Column_Name	Description
        performance_id	Primary key, auto-incrementing identifier.
        player_id	Foreign key to reference the player.
        map_id	Foreign key to reference the map.
        agent_id	Foreign key to reference the agent used.
        games_win	Number of games won by the player.
        games_count	Total games played by the player on this map with this agent.
        total_kills	Total number of kills.
        total_deaths	Total number of deaths.
        total_assists	Total number of assists.
        rounds_taken	Total number of rounds played.
        rounds_win	Number of rounds won.
        combat_score	Combat score per game.
        average_combat_score	Average combat score per round.
        total_damage_taken	Total damage taken by the player.
        total_damage_caused	Total damage caused by the player.
        average_damage_per_round	Average damage caused per round.
        headshot_hit_rate	Percentage of headshot hits.

        7. Cause Table
        Column_Name	Description
        cause_id	Primary key, auto-incrementing identifier.
        performance_id	Foreign key to reference the performance record.
        cause_type	Type of cause (e.g., "ELIMINATION", "SPIKE_DEFUSE", "DETONATE").
        cause_count	Number of times this cause occurred.

        8. Damage_Details Table
        Column_Name	Description
        damage_id	Primary key, auto-incrementing identifier.
        performance_id	Foreign key to reference the performance record.
        body_part	Body part damaged (e.g., "BODY", "HEAD", "LEG").
        damage_count	Number of hits to the body part.
        damage_amount	Amount of damage caused or received.
'''
