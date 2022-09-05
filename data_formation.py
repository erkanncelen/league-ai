import pandas as pd
import numpy as np
from riot_api_connection import riot_api, game_to_df
import json

def game_report_data(game):
    api = riot_api()
    game = api.get_match_info_by_match_id(game)
    game_df = game_to_df(game)[[
        'championName',
        'championId',
        'teamId',
        'teamPosition',
        'kills',
        'assists',
        'deaths',
        'totalTimeSpentDead',
        'longestTimeSpentLiving',
        'goldEarned',
        'timeCCingOthers',
        'visionScore',
        'totalDamageDealtToChampions',
        'damageDealtToObjectives',
        'damageDealtToBuildings',
        'totalHealsOnTeammates',
        'totalDamageShieldedOnTeammates',
    ]]
    game_df = game_df.sort_values(by=['teamId','teamPosition'])
    champions = game_df['championName'].to_list()
    metrics = [
        'totalDamageDealtToChampions',
        'damageDealtToObjectives',
        'damageDealtToBuildings',
        'visionScore',
        'timeCCingOthers',
        'HealsAndShieldOnTeammates',
        'goldEarned',
    ]
    game_df['HealsAndShieldOnTeammates'] = game_df['totalHealsOnTeammates'] + game_df['totalDamageShieldedOnTeammates']
    metrics_normalized = []
    for metric in metrics:
        if game_df[metric].sum() == 0:
            game_df[f'{metric}_normalized'] = 0
        else:
            game_df[f'{metric}_normalized'] = (game_df[metric]/(game_df[metric].sum()))*100
        metrics_normalized.append(f'{metric}_normalized')
    chart_data = {}
    for i in range(len(game_df['championName'])):
        chart_data[i] = game_df.iloc[i][metrics_normalized]
    labels = ['Damage', 'Objectives', 'Buildings', 'Vision', 'CC', 'Heal & Shield', 'Gold']

    chart_data_js = []
    for i in range(len(chart_data)):
        chart_data_js.append(np.array2string(chart_data[i].values, separator=', '))

    return champions, chart_data_js, labels