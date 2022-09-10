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
    summoner1_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([1])]['position'])).replace('"','')
    summoner2_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([2])]['position'])).replace('"','')
    summoner3_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([3])]['position'])).replace('"','')
    summoner4_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([4])]['position'])).replace('"','')
    summoner5_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([5])]['position'])).replace('"','')
    summoner6_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([6])]['position'])).replace('"','')
    summoner7_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([7])]['position'])).replace('"','')
    summoner8_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([8])]['position'])).replace('"','')
    summoner9_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([9])]['position'])).replace('"','')
    summoner10_positions = json.dumps(list(game_timeline_df[game_timeline_df['participantId'].isin([10])]['position'])).replace('"','')


    
    
    return render_template('game_report.html',
    champions = champions,
    chart_data_js = chart_data_js,
    labels = labels,

    summoner1_positions = summoner1_positions,
    summoner2_positions = summoner2_positions,
    summoner3_positions = summoner3_positions,
    summoner4_positions = summoner4_positions,
    summoner5_positions = summoner5_positions,
    summoner6_positions = summoner6_positions,
    summoner7_positions = summoner7_positions,
    summoner8_positions = summoner8_positions,
    summoner9_positions = summoner9_positions,
    summoner10_positions = summoner10_positions
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)