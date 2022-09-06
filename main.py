from flask import Flask, render_template
from flask import request, escape
import pandas as pd
import numpy as np
import logging
from riot_api_connection import riot_api
import json
import data_formation

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
    summoner = api.get_summoner_by_name(summoner_name)
    matches = api.get_matches_by_summoner_name(summoner['name'])
    last_game = matches[0]
    game = last_game
    champions, chart_data_js, labels = data_formation.game_report_data(game)
    game_timeline = api.get_game_timeline_by_match_id(game)
    game_timeline_df = data_formation.game_timeline_to_df(game_timeline)
    red_team_positions = game_timeline_df[game_timeline_df['participantId'].isin([1,2,3,4,5])]['position']
    blue_team_positions = game_timeline_df[game_timeline_df['participantId'].isin([6,7,8,9,10])]['position']

    red_team_positions = json.dumps(list(red_team_positions)).replace('"','')
    blue_team_positions = json.dumps(list(blue_team_positions)).replace('"','')
    
    return render_template('game_report.html',
    champions = champions,
    chart_data_js = chart_data_js,
    labels = labels,

    red_team_positions = red_team_positions,
    blue_team_positions = blue_team_positions
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)