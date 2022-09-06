import pandas as pd
import numpy as np
from riot_api_connection import riot_api
import json

def game_to_df(game):
    columns = pd.DataFrame.from_dict(game['info']['participants'][0]).set_index('participantId').columns
    df = pd.DataFrame(columns=columns)
    for item in game['info']['participants']:
        temp = pd.DataFrame.from_dict(item).set_index('participantId')[:1]
        df = pd.concat([df, temp])
    return df

def game_timeline_to_df(game_timeline):
    df = pd.DataFrame.from_dict(game_timeline)
    frames_info = pd.DataFrame.from_dict(df.loc['frames']['info'])
    # Expand timeline data into a final dataframe
    game_timeline_df = pd.DataFrame()
    for i in range(len(frames_info['participantFrames'])):
        df = pd.DataFrame.from_dict(frames_info['participantFrames'][i], orient='index')
        df['timeframe'] = i
        frames = [game_timeline_df, df]
        game_timeline_df = pd.concat(frames)
    # Expand championStats column
    keys = game_timeline_df['championStats'][0].keys()
    for key in keys:
        game_timeline_df[key] = game_timeline_df['championStats'].apply(lambda a: a[key])
    # Expand damageStats column
    keys = game_timeline_df['damageStats'][0].keys()
    for key in keys:
        game_timeline_df[key] = game_timeline_df['damageStats'].apply(lambda a: a[key])
    # Expand position column
    game_timeline_df['position_x'] = game_timeline_df['position'].apply(lambda a: a['x'])
    game_timeline_df['position_y'] = game_timeline_df['position'].apply(lambda a: a['y'])

    return game_timeline_df

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