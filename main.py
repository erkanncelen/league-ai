from flask import Flask, render_template
from flask import request, escape
import pandas as pd
import numpy as np
import logging
from riot_api_connection import riot_api, game_to_df
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
    matches = api.get_matches_by_summoner_name(summoner_name)
    last_game = matches[0]
    game = last_game
    champions, chart_data_js, labels = data_formation.game_report_data(game)
    
    return render_template('game_report.html',
    champions = champions,
    chart_data_js = chart_data_js,
    labels = labels
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)