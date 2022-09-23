from flask import Flask, render_template
from flask import request, escape
import pandas as pd
import numpy as np
import logging
import json

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from riot_api_connection import riot_api
import data_formation

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/patreon")
def patreon():
    return render_template('patreon.html')

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
        fig = px.bar(game_df.sort_values(by=['teamId','teamPosition'], ascending=False), y="championName", x=f"{key}", opacity=0.8, color='teamId', orientation='h', title=bar_charts[key], color_discrete_sequence=["rgb(180,0,0, 0.8)", "rgb(0,128,128, 0.8)"])
        fig.update_layout(layout)
        fig.update_layout(showlegend=False, title_x=0.5)
        fig.update_xaxes(title_text='')
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(title_text='')
        fig.update_yaxes(showgrid=False)
        chart_html = pio.to_html(fig,full_html=False, include_plotlyjs=False, config = {'displayModeBar': False})
        plotly_bar_charts[key] = chart_html

    fig = px.scatter(game_timeline_df, x="position_x", y="position_y", opacity=0.8, color="teamId", text="championName", animation_frame="timeframe", 
    color_discrete_sequence=[ "rgb(0,128,128, 0.8)", "rgb(180,0,0, 0.8)"], title='Player Positioning')
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1500
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 1500
    fig.update_layout(layout)
    fig.update_layout(showlegend=False, title_x=0.5)
    fig.update_xaxes(range=[0, 15000])
    fig.update_yaxes(range=[0, 15000])
    fig.update_xaxes(visible=False)
    fig.update_xaxes(showgrid=False, showticklabels=False)
    fig.update_yaxes(visible=False)
    fig.update_yaxes(showgrid=False, showticklabels=False)
    fig.update_traces(textposition='top center')
    fig.update_traces(marker_size=10)
    fig.update_layout(
                images= [dict(
                    source='/static/img/lol-minimap.jpg',
                    xref="paper", yref="paper",
                    x=0, y=1,
                    sizex=1, sizey=1,
                    xanchor="left",
                    yanchor="top",
                    sizing="stretch",
                    opacity=0.8,
                    layer="below")])
    
    heatmap_html = pio.to_html(fig,full_html=False, include_plotlyjs=False, config = {'displayModeBar': False}, auto_play=True)

    fig = px.scatter(game_timeline_df, y="xp", x="totalGold", size="totalDamageDoneToChampions", size_max=50, opacity=0.8, color="teamId", text="championName", animation_frame="timeframe", 
    color_discrete_sequence=[ "rgb(0,128,128, 0.8)", "rgb(180,0,0, 0.8)"], title="Game Evolution (Bubble Size ~ Damage to Champions)")
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 700
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 1000
    fig.update_layout(layout)
    fig.update_layout(showlegend=False, title_x=0.5)
    fig.update_yaxes(range=[0, game_timeline_df['xp'].max()+3000])
    fig.update_xaxes(range=[0, game_timeline_df['totalGold'].max()+1500])
    fig.update_yaxes(title_text='XP')
    fig.update_xaxes(title_text='Gold Earned')
    fig.update_traces(textposition='middle center')

    bubble_html = pio.to_html(fig,full_html=False, include_plotlyjs=False, config = {'displayModeBar': False}, auto_play=True)
    
    return render_template('game_report.html',
    champions = champions,
    champion_medals = champion_medals, 
    medal_definitions = medal_definitions,
    chart_data_js = chart_data_js,
    labels = labels,

    plotly_line_charts = plotly_line_charts,
    line_chart_keys = line_charts.keys(),
    plotly_bar_charts = plotly_bar_charts,
    bar_chart_keys = bar_charts.keys(),
    heatmap_html = heatmap_html,
    bubble_html = bubble_html
    
    )


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)