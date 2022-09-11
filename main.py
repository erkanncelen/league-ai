from flask import Flask, render_template
from flask import request, escape
import pandas as pd
import numpy as np
import logging
import json

import plotly.express as px
import plotly.io as pio

from riot_api_connection import riot_api
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
    game = api.get_match_info_by_match_id(last_game)
    game_df = data_formation.game_to_df(game)

    champions, champion_medals, medal_definitions, chart_data_js, labels = data_formation.game_report_data(game_df)
    
    game_timeline = api.get_game_timeline_by_match_id(last_game)

    game_timeline_df = data_formation.game_timeline_to_df(game_timeline, game_df)
    summoner1_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[0]])]['position'])).replace('"','')
    summoner2_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[1]])]['position'])).replace('"','')
    summoner3_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[2]])]['position'])).replace('"','')
    summoner4_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[3]])]['position'])).replace('"','')
    summoner5_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[4]])]['position'])).replace('"','')
    summoner6_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[5]])]['position'])).replace('"','')
    summoner7_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[6]])]['position'])).replace('"','')
    summoner8_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[7]])]['position'])).replace('"','')
    summoner9_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[8]])]['position'])).replace('"','')
    summoner10_positions = json.dumps(list(game_timeline_df[game_timeline_df['championName'].isin([champions[9]])]['position'])).replace('"','')

    pio.templates.default = "plotly_dark"
    layout = {'plot_bgcolor': "rgba(0, 0, 0, 0)",'paper_bgcolor': "rgba(0, 0, 0, 0.5)",'legend_bgcolor': "rgba(0, 0, 0, 0)"}

    line_charts = {
        "totalDamageDoneToChampions": "Total Damage to Champions",
        "totalGold": "Gold Earned",
        "xp": "Experience Points",
        "level": "Champion Level",
    }
    plotly_line_charts = {}

    for key in line_charts.keys():
        fig = px.line(game_timeline_df, x="timeframe", y=f"{key}", color='championName', title=line_charts[key])
        fig.update_layout(layout)
        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), legend_title_text='', title_x=0.5)
        fig.update_xaxes(title_text='')
        fig.update_yaxes(title_text='')
        chart_html = pio.to_html(fig,full_html=False, include_plotlyjs=False, config = {'displayModeBar': False})
        plotly_line_charts[key] = chart_html


    bar_charts = {
        "totalDamageDealtToChampions": "Total Damage to Champions",
        "damageDealtToObjectives": "Total Damage to Objectives",
        "damageDealtToBuildings": "Total Damage to Buildings",
        "damageSelfMitigated": "Self Mitigated Damage",
        "totalMinionsKilled": "Total Minions Killed",
        "goldEarned": "Gold Earned",
        "visionScore": "Vision Score",
        "timeCCingOthers": "Time CCing Others",
        "totalTimeSpentDead": "Total Time Spent Dead",
        "longestTimeSpentLiving": "Longest Time Spent Living",
    }

    plotly_bar_charts = {}

    for key in bar_charts.keys():
        fig = px.bar(game_df, y="championName", x=f"{key}", color='teamId', orientation='h', title=bar_charts[key])
        fig.update_layout(layout)
        fig.update_layout(showlegend=False, title_x=0.5)
        fig.update_xaxes(title_text='')
        fig.update_yaxes(title_text='')
        chart_html = pio.to_html(fig,full_html=False, include_plotlyjs=False, config = {'displayModeBar': False})
        plotly_bar_charts[key] = chart_html
    
    return render_template('game_report.html',
    champions = champions,
    champion_medals = champion_medals, 
    medal_definitions = medal_definitions,
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
    summoner10_positions = summoner10_positions,

    plotly_line_charts = plotly_line_charts,
    line_chart_keys = line_charts.keys(),
    plotly_bar_charts = plotly_bar_charts,
    bar_chart_keys = bar_charts.keys()
    
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)