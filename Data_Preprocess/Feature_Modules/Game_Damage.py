import pandas as pd


class DataExtractorFactory:
    @staticmethod
    def create_extractor(data_type):
        if data_type == 'team':
            return TeamInfoExtractor()
        elif data_type == 'damage':
            return DamageEventExtractor()
        elif data_type == 'player':
            return PlayerInfoExtractor()
        else:
            raise ValueError("Unknown data type")


class PlayerInfoExtractor:
    def extract(self, json_data):
        temp_player_info = json_data[['id', 'first_name', 'last_name']]
        return pd.DataFrame(temp_player_info)


class TeamInfoExtractor:
    def extract(self, json_data):
        team_info_json = json_data['configuration'].dropna().iloc[0]
        MAP = team_info_json['selectedMap']['fallback']['displayName']
        team_player_list = [
            {'PlayerID': player['value'], 'TeamID': team['teamId']['value'], 'Map': MAP}
            for team in team_info_json['teams']
            for player in team['playersInTeam']
        ]
        return pd.DataFrame(team_player_list)


class DamageEventExtractor:
    def extract(self, file_json):
        df_damage_cleaned = self.clean_damage_data(file_json['damageEvent'])
        TOTAL_ROUND_NUM = self.get_total_round_num(file_json)

        combined_df = self.total_damage_stat(df_damage_cleaned, TOTAL_ROUND_NUM)
        combined_df['headshotHitRate'] = self.without_general_damage_stat(df_damage_cleaned, TOTAL_ROUND_NUM)

        add_df = self.get_player_add_stats(file_json)
        result_df = pd.merge(add_df, combined_df, right_on='causerID', left_on='PlayerID', how='inner') \
            .drop(columns=['causerID', 'victimID'])

        return result_df

    def clean_damage_data(self, damage_events):
        df_damage_cleaned = pd.DataFrame(damage_events).dropna()
        df_damage_cleaned[['causerID', 'victimID', 'damageAmount']] = df_damage_cleaned['damageEvent'].apply(
            lambda x: pd.Series({
                'causerID': x.get('causerId', {}).get('value', None),
                'victimID': x.get('victimId', {}).get('value', None),
                'damageAmount': x.get('damageAmount', 0)
            })
        )
        return df_damage_cleaned

    def total_damage_stat(self, damage_df, total_round_num):
        damage_taken_by_victim = damage_df.groupby('victimID')['damageAmount'].sum().reset_index(
            name='totalDamageTaken')
        damage_caused_by_causer = damage_df.groupby('causerID')['damageAmount'].sum().reset_index(
            name='totalDamageCaused')

        combined_df = pd.merge(damage_taken_by_victim, damage_caused_by_causer, left_on='victimID', right_on='causerID',
                               how='inner')

        combined_df['AverageDamagePerRound'] = combined_df['totalDamageCaused'] / total_round_num
        combined_df['AverageDamageTakenPerRound'] = combined_df['totalDamageTaken'] / total_round_num
        combined_df['DDDelta'] = combined_df['totalDamageCaused'] - combined_df['totalDamageTaken']

        combined_df = combined_df.map(format_float)  # 将所有浮点数进行格式化
        return combined_df

    def without_general_damage_stat(self, df_damage_cleaned, total_round_num):
        df_without_location_general = df_damage_cleaned[
            df_damage_cleaned['damageEvent'].apply(lambda x: x['location'] != 'GENERAL')
        ]

        df_without_location_general.loc[:, ['causerID', 'isHeadShot']] = df_without_location_general['damageEvent'].apply(
            lambda x: pd.Series({
                'causerID': x.get('causerId', {}).get('value', None),
                'isHeadShot': x.get('location') == 'HEAD'
            })
        )

        headshot_hits = df_without_location_general.groupby('causerID')['isHeadShot'].sum().reset_index(
            name='headshotHits')
        total_hits = df_without_location_general.groupby('causerID').size().reset_index(name='totalHits')

        player_hs_stats = pd.merge(headshot_hits, total_hits, on='causerID', how='outer')
        player_hs_stats['headshotHitRate'] = (
                player_hs_stats['headshotHits'] / player_hs_stats['totalHits'] * 100).round(2)

        return player_hs_stats['headshotHitRate']

    def get_total_round_num(self, file_json):
        return file_json['gamePhase'].dropna().iloc[-1]['roundNumber'] + 1

    def get_player_add_stats(self, file_json):
        snapshot_data = file_json['snapshot'].dropna()
        player_result_data = snapshot_data.iloc[-1]['players']

        player_add_data_list = [
            {
                'PlayerID': player['playerId']['value'],
                'CombatScore': player['scores']['combatScore']['totalScore'],
                'AverageCombatScore': format_float(
                    player['scores']['combatScore']['totalScore'] / self.get_total_round_num(file_json), 2),
                'Kills': player.get('kills', 0),
                'Deaths': player.get('deaths', 0),
                'Assists': player.get('assists', 0),
                '+-': player.get('kills', 0) - player.get('deaths', 0),
                'KPR': format_float(player.get('kills', 0) / self.get_total_round_num(file_json), 2),
                'DPR': format_float(player.get('deaths', 0) / self.get_total_round_num(file_json), 2),
            }
            for player in player_result_data
        ]

        return pd.DataFrame(player_add_data_list)


def format_float(value, decimal_places=2):
    return round(value, decimal_places)

def main(game_file_path):
    # 加载 JSON 文件
    # output_file.json 为val导出的 GAME_ID = "val:6ac110c8-4048-421e-8b2b-86d3ac6c72ed"的所有数据
    file_json = pd.read_json(game_file_path)
    # 提取不同类型的数据
    team_info_extractor = DataExtractorFactory.create_extractor('team')
    team_info_df = team_info_extractor.extract(file_json)
    damage_event_extractor = DataExtractorFactory.create_extractor('damage')
    damage_event_df = damage_event_extractor.extract(file_json)
    return damage_event_df

