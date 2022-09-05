from flask import Flask, render_template
from flask import request, escape
import pandas as pd
import numpy as np
import logging
from riot_api_connection import riot_api, game_to_df
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/", methods=['POST'])
def game_report():
    summoner_name = request.form['summoner_name']
    api = riot_api()
    matches = api.get_matches_by_summoner_name(summoner_name)
    logging.info(summoner_name)
    print(summoner_name)
    last_game = matches[0]
    game = api.get_match_info_by_match_id(last_game)
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
    
    return render_template('game_report.html',
    champions = champions,
    chart_data_js = chart_data_js,
    labels = labels
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)