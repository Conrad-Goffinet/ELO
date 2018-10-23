import dash
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

app.layout = html.Div([
            html.H2(children = 'Pong Stats'),
            html.Table(
            # Header
            [html.Tr([html.Th(col) for col in table.columns])] +

            # Body
            [html.Tr([
                html.Td(table.iloc[i][col]) for col in table.columns
            ]) for i in range(len(table))]
            ),
                
            
            
            html.H2(children = 'Enter a New Name or Kerb'),
            dcc.Input(
                id = 'kerb',
                placeholder='Enter a name/kerb',
                type='text',
                value=''
            ),
            

            html.Button(id='kerb_button', children='Submit'),
            html.Div(id='announcement', children = 'Foo'),
            html.H2(children = 'Game Input'),
            html.H3(children = 'Winning Team'),
            dcc.Dropdown(
                id = 'player1',
                placeholder = 'Enter Player 1 of the winning team',
                options = create_player_dropdown(data)
            ),
            dcc.Input(
                id = 'player1_score',
                placeholder = 'Number of Cups sank by Player 1',
                type = 'number',
                value = [i for i in range(11)]
            ),
            dcc.Dropdown(
                id = 'player2',
                placeholder = 'Enter Player 2 of the winning team',
                options = create_player_dropdown(data)
            ),
            dcc.Input(
                id = 'player2_score',
                placeholder = 'Number of Cups sank by Player 2',
                type = 'number',
                value = [i for i in range(11)]
            ),
            html.H3(children = 'Losing Team'),
            dcc.Dropdown(
                id = 'player3',
                placeholder = 'Enter Player 3 of the winning team',
                options = create_player_dropdown(data)
            ),
            dcc.Input(
                id = 'player3_score',
                placeholder = 'Number of Cups sank by Player 3',
                type = 'number',
                value = [i for i in range(11)]
            ),
            dcc.Dropdown(
                id = 'player4',
                placeholder = 'Enter Player 4 of the winning team',
                options = create_player_dropdown(data)
            ),
            dcc.Input(
                id = 'player4_score',
                placeholder = 'Number of Cups sank by Player 4',
                type = 'number',
                value = [i for i in range(11)]
            ),
            html.Button('Submit Game', id='submit_button'),
            html.Div(id='game_played', children='Foo')
        ])


@app.callback(
    # Addition of a player
    Output(component_id='announcement', component_property='children'),
    [Input(component_id='kerb_button', component_property='n_clicks')],
    [State(component_id='kerb', component_property = 'value' )]
)
def create_kerb(clicks, name):
    if clicks is not None:
        #Avoids errors with typing inputs
        data.add_player(Player(name))
        print('callback fired', data.players)
        pickle.dump(data, open( "data.p", "wb" ) )
        return name

@app.callback(
    # Changing the dropdown menu for player one
    Output(component_id= 'player1', component_property= 'options'),
    [Input(component_id='kerb_button', component_property='n_clicks')]
)
def change_dropdown1(clicks):
    if clicks is not None:
        return create_player_dropdown(data)

@app.callback(
    # Changing the dropdown menu for player two
    Output(component_id= 'player2', component_property= 'options'),
    [Input(component_id='kerb_button', component_property='n_clicks')]
)
def change_dropdown2(clicks):
    if clicks is not None:
        return create_player_dropdown(data)

@app.callback(
    # Changing the dropdown menu for player three
    Output(component_id= 'player3', component_property= 'options'),
    [Input(component_id='kerb_button', component_property='n_clicks')]
)
def change_dropdown3(clicks):
    if clicks is not None:
        return create_player_dropdown(data)

@app.callback(
    # Changing the dropdown menu for player four
    Output(component_id= 'player4', component_property= 'options'),
    [Input(component_id='kerb_button', component_property='n_clicks')]
)
def change_dropdown4(clicks):
    if clicks is not None:
        return create_player_dropdown(data)

@app.callback(
    # Adding a game
    Output(component_id= 'game_played', component_property= 'children'),
    [Input(component_id= 'submit_button', component_property= 'n_clicks')],
    [State(component_id= 'player1', component_property= 'value'),
    State(component_id= 'player1_score', component_property= 'value'),
    State(component_id= 'player2', component_property= 'value'),
    State(component_id= 'player2_score', component_property= 'value'),
    State(component_id= 'player3', component_property= 'value'),
    State(component_id= 'player3_score', component_property= 'value'),
    State(component_id= 'player4', component_property= 'value'),
    State(component_id= 'player4_score', component_property= 'value')]

)

def submit_game(clicks, player1_name, player1_score,
                player2_name, player2_score,
                player3_name, player3_score,
                player4_name, player4_score):

    if clicks is not None:
        team1 = ((data.fetch_player(player1_name), player1_score),(data.fetch_player(player2_name), player2_score))
        team2 = ((data.fetch_player(player3_name), player3_score),(data.fetch_player(player4_name), player4_score))

        game = Game(team1, team2)

        data.add_game(game)
        pickle.dump(data, open( "data.p", "wb" ) )

    return 'Game Played'

if __name__ == '__main__':
    app.run_server(debug=True)
    