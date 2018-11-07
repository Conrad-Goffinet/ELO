#!/usr/bin/python
import os

import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import pickle

from dash.dependencies import Input, Output, State
from Game_and_Player import * 
from app_utilities import *

data = pickle.load(open('data.p','rb'))
table = create_data_table(data)
    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
server = app.server

# Anytime a player is referenced in this file, it refers to the string.
# To created the object, fetch_player() must be called--this must be done
# to create a game

app.layout = html.Div([
            html.H2(children = 'Pong Stats'),
            #Stats table
            dash_table.DataTable(id = 'data_table', 
            columns = [
                {"name": i, "id": i} for i in table.columns
            ],
            data=table.to_dict("rows"),
            filtering='be',
            filtering_settings='',

            sorting='fe',
            sorting_type='multi'

            ),
            #Elo graph
            dcc.Graph(
                id = 'elo_over_time',
                figure = {
                    'data': [
                    {'x': list(range(len(data.get_players()[0].pelo_history))), 
                     'y': data.get_players()[0].pelo_history,
                     'type': 'line', 'name': 'PELO'}
                    ],
                    'layout': {
                        'title':data.get_players()[0].name + '\'s PELO vs. Games Played'
                    }
                }
            ),
            dcc.Dropdown(
                id = 'player_elo',
                value = data.get_players()[0].name,
                options = create_player_dropdown(data)
            ),
            dcc.Markdown('''
                Made with love for Slugfest <3. In order to filter, use a space in between
                a greater than or less than sign (eg '> 3', but without the quotes). v0.2.0 Beta
            ''')

        ])

@app.callback(
    # Changes the graph to the player selected
    Output(component_id= 'elo_over_time', component_property= 'figure'),
    [Input(component_id= 'player_elo', component_property= 'value')]
)
def change_elo_graph(player):
    '''Creates an Elo graph over time for the 
    selected player'''
    player_to_graph = data.fetch_player(player)
    data_to_graph = player_to_graph.pelo_history
    graph = {
                    'data': [
                    {'x': list(range(len(data_to_graph))), 
                     'y': data_to_graph,
                     'type': 'line', 'name': 'PELO'}
                    ],
                    'layout': {
                        'title':player + '\'s PELO vs. Games Played'
                    }
                }

    return graph

@app.callback(
    Output('data_table', "data"),
    [Input('data_table', "filtering_settings")])
def update_graph(filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = table
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0]
            filter_value = filter.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        if ' > ' in filter:
            col_name = filter.split(' > ')[0]
            filter_value = float(filter.split(' > ')[1])
            dff = dff.loc[dff[col_name] > filter_value]
        if ' < ' in filter:
            col_name = filter.split(' < ')[0]
            filter_value = float(filter.split(' < ')[1])
            dff = dff.loc[dff[col_name] < filter_value]

    return dff.to_dict('rows')

if __name__ == '__main__':
    app.run_server(debug=True)
    
