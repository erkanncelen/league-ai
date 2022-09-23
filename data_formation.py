import pandas as pd
import numpy as np
from riot_api_connection import riot_api
import json

def game_to_df(game) -> pd.DataFrame:

    columns = pd.DataFrame.from_dict(game['info']['participants'][:1]).columns
    game_df = pd.DataFrame(columns=columns)
    for item in game['info']['participants']:
        temp = pd.DataFrame(item).reset_index(drop=True)[:1]
        game_df = pd.concat([game_df, temp])
    game_df = game_df.sort_values(by=['teamId','teamPosition'])
    return game_df

def game_timeline_to_df(game_timeline, game_df):

    df = pd.DataFrame.from_dict(game_timeline)
    frames_info = pd.DataFrame.from_dict(df.loc['frames']['info'])
    # Expand timeline data into a final dataframe
    game_timeline_df = pd.DataFrame()
    for i in range(len(frames_info['participantFrames'])):
        df = pd.DataFrame.from_dict(frames_info['participantFrames'][i], orient='index')
        df['timeframe'] = i
        frames = [game_timeline_df, df]
        game_timeline_df = pd.concat(frames)
    game_timeline_df = game_timeline_df.merge(game_df[['participantId', 'championName', 'win', 'teamId', 'teamPosition']], on='participantId', how='left')
    game_timeline_df = game_timeline_df.sort_values(by=['timeframe', 'teamId','teamPosition'])
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

def game_report_data(game_df):

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
    game_df['HealsAndShieldOnTeammates_normalized'] = game_df['HealsAndShieldOnTeammates_normalized']/2
    chart_data = {}
    for champion in list(game_df['championName']):
        chart_data[champion] = game_df[game_df['championName'] == champion][metrics_normalized].iloc[0]
    labels = ['Damage', 'Objectives', 'Buildings', 'Vision', 'CC', 'Heal & Shield', 'Gold']

    chart_data_js = []
    for key in chart_data.keys():
        chart_data_js.append(np.array2string(chart_data[key].values, separator=', '))

    metrics_to_medals = {
        'totalDamageDealtToChampions': "Terminator",
        'damageDealtToObjectives': "Dragon Slayer",
        'damageDealtToBuildings': "Bulldozer",
        'visionScore': "Visionaire",
        'timeCCingOthers': "Mr. Policeman",
        'HealsAndShieldOnTeammates': "Nurse",
        'goldEarned': "Rockefeller",
    }

    champion_medals = {}
    for champion in chart_data.keys():
        medals = []
        performance = []
        great = 0
        good = 0
        for metric in metrics_to_medals.keys():
            if chart_data[champion][f"{metric}_normalized"] >= 15:
                medals.append(metrics_to_medals[metric])
                great+=1
            if chart_data[champion][f"{metric}_normalized"] >= 10:
                good+= 1
        if great >= 6:
            medals = ['One of a Kind'] + medals
        elif great >= 5:
            medals = ['Elite +'] + medals
        elif great >= 4:
            medals = ['Example Citizen'] + medals
        elif good >= 4:
            medals = ['Steven Gerrard'] + medals
        
        if len(medals) > 0:
            champion_medals[champion] = medals
        elif good >= 2:
            champion_medals[champion] = ['Average Dude']
        else:
            champion_medals[champion] = ['Impostor']
        


    medal_definitions = {
        "Terminator": "<b>Terminator</b><hr>This champion dealt incredible damage to opponents in this game.",
        "Nurse": "<b>Nurse</b><hr>This player healed and shielded teammates a lot.",
        "Bulldozer": "<b>Bulldozer</b><hr>This player dealt a lot of damage to buildings. Remember you must take down buildings to win the game.",
        "Dragon Slayer": "<b>Dragon Slayer</b><hr>This player beat the shit out of epic neutral monsters to secure objectives.",
        "Visionaire": "<b>Visionaire</b><hr>This player had an incredible vision score which gave the team an information advantage.",
        "Rockefeller": "<b>Rockefeller</b><hr>This player earned tons of gold in this game. Were they well-spent? That's another question.",
        "Mr. Policeman": "<b>Mr. Policeman</b><hr>This player did a lot of crowd control and handcuffed opponents during the game. They were annoyed for sure.",
        "Average Dude": "<b>Average Dude</b><hr>Although not too bad, this player did not have any major impact in this game.",
        "Impostor": "<b>Impostor</b><hr>Only God knows what this player did during the game.",
        "One of a Kind": "<b>One of a Kind</b><hr>Can one impact every critical aspect of the game heavily? This player did, and overall exhibited an unforgettable performance in this game.",
        "Elite +": "<b>Elite +</b><hr>What a show! This player had a remarkable performance and carried the team in almost every aspect of the game.",
        "Example Citizen": "<b>Example Citizen</b><hr>We have an example citizen here. Someone that all summoners should learn from. Great game!",
        "Steven Gerrard": "<b>Steven Gerrard</b><hr>This player performed good in many areas of the game and played a critical role for the team.",
    }

    return champions, champion_medals, medal_definitions, chart_data_js, labels